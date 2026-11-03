"""Two-chapter portraits, report-only version migration, and preserved scoring."""
from copy import deepcopy
import unittest
from youge import v04
from youge.engine import InputError
from tests.test_v04 import response,finish


class PersonalityPortraitTests(unittest.TestCase):
    def test_every_persona_has_a_complete_original_portrait_in_bootstrap(self):
        people=v04.bootstrap()['personas']
        self.assertEqual({p['id'] for p in people},set(v04.config()['personality_portraits']['personas']))
        for p in people:
            profile=p['personality_profile']
            self.assertEqual(len(profile['traits']),3)
            self.assertTrue(profile['headline'] and profile['credo'])
            self.assertEqual(len(profile['inner_world']),3)
            self.assertEqual(len(profile['with_others']),2)

    def test_report_exposes_exactly_two_reader_chapters_without_answer_recitals(self):
        for case in 'ABC':
            r=v04.demo(case)['report']
            self.assertEqual([s['title'] for s in r['report_sections']],['你的性格底色','与你相处的方式'])
            self.assertEqual([s['id'] for s in r['report_sections']],['character','relations'])
            for s in r['report_sections']:
                self.assertNotIn('evidence_refs',s)
                self.assertTrue(s['paragraphs'])
                self.assertTrue(all('你选了' not in p and '答案依据' not in p for p in s['paragraphs']))

    def test_old_report_version_migrates_without_changing_persona_or_points(self):
        raw=deepcopy(v04.demo('B')['response']);old=deepcopy(raw)
        old['versions']['report_rules']='0.4.0'
        before=v04.report(raw);after=v04.report(old)
        self.assertEqual(before,after)
        self.assertEqual(after['response']['versions']['report_rules'],'0.4.1')
        self.assertEqual(after['report']['persona']['id'],'wanderer')

    def test_only_known_copy_version_migration_is_accepted(self):
        for key,value in [('instrument','0.4.1'),('scoring','0.4.1'),('catalog','0.4.1'),('report_rules','0.9.9')]:
            raw=response();raw['versions'][key]=value
            with self.assertRaises(InputError):v04.report(raw)

    def test_time_and_mod_limits_change_relationship_copy_not_character(self):
        raw=deepcopy(v04.demo('B')['response']);changed=deepcopy(raw)
        changed['answers']['G09']='B';changed['answers']['G10']='C'
        a,b=[v04.report(v)['report'] for v in (raw,changed)]
        self.assertEqual(a['audit']['points'],b['audit']['points'])
        self.assertEqual(a['report_sections'][0],b['report_sections'][0])
        self.assertNotEqual(a['report_sections'][1],b['report_sections'][1])
        text=''.join(b['report_sections'][1]['paragraphs'])
        self.assertIn('现实时间',text);self.assertIn('平台',text)
