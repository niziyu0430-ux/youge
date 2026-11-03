"""Contracts that keep authored drafts reviewable and out of the live instrument."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from youge import v04,v05

ROOT=Path(__file__).resolve().parents[1]


class QuestionDesignDraftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.draft=json.loads((ROOT/'config/question-packs.v0.5.draft.json').read_text(encoding='utf-8'))

    def test_every_authored_game_has_twelve_specific_items_and_the_same_four_shared_items(self):
        current=[q for q in v04.config()['common'] if q['scope']=='cross']
        self.assertEqual(self.draft['shared_questions'],current)
        identifiers=set()
        game_ids={g['id'] for g in v04.catalog()['games']}
        sources={s['id'] for s in self.draft['sources']}
        for pack in self.draft['packs']:
            self.assertTrue(set(pack['game_ids'])<=game_ids)
            self.assertEqual(len(pack['questions']),12)
            self.assertEqual(sum(q['question_type']=='situational_action' for q in pack['questions']),8)
            self.assertEqual(sum(q['question_type']=='experience_reflection' for q in pack['questions']),4)
            for question in pack['questions']:
                self.assertNotIn(question['id'],identifiers)
                identifiers.add(question['id'])
                self.assertTrue(question['source_ids'])
                self.assertTrue(set(question['source_ids'])<=sources)
                self.assertEqual([o['id'] for o in question['options']],list('ABCD'))
                self.assertEqual(len({o['label'] for o in question['options']}),4)
                self.assertNotIn('{game}',question['text'])
                self.assertTrue(question['design_purpose'])
                self.assertTrue(question['interpretation_boundary'])

    def test_unexperienced_choices_are_not_answers_or_negative_scores(self):
        self.assertEqual(self.draft['decisions']['replace_means'],
                         'no_answer_no_score_replace_with_reviewed_alternative')
        for pack in self.draft['packs']:
            for question in pack['questions']:
                self.assertFalse(any(o['label']=='没体验过' for o in question['options']))
                for alternative in question['alternatives']:
                    self.assertEqual([o['id'] for o in alternative['options']],list('ABCD'))
                    self.assertEqual(len({o['label'] for o in alternative['options']}),4)
                    self.assertFalse(any(o['label']=='没体验过' for o in alternative['options']))
                    self.assertEqual(alternative['equivalence_status'],
                                     'independent_scene_not_empirically_equated')

    def test_solo_early_story_alternative_does_not_require_social_evidence(self):
        genshin=next(p for p in self.draft['packs'] if p['id']=='gi')
        question=next(q for q in genshin['questions'] if q['id']=='GI06')
        original={o['proposed_signal'] for o in question['options']}
        alternative={o['proposed_signal'] for o in question['alternatives'][0]['options']}
        self.assertIn('social_spark',original)
        self.assertNotIn('social_spark',alternative)
        self.assertNotIn('quest_board',alternative)
        self.assertIn('wanderer',alternative)

    def test_drafts_cannot_silently_replace_existing_answers(self):
        self.assertFalse(self.draft['runtime_enabled'])
        live_versions=deepcopy(v04.config()['versions'])
        for pack in self.draft['packs']:
            self.assertFalse(pack['runtime_enabled'])
            self.assertEqual(pack['player_review'],'pending')
            new_ids={q['id'] for q in pack['questions']}
            for game_id in pack['game_ids']:
                self.assertFalse(new_ids & {q['id'] for q in v04.questionnaire(game_id)})
        self.assertEqual(v04.config()['versions'],live_versions)

    def test_proposed_signals_have_a_known_persona_or_explicit_behavior_only_status(self):
        personas={p['id'] for p in v04.config()['personas']}
        behavior_only=set(v05.bank()['behavior_copy'])
        for pack in self.draft['packs']:
            for q in pack['questions']:
                for option in q['options']+[o for a in q['alternatives'] for o in a['options']]:
                    self.assertIn(option['proposed_signal'],personas|behavior_only)
                    self.assertNotIn('weights',option)


if __name__=='__main__':
    unittest.main()
