"""Loopback-only local website using the existing deterministic report engine."""

from __future__ import annotations

import argparse
from copy import deepcopy
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import json
from pathlib import Path
import sys
from urllib.parse import parse_qs,urlsplit

from .engine import InputError,build_report,compare_reports,load_config
from . import v04

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
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'self'; font-src 'self'; object-src 'none'; base-uri 'self'")
        super().end_headers()

    def json_response(self,value,status=200):
        body=json.dumps(value,ensure_ascii=False,separators=(',',':')).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url=urlsplit(self.path)
        if url.path=='/api/v4/bootstrap':
            return self.json_response(v04.bootstrap())
        if url.path=='/api/v4/questions':
            try:
                gid=parse_qs(url.query).get('game_id',[''])[0]
                return self.json_response({'game':v04.find_game(gid),'questions':[v04.public_question(q) for q in v04.questionnaire(gid)],'versions':v04.config()['versions']})
            except InputError as error:return self.json_response({'error':str(error)},400)
        if url.path=='/api/v4/demo':
            try:return self.json_response(v04.demo(parse_qs(url.query).get('case',['A'])[0]))
            except InputError as error:return self.json_response({'error':str(error)},400)
        if url.path=='/api/health':
            return self.json_response({'app':'youge-local','status':'ok','versions':v04.config()['versions']})
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
        if url.path in ('/','/index.html'):
            self.path='/index.html'
        return super().do_GET()

    def do_POST(self):
        try:
            if self.headers.get_content_type()!='application/json':
                return self.json_response({'error':'请使用JSON答卷。'},415)
            length=int(self.headers.get('Content-Length','0'))
            if length<=0 or length>2_000_000:
                return self.json_response({'error':'答卷为空或文件过大。'},413)
            body=json.loads(self.rfile.read(length).decode('utf-8'))
            path=urlsplit(self.path).path
            if path=='/api/v4/report':return self.json_response(v04.report(body))
            if path=='/api/v4/compare':
                if not isinstance(body,dict) or 'left' not in body or 'right' not in body:raise InputError('请选择两份完整答卷。')
                return self.json_response(v04.compare(body['left'],body['right']))
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
        except (ValueError,TypeError,KeyError,UnicodeDecodeError):
            return self.json_response({'error':'答卷格式不完整，请检查文件或重新导出。'},400)


def main():
    if hasattr(sys.stdout,'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser=argparse.ArgumentParser(description='游格本地体验，不上传或持久保存答卷。')
    parser.add_argument('--port',type=int,default=8765)
    args=parser.parse_args()
    load_config(WEB_CONFIG)
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    print(f'游格本地预览 Local: http://127.0.0.1:{args.port}',flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__=='__main__':main()
