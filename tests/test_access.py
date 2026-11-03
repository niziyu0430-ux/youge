"""Real HTTP access checks and the page-memory authentication contract."""
import base64
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request,urlopen

from youge.access import AccessController,password_record,write_record
from youge.web import Handler

ROOT=Path(__file__).resolve().parents[1]


class QuietHandler(Handler):
    def log_message(self,*args):pass


class AccessHTTPTests(unittest.TestCase):
    password='a-test-only-Password-2026'

    @classmethod
    def setUpClass(cls):
        cls.record=password_record(cls.password)
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),QuietHandler)
        cls.base='http://127.0.0.1:'+str(cls.server.server_port)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join(timeout=2)

    def setUp(self):
        self.now=0
        self.server.access_control=AccessController(self.record,clock=lambda:self.now,failure_limit=4,session_seconds=30)

    def request(self,path,body=None,token=None,headers=None,method=None):
        request_headers={'Content-Type':'application/json',**(headers or {})}
        if token:request_headers['Authorization']='Bearer '+token
        request=Request(self.base+path,data=json.dumps(body).encode() if body is not None else None,
                        headers=request_headers,method=method)
        try:
            with urlopen(request) as response:return response.status,response.headers,response.read()
        except HTTPError as error:
            result=error.code,error.headers,error.read();error.close();return result

    def login(self,password=None):
        status,headers,body=self.request('/api/access/login',{'password':self.password if password is None else password})
        self.assertEqual(status,200,body)
        self.assertNotIn('Set-Cookie',headers)
        return json.loads(body)['access_token']

    def test_anonymous_apis_and_export_helpers_are_blocked(self):
        for route in ['/api/v4/bootstrap','/api/v4/questions?game_id=steam-261550','/api/v4/demo',
                      '/api/bootstrap','/api/demo','/api/access/app-shell']:
            with self.subTest(route=route):
                status,_,body=self.request(route)
                self.assertEqual(status,401)
                self.assertEqual(json.loads(body)['code'],'login_required')
        for route in ['/api/v4/report','/api/v4/compare','/api/report','/api/compare']:
            self.assertEqual(self.request(route,{},method='POST')[0],401)
        self.assertEqual(self.request('/api/v4/bootstrap',method='HEAD')[0],401)

    def test_all_document_entries_including_encoded_aliases_show_login(self):
        for route in ['/','/#home','/index.html','/v4.html','/index.v03.html','/wardrobe.html',
                      '/%69ndex%2ehtml','/INDEX.HTML','/folder/../index.html','/login']:
            with self.subTest(route=route):
                status,_,body=self.request(route)
                self.assertEqual(status,200)
                self.assertIn(b'id="access-password"',body)
                self.assertNotIn(b'src="/v4.js"',body)
                self.assertNotIn(b'id="main"',body)

    def test_valid_login_unlocks_shell_and_unlimited_reports(self):
        token=self.login()
        self.assertGreaterEqual(len(token),40)
        status,_,body=self.request('/api/access/app-shell',token=token)
        self.assertEqual(status,200)
        shell=json.loads(body)
        self.assertEqual(shell['module'],'/v4.js')
        self.assertIn('id="main"',shell['html'])
        self.assertNotIn(self.password,shell['html'])
        self.assertEqual(self.request('/api/v4/bootstrap',token=token)[0],200)
        status,_,body=self.request('/api/v4/demo?case=A',token=token)
        self.assertEqual(status,200)
        answer=json.loads(body)['response']
        for _ in range(4):
            status,_,result=self.request('/api/v4/report',answer,token)
            self.assertEqual(status,200)
            self.assertTrue(json.loads(result)['complete'])

    def test_wrong_password_and_missing_token_cannot_reuse_a_login(self):
        self.assertEqual(self.request('/api/access/login',{'password':'wrong-password'})[0],401)
        token=self.login()
        self.assertEqual(self.request('/api/v4/bootstrap',token=token)[0],200)
        self.assertEqual(self.request('/api/v4/bootstrap',headers={'Cookie':'access_token='+token})[0],401)
        self.assertEqual(self.request('/api/v4/bootstrap?access_token='+token)[0],401)
        self.assertEqual(self.request('/api/v4/bootstrap')[0],401)
        # A refreshed document always renders the login screen, even with an old header.
        self.assertIn(b'id="access-password"',self.request('/',token=token)[2])

    def test_logout_revokes_only_that_page_token(self):
        first,second=self.login(),self.login()
        self.assertNotEqual(first,second)
        self.assertEqual(self.request('/api/access/logout',{},first)[0],200)
        self.assertEqual(self.request('/api/v4/bootstrap',token=first)[0],401)
        self.assertEqual(self.request('/api/v4/bootstrap',token=second)[0],200)

    def test_expired_token_is_rejected(self):
        token=self.login();self.now=31
        self.assertEqual(self.request('/api/v4/bootstrap',token=token)[0],401)

    def test_brute_force_limit_uses_socket_address_and_has_retry_after(self):
        for i in range(3):
            self.assertEqual(self.request('/api/access/login',{'password':'wrong-password'},headers={'X-Forwarded-For':f'10.0.0.{i}'})[0],401)
        status,headers,_=self.request('/api/access/login',{'password':'wrong-password'})
        self.assertEqual(status,429);self.assertEqual(headers['Retry-After'],'60')
        self.assertEqual(self.request('/api/access/login',{'password':self.password})[0],429)
        self.now=61;self.login()

    def test_malformed_or_cross_origin_logins_do_not_create_sessions(self):
        for body in [[],{},None,{'password':[]},{'password':'x'*257}]:
            if body is None:continue
            self.assertEqual(self.request('/api/access/login',body)[0],400)
        self.assertEqual(self.request('/api/access/login',{'password':self.password},headers={'Origin':'https://unrelated.example'})[0],403)
        self.assertEqual(self.request('/api/access/login',{'password':'x'*5000})[0],413)
        self.assertEqual(len(self.server.access_control.sessions),0)

    def test_shell_allowlist_and_private_files_cannot_be_traversed(self):
        token=self.login()
        self.assertEqual(self.request('/api/access/app-shell?app=../../.local/access.json',token=token)[0],400)
        for route in ['/.local/access.json','/../.local/access-password.txt','/config/youge.v0.4.0.json','/assets/']:
            self.assertEqual(self.request(route)[0],404)

    def test_unconfigured_server_fails_closed_but_health_is_public(self):
        self.server.access_control=None
        self.assertEqual(self.request('/api/v4/bootstrap')[0],401)
        self.assertEqual(self.request('/api/access/login',{'password':self.password})[0],503)
        self.assertEqual(self.request('/api/health')[0],200)


class AccessStorageTests(unittest.TestCase):
    def test_password_rotation_invalidates_old_sessions_without_restart(self):
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/'access.json'
            write_record(path,password_record('first-test-password'))
            controller=AccessController.from_file(path)
            response,status,_=controller.login('first-test-password','127.0.0.1')
            self.assertEqual(status,200);token=response['access_token']
            self.assertTrue(controller.authorize(token))
            write_record(path,password_record('second-test-password'))
            self.assertFalse(controller.authorize(token))
            self.assertEqual(controller.login('first-test-password','127.0.0.1')[1],401)
            self.assertEqual(controller.login('second-test-password','127.0.0.1')[1],200)
            self.assertNotIn('second-test-password',path.read_text())

    @unittest.skipUnless(shutil.which('node'),'Node is needed for the document-memory check')
    def test_new_document_has_no_token_and_pagehide_revokes_the_old_one(self):
        module=base64.b64encode((ROOT/'web/access-client.js').read_bytes()).decode()
        code=r"""
import assert from 'node:assert/strict';
const events=new EventTarget();let reloads=0,calls=[];
globalThis.window=events;window.location={reload:()=>reloads++};
globalThis.fetch=async(url,options={})=>{calls.push({url,options});return new Response('{}',{status:200});};
const first=await import('data:text/javascript;base64,MODULE#first');
first.setAccessToken('a'.repeat(43));
await first.authorizedFetch('/api/v4/bootstrap');
assert.equal(calls[0].options.headers.get('Authorization'),'Bearer '+'a'.repeat(43));
const refreshed=await import('data:text/javascript;base64,MODULE#refreshed');
await assert.rejects(refreshed.authorizedFetch('/api/v4/bootstrap'));
assert.equal(reloads,1);assert.equal(calls.length,1);
events.dispatchEvent(new Event('pagehide'));
assert.equal(calls[1].url,'/api/access/logout');
assert.equal(calls[1].options.keepalive,true);
assert.equal(calls[1].options.headers.Authorization,'Bearer '+'a'.repeat(43));
await assert.rejects(first.authorizedFetch('/api/v4/bootstrap'));
assert.equal(reloads,2);
console.log('Fresh documents cannot reuse login state; pagehide revokes only the old token');
""".replace('MODULE',module)
        result=subprocess.run(['node','--input-type=module','-e',code],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
