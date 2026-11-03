"""Contracts for the new 16-item, four-choice instrument and its real HTTP routes."""
from copy import deepcopy
from http.server import ThreadingHTTPServer
import json
import random
import hashlib
from pathlib import Path
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from unittest.mock import patch

from youge import v04
from youge.engine import InputError
from youge.web import Handler


def response(game_id=None):
    gid=game_id or v04.catalog()['featured'][0]
    return {'versions':deepcopy(v04.config()['versions']),'respondent_id':'fictional-test',
            'display_name':'虚构测试','game_id':gid,
            'answers':{q['id']:'A' for q in v04.questionnaire(gid)},'extra_answers':[],'fictional':True}


def finish(raw,choose='A'):
    for _ in range(3):
        result=v04.report(raw)
        if result['complete']:return result
        raw['extra_answers'].append({'question_id':result['next_question']['id'],'answer':choose})
    raise AssertionError('More than two extra questions')


class InstrumentV04Tests(unittest.TestCase):
    def test_catalogue_has_unlimited_consistent_categories_and_preserves_question_packs(self):
        lib=v04.catalog();ids={g['id'] for g in lib['games']}
        self.assertGreaterEqual(len(lib['categories']),47)
        self.assertGreater(len(ids),753)
        self.assertEqual(sum(len(c['game_ids']) for c in lib['categories']),lib['category_assignment_count'])
        self.assertTrue(any(len(c['game_ids'])>20 for c in lib['categories']))
        for c in lib['categories']:
            self.assertEqual(len(set(c['game_ids'])),len(c['game_ids']),c['id'])
            self.assertTrue(set(c['game_ids'])<=ids)
        self.assertEqual(v04.find_game('steam-261550')['question_pack'],'bannerlord')

    def test_every_catalogue_form_has_sixteen_single_four_choice_items(self):
        for g in v04.catalog()['games']:
            items=v04.questionnaire(g['id'])
            self.assertEqual(len(items),16)
            self.assertEqual(len({q['id'] for q in items}),16)
            self.assertEqual(sum(q['scope']=='cross' for q in items),4)
            for q in items:
                self.assertEqual(q['response_type'],'single')
                self.assertEqual([o['id'] for o in q['options']],list('ABCD'))
                self.assertEqual(len({o['label'] for o in q['options']}),4)
                for o in q['options']:
                    for hint in ('更接近','倾向','人格','加分','维度'):
                        self.assertNotIn(hint,o['label'])

    def test_public_items_do_not_reveal_the_scoring_key(self):
        for q in v04.questionnaire('steam-261550'):
            public=v04.public_question(q)
            self.assertEqual(set(public),{'id','text','scope','order','options'})
            self.assertTrue(all(set(o)=={'id','label'} for o in public['options']))

    def test_renaming_a_game_changes_no_persona_points(self):
        raw=response();before=finish(deepcopy(raw))['report'];changed=deepcopy(v04.catalog())
        next(g for g in changed['games'] if g['id']==raw['game_id'])['title']='只替换显示名称'
        with patch.object(v04,'catalog',return_value=changed):after=finish(deepcopy(raw))['report']
        self.assertEqual(before['audit']['points'],after['audit']['points'])
        self.assertEqual(before['persona']['id'],after['persona']['id'])

    def test_all_sixteen_portraits_are_distinct_local_png_assets(self):
        hashes=set()
        for p in v04.config()['personas']:
            data=(v04.ROOT/'web'/p['portrait'].lstrip('/')).read_bytes()
            self.assertEqual(data[:8],b'\x89PNG\r\n\x1a\n')
            self.assertGreater(len(data),100_000)
            hashes.add(hashlib.sha256(data).hexdigest())
        self.assertEqual(len(hashes),16)

    def test_every_game_has_a_primary_source_and_c_is_the_limited_mod_example(self):
        self.assertTrue(all(g['source_url'].startswith('https://') for g in v04.catalog()['games']))
        c=v04.demo('C')['report']
        self.assertEqual(c['response']['answers']['G09'],'B')
        self.assertEqual(c['response']['answers']['G10'],'C')

    def test_only_catalogue_games_and_exact_single_choices_are_accepted(self):
        for value in ('unknown',None,['steam-261550']):
            raw=response();raw['game_id']=value
            with self.assertRaises(InputError):v04.report(raw)
        for value in ('E',3,None,['A','B'],True):
            raw=response();raw['answers']['G01']=value
            with self.assertRaises(InputError):v04.report(raw)
        raw=response();del raw['answers']['G01']
        with self.assertRaises(InputError):v04.report(raw)

    def test_same_game_different_motives_and_different_games_same_persona(self):
        a,b,c=[v04.demo(x)['report'] for x in 'ABC']
        self.assertEqual(a['game']['id'],b['game']['id'])
        self.assertNotEqual(a['persona']['id'],b['persona']['id'])
        self.assertNotEqual(b['game']['id'],c['game']['id'])
        self.assertEqual(b['persona']['id'],c['persona']['id'])
        self.assertTrue(all(r['fictional'] for r in (a,b,c)))

    def test_mod_conditions_guide_and_replay_do_not_change_persona_points(self):
        baseline=finish(response())['report']
        for qid in ('G05','G07','G08','G09','G10','G12'):
            for option in 'ABCD':
                raw=response();raw['answers'][qid]=option
                r=finish(raw)['report']
                self.assertEqual(r['audit']['points'],baseline['audit']['points'])
                self.assertEqual(r['persona']['id'],baseline['persona']['id'])

    def test_time_limited_replay_has_a_different_explanation_from_new_first(self):
        a=response();a['answers']['G09']='B';a=finish(a)['report']
        b=response();b['answers']['G09']='C';b=finish(b)['report']
        self.assertIn('时间',next(x['text'] for x in a['advice'] if x['topic']=='replay'))
        self.assertIn('新作品',next(x['text'] for x in b['advice'] if x['topic']=='replay'))
        self.assertFalse(any(x['rule_id']=='D_REPLAY' for x in a['drains']))
        self.assertTrue(any(x['rule_id']=='D_REPLAY' for x in b['drains']))

    def test_all_sixteen_personas_can_be_reached(self):
        reached=set()
        candidates=v04.catalog()['featured']+[g['id'] for g in v04.catalog()['games'] if g['mechanic_family'] in ('sports','shooter','puzzle','creative','story','racing')][:120]
        for p in v04.config()['personas']:
            for gid in candidates:
                raw=response(gid)
                for q in v04.questionnaire(gid):
                    raw['answers'][q['id']]=max(q['options'],key=lambda o:o['weights'].get(p['id'],0))['id']
                for _ in range(3):
                    result=v04.report(raw)
                    if result['complete']:
                        if result['report']['persona']['id']==p['id']:reached.add(p['id'])
                        break
                    q=result['next_question'];label=v04.config()['tie_actions'][p['id']][len(raw['extra_answers'])]
                    chosen=next((o['id'] for o in q['options'] if o['label']==label),'A')
                    raw['extra_answers'].append({'question_id':q['id'],'answer':chosen})
                if p['id'] in reached:break
        self.assertEqual(reached,{p['id'] for p in v04.config()['personas']})

    def test_ties_are_deterministic_and_always_finish_by_eighteen(self):
        rng=random.Random(42);lengths=set();first_extra=None
        for _ in range(150):
            raw=response(rng.choice(v04.catalog()['featured']))
            raw['answers']={q:rng.choice('ABCD') for q in raw['answers']}
            base=v04.report(raw)
            if not base['complete'] and first_extra is None:first_extra=deepcopy(raw)
            result=finish(raw,rng.choice('ABCD'));r=result['report'];lengths.add(r['question_count'])
            self.assertIn(r['question_count'],(16,17,18))
            self.assertEqual(result,v04.report(result['response']))
            self.assertEqual(len([r['persona']]),1)
            self.assertTrue(v04.verify(r))
            for claim in r['insights']:
                if claim['scope']=='gaming':self.assertGreaterEqual(len(claim['evidence_refs']),2)
        self.assertEqual(lengths,{16,17,18})
        q=v04.report(first_extra)['next_question']
        self.assertEqual(len(q['options']),4)
        self.assertTrue(all(set(o)=={'id','label'} for o in q['options']))

    def test_wrong_or_unneeded_discriminator_and_other_versions_are_rejected(self):
        raw=response();raw['extra_answers']=[{'question_id':'T01.wrong','answer':'A'}]
        with self.assertRaises(InputError):v04.report(raw)
        raw=response();raw['versions']['instrument']='0.3.0'
        with self.assertRaises(InputError):v04.report(raw)

    def test_all_reports_keep_actual_answer_evidence_and_no_compatibility_percentage(self):
        a,b=[v04.demo(x) for x in 'AB']
        r=a['report']
        for ref,e in r['evidence'].items():
            self.assertTrue(ref.startswith('answer:'))
            q=next(q for q in v04.questionnaire(r['game']['id']) if q['id']==e['question_id'])
            self.assertEqual(e['label'],next(o['label'] for o in q['options'] if o['id']==e['answer']))
        pair=v04.compare(a['response'],b['response'])
        self.assertTrue(pair['same_game']);self.assertEqual(len(pair['coordination']),8)
        self.assertNotIn('compatibility',pair)


class QuietHandler(Handler):
    def log_message(self,*args):pass


class HTTPV04Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),QuietHandler)
        from youge.access import AccessController,password_record
        cls.server.access_control=AccessController(password_record('test-only-shared-password'))
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        cls.base='http://127.0.0.1:'+str(cls.server.server_port)
        request=Request(cls.base+'/api/access/login',json.dumps({'password':'test-only-shared-password'}).encode(),headers={'Content-Type':'application/json'})
        with urlopen(request) as response:cls.access_token=json.load(response)['access_token']

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join()

    def request(self,path,data=None):
        req=Request(self.base+path,json.dumps(data).encode() if data else None,headers={'Content-Type':'application/json','Authorization':'Bearer '+self.access_token})
        with urlopen(req) as r:return json.load(r)

    def test_authenticated_bootstrap_and_game_questions(self):
        data=self.request('/api/v4/bootstrap')
        self.assertEqual(len(data['personas']),16)
        data=self.request('/api/v4/questions?game_id=steam-261550&instrument=0.4.0')
        self.assertEqual(len(data['questions']),16)
        self.assertIn('战场',data['questions'][0]['options'][0]['label'])

    def test_complete_report_and_compare(self):
        a=self.request('/api/v4/demo?case=A');b=self.request('/api/v4/demo?case=B')
        self.assertEqual(self.request('/api/v4/report',a['response']),a)
        self.assertTrue(self.request('/api/v4/compare',{'left':a['response'],'right':b['response']})['same_game'])

    def test_invalid_game_and_fifth_choice_produce_user_errors(self):
        with self.assertRaises(HTTPError) as e:self.request('/api/v4/questions?game_id=unlisted')
        self.assertEqual(e.exception.code,400);e.exception.close()
        raw=response();raw['answers']['G01']='E'
        with self.assertRaises(HTTPError) as e:self.request('/api/v4/report',raw)
        self.assertEqual(e.exception.code,400);e.exception.close()
