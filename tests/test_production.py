"""Exercise the deployed WSGI boundary, not a second scoring implementation."""
from io import BytesIO
import json
import os
import unittest
from unittest.mock import patch
from wsgiref.util import setup_testing_defaults
from wsgiref.validate import validator

from youge.access import AccessController, password_record
from youge.production import create_app, MAX_BODY


class ProductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = password_record('deployment-test-password')

    def setUp(self):
        self.app = validator(create_app(controller=AccessController(self.record)))

    def request(self, path='/', method='GET', data=None, token=None, **overrides):
        environ = {}
        setup_testing_defaults(environ)
        path, _, query = path.partition('?')
        body = json.dumps(data).encode() if data is not None else b''
        environ.update(PATH_INFO=path, QUERY_STRING=query, REQUEST_METHOD=method,
                       HTTP_HOST='youge.example', REMOTE_ADDR='192.0.2.10',
                       CONTENT_LENGTH=str(len(body)), CONTENT_TYPE='application/json',
                       **{'wsgi.input': BytesIO(body)})
        if token:
            environ['HTTP_AUTHORIZATION'] = 'Bearer ' + token
        environ.update(overrides)
        response = {}
        def start(status, headers, exc_info=None):
            response.update(status=int(status.split()[0]), headers=dict(headers))
        iterator = self.app(environ, start)
        try:
            response['body'] = b''.join(iterator)
        finally:
            iterator.close()
        return response

    def login(self):
        response = self.request('/api/access/login', 'POST', {'password':'deployment-test-password'})
        self.assertEqual(response['status'], 200)
        return json.loads(response['body'])['access_token']

    def test_missing_secret_fails_closed(self):
        with patch.dict(os.environ, {'YOUGE_ACCESS_PASSWORD':''}):
            with self.assertRaises(RuntimeError):
                create_app()

    def test_document_gate_and_public_assets(self):
        for path in ('/', '/index.html', '/v4.html', '/wardrobe.html', '/%69ndex.html'):
            with self.subTest(path=path):
                response = self.request(path)
                self.assertEqual(response['status'], 200)
                self.assertIn(b'access-password', response['body'])
                self.assertIn("frame-ancestors 'none'", response['headers']['Content-Security-Policy'])
        response = self.request('/assets/mark.svg')
        self.assertEqual(response['status'], 200)
        self.assertIn(b'<svg', response['body'])
        self.assertEqual(self.request('/wardrobe.js')['status'], 404)
        for old, current in (
            ('/assets/personas/style_director.png', '/assets/personas-v2/style_director-r2.png'),
            ('/assets/personas-hero/v1/wanderer.webp', '/assets/personas-hero/v2/wanderer.webp'),
            ('/assets/personas-ribbon/v1/wanderer.webp', '/assets/personas-ribbon/v2/wanderer.webp'),
        ):
            with self.subTest(path=old):
                previous, latest = self.request(old), self.request(current)
                self.assertEqual(previous['status'], 200)
                self.assertEqual(latest['status'], 200)
                self.assertEqual(previous['body'], latest['body'])

    def test_login_bootstrap_questions_and_report(self):
        self.assertEqual(self.request('/api/v4/bootstrap')['status'], 401)
        token = self.login()
        self.assertEqual(self.request('/api/access/app-shell?app=wardrobe', token=token)['status'], 400)
        for path in ('/api/access/app-shell?app=main', '/api/v4/bootstrap', '/api/v4/demo?case=A'):
            self.assertEqual(self.request(path, token=token)['status'], 200, path)
        demo = json.loads(self.request('/api/v4/demo?case=A', token=token)['body'])
        response = self.request('/api/v4/report', 'POST', demo['response'], token)
        self.assertEqual(response['status'], 200)

    def test_wrong_password_refresh_and_logout(self):
        self.assertEqual(self.request('/api/access/login','POST',{'password':'incorrect'})['status'],401)
        token = self.login()
        self.assertIn(b'access-password',self.request('/',token=token)['body'])
        self.assertEqual(self.request('/api/access/logout','POST',{},token)['status'],200)
        self.assertEqual(self.request('/api/v4/bootstrap',token=token)['status'],401)

    def test_independent_deployments_do_not_share_sessions(self):
        token = self.login()
        self.app = validator(create_app(controller=AccessController(self.record)))
        self.assertEqual(self.request('/api/v4/bootstrap',token=token)['status'],401)

    def test_body_limits_and_header_injection(self):
        for length, status in ((str(MAX_BODY+1),413), ('10',400)):
            self.assertEqual(self.request(CONTENT_LENGTH=length)['status'],status)
        self.assertEqual(self.request(HTTP_ORIGIN='bad\r\nHost: bad')['status'],400)

    def test_same_origin_and_ignored_spoofed_forwarding(self):
        response = self.request('/api/access/login','POST',{'password':'deployment-test-password'},
                                HTTP_ORIGIN='https://elsewhere.example')
        self.assertEqual(response['status'],403)
        response = self.request('/api/access/login','POST',{'password':'deployment-test-password'},
                                HTTP_ORIGIN='https://youge.example',HTTP_X_FORWARDED_FOR='untrusted')
        self.assertEqual(response['status'],200)

    def test_health_and_head(self):
        response = self.request('/api/health')
        self.assertEqual(response['status'],200)
        self.assertEqual(json.loads(response['body'])['app'],'youge-local')
        response = self.request('/', 'HEAD')
        self.assertEqual(response['status'],200)
        self.assertEqual(response['body'],b'')


if __name__ == '__main__':
    unittest.main()
