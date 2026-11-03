"""Authored forms: replacement, modes, evidence, snapshots and live HTTP contracts."""
from collections import Counter
from copy import deepcopy
from http.server import ThreadingHTTPServer
import json
import random
import threading
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request,urlopen

from youge import v04,v05,questionnaires
from youge.engine import InputError
from youge.web import Handler
from youge.access import AccessController,password_record


def finish(raw,letter='A'):
    raw=deepcopy(raw)
    for _ in range(3):
        result=questionnaires.report(raw)
        if result['complete']:return result
        raw['extra_answers'].append({'question_id':result['next_question']['id'],'answer':letter})
    raise AssertionError('More than two extra questions')


def answered(game_id='genshin-impact',mode_id=None):
    form=questionnaires.questions(game_id,mode_id=mode_id)
    raw=deepcopy(form['response']);raw['fictional']=True
    raw['answers']={q['id']:'A' for q in form['questions']}
    return raw


class AuthoredQuestionTests(unittest.TestCase):
    def test_variable_choices_validate_and_survive_replacement(self):
        original=v05.pack_for('genshin-impact')
        modified=deepcopy(original)
        modified['slots'][0]['variants'][0]['options']=modified['slots'][0]['variants'][0]['options'][:2]
        modified['slots'][0]['variants'][1]['options']=modified['slots'][0]['variants'][1]['options'][:3]
        lookup=v05.pack_for
        with patch.object(v05,'pack_for',side_effect=lambda gid,version=None: modified if gid=='genshin-impact' else lookup(gid,version)):
            form=v05.questions('genshin-impact')
            self.assertEqual(len(form['questions'][0]['options']),2)
            raw=deepcopy(form['response']);raw['fictional']=True
            raw['answers']={q['id']:'A' for q in form['questions']}
            self.assertTrue(finish(raw)['complete'])
            raw['answers'][form['questions'][0]['id']]='C'
            with self.assertRaises(InputError): v05.questions(raw=raw)
            raw['answers'][form['questions'][0]['id']]='B'
            replaced=v05.replace_question(raw,form['questions'][0]['id'])
            self.assertEqual(len(replaced['questions'][0]['options']),3)
            self.assertNotIn(form['questions'][0]['id'],replaced['response']['answers'])
            restored=v05.replace_question(replaced['response'],replaced['questions'][0]['id'],undo=True)
            self.assertEqual(restored['questions'][0]['options'],form['questions'][0]['options'])

    def test_all_released_packs_have_twelve_slots_and_four_unchanged_shared_questions(self):
        self.assertTrue({'gi','lol','cs2','sv','er','bg3'}<={p['id'] for p in v05.bank()['packs']})
        old=[q for q in v04.config()['common'] if q['scope']=='cross']
        for pack in v05.bank()['packs']:
            self.assertEqual(len(pack['slots']),12)
            for mode in pack['modes']:
                form=questionnaires.questions(pack['game_ids'][0],mode_id=mode['id'])
                self.assertEqual(len(form['questions']),16)
                self.assertTrue(all(q['can_replace'] for q in form['questions'][:12]))
                self.assertEqual([q['text'] for q in form['questions'][12:]],[q['text'] for q in old])
                self.assertEqual([q['options'] for q in form['questions'][12:]],
                                 [[{k:o[k] for k in ('id','label')} for o in q['options']] for q in old])
                self.assertTrue(all(set(o)=={'id','label'} for q in form['questions'] for o in q['options']))

    def test_aram_and_nondefusal_paths_do_not_require_the_other_mode(self):
        aram=questionnaires.questions('league-of-legends',mode_id='aram')
        text=' '.join(q['text']+' '.join(o['label'] for o in q['options']) for q in aram['questions'][:12])
        for wrong in ('小龙','大龙','排位','打野'):self.assertNotIn(wrong,text)
        self.assertIn('兵线',text,'普通大乱斗确有兵线，不能把它误当成峡谷专属规则')
        cs=questionnaires.questions('steam-730',mode_id='gunplay')
        text=' '.join(q['text'] for q in cs['questions'][:12])
        for wrong in ('拆弹','回防','预算','购买阶段'):self.assertNotIn(wrong,text)

    def test_scoped_planning_recording_and_reference_choices_do_not_create_persona_points(self):
        cases=[
            ('steam-730','gunplay','CS203.CORE','practice_route_plan','systems_builder'),
            ('steam-730','gunplay','CS209.CORE','game_recording','collector'),
            ('steam-730','gunplay','CS202.CORE','route_choice','play_inventor'),
            ('steam-322170',None,'GD602.V1','rhythm_workflow_plan','systems_builder'),
            ('steam-356400',None,'THUMP601.V1','rhythm_reference_first','puzzle_breaker'),
            ('steam-1029690',None,'SE5SC03.V1','try_available_setup','play_inventor'),
            ('steam-1817230',None,'HIFIV501.V1','try_action_variant','play_inventor'),
            ('steam-1659420','thiefs_end','UCLEGSC02.V1','route_variant','play_inventor'),
            ('steam-1113560',None,'NIERRV504.V1','mission_preparation_plan','systems_builder'),
            ('steam-460810',None,'VANV501.V1','combat_resource_cycle','systems_builder'),
            ('steam-504230',None,'CELESTV502.V1','platform_route_plan','systems_builder'),
            ('steam-1761390',None,'MIKU7C05.V1','tool_reference_first','puzzle_breaker'),
            ('steam-1003590','journey','TETFX7C01.JOURNEY.V1','game_reference_first','puzzle_breaker'),
            ('steam-17410',None,'MIRORIGV506.V1','scene_inspection','role_player'),
            ('steam-601150',None,'DMC5SC01.ALT1','compare_available_setup','build_alchemist'),
            ('steam-601150',None,'DMC5SC07.V1','purchase_available_upgrade','build_alchemist'),
            ('steam-552500',None,'VMT2SC604.V1','optional_objective','collector'),
            ('steam-1744330',None,'NMH3SC606.V1','tool_operation_plan','systems_builder'),
        ]
        for gid,mode_id,question_id,signal,excluded in cases:
            with self.subTest(game=gid,signal=signal):
                form=questionnaires.questions(gid,mode_id=mode_id)
                raw=deepcopy(form['response']);raw['fictional']=True
                pack=v05.pack_for(gid);mode=v05.mode_for(pack,raw['mode_id'])
                slot=next(s for s in pack['slots'] if any(v['id']==question_id for v in s['variants']))
                raw['question_variants'][slot['id']]=question_id
                internal=v05._form(pack,mode,raw['question_variants'],raw['replacement_history'])
                item=next(q for q in internal if q['id']==question_id)
                selected=next(o for o in item['options'] if o['signal']==signal)
                for q in internal:
                    choice=selected if q['id']==question_id else next(o for o in q['options'] if o['signal']!=excluded)
                    raw['answers'][q['id']]=choice['id']
                report=finish(raw)['report'];ref='answer:'+question_id
                self.assertEqual(report['evidence'][ref]['signal'],signal)
                self.assertEqual(report['evidence'][ref]['label'],selected['label'])
                self.assertEqual(report['audit']['uncapped_semantic_points'][excluded],0)
                self.assertTrue(any(ref in tag['evidence_refs'] for tag in report['behavior_tags']))
                self.assertTrue(any(ref in advice['evidence_refs'] and advice['scope']=='specific_scenario' for advice in report['advice']))

    def test_connected_can_replace_twice_to_cpu_and_undo_without_answering(self):
        form=questionnaires.questions('steam-1003590',mode_id='connected')
        initial=form['questions'][0]
        pack=v05.pack_for('steam-1003590');mode=v05.mode_for(pack,'connected')
        def internal(current):
            raw=current['response']
            return v05._form(pack,mode,raw['question_variants'],raw['replacement_history'])[0]
        self.assertTrue({'quest_board','social_spark'}<={o['signal'] for o in internal(form)['options']})
        first=v05.replace_question(form['response'],initial['id'])
        self.assertEqual(first['questions'][0]['id'],'TETFX7C01.CONNECTED.ALT1')
        self.assertTrue({'quest_board','social_spark'}<={o['signal'] for o in internal(first)['options']})
        cpu=v05.replace_question(first['response'],first['questions'][0]['id'])
        self.assertEqual(cpu['questions'][0]['id'],'TETFX7C01.CONNECTED.ALT2')
        self.assertIn('AI',cpu['questions'][0]['text'])
        self.assertFalse({'quest_board','social_spark'}&{o['signal'] for o in internal(cpu)['options']})
        self.assertEqual(len(cpu['questions']),16)
        self.assertEqual(cpu['response']['answers'],{})
        self.assertEqual(cpu['response']['extra_answers'],[])
        resumed=questionnaires.questions(raw=cpu['response'])
        self.assertEqual(resumed['questions'],cpu['questions'])
        undo=v05.replace_question(cpu['response'],cpu['questions'][0]['id'],undo=True)
        self.assertEqual(undo['questions'],first['questions'])
        original=v05.replace_question(undo['response'],undo['questions'][0]['id'],undo=True)
        self.assertEqual(original['questions'],form['questions'])

    def test_every_authored_variant_can_be_answered_and_preserves_actual_evidence(self):
        for pack in v05.bank()['packs']:
            for mode in pack['modes']:
                initial=questionnaires.questions(pack['game_ids'][0],mode_id=mode['id'])
                for slot in pack['slots']:
                    for variant in slot['variants']:
                        if variant.get('modes') and mode['id'] not in variant['modes']:continue
                        raw=deepcopy(initial['response']);raw['question_variants'][slot['id']]=variant['id']
                        form=questionnaires.questions(raw=raw)
                        raw['answers']={q['id']:'B' for q in form['questions']}
                        result=finish(raw)['report']
                        self.assertEqual(result['evidence']['answer:'+variant['id']]['question'],variant['text'])
                        self.assertLessEqual(result['question_count'],18)
                        self.assertNotIn('Mod',json.dumps(result['report_sections'],ensure_ascii=False))

    def test_replace_removes_old_answer_and_ties_without_counting_unexperienced(self):
        raw=answered();old=next(iter(raw['answers']))
        raw['extra_answers']=[{'question_id':'old-tie','answer':'A'}]
        form=v05.replace_question(raw,old);response=form['response']
        self.assertEqual(len(form['questions']),16)
        self.assertNotIn(old,response['answers'])
        self.assertEqual(response['extra_answers'],[])
        self.assertEqual(len(response['answers']),15)
        with self.assertRaises(InputError):v05.report(response)
        new=form['questions'][0]
        response['answers'][new['id']]='C'
        result=finish(response)['report']
        self.assertNotIn('answer:'+old,result['evidence'])
        self.assertIn('answer:'+new['id'],result['evidence'])
        self.assertIn(old,response['replacement_history'][new['slot_id']])

    def test_exhausted_replacements_can_be_undone_and_resume_exact_form(self):
        form=questionnaires.questions('genshin-impact');first=form['questions'][0]['id']
        seen={first}
        while form['questions'][0]['can_replace']:
            form=v05.replace_question(form['response'],form['questions'][0]['id'])
            self.assertNotIn(form['questions'][0]['id'],seen);seen.add(form['questions'][0]['id'])
        with self.assertRaises(InputError):v05.replace_question(form['response'],form['questions'][0]['id'])
        restored=v05.replace_question(form['response'],form['questions'][0]['id'],undo=True)
        self.assertEqual(restored['questions'][0]['id'],first)
        resumed=questionnaires.questions(raw=restored['response'])
        self.assertEqual(restored,resumed)

    def test_foreign_questions_history_versions_and_stale_answers_are_rejected(self):
        for mutate in (
            lambda r:r.update(pack_version='../../arbitrary'),
            lambda r:r.update(mode_id='unknown-mode'),
            lambda r:r['question_variants'].update(GI01='CS201.V1'),
            lambda r:r['replacement_history'].update(GI01=['GI01.V1','GI01.V1']),
            lambda r:r['answers'].update(GI01='A'),
        ):
            raw=answered();mutate(raw)
            with self.assertRaises(InputError):v05.report(raw)
        with self.assertRaises(InputError):v05.replace_question(answered(),'X14')

    def test_archived_pack_snapshot_still_reconstructs_saved_answers(self):
        raw=answered();before=finish(raw)
        updated=deepcopy(v05.bank())
        pack=next(p for p in updated['packs'] if raw['game_id'] in p['game_ids'])
        pack['version']='0.5.0+000000000000'
        pack['slots'][0]['variants'][0]['text']='New question with a new meaning'
        with patch.object(v05,'bank',return_value=updated):
            self.assertEqual(finish(raw),before)

    def test_legacy_six_game_responses_keep_old_questions_points_and_copy(self):
        for pack in v05.bank()['packs']:
            gid=pack['game_ids'][0]
            raw={'versions':deepcopy(v04.config()['versions']),'game_id':gid,
                 'answers':{q['id']:'A' for q in v04.questionnaire(gid)},'extra_answers':[]}
            a=finish(raw);b=v04.report(a['response'])
            self.assertEqual(a,b)
            form=questionnaires.questions(raw=a['response'])
            self.assertEqual([q['id'] for q in form['questions']],[q['id'] for q in v04.questionnaire(gid)])

    def test_same_signal_cannot_gain_nine_times_the_anchor_contribution(self):
        raw=answered('steam-730');form=v05.questions(raw=raw)['questions'];signal='practice_seeker'
        for q in form:
            internal=next(i for i in v05._form(v05.pack_for(raw['game_id']),v05.mode_for(v05.pack_for(raw['game_id'])),{}, {}) if i['id']==q['id'])
            option=next((o for o in internal['options'] if o['signal']==signal),internal['options'][0])
            raw['answers'][q['id']]=option['id']
        result=finish(raw)['report']['audit']
        self.assertGreater(result['anchor_support_count'][signal],2)
        self.assertGreater(result['uncapped_semantic_points'][signal],6)
        bonus=sum(t['bonus'] for t in result['tie_trace'] if t['candidate_ids'][ord(t['choice'])-65]==signal)
        self.assertLessEqual(result['points'][signal]-bonus,6)

    def test_random_and_replaced_forms_finish_with_at_most_two_extra_questions(self):
        rng=random.Random(705)
        for pack in v05.bank()['packs']:
            for mode in pack['modes']:
                for _ in range(8):
                    form=questionnaires.questions(pack['game_ids'][0],mode_id=mode['id'])
                    for n in rng.sample(range(12),3):
                        if form['questions'][n]['can_replace']:form=v05.replace_question(form['response'],form['questions'][n]['id'])
                    raw=form['response'];raw['answers']={q['id']:rng.choice(q['options'])['id'] for q in form['questions']}
                    self.assertTrue(finish(raw,letter=rng.choice('ABCD'))['complete'])

    def test_mixed_version_comparison_only_compares_matching_semantics(self):
        old=v04.demo('B')['response'];new=finish(answered())['response']
        result=questionnaires.compare(old,new)
        self.assertTrue(any(row['topic']=='coop' for row in result['coordination']))
        self.assertTrue(any(row['status']=='先聊一聊' for row in result['coordination']))
        self.assertTrue(all(row['left']['text'] and row['right']['text'] for row in result['coordination']))

    def test_different_scenes_in_same_slot_are_not_called_a_behavior_conflict(self):
        a=answered('steam-1245620')
        q=questionnaires.questions(raw=a)['questions'][4]
        form=v05.replace_question(a,q['id']);b=form['response']
        b['answers'][form['questions'][4]['id']]='A'
        result=questionnaires.compare(finish(a)['response'],finish(b)['response'])
        row=next(r for r in result['coordination'] if r['topic']=='v05:ER05')
        self.assertEqual(row['status'],'先聊一聊')


class QuietHandler(Handler):
    def log_message(self,*args):pass


class AuthoredHTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),QuietHandler)
        cls.server.access_control=AccessController(password_record('test-only-question-password'))
        cls.base='http://127.0.0.1:'+str(cls.server.server_port)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        _,data=cls.request('/api/access/login',{'password':'test-only-question-password'})
        cls.token=data['access_token']

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join(timeout=2)

    @classmethod
    def request(cls,path,body=None,authenticated=False):
        headers={'Content-Type':'application/json'}
        if authenticated:headers['Authorization']='Bearer '+cls.token
        request=Request(cls.base+path,data=json.dumps(body).encode() if body is not None else None,headers=headers)
        try:
            with urlopen(request) as response:return response.status,json.load(response)
        except HTTPError as error:
            result=error.code,json.load(error);error.close();return result

    def test_new_routes_require_login(self):
        for path in ('/api/v4/questions','/api/v4/replace-question'):
            self.assertEqual(self.request(path,{})[0],401)

    def test_real_http_replacement_resume_and_report(self):
        status,form=self.request('/api/v4/questions?game_id=genshin-impact',authenticated=True)
        self.assertEqual(status,200)
        status,replaced=self.request('/api/v4/replace-question',{'response':form['response'],'question_id':form['questions'][0]['id']},True)
        self.assertEqual(status,200)
        self.assertNotEqual(form['questions'][0]['id'],replaced['questions'][0]['id'])
        status,resumed=self.request('/api/v4/questions',replaced['response'],True)
        self.assertEqual(resumed['questions'],replaced['questions'])
        raw=resumed['response'];raw['answers']={q['id']:'D' for q in resumed['questions']}
        for _ in range(3):
            status,result=self.request('/api/v4/report',raw,True)
            self.assertEqual(status,200)
            if result['complete']:break
            raw['extra_answers'].append({'question_id':result['next_question']['id'],'answer':'D'})
        self.assertTrue(result['complete'])
        self.assertEqual(result['report']['versions']['instrument'],'0.5.0')


if __name__=='__main__':unittest.main()
