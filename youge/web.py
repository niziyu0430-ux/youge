"""Loopback-only local website using the existing deterministic report engine."""

from __future__ import annotations

import argparse
from copy import deepcopy
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import json
from pathlib import Path
import posixpath
import sys
from urllib.parse import parse_qs,urlsplit,unquote

from .engine import InputError,build_report,compare_reports,load_config
from . import v04,v05,questionnaires
from .access import AccessController

ROOT=Path(__file__).resolve().parents[1]
WEB_ROOT=ROOT/'web'
WEB_CONFIG=ROOT/'config/youge.v0.3.0.json'


def client_config(config):
    """Quiz payload contains actions, not trait labels or scoring explanations."""
    return {
        'versions':config['manifest']['versions'],'web':config['web'],
        'reference':config['instructions']['reference'],
        'questions':[{'id':q['id'],'text':q['text'],'options':q['response_options'],
                      'order':q['display_order']} for q in sorted(config['core_questions'],key=lambda q:q['display_order'])],
        'attractions':[{'id':o['id'],'label':o['label']} for o in config['taste']['attractions']],
        'experience_options':config['taste']['experience_options'],
        'negative_reasons':config['taste']['negative_reasons'],
        'supplement':config['supplement'],
        'background':config['background_questions'],
        'modules':config['branch_applicability'],
        'followups':[{k:deepcopy(v) for k,v in q.items() if k not in ('dimension','scored')} for q in config['followup_questions']],
        'catalog':[{'id':g['id'],'title':g['title'],'aliases':g['aliases']} for g in config['game_catalog']],
    }


def example_response(config,case='A'):
    if case not in ('A','B','C'):
        raise InputError('示例不存在。')
    raw=json.loads((ROOT/'examples'/f'{case}.json').read_text(encoding='utf-8'))
    raw['versions']=deepcopy(config['manifest']['versions'])
    raw['display_name']=f'示例玩家{case}'
    raw['fictional']=True
    return raw


class Handler(SimpleHTTPRequestHandler):
    server_version='YougeLocal/0.4'
    # Windows MIME registrations can label WebP as application/octet-stream.
    extensions_map={**SimpleHTTPRequestHandler.extensions_map,'.webp':'image/webp'}

    def __init__(self,*args,**kwargs):
        super().__init__(*args,directory=str(WEB_ROOT),**kwargs)

    def end_headers(self):
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','no-referrer')
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'self'; font-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'")
        self.send_header('X-Frame-Options','DENY')
        super().end_headers()

    def json_response(self,value,status=200,extra_headers=None):
        body=json.dumps(value,ensure_ascii=False,separators=(',',':')).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(body)))
        for name,value in (extra_headers or {}).items():self.send_header(name,str(value))
        self.end_headers()
        if self.command!='HEAD':self.wfile.write(body)

    def access_token(self):
        header=self.headers.get('Authorization','')
        if not header.startswith('Bearer '):return None
        return header[7:]

    def require_access(self):
        controller=getattr(self.server,'access_control',None)
        try:
            if controller and controller.authorize(self.access_token()):return True
        except (OSError,ValueError,KeyError,TypeError):
            self.json_response({'error':'访问验证暂时不可用，请稍后重试。'},503)
            return False
        self.json_response({'error':'请先输入访问密码登录。','code':'login_required'},401,
                           {'WWW-Authenticate':'Bearer realm="Youge"'})
        return False

    def send_head(self):
        normalized=posixpath.normpath(unquote(urlsplit(self.path).path).replace('\\','/')).casefold()
        if normalized.startswith('/api/'):
            if self.require_access():self.json_response({'error':'请使用相应接口的GET或POST方法。'},405)
            return None
        # Every document load starts at the access page, even after a prior successful login.
        if normalized in ('/','/login') or normalized.endswith(('.html','.htm')):
            original=self.path
            try:
                self.path='/access.html'
                return super().send_head()
            finally:self.path=original
        return super().send_head()

    def list_directory(self,path):
        self.send_error(404,'Not found')
        return None

    def do_GET(self):
        url=urlsplit(self.path)
        if url.path=='/api/health':
            return self.json_response({'app':'youge-local','status':'ok','versions':v04.config()['versions'],
                                       'question_release':v05.bank()['version'],'authored_game_count':sum(len(p['game_ids']) for p in v05.bank()['packs']),
                                       'public_game_count':len(v04.public_game_ids())})
        if url.path.startswith('/api/'):
            if not self.require_access():return
        if url.path=='/api/access/app-shell':
            app=parse_qs(url.query).get('app',['main'])[0]
            if app not in ('main','wardrobe'):
                return self.json_response({'error':'这个页面不存在。'},400)
            name,module=('index.html','/v4.js') if app=='main' else ('wardrobe.html','/wardrobe.js')
            return self.json_response({'html':(WEB_ROOT/name).read_text(encoding='utf-8'), 'module':module})
        if url.path=='/api/v4/bootstrap':
            return self.json_response(questionnaires.bootstrap())
        if url.path=='/api/v4/questions':
            try:
                gid=parse_qs(url.query).get('game_id',[''])[0]
                query=parse_qs(url.query)
                redirects=v04.catalog().get('search_redirects',{})
                if gid not in v04.public_game_ids() and gid not in redirects:
                    raise InputError('这款作品已不在新问卷的可选范围。')
                if gid not in redirects and v05.pack_for(gid) is None:
                    return self.json_response({'error':'这款作品的专属问卷暂未开放。'},409)
                return self.json_response(questionnaires.questions(gid,instrument=query.get('instrument',[None])[0],mode_id=query.get('mode',[None])[0]))
            except InputError as error:return self.json_response({'error':str(error)},400)
        if url.path=='/api/v4/demo':
            try:return self.json_response(v04.demo(parse_qs(url.query).get('case',['A'])[0]))
            except InputError as error:return self.json_response({'error':str(error)},400)
        if url.path=='/api/bootstrap':
            return self.json_response(client_config(load_config(WEB_CONFIG)))
        if url.path=='/api/demo':
            try:
                config=load_config(WEB_CONFIG)
                case=parse_qs(url.query).get('case',['A'])[0]
                response=example_response(config,case)
                return self.json_response({'response':response,'report':build_report(response,config)})
            except InputError as error:
                return self.json_response({'error':str(error)},400)
        if url.path.startswith('/api/'):
            return self.json_response({'error':'这个本地接口不存在。'},404)
        return super().do_GET()

    def do_POST(self):
        try:
            path=urlsplit(self.path).path
            if path!='/api/access/login' and not self.require_access():return
            origin=self.headers.get('Origin')
            if origin and urlsplit(origin).netloc.casefold()!=self.headers.get('Host','').casefold():
                return self.json_response({'error':'请从游格网站提交请求。'},403)
            if self.headers.get_content_type()!='application/json':
                return self.json_response({'error':'请使用JSON答卷。'},415)
            length=int(self.headers.get('Content-Length','0'))
            limit=4096 if path=='/api/access/login' else 2_000_000
            if length<=0 or length>limit:
                return self.json_response({'error':'答卷为空或文件过大。'},413)
            body=json.loads(self.rfile.read(length).decode('utf-8'))
            if path=='/api/access/login':
                controller=getattr(self.server,'access_control',None)
                if controller is None:return self.json_response({'error':'访问密码尚未配置。'},503)
                if not isinstance(body,dict):return self.json_response({'error':'请输入访问密码。'},400)
                result,status,retry=controller.login(body.get('password'),self.client_address[0])
                return self.json_response(result,status,{'Retry-After':retry} if retry else None)
            if path=='/api/access/logout':
                self.server.access_control.revoke(self.access_token())
                return self.json_response({'ok':True})
            if path=='/api/v4/questions':return self.json_response(questionnaires.questions(raw=body))
            if path=='/api/v4/replace-question':
                if not isinstance(body,dict) or type(body.get('undo',False)) is not bool:raise InputError('换题请求不正确。')
                return self.json_response(v05.replace_question(body.get('response'),body.get('question_id'),body.get('undo',False)))
            if path=='/api/v4/report':return self.json_response(questionnaires.report(body))
            if path=='/api/v4/compare':
                if not isinstance(body,dict) or 'left' not in body or 'right' not in body:raise InputError('请选择两份完整答卷。')
                return self.json_response(questionnaires.compare(body['left'],body['right']))
            config=load_config(WEB_CONFIG)
            if path=='/api/report':
                report=build_report(body,config)
                return self.json_response({'response':report['response'],'report':report})
            if path=='/api/compare':
                if not isinstance(body,dict) or 'left' not in body or 'right' not in body:
                    raise InputError('请选择两份完整答卷。')
                left=build_report(body['left'],config)
                right=build_report(body['right'],config)
                return self.json_response(compare_reports(left,right,config))
            return self.json_response({'error':'这个本地接口不存在。'},404)
        except InputError as error:
            return self.json_response({'error':str(error)},400)
        except (ValueError,TypeError,KeyError,UnicodeError):
            return self.json_response({'error':'答卷格式不完整，请检查文件或重新导出。'},400)
        except OSError:
            return self.json_response({'error':'访问验证暂时不可用，请稍后重试。'},503)


def main():
    if hasattr(sys.stdout,'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser=argparse.ArgumentParser(description='游格本地体验，不上传或持久保存答卷。')
    parser.add_argument('--port',type=int,default=8765)
    args=parser.parse_args()
    load_config(WEB_CONFIG)
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    server.access_control=AccessController.from_file()
    print(f'游格本地预览 Local: http://127.0.0.1:{args.port}',flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__=='__main__':main()
