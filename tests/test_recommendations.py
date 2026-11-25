"""Verified recommendation content, answer signals, and selection rules."""
from collections import defaultdict
from copy import deepcopy
import unittest

from tests.test_v04 import finish as finish_legacy, response
from tests.test_v05 import answered, finish
from youge import recommendations, v04, v05


class GameRecommendationsTests(unittest.TestCase):
    def test_every_motive_has_eight_distinct_verified_pc_works(self):
        games = {game['id']: game for game in v04.catalog()['games']}
        motives = {persona['id'] for persona in v04.config()['personas']}
        coverage = defaultdict(set)
        for game_id, entry in recommendations.curated_games().items():
            with self.subTest(game=game_id):
                self.assertIn(game_id, v04.public_game_ids())
                self.assertNotIn(game_id, v04.catalog().get('search_redirects', {}))
                game = games[game_id]
                self.assertEqual(game['visibility'], 'published')
                self.assertTrue(game['source_url'].startswith('https://'))
                self.assertTrue(entry['reasons'])
                if 'platform' in entry:
                    self.assertIn(entry['platform'], game['platforms'])
                for motive, reason in entry['reasons'].items():
                    self.assertIn(motive, motives)
                    self.assertTrue(15 <= len(reason) <= 30, reason)
                    if 'PC' in game['platforms']:
                        coverage[motive].add(game['work_id'])
        self.assertEqual(set(coverage), motives)
        self.assertTrue(all(len(works) >= 8 for works in coverage.values()))

    def assert_valid_recommendations(self, report):
        rows = recommendations.for_report(report)
        games = [v04.find_game(row['game_id']) for row in rows]
        work_ids = {game['work_id'] for game in games}
        favorite = v04.find_game(report['game']['id'])
        weights = recommendations.preferences(report)
        self.assertTrue(3 <= len(rows) <= 5)
        self.assertEqual(len(work_ids), len(rows))
        self.assertNotIn(favorite['work_id'], work_ids)
        self.assertTrue(all('PC' in game['platforms'] for game in games[:3]))
        self.assertLessEqual(sum('PC' not in game['platforms'] for game in games), 1)
        for row in rows:
            self.assertEqual(set(row), {'game_id', 'title', 'platform', 'reason'})
            self.assertIn(row['game_id'], v04.public_game_ids())
            reasons = recommendations.curated_games()[row['game_id']]['reasons']
            self.assertTrue(any(reason == row['reason'] and weights.get(motive, 0)
                                for motive, reason in reasons.items()))
        return rows

    def test_same_persona_and_favorite_can_have_different_recommendations(self):
        raw = answered('genshin-impact')
        raw['fictional'] = False
        changed = deepcopy(raw)
        changed['answers']['X16'] = 'B'
        a, b = [finish(value)['report'] for value in (raw, changed)]
        self.assertEqual(a['persona']['id'], b['persona']['id'])
        self.assertEqual(a['game']['id'], b['game']['id'])
        self.assertGreater(recommendations.preferences(a)['puzzle_breaker'],
                           recommendations.preferences(b)['puzzle_breaker'])
        self.assertNotEqual(self.assert_valid_recommendations(a), self.assert_valid_recommendations(b))
        self.assertEqual(recommendations.for_report(a), recommendations.for_report(a))

    def test_legacy_answer_excludes_other_editions_of_the_favorite(self):
        raw = response('steam-72850')
        raw['versions']['report_rules'] = '0.4.0'
        raw['fictional'] = False
        report = finish_legacy(raw)['report']
        self.assertIn('steam-489830', recommendations.curated_games())
        rows = self.assert_valid_recommendations(report)
        self.assertNotIn('steam-489830', {row['game_id'] for row in rows})

    def test_replaced_question_uses_the_answer_actually_shown(self):
        raw = answered('genshin-impact')
        raw['fictional'] = False
        old_id = v05.questions(raw=raw)['questions'][0]['id']
        replacement = v05.replace_question(raw, old_id)
        new_id = replacement['questions'][0]['id']
        self.assertNotEqual(old_id, new_id)
        self.assertNotIn(old_id, replacement['response']['answers'])
        replacement['response']['answers'][new_id] = 'A'
        report = finish(replacement['response'])['report']
        self.assertNotIn('answer:' + old_id, report['evidence'])
        self.assertIn('answer:' + new_id, report['evidence'])
        self.assert_valid_recommendations(report)

    def test_console_can_fill_an_extra_slot_but_only_when_strongly_matched(self):
        def match(game_id, pc, strength, genre):
            return recommendations.Match(
                game_id, game_id, game_id, 'PC' if pc else 'Nintendo Switch',
                'reason', 'wanderer', strength, 0, frozenset({genre}), True, pc, 0)

        matches = sorted([
            match('pc-a', True, 5, 'puzzle'), match('pc-b', True, 5, 'puzzle'),
            match('pc-c', True, 5, 'puzzle'), match('pc-extra', True, 4, 'horror'),
            match('console-a', False, 6, 'platformer'), match('console-b', False, 6, 'survival'),
            match('console-weak', False, 4, 'shooter'),
        ], key=recommendations.Match.rank)
        chosen = recommendations._choose(matches)
        self.assertEqual([game.game_id for game in chosen],
                         ['pc-a', 'pc-b', 'pc-c', 'console-a', 'pc-extra'])
        weak_only = [game for game in matches if game.game_id not in {'console-a', 'console-b'}]
        self.assertTrue(all(game.pc for game in recommendations._choose(weak_only)))
