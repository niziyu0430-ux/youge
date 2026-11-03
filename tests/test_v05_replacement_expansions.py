"""Explicit replacement into compatible expansions; no automatic rescoring."""
from copy import deepcopy
from http.server import ThreadingHTTPServer
import json
import threading
import unittest
from unittest.mock import patch
from urllib.request import Request, urlopen

from youge import v05
from youge.access import AccessController, password_record
from youge.engine import InputError
from youge.web import Handler


def finish(raw):
    raw=deepcopy(raw)
    for _ in range(3):
        result=v05.report(raw)
        if result['complete']:return result
        raw['extra_answers'].append({'question_id':result['next_question']['id'],'answer':'A'})
    raise AssertionError('More than two followups')


class ReplacementExpansionTests(unittest.TestCase):
    def setUp(self):
        self.gid='genshin-impact'
        form=v05.questions(self.gid)
        self.raw=deepcopy(form['response']);self.raw['fictional']=True
        self.raw['answers']={q['id']:'A' for q in form['questions']}
        self.old=deepcopy(v05.pack_for(self.gid))
        self.latest=deepcopy(self.old);self.latest['version']='test-only-append-expansion'
        self.addition=deepcopy(self.old['slots'][0]['variants'][-1])
        self.addition.update(id=self.old['slots'][0]['id']+'.APPEND_TEST_ONLY',
                             text='仅用于运行测试的新增情境，不会发布进题库。',
                             modes=[self.raw['mode_id']])
        self.latest['slots'][0]['variants'].append(self.addition)
        self.original_lookup=v05.pack_for

    def lookup(self,game_id,version=None):
        if game_id!=self.gid:return self.original_lookup(game_id,version)
        if version is None or version==self.latest['version']:return self.latest
        if version==self.old['version']:return self.old
        return None

    def mocked_lookup(self):
        return patch.object(v05,'pack_for',side_effect=self.lookup)

    def exhaust_old(self):
        form=v05.questions(raw=self.raw)
        while form['questions'][0]['can_replace']:
            form=v05.replace_question(form['response'],form['questions'][0]['id'])
            self.assertEqual(form['response']['pack_version'],self.old['version'])
        return form

    def test_resume_and_old_completed_report_remain_exactly_pinned(self):
        form=v05.questions(raw=self.raw);report=finish(self.raw)
        unchanged=deepcopy(self.raw)
        with self.mocked_lookup():
            self.assertEqual(v05.questions(raw=self.raw),form)
            self.assertEqual(finish(self.raw),report)
            self.assertEqual(self.raw,unchanged)

    def test_only_explicit_exhausted_replacement_uses_new_scene(self):
        with self.mocked_lookup():
            exhausted=self.exhaust_old();raw=exhausted['response'];old_question=exhausted['questions'][0]
            raw['answers'][old_question['id']]='C'
            raw['extra_answers']=[{'question_id':'obsolete-test-followup','answer':'A'}]
            before=deepcopy(raw)
            other_answers={key:value for key,value in raw['answers'].items() if key!=old_question['id']}
            result=v05.replace_question(raw,old_question['id'])
            self.assertEqual(raw,before,'The stored old response must not be mutated')
            self.assertEqual(result['response']['pack_version'],self.latest['version'])
            self.assertEqual(result['response']['mode_id'],raw['mode_id'])
            self.assertEqual(result['questions'][0]['id'],self.addition['id'])
            self.assertEqual(len(result['questions']),16)
            self.assertEqual(result['questions'][12:],exhausted['questions'][12:])
            self.assertEqual(result['response']['answers'],other_answers)
            self.assertEqual(result['response']['extra_answers'],[])
            self.assertIn(old_question['id'],result['response']['replacement_history'][old_question['slot_id']])
            with self.assertRaises(InputError):v05.report(result['response'])
            result['response']['answers'][self.addition['id']]='D'
            report=finish(result['response'])['report']
            self.assertNotIn('answer:'+old_question['id'],report['evidence'])
            self.assertEqual(report['evidence']['answer:'+self.addition['id']]['question'],self.addition['text'])

    def test_expanded_form_undo_and_resume_keep_exact_scene_and_answers(self):
        with self.mocked_lookup():
            exhausted=self.exhaust_old();old_question=exhausted['questions'][0]
            expanded=v05.replace_question(exhausted['response'],old_question['id'])
            self.assertEqual(v05.questions(raw=expanded['response']),expanded)
            undone=v05.replace_question(expanded['response'],self.addition['id'],undo=True)
            self.assertEqual(undone['questions'][0]['id'],old_question['id'])
            self.assertEqual(undone['questions'][0]['text'],old_question['text'])
            self.assertEqual(undone['questions'][0]['options'],old_question['options'])
            self.assertEqual(undone['response']['answers'],exhausted['response']['answers'])
            self.assertEqual(undone['questions'][12:],exhausted['questions'][12:])
            self.assertEqual(v05.questions(raw=undone['response']),undone)
            # The newer uniform version remains; all restored old payloads are identical.
            self.assertEqual(undone['response']['pack_version'],self.latest['version'])

    def test_changes_to_any_old_semantics_or_mode_refuse_continuation(self):
        def change_signal(pack):
            option=pack['slots'][1]['variants'][0]['options'][0]
            option['signal']='practice_seeker' if option['signal']!='practice_seeker' else 'wanderer'
        mutators={
            'old_text':lambda p:p['slots'][1]['variants'][0].update(text='Changed original meaning'),
            'old_choice_label':lambda p:p['slots'][1]['variants'][0]['options'][0].update(label='Changed old answer'),
            'old_signal':change_signal,
            'old_source_binding':lambda p:p['slots'][1]['variants'][0]['source_ids'].append('changed-test-source'),
            'old_mode':lambda p:p['modes'][0].update(label='Changed old experience scope'),
            'old_scene_mode':lambda p:p['slots'][1]['variants'][0].update(modes=['another-test-mode']),
            'scope':lambda p:p.update(scope='Changed whole-game scope'),
            'removed_old_variant':lambda p:p['slots'][1]['variants'].pop(0),
            'slot_order':lambda p:p['slots'].reverse(),
        }
        pristine=deepcopy(self.latest)
        for name,mutate in mutators.items():
            with self.subTest(change=name):
                self.latest=deepcopy(pristine);mutate(self.latest)
                with self.mocked_lookup():
                    exhausted=self.exhaust_old();before=deepcopy(exhausted['response'])
                    with self.assertRaises(InputError):v05.replace_question(before,exhausted['questions'][0]['id'])
                    self.assertEqual(exhausted['response'],before)
                    self.assertEqual(v05.questions(raw=before),exhausted)

    def test_new_scene_for_another_mode_is_not_borrowed(self):
        self.latest['slots'][0]['variants'][-1]['modes']=['different-test-mode']
        with self.mocked_lookup():
            exhausted=self.exhaust_old();before=deepcopy(exhausted['response'])
            with self.assertRaises(InputError):v05.replace_question(before,exhausted['questions'][0]['id'])
            self.assertEqual(before,exhausted['response'])

    def test_new_scene_for_another_slot_is_not_borrowed(self):
        addition=self.latest['slots'][0]['variants'].pop()
        addition['id']=self.latest['slots'][1]['id']+'.APPEND_TEST_ONLY'
        self.latest['slots'][1]['variants'].append(addition)
        with self.mocked_lookup():
            exhausted=self.exhaust_old();before=deepcopy(exhausted['response'])
            with self.assertRaises(InputError):v05.replace_question(before,exhausted['questions'][0]['id'])
            self.assertEqual(before,exhausted['response'])

    def test_new_pool_exhaustion_does_not_skip_score_or_mutate(self):
        with self.mocked_lookup():
            exhausted=self.exhaust_old()
            expanded=v05.replace_question(exhausted['response'],exhausted['questions'][0]['id'])
            before=deepcopy(expanded)
            self.assertFalse(expanded['questions'][0]['can_replace'])
            with self.assertRaises(InputError):v05.replace_question(expanded['response'],self.addition['id'])
            self.assertEqual(expanded,before)
            self.assertEqual(len(expanded['questions']),16)
            self.assertNotIn(self.addition['id'],expanded['response']['answers'])

    def test_real_http_explicit_recheck_resumes_compatible_expansion(self):
        class QuietHandler(Handler):
            def log_message(self,*args):pass
        with self.mocked_lookup():
            exhausted=self.exhaust_old()
            server=ThreadingHTTPServer(('127.0.0.1',0),QuietHandler)
            server.access_control=AccessController(password_record('expansion-test-only'))
            base='http://127.0.0.1:'+str(server.server_port)
            thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            def post(path,body,token=None):
                headers={'Content-Type':'application/json'}
                if token:headers['Authorization']='Bearer '+token
                req=Request(base+path,data=json.dumps(body).encode(),headers=headers)
                with urlopen(req,timeout=10) as response:return json.load(response)
            try:
                token=post('/api/access/login',{'password':'expansion-test-only'})['access_token']
                original=post('/api/v4/questions',exhausted['response'],token)
                self.assertEqual(original,exhausted)
                updated=post('/api/v4/replace-question',{'response':exhausted['response'],'question_id':exhausted['questions'][0]['id']},token)
                self.assertEqual(updated['questions'][0]['id'],self.addition['id'])
                self.assertEqual(updated['response']['pack_version'],self.latest['version'])
                self.assertEqual(post('/api/v4/questions',updated['response'],token),updated)
                self.assertEqual(post('/api/v4/questions',exhausted['response'],token),exhausted)
            finally:
                server.shutdown();server.server_close();thread.join(timeout=2)


if __name__=='__main__':unittest.main()
