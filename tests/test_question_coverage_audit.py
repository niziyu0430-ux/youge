"""Guard audit claims against renamed templates, shuffled answers and missing records."""
from copy import deepcopy
import unittest

from scripts.check_game_question_coverage import audit,inspect_form,status_for,template_keys
from youge import v04


class QuestionCoverageAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.templates=template_keys(v04.config())

    def test_game_title_substitution_cannot_make_a_template_dedicated(self):
        form=deepcopy(v04.questionnaire('steam-730'))
        for q in form:
            q['text']=q['text'].replace('反恐精英2','另一款作品')
            for o in q['options']:o['label']=o['label'].replace('反恐精英2','另一款作品')
        # Even falsely claiming that every ID was authored cannot override the actual text.
        finding=inspect_form(form,'另一款作品',self.templates,{q['id'] for q in form})
        self.assertEqual(len(finding['dedicated_ids']),0)
        self.assertEqual(len(finding['template_ids']),12)
        self.assertEqual(status_for([finding],[]),'generic_template')

    def test_reordering_choices_is_not_authorship(self):
        form=deepcopy(v04.questionnaire('steam-730'))
        for q in form:
            q['options'].reverse()
            for i,o in enumerate(q['options']):o['id']='ABCD'[i]
        finding=inspect_form(form,'反恐精英2',self.templates,{q['id'] for q in form})
        self.assertEqual(len(finding['dedicated_ids']),0)
        self.assertEqual(status_for([finding],[]),'generic_template')

    def test_old_named_pack_is_partial_and_four_cross_questions_are_allowed(self):
        config=v04.config();pack='civ6'
        authored={q['id'] for q in config['packs'][pack]}|set(config['anchor_context'][pack])
        finding=inspect_form(v04.questionnaire('steam-289070'),'文明6',self.templates,authored)
        self.assertEqual(finding['errors'],[])
        self.assertEqual(len(finding['dedicated_ids']),8)
        self.assertEqual(finding['template_ids'],['G08','G09','G10','G11'])
        self.assertEqual(len(finding['shared_ids']),4)
        self.assertEqual(status_for([finding],[]),'partial_dedicated')

    def test_new_text_without_authoring_record_needs_review(self):
        form=deepcopy(v04.questionnaire('steam-730'))
        form[0]['text']='一个未登记来源的全新场景，下一步先做什么？'
        finding=inspect_form(form,'反恐精英2',self.templates,set())
        self.assertEqual(finding['uncertain_ids'],['G01'])
        self.assertEqual(status_for([finding],[]),'needs_review')

    def test_all_current_records_and_mode_routes_are_accounted_for(self):
        report=audit('2026-10-30');catalog=v04.catalog()
        self.assertEqual({r['game_id'] for r in report['games']},{g['id'] for g in catalog['games']})
        self.assertEqual({r['game_id'] for r in report['candidates']},{g['id'] for g in catalog['candidates']})
        self.assertEqual(len(report['games']),len(catalog['games']))
        self.assertEqual(sum(report['published_status_counts'].values()),len(catalog['games']))
        self.assertEqual(report['duplicate_game_ids'],[])
        self.assertEqual(report['orphan_authored_game_ids'],[])
        self.assertTrue(report['inputs_unchanged_during_audit'])
        self.assertEqual(report['candidate_legacy_forms_checked'],report['candidate_legacy_forms_structurally_valid'])
        for row in report['games']:
            self.assertEqual(row['errors'],[])
            self.assertEqual(len(row['forms']),row['mode_count'])
            if row['has_complete_dedicated_form']:
                self.assertTrue(all(len(f['dedicated_ids'])==12 and not f['template_ids'] for f in row['forms']))
        grouped=sum(g['count'] for g in report['generic_template_groups'])
        self.assertEqual(grouped,report['published_status_counts'].get('generic_template',0))


if __name__=='__main__':unittest.main()
