"""Local website contracts, real HTTP handlers, and scenario evidence."""
from copy import deepcopy
from http.server import ThreadingHTTPServer
import json
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from youge.engine import build_report, score_core, validate_config, verify_report_evidence
from youge.web import Handler, WEB_CONFIG, client_config, example_response, load_config
from youge.access import AccessController,password_record


CONFIG = load_config(WEB_CONFIG)


class ScenarioTests(unittest.TestCase):
    def test_scenarios_preserve_all_eight_independent_axes(self):
        self.assertTrue(validate_config(CONFIG))
        self.assertEqual(len(CONFIG['core_questions']), 32)
        self.assertEqual(CONFIG['manifest']['allowed_score_inputs'], ['core'])
        for dimension in CONFIG['dimensions']:
            self.assertEqual(len(dimension['question_ids']), 4)

    def test_each_scene_has_five_unique_concrete_choices(self):
        for q in CONFIG['core_questions']:
            with self.subTest(q=q['id']):
                self.assertEqual(q['response_type'], 'scenario_single')
                self.assertEqual({o['value'] for o in q['response_options']}, {1, 2, 3, 4, 5})
                self.assertEqual(len({o['label'] for o in q['response_options']}), 5)
                for option in q['response_options']:
                    for hint in ('更接近', '倾向', '人格', '加分', '维度'):
                        self.assertNotIn(hint, option['label'])

    def test_client_does_not_receive_trait_annotations_for_core_questions(self):
        payload = client_config(CONFIG)
        for question in payload['questions']:
            self.assertEqual(set(question), {'id', 'text', 'options', 'order'})
            self.assertNotIn('dimension', question)
            self.assertNotIn('measurement_target', question)
        self.assertEqual([q['order'] for q in payload['questions']], list(range(1, 33)))

    def test_report_evidence_quotes_actual_chosen_action(self):
        raw = example_response(CONFIG)
        report = build_report(raw, CONFIG)
        for q in CONFIG['core_questions']:
            chosen = next(o['label'] for o in q['response_options'] if o['value'] == raw['core'][q['id']])
            self.assertEqual(report['evidence']['answer:' + q['id']]['label'], chosen)
        self.assertTrue(verify_report_evidence(report))

    def test_renaming_and_removing_games_cannot_change_profile(self):
        raw = example_response(CONFIG)
        other = deepcopy(raw)
        other['favorites'] = []
        other['followups']['M01'] = 'platform_unavailable'
        other['followups']['M02'] = {'basis': 'hypothetical', 'purposes': ['visual']}
        first, second = build_report(raw, CONFIG), build_report(other, CONFIG)
        self.assertEqual(first['scores'], second['scores'])
        self.assertEqual(first['display'], second['display'])

    def test_same_games_different_motives_and_different_games_same_profile(self):
        a, b, c = [build_report(example_response(CONFIG, x), CONFIG) for x in 'ABC']
        self.assertEqual([g['game_id'] for g in a['response']['favorites']], [g['game_id'] for g in b['response']['favorites']])
        self.assertNotEqual(a['scores'], b['scores'])
        self.assertEqual(a['scores'], c['scores'])

    def test_missing_answers_do_not_become_neutral(self):
        rows = score_core({q['id']: None for q in CONFIG['core_questions']}, CONFIG)
        self.assertTrue(all(row['score'] is None for row in rows.values()))

    def test_current_version_is_separate_from_original_questionnaire(self):
        self.assertEqual(CONFIG['manifest']['versions']['instrument'], '0.3.0')
        self.assertEqual(CONFIG['manifest']['versions']['scoring'], '0.2.0')


class QuietHandler(Handler):
    def log_message(self, *args):
        pass


class HTTPTests(unittest.TestCase):
    def test_ribbon_portrait_is_served_as_a_browser_image(self):
        with urlopen(self.base + '/assets/personas-ribbon/v2/wanderer.webp') as response:
            self.assertEqual(response.headers.get_content_type(), 'image/webp')
            self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')
            payload = response.read()
            self.assertEqual(payload[:4], b'RIFF')
            self.assertEqual(payload[8:12], b'WEBP')

    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), QuietHandler)
        cls.server.access_control = AccessController(password_record('test-only-shared-password'))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = 'http://127.0.0.1:' + str(cls.server.server_port)
        request=Request(cls.base+'/api/access/login',json.dumps({'password':'test-only-shared-password'}).encode(),headers={'Content-Type':'application/json'})
        with urlopen(request) as response:cls.access_token=json.load(response)['access_token']

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def request(self, path, body=None, content_type='application/json'):
        data = None if body is None else json.dumps(body, ensure_ascii=False).encode('utf-8')
        request = Request(self.base + path, data=data, headers={'Content-Type': content_type,'Authorization':'Bearer '+self.access_token})
        try:
            with urlopen(request, timeout=10) as response:
                return response.status, response.headers, response.read()
        except HTTPError as error:
            return error.code, error.headers, error.read()

    def test_static_assets_and_sanitized_bootstrap_are_served(self):
        for path in ('/', '/app.js', '/poster.js', '/styles.css', '/assets/world-dawn-v1.png'):
            with self.subTest(path=path):
                status, headers, body = self.request(path)
                self.assertEqual(status, 200)
                self.assertTrue(body)
                self.assertEqual(headers['Cache-Control'], 'no-store')
        status, _, body = self.request('/api/bootstrap')
        self.assertEqual(status, 200)
        self.assertEqual(len(json.loads(body)['questions']), 32)

    def test_health_identifies_the_local_application(self):
        status, _, body = self.request('/api/health')
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)['app'], 'youge-local')

    def test_report_endpoint_matches_engine_and_repeats_exactly(self):
        raw = example_response(CONFIG)
        first = self.request('/api/report', raw)
        second = self.request('/api/report', raw)
        self.assertEqual(first[0], 200)
        self.assertEqual(first[2], second[2])
        self.assertEqual(json.loads(first[2])['report'], build_report(raw, CONFIG))

    def test_comparison_retains_seven_negotiation_topics_without_percentage(self):
        status, _, body = self.request('/api/compare', {'left': example_response(CONFIG, 'A'), 'right': example_response(CONFIG, 'B')})
        self.assertEqual(status, 200)
        result = json.loads(body)
        self.assertEqual(len(result['coordination']), 7)
        self.assertNotIn('compatibility_percent', result)

    def test_demo_is_explicitly_fictional(self):
        for case in 'ABC':
            status, _, body = self.request('/api/demo?case=' + case)
            self.assertEqual(status, 200)
            self.assertTrue(json.loads(body)['report']['fictional'])

    def test_input_errors_are_returned_as_json(self):
        bad = example_response(CONFIG)
        bad['core']['EXP01'] = 6
        for body in (bad, [], {'core': {}}, None):
            if body is None:
                continue
            with self.subTest(body_type=type(body).__name__):
                status, _, data = self.request('/api/report', body)
                self.assertEqual(status, 400)
                self.assertIn('error', json.loads(data))

    def test_original_version_cannot_be_silently_mixed(self):
        raw = example_response(CONFIG)
        raw['versions']['instrument'] = '0.2.0'
        self.assertEqual(self.request('/api/report', raw)[0], 400)

    def test_other_content_types_and_unknown_routes_are_rejected(self):
        self.assertEqual(self.request('/api/report', {}, 'text/plain')[0], 415)
        self.assertEqual(self.request('/api/not-here')[0], 404)
        self.assertEqual(self.request('/config/youge.v0.3.0.json')[0], 404)
        self.assertEqual(self.request('/api/demo?case=Z')[0], 400)


if __name__ == '__main__':
    unittest.main()
