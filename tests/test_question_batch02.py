"""New authored packs must work as forms, replacements, reports and old saves."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from question_batch02 import PACKS as BATCH02_PACKS,SOURCES as BATCH02_SOURCES
from question_batch03 import PACKS as BATCH03_PACKS,SOURCES as BATCH03_SOURCES
from question_authoring import validate
from check_game_question_coverage import inspect_form,template_keys
from youge import v04,v05,questionnaires
PACKS=BATCH02_PACKS+BATCH03_PACKS
SOURCES=BATCH02_SOURCES+BATCH03_SOURCES


class QuestionBatch02Tests(unittest.TestCase):
    def test_every_declared_record_uses_its_authored_pack_and_preserves_legacy_route(self):
        for pack in PACKS:
            for gid in pack['game_ids']:
                with self.subTest(game_id=gid):
                    form=questionnaires.questions(gid)
                    self.assertEqual(form['pack']['id'],pack['id'])
                    self.assertEqual(form['versions']['instrument'],'0.5.0')
                    old=questionnaires.questions(gid,instrument='0.4.0')
                    self.assertEqual(old['versions']['instrument'],'0.4.0')
                    self.assertEqual(old['questions'],[v04.public_question(q) for q in v04.questionnaire(gid)])

    def test_sources_variants_and_all_mode_paths_are_authored(self):
        validate(PACKS,SOURCES,{p['id'] for p in v04.config()['personas']}|set(v05.bank()['behavior_copy']))
        templates=template_keys(v04.config())
        for pack in PACKS:
            authored={v['id'] for s in pack['slots'] for v in s['variants']}
            for mode in pack['modes']:
                form=questionnaires.questions(pack['game_ids'][0],mode_id=mode['id'])
                finding=inspect_form(form['questions'],pack['title'],templates,authored)
                self.assertEqual(len(finding['dedicated_ids']),12)
                self.assertFalse(finding['template_ids'] or finding['uncertain_ids'] or finding['errors'])
                kinds=[]
                for q in form['questions'][:12]:
                    self.assertTrue(q['can_replace'])
                    selected=next(v for s in pack['slots'] for v in s['variants'] if v['id']==q['id'])
                    kinds.append(selected['question_type'])
                    replaced=v05.replace_question(form['response'],q['id'])
                    raw=deepcopy(replaced['response']);raw['fictional']=True
                    raw['answers']={v['id']:'D' for v in replaced['questions']}
                    for _ in range(3):
                        result=questionnaires.report(raw)
                        if result['complete']:break
                        raw['extra_answers'].append({'question_id':result['next_question']['id'],'answer':'B'})
                    self.assertTrue(result['complete'])
                    self.assertLessEqual(result['report']['question_count'],18)
                    self.assertNotIn('answer:'+q['id'],result['report']['evidence'])
                self.assertEqual(Counter(kinds),{'situational_action':8,'experience_reflection':4})

    def test_battle_only_bannerlord_form_has_no_campaign_prerequisites(self):
        pack=next(p for p in PACKS if p['id']=='blv5')
        form=questionnaires.questions('steam-261550',mode_id='combat')
        visible=' '.join(q['text']+' '.join(o['label'] for o in q['options']) for q in form['questions'][:12])
        for word in ('领地','锻造','家族','招募','交易','补给','城镇'):
            self.assertNotIn(word,visible)
        for slot in pack['slots']:
            self.assertEqual(sum(v['modes']==['combat'] for v in slot['variants']),2)
            self.assertEqual(sum(v['modes']==['campaign'] for v in slot['variants']),2)

    def test_death_stranding_versions_share_only_core_delivery_mechanics(self):
        original=questionnaires.questions('steam-1190460')
        directors=questionnaires.questions('steam-1850570')
        self.assertEqual(original['questions'],directors['questions'])
        pack=next(p for p in PACKS if p['id']=='ds1v5')
        visible=' '.join(v['text']+' '.join(o['label'] for o in v['options']) for s in pack['slots'] for v in s['variants'])
        for exclusive in ('靶场','赛道','伙伴机器人','弹射器'):
            self.assertNotIn(exclusive,visible)

    def test_handwritten_labels_and_signals_survive_position_rotation(self):
        # A recurring motive is moved along with its label; rotation never reassigns meaning.
        for pack in PACKS:
            for slot in pack['slots']:
                for v in slot['variants']:
                    self.assertEqual([o['id'] for o in v['options']],list('ABCD'))
        first=PACKS[0]['slots'][0]['variants'][0]['options'][0]
        self.assertEqual(first['signal'],'wanderer')
        second=PACKS[0]['slots'][1]['variants'][0]['options'][0]
        self.assertEqual(second['signal'],'collector')
        self.assertIn('图鉴',second['label'])

    def test_published_snapshots_reconstruct_current_packs_exactly(self):
        for source_pack in PACKS:
            pack=v05.pack_for(source_pack['game_ids'][0])
            entry=next(e for e in v05.bank()['pack_history'] if e['version']==pack['version'] and e['game_ids']==pack['game_ids'])
            self.assertEqual(json.loads((ROOT/entry['path']).read_text(encoding='utf-8')),pack)

    def test_solo_monster_hunter_replacement_does_not_score_npc_as_social(self):
        initial=questionnaires.questions('steam-582010')
        form=v05.replace_question(initial['response'],initial['questions'][5]['id'])
        question=form['questions'][5]
        raw=deepcopy(form['response']);raw['fictional']=True
        # The exploration option is moved together with its explicit, solo signal.
        raw['answers']={q['id']:'A' for q in form['questions']}
        pack=v05.pack_for('steam-582010')
        item=next(v for s in pack['slots'] for v in s['variants'] if v['id']==question['id'])
        self.assertNotIn('social_spark',{o['signal'] for o in item['options']})
        self.assertNotIn('quest_board',{o['signal'] for o in item['options']})

    def test_asynchronous_delivery_connection_is_preserved_without_persona_points(self):
        form=questionnaires.questions('steam-1190460')
        pack=v05.pack_for('steam-1190460')
        mode=v05.mode_for(pack,form['response']['mode_id'])
        items=v05._form(pack,mode,form['response']['question_variants'],form['response']['replacement_history'])
        excluded={'social_spark','quest_board','role_player'}
        raw=deepcopy(form['response']);raw['fictional']=True
        picked=None
        for item in items:
            connection=next((o for o in item['options'] if o.get('signal')=='async_connection'),None)
            choice=connection or next(o for o in item['options'] if o.get('signal') not in excluded)
            raw['answers'][item['id']]=choice['id']
            if connection:picked=(item,choice)
        self.assertIsNotNone(picked,'配送中的异步连接应保留独立证据')
        for _ in range(3):
            result=questionnaires.report(raw)
            if result['complete']:break
            raw['extra_answers'].append({'question_id':result['next_question']['id'],'answer':'A'})
        self.assertTrue(result['complete'])
        report=result['report'];item,choice=picked;ref='answer:'+item['id']
        self.assertEqual(report['evidence'][ref]['signal'],'async_connection')
        self.assertEqual(report['evidence'][ref]['label'],choice['label'])
        self.assertTrue(any(ref in tag['evidence_refs'] for tag in report['behavior_tags']))
        claim=next(a for a in report['advice'] if ref in a['evidence_refs'])
        self.assertEqual(claim['scope'],'specific_scenario')
        for persona in excluded:
            self.assertEqual(report['audit']['uncapped_semantic_points'][persona],0)


if __name__=='__main__':unittest.main()
