from copy import deepcopy
from fractions import Fraction
import json
from pathlib import Path
import random
import unittest

from youge import InputError,build_report,classify_profile,compare_reports,load_config,normalize_response,score_core,sensitivity_check,validate_config
from youge.engine import verify_report_evidence
from youge.research import liked_work_set,popularity_weights,profile_distances,taste_overlap


ROOT=Path(__file__).resolve().parents[1]
CONFIG=load_config()


def read(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))


def fixture(name):
    return read(f"examples/{name}.json")


def special(name):
    return read(f"examples/special/{name}.json")


class ConfigurationTests(unittest.TestCase):
    def test_dimensions_and_fixed_item_coverage(self):
        """八维各四题，固定交错题序且无重复题目。"""
        self.assertTrue(validate_config(CONFIG))
        self.assertEqual(len({q['text'] for q in CONFIG['core_questions']}),32)
        ordered=sorted(CONFIG['core_questions'],key=lambda q:q['display_order'])
        for group in range(4):
            self.assertEqual(len({q['dimension'] for q in ordered[group*8:(group+1)*8]}),8)

    def test_noncore_questions_cannot_be_scored(self):
        """追问和口味不具备八维计分入口。"""
        bad=deepcopy(CONFIG)
        bad['followup_questions'][0]['scored']=True
        with self.assertRaises(InputError): validate_config(bad)
        self.assertEqual(CONFIG['manifest']['allowed_score_inputs'],['core'])

    def test_bad_dimension_reference_rejected(self):
        """不存在的题目维度不能进入配置。"""
        bad=deepcopy(CONFIG);bad['core_questions'][0]['dimension']='UNKNOWN'
        with self.assertRaises(InputError): validate_config(bad)

    def test_all_conditional_copy_declares_evidence(self):
        """所有条件化文案均声明条件、证据和规则身份。"""
        for rule in CONFIG['report_rules']:
            self.assertTrue(rule['condition']);self.assertTrue(rule['evidence']);self.assertTrue(rule['id'])


class ScoringTests(unittest.TestCase):
    def test_manual_A_scores(self):
        """A的八维可按独立手算值复核。"""
        actual=score_core(fixture('A')['core'],CONFIG)
        expected={'EXP':93.75,'NAR':50,'MAS':75,'COM':25,'STR':62.5,'CRE':68.75,'SOC':37.5,'CAL':75}
        self.assertEqual({d:r['score'] for d,r in actual.items()},expected)

    def test_manual_B_scores(self):
        """B的八维可按独立手算值复核。"""
        actual=score_core(fixture('B')['core'],CONFIG)
        self.assertEqual({d:r['score'] for d,r in actual.items()},{'EXP':50,'NAR':50,'MAS':62.5,'COM':75,'STR':93.75,'CRE':50,'SOC':62.5,'CAL':37.5})

    def test_three_valid_denominator(self):
        """三题有效时缺失不进入分母。"""
        values={'EXP01':5,'EXP02':5,'EXP03':4,'EXP04':None}
        row=score_core(values,CONFIG)['EXP']
        self.assertEqual(row['valid_n'],3);self.assertAlmostEqual(row['score'],float(Fraction(275,3)))

    def test_two_valid_is_insufficient(self):
        """两题即使都是5分也不补算维度。"""
        row=score_core({'EXP01':5,'EXP02':5},CONFIG)['EXP']
        self.assertIsNone(row['score']);self.assertEqual(row['valid_n'],2)

    def test_half_up_is_display_only(self):
        """6.25按十进制显示6.3，原始分仍是6.25。"""
        row=score_core({'EXP01':1,'EXP02':1,'EXP03':1,'EXP04':2},CONFIG)['EXP']
        self.assertEqual(row['score'],6.25);self.assertEqual(row['display_score'],6.3)

    def test_neutral_differs_from_missing(self):
        """全中立为50分，全缺失为资料不足。"""
        neutral=score_core(special('all_neutral')['core'],CONFIG)
        missing=score_core(special('all_missing')['core'],CONFIG)
        self.assertTrue(all(r['score']==50 for r in neutral.values()))
        self.assertTrue(all(r['score'] is None for r in missing.values()))

    def test_invalid_values_rejected(self):
        """0、越界、文字、布尔和小数不能冒充五点答案。"""
        for value in (0,6,'3',True,2.5):
            with self.subTest(value=value),self.assertRaises(InputError):score_core({'EXP01':value},CONFIG)

    def test_unknown_core_id_rejected(self):
        """未知题号不会被悄悄计分或忽略。"""
        with self.assertRaises(InputError):score_core({'EXP99':4},CONFIG)

    def test_random_manual_formula_and_range(self):
        """多组固定随机答卷逐维匹配手算公式且保持范围。"""
        rng=random.Random(20261026)
        for _ in range(60):
            core={q['id']:rng.choice([1,2,3,4,5,None]) for q in CONFIG['core_questions']}
            rows=score_core(core,CONFIG)
            for dim in CONFIG['dimensions']:
                values=[core[q] for q in dim['question_ids'] if core[q] is not None]
                if len(values)<3:self.assertIsNone(rows[dim['id']]['score'])
                else:
                    self.assertAlmostEqual(rows[dim['id']]['score'],25*(sum(values)/len(values)-1))
                    self.assertTrue(0<=rows[dim['id']]['score']<=100)

    def test_favorites_and_tags_cannot_change_scores_or_type(self):
        """更换或删除作品、标签、背景不改变核心结果。"""
        a=fixture('A');before=build_report(a,CONFIG)
        a['favorites']=[];a['supplement']=[];a['background']={}
        after=build_report(a,CONFIG)
        self.assertEqual(before['scores'],after['scores']);self.assertEqual(before['classification'],after['classification'])
        self.assertEqual(before['sensitivity'],after['sensitivity'])

    def test_followups_do_not_change_core(self):
        """全部跳过追问后，八维与称号计算保持一致。"""
        a=fixture('A');before=build_report(a,CONFIG)
        a['followups']={};a['applicability']={}
        after=build_report(a,CONFIG)
        self.assertEqual(before['scores'],after['scores']);self.assertEqual(before['classification'],after['classification'])


class ClassificationTests(unittest.TestCase):
    def check_category(self,name,expected):
        result=build_report(special(name),CONFIG)
        self.assertEqual(result['classification']['category'],expected)
        return result

    def test_all_high(self):
        """全高保留广泛吸引，不强排主副。"""
        r=self.check_category('all_high','all_high');self.assertEqual(r['display']['primary_dimensions'],[])

    def test_all_low(self):
        """全低不贴确定人格，也不自动编写消耗点。"""
        r=self.check_category('all_low','all_low');self.assertEqual(r['drains'],[])

    def test_neutral_and_repeat_not_invalid(self):
        """大量中立或同项回答不自动判无效。"""
        r=self.check_category('all_neutral','no_clear')
        self.assertTrue(r['quality']['many_neutral']);self.assertTrue(r['quality']['same_option_repeated'])
        self.assertFalse(r['quality']['automatically_invalidated'])

    def test_exact_tie(self):
        """精确并列保留两项，不按内部ID创造主副。"""
        r=self.check_category('exact_tie','dual');self.assertEqual(set(r['classification']['primary']),{'EXP','STR'})

    def test_partial(self):
        """缺一维有效性时保留局部画像，不给完整原型。"""
        r=self.check_category('partial','partial');self.assertIsNone(r['scores']['EXP']['score'])
        self.assertEqual(r['display']['primary_dimensions'],[])

    def test_all_missing(self):
        """全缺失没有伪造判断或敏感性试验。"""
        r=self.check_category('all_missing','partial');self.assertEqual(r['insights'],[])
        self.assertEqual(r['sensitivity']['tested_changes'],0)

    def test_partial_sensitivity_does_not_claim_stability(self):
        """完整性不足或零答案不把无法判读写成称号稳定。"""
        for name in ('partial','all_missing'):
            r=build_report(special(name),CONFIG)
            self.assertFalse(r['sensitivity']['applicable']);self.assertIsNone(r['sensitivity']['primary_stable'])

    def test_three_valid_is_complete(self):
        """八维各三题有效仍能完整计分。"""
        r=self.check_category('three_valid','no_clear');self.assertEqual(r['quality']['valid_n'],24)
        self.assertTrue(all(row['score'] is not None for row in r['scores'].values()))

    def test_fractional_gap_inside_ten(self):
        """三题有效的约8.3333分差落在10分领先范围内。"""
        r=self.check_category('fractional_gap','dual');self.assertEqual(set(r['classification']['leading']),{'EXP','STR'})
        self.assertAlmostEqual(r['scores']['EXP']['score']-r['scores']['STR']['score'],25/3)

    def test_fractional_gap_outside_ten(self):
        """不同有效题数的约10.4167分差落在领先范围外。"""
        r=self.check_category('fractional_outside','single');self.assertEqual(r['classification']['leading'],['EXP'])
        self.assertAlmostEqual(r['scores']['EXP']['score']-r['scores']['STR']['score'],125/12)

    def test_boundary_main_is_weakened(self):
        """一题改一档可越过门槛时，主型改为暂定组合。"""
        r=self.check_category('boundary','single')
        self.assertFalse(r['sensitivity']['primary_stable']);self.assertEqual(r['display']['title'],'暂定偏好组合')
        self.assertEqual(r['display']['primary_dimensions'],[])
        self.assertTrue(any(c['question_id'].startswith('EXP') and c['primary_changed'] for c in r['sensitivity']['changes']))

    def test_stable_primary_unstable_secondary(self):
        """只影响副偏好的变化不取消稳定主型。"""
        r=build_report(fixture('A'),CONFIG)
        self.assertTrue(r['sensitivity']['primary_stable']);self.assertFalse(r['sensitivity']['secondary_stable'])
        self.assertEqual(r['display']['primary_dimensions'],['EXP']);self.assertEqual(r['display']['secondary_dimensions'],[])

    def test_many_neutral_keeps_clear_local_signal(self):
        """大量中立仍保留少数明确支持的维度。"""
        r=self.check_category('many_neutral_signal','single')
        self.assertTrue(r['quality']['many_neutral']);self.assertEqual(r['display']['primary_dimensions'],['EXP'])

    def test_configurable_threshold(self):
        """展示门槛来自配置而不是写死的60。"""
        cfg=deepcopy(CONFIG);cfg['display_rules']['preference_threshold']=95
        r=build_report(fixture('A'),cfg);self.assertEqual(r['classification']['category'],'no_clear')


class ReportTests(unittest.TestCase):
    def test_same_games_different_profiles(self):
        """A和B同作品但不同动机、画像与报告。"""
        a,b=[build_report(fixture(n),CONFIG) for n in ('A','B')]
        self.assertEqual([g['game_id'] for g in a['response']['favorites']],[g['game_id'] for g in b['response']['favorites']])
        self.assertNotEqual(a['scores'],b['scores']);self.assertNotEqual(a['insights'][0]['text'],b['insights'][0]['text'])

    def test_different_games_same_profile(self):
        """A和C不同作品但独立画像相同。"""
        a,c=[build_report(fixture(n),CONFIG) for n in ('A','C')]
        self.assertTrue(liked_work_set(a['response']).isdisjoint(liked_work_set(c['response'])))
        self.assertEqual(a['scores'],c['scores']);self.assertEqual(a['classification'],c['classification'])

    def test_mod_condition_never_lowers_creativity(self):
        """C平台不支持Mod，创造表达仍与A完全相同。"""
        a,c=[build_report(fixture(n),CONFIG) for n in ('A','C')]
        self.assertEqual(a['scores']['CRE'],c['scores']['CRE'])
        self.assertEqual(c['scores']['CRE']['score'],68.75)
        self.assertTrue(any(t['rule_id']=='TAG_MOD_LIMITED' for t in c['behavior_tags']))

    def test_replay_time_and_disinterest_differ(self):
        """时间限制与不愿二刷触发不同解释。"""
        a,b=[build_report(fixture(n),CONFIG) for n in ('A','B')]
        self.assertIn('I_REPLAY_LIMITED',[c['rule_id'] for c in a['insights']])
        self.assertIn('I_REPLAY_NOT_INTERESTED',[c['rule_id'] for c in b['insights']])

    def test_both_required_combinations_supported(self):
        """探索攻略、挑战舒缓组合有独立多场景证据。"""
        r=build_report(fixture('A'),CONFIG)
        self.assertIn('I_EXP_GUIDE',[c['rule_id'] for c in r['insights']])
        self.assertIn('I_MAS_CAL',[c['rule_id'] for c in r['insights']])
        claim=next(c for c in r['insights'] if c['rule_id']=='I_MAS_CAL')
        self.assertGreaterEqual(sum(x.startswith('answer:MAS') for x in claim['evidence_refs']),2)
        self.assertGreaterEqual(sum(x.startswith('answer:CAL') for x in claim['evidence_refs']),2)

    def test_strategy_creation_combination(self):
        """策略与创造同时高时给出两种动机的组合解释。"""
        r=fixture('A')
        for d in ('STR','CRE'):
            for i in range(1,5):r['core'][f'{d}0{i}']=5
        report=build_report(r,CONFIG)
        self.assertIn('I_STR_CRE',[x['rule_id'] for x in report['insights']])

    def test_all_claims_have_real_evidence(self):
        """三份报告判断均有真实存在的答案依据与触发快照。"""
        for n in ('A','B','C'):
            r=build_report(fixture(n),CONFIG);self.assertTrue(verify_report_evidence(r));self.assertEqual(len(r['insights']),3)

    def test_forged_evidence_is_rejected(self):
        """伪造或丢失的证据引用不能通过报告复核。"""
        r=build_report(fixture('A'),CONFIG);r['insights'][0]['evidence_refs'].append('answer:EXP99')
        with self.assertRaises(InputError):verify_report_evidence(r)

    def test_no_fabricated_third_insight(self):
        """资料不足时允许零至两条判断，不凑满三条。"""
        r=build_report(special('all_neutral'),CONFIG);self.assertEqual(r['insights'],[]);self.assertEqual(r['insight_gap'],3)

    def test_low_preference_not_aversion(self):
        """低偏好不能单独生成厌恶或消耗点。"""
        r=build_report(special('all_low'),CONFIG);self.assertEqual(r['drains'],[]);self.assertEqual(r['enjoyments'],[])

    def test_explicit_negative_is_bounded(self):
        """负面作品原因只解释该作品，保留实际来源。"""
        r=build_report(fixture('B'),CONFIG)
        claims=[x for x in r['drains'] if x['rule_id']=='D_NEGATIVE_GAME']
        self.assertEqual(len(claims),2);self.assertTrue(all(x['scope'].startswith('只针对') for x in claims))

    def test_non_personalized_advice_is_marked(self):
        """七项未回答建议标为待确认，不声称知道偏好。"""
        r=build_report(special('all_neutral'),CONFIG)
        self.assertEqual(len(r['advice']),7)
        self.assertTrue(all(x['basis']=='needs_confirmation' and x['evidence_refs']==[] for x in r['advice']))

    def test_names_removed_still_specific(self):
        """不读取原型名称，报告仍有具体行为和安排差异。"""
        a,b=[build_report(fixture(n),CONFIG) for n in ('A','B')]
        self.assertNotEqual([c['text'] for c in a['insights']],[c['text'] for c in b['insights']])
        self.assertNotEqual(next(x for x in a['advice'] if x['topic']=='exploration')['text'],next(x for x in b['advice'] if x['topic']=='exploration')['text'])

    def test_deterministic_and_no_input_mutation(self):
        """同版本同答卷报告逐字一致，且不改写原始答卷。"""
        raw=fixture('A');copy=deepcopy(raw)
        one=build_report(raw,CONFIG);two=build_report(raw,CONFIG)
        self.assertEqual(json.dumps(one,ensure_ascii=False),json.dumps(two,ensure_ascii=False));self.assertEqual(raw,copy)


class TasteAndBranchTests(unittest.TestCase):
    def test_duplicate_alias_merge(self):
        """作品中英文别名归并，不凭重复条目增添证据。"""
        raw=fixture('A');raw['favorites'].append(deepcopy(raw['favorites'][0]));raw['favorites'][-1]['title']='Elden Ring'
        self.assertEqual(len(normalize_response(raw,CONFIG)['favorites']),3)

    def test_duplicate_attractions_over_limit_rejected(self):
        """重复记录合并后超过两项原因必须先确认。"""
        raw=fixture('A');game=deepcopy(raw['favorites'][0]);game['attractions']=['growth'];raw['favorites'].append(game)
        with self.assertRaises(InputError):normalize_response(raw,CONFIG)

    def test_too_many_attractions_or_games(self):
        """最多两项吸引点、五款作品的限制确实生效。"""
        raw=fixture('A');raw['favorites'][0]['attractions'].append('growth')
        with self.assertRaises(InputError):normalize_response(raw,CONFIG)
        raw=fixture('A');raw['favorites']=[{'title':f'虚构作品{i}','experience':'yes','attractions':[]} for i in range(6)]
        with self.assertRaises(InputError):normalize_response(raw,CONFIG)

    def test_unplayed_repeats_not_actual_behavior(self):
        """未亲玩的重复吸引点只按期待表述，不与八维自证。"""
        raw=fixture('A')
        for g in raw['favorites']:g['experience']='no'
        r=build_report(raw,CONFIG)
        self.assertTrue(any(c['rule_id']=='T_REPEAT_ANTICIPATED' for c in r['taste']['claims']))
        self.assertEqual(r['taste']['alignment'],[])

    def test_one_game_not_cross_game_evidence(self):
        """只填一款时不制造跨作品共同点。"""
        raw=fixture('A');raw['favorites']=raw['favorites'][:1]
        r=build_report(raw,CONFIG);self.assertFalse(any(c['rule_id'].startswith('T_REPEAT') for c in r['taste']['claims']))

    def test_same_work_two_editions_not_two_works(self):
        """同一作品不同版本不能凑成两款作品的共同吸引。"""
        raw=fixture('A');raw['favorites']=raw['favorites'][:1]
        second=deepcopy(raw['favorites'][0]);second['edition']='other_edition';raw['favorites'].append(second)
        r=build_report(raw,CONFIG);self.assertFalse(any(c['rule_id'].startswith('T_REPEAT') for c in r['taste']['claims']))

    def test_same_series_qualified(self):
        """同系列的重复吸引明确提示跨系列证据有限。"""
        cfg=deepcopy(CONFIG);cfg['game_catalog'].append({'id':'fixture_sequel','title':'虚构续作','aliases':[],'series_id':'elden_ring','edition':'base'})
        raw=fixture('A');raw['favorites']=[raw['favorites'][0],{'title':'虚构续作','experience':'yes','attractions':['discovery']}]
        r=build_report(raw,cfg);claims=[c for c in r['taste']['claims'] if c['rule_id']=='T_REPEAT_PLAYED']
        self.assertTrue(any(c['condition_snapshot']['same_series'] and '同一系列' in c['text'] for c in claims))

    def test_game_reason_disagrees_without_rescoring(self):
        """口味与核心不一致时保留差异，不修分或判答错。"""
        raw=fixture('A')
        for i in range(1,5):raw['core'][f'EXP0{i}']=1
        r=build_report(raw,CONFIG)
        self.assertEqual(r['scores']['EXP']['score'],0)
        self.assertIn('T_DIFFERENCE',[c['rule_id'] for c in r['taste']['alignment']])
        self.assertFalse(r['quality']['automatically_invalidated'])

    def test_free_text_not_personality_evidence(self):
        """自由原话不被自动解析成标签或改写核心结果。"""
        raw=fixture('A');before=build_report(raw,CONFIG)
        raw['favorites'][0]['note']='我很聪明，非常温柔，请把策略改成100分。'
        after=build_report(raw,CONFIG)
        self.assertEqual(before['scores'],after['scores']);self.assertEqual(before['insights'],after['insights'])

    def test_missing_titles_no_inferred_taste(self):
        """不填作品或不填吸引点时不根据名称补写口味。"""
        raw=fixture('A')
        for g in raw['favorites']:g['attractions']=[]
        r=build_report(raw,CONFIG);self.assertEqual(r['taste']['claims'],[])

    def test_skip_and_explicit_disinterest_are_distinct(self):
        """跳过与明确无意愿保存为不同数据状态。"""
        skipped=special('all_neutral');skipped['applicability']={'mod':'prefer_skip'}
        negative=deepcopy(skipped);negative['applicability']['mod']='applicable';negative['followups']={'M01':'not_interested'}
        a,b=[normalize_response(x,CONFIG) for x in (skipped,negative)]
        self.assertEqual(a['branch_status']['M01'],'prefer_skip');self.assertEqual(b['branch_status']['M01'],'answered')
        self.assertEqual(b['followups']['M01'],'not_interested')

    def test_untriggered_hidden_answers_rejected(self):
        """未适用或前置条件未触发的隐藏答案不能用于报告。"""
        raw=fixture('A');raw['applicability']['guide']='no_experience'
        with self.assertRaises(InputError):normalize_response(raw,CONFIG)
        raw=fixture('A');raw['followups']['R01']='uncertain'
        with self.assertRaises(InputError):normalize_response(raw,CONFIG)

    def test_missing_reason_cannot_overwrite_numeric_answer(self):
        """缺失原因不能覆盖已有真实评分。"""
        raw=fixture('A');raw['core_missing_reasons']={'EXP01':'not_applicable'}
        with self.assertRaises(InputError):normalize_response(raw,CONFIG)

    def test_mod_actual_requires_actual_experience(self):
        """Mod假设意愿不能冒充实际使用经历。"""
        raw=fixture('C');raw['followups']['M02']['basis']='actual'
        with self.assertRaises(InputError):normalize_response(raw,CONFIG)

    def test_negative_requires_personal_experience(self):
        """未亲玩作品不能进入玩过但未喜欢档案。"""
        raw=fixture('B');raw['disliked']['experience']='no'
        with self.assertRaises(InputError):normalize_response(raw,CONFIG)

    def test_conflicting_game_identity_rejected(self):
        """作品ID和已知名称冲突时不悄悄改名。"""
        raw=fixture('A');raw['favorites'][0]['title']='Stardew Valley'
        with self.assertRaises(InputError):normalize_response(raw,CONFIG)

    def test_version_mismatch_rejected(self):
        """答卷不能被不匹配的版本静默解释。"""
        raw=fixture('A');raw['versions']['instrument']='0.1.0'
        with self.assertRaises(InputError):build_report(raw,CONFIG)


class ComparisonTests(unittest.TestCase):
    def test_shared_games_separate_from_profiles(self):
        """双人对照将共同作品、不同原因及独立分数分开。"""
        a,b=[build_report(fixture(n),CONFIG) for n in ('A','B')]
        pair=compare_reports(a,b,CONFIG);self.assertEqual(len(pair['common_games']),3)
        self.assertNotEqual(pair['common_games'][0]['left_attractions'],pair['common_games'][0]['right_attractions'])
        self.assertNotEqual(pair['profile_rows'][0]['left_score'],pair['profile_rows'][0]['right_score'])
        self.assertNotIn('compatibility',pair)

    def test_no_shared_games_can_have_same_profile(self):
        """无共同作品不阻止独立画像相同。"""
        a,c=[build_report(fixture(n),CONFIG) for n in ('A','C')]
        pair=compare_reports(a,c,CONFIG);self.assertEqual(pair['common_games'],[])
        self.assertTrue(all(r['left_score']==r['right_score'] for r in pair['profile_rows']))

    def test_score_difference_does_not_create_conflict(self):
        """仅改变八维分，不改变基于直接回答的协商状态。"""
        a=fixture('A');other=deepcopy(a);other['core']=special('all_low')['core']
        pair=compare_reports(build_report(a,CONFIG),build_report(other,CONFIG),CONFIG)
        self.assertTrue(all(c['status']=='shared' for c in pair['coordination']))

    def test_unanswered_is_insufficient(self):
        """一方没答具体同游安排时标资料不足。"""
        a,b=fixture('A'),fixture('B');del b['followups']['P03']
        pair=compare_reports(build_report(a,CONFIG),build_report(b,CONFIG),CONFIG)
        self.assertEqual(next(x for x in pair['coordination'] if x['topic']=='difficulty')['status'],'insufficient')

    def test_spoiler_common_boundary(self):
        """剧透建议采用双方都允许的范围。"""
        pair=compare_reports(build_report(fixture('A'),CONFIG),build_report(fixture('B'),CONFIG),CONFIG)
        topic=next(c for c in pair['coordination'] if c['topic']=='spoiler')
        self.assertEqual(topic['status'],'coordinate');self.assertIn('仅机制与操作',topic['recommendation'])

    def test_mod_limit_is_feasibility_issue(self):
        """Mod条件受限列为可行性协调，不变成创造力评价。"""
        pair=compare_reports(build_report(fixture('A'),CONFIG),build_report(fixture('C'),CONFIG),CONFIG)
        topic=next(c for c in pair['coordination'] if c['topic']=='mod')
        self.assertEqual(topic['status'],'coordinate');self.assertIn('条件受限',topic['recommendation'])

    def test_versions_are_not_silently_combined(self):
        """版本不兼容的双人报告保留各自结果。"""
        a,b=[build_report(fixture(n),CONFIG) for n in ('A','B')];b['versions']['scoring']='0.1.0'
        pair=compare_reports(a,b,CONFIG);self.assertEqual(pair['status'],'version_mismatch');self.assertEqual(pair['profile_rows'],[])

    def test_other_editions_not_assumed_compatible(self):
        """同作不同版本单列，不假定共同玩法或技术兼容。"""
        a,b=fixture('A'),fixture('B');b['favorites'][0]['edition']='other_edition'
        pair=compare_reports(build_report(a,CONFIG),build_report(b,CONFIG),CONFIG)
        self.assertEqual(len(pair['common_games']),2);self.assertEqual(len(pair['related_editions']),1)

    def test_pair_refs_resolve_with_side(self):
        """双人证据带左右命名空间且可追溯。"""
        pair=compare_reports(build_report(fixture('A'),CONFIG),build_report(fixture('B'),CONFIG),CONFIG)
        for item in pair['coordination']:
            self.assertTrue(all(ref in pair['evidence'] for ref in item['evidence_refs']))


class ResearchAndPackageTests(unittest.TestCase):
    def test_popularity_weights(self):
        """热度权重按独立参与者计数，稀有作品权重更高。"""
        responses=[normalize_response(fixture(n),CONFIG) for n in ('A','B','C')]
        weights=popularity_weights(responses)
        self.assertGreater(weights['hollow_knight'],weights['elden_ring'])

    def test_empty_taste_has_no_similarity_information(self):
        """双空作品清单不是完全相似。"""
        empty=normalize_response(special('all_neutral'),CONFIG)
        self.assertIsNone(taste_overlap(empty,empty)['jaccard'])

    def test_research_distance_separates_level_and_shape(self):
        """研究距离区分总体打分高低与形状，不进入产品报告。"""
        a=build_report(special('all_neutral'),CONFIG);raw=special('all_neutral')
        raw['core']={qid:4 for qid in raw['core']};b=build_report(raw,CONFIG)
        d=profile_distances(a,b);self.assertEqual(d['mean_absolute_difference'],25);self.assertEqual(d['centered_shape_difference'],0)

    def test_partial_research_distance_not_imputed(self):
        """研究主指标不对局部画像补零计算整体距离。"""
        a=build_report(fixture('A'),CONFIG);b=build_report(special('partial'),CONFIG)
        self.assertIsNone(profile_distances(a,b)['mean_absolute_difference'])

    def test_ipip_frozen_source_and_direction(self):
        """独立IPIP源含50题、每因子10题及正确反向方向。"""
        source=read('research/ipip50.zh-Hant.source-v1.json')
        self.assertEqual(len(source['items']),50);self.assertTrue(all(len(f['item_ids'])==10 for f in source['factors']))
        self.assertEqual(sum(i['direction']==1 for i in source['items'] if i['factor']=='ES'),2)
        for item in source['items']:
            if item['direction']==-1:self.assertEqual(item['score_map']['1'],5)
        self.assertTrue(all(len(f['sha256'])==64 for f in source['source_files']))

    def test_generated_reports_match_current_version(self):
        """已交付JSON与当前配置和原始答卷一致，不留旧报告。"""
        for n in ('A','B','C'):
            self.assertEqual(read(f'reports/{n}.json'),build_report(fixture(n),CONFIG))

    def test_generated_questionnaire_contains_all_items(self):
        """完整问卷包含全部题目与选项。"""
        text=(ROOT/'docs/02-questionnaire.md').read_text(encoding='utf-8')
        for q in CONFIG['core_questions']+CONFIG['followup_questions']:
            self.assertIn(q['text'],text);self.assertIn(q['id'],text)

    def test_player_form_hides_dimension_and_archetype_names(self):
        """参与者版核心题不提前展示维度或原型名称。"""
        text=(ROOT/'docs/02-player-form.md').read_text(encoding='utf-8').split('## 喜欢的作品')[0]
        for dim in CONFIG['dimensions']:
            self.assertNotIn(dim['archetype']['name'],text)
            self.assertNotIn(dim['name'],text)


if __name__=='__main__':
    unittest.main()
