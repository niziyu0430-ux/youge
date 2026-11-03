"""Private loopback UI fixture; synthetic expansion never enters the real bank."""
import argparse
from copy import deepcopy
from http.server import ThreadingHTTPServer
from pathlib import Path
import hashlib, json, os, sys

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from youge import v05
from youge.access import AccessController,password_record
from youge.web import Handler

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--port',type=int,default=8767)
    parser.add_argument('--fixture-data',required=True)
    args=parser.parse_args()
    out=Path(args.fixture_data);assert not out.exists()
    original_lookup=v05.pack_for
    gid='genshin-impact';old=deepcopy(original_lookup(gid));new=deepcopy(old)
    new['version']='0.5.0+ui-expansion-test-only'
    mode=old['modes'][0]['id'];addition=deepcopy(old['slots'][0]['variants'][-1])
    addition.update(id=old['slots'][0]['id']+'.UI_EXPANSION_TEST_ONLY',modes=[mode],
        text='测试服务器后来补充的情境：这里只检查旧答卷接续流程，不会写入正式题库。你会选择哪一项已有操作？')
    new['slots'][0]['variants'].append(addition)
    def lookup(game_id,version=None):
        if game_id!=gid:return original_lookup(game_id,version)
        if version is None or version==new['version']:return new
        if version==old['version']:return old
        return None
    v05.pack_for=lookup
    raw={'versions':deepcopy(v05.VERSIONS),'pack_version':old['version'],'mode_id':mode,
         'game_id':gid,'display_name':'接续流程测试','respondent_id':'private-expansion-ui-test',
         'answers':{},'extra_answers':[],'fictional':True}
    initial=v05.questions(raw=raw)
    initial['response']['answers']={q['id']:'A' for q in initial['questions']}
    form=initial
    while form['questions'][0]['can_replace']:
        form=v05.replace_question(form['response'],form['questions'][0]['id'])
    assert form['response']['pack_version']==old['version']
    assert len(form['response']['answers'])==15
    banksha=hashlib.sha256((ROOT/'config/question-packs.v0.5.0.json').read_bytes()).hexdigest()
    data={'fixture_only':True,'public_bank_sha256':banksha,'pid':os.getpid(),'port':args.port,
          'old_exhausted_form':form,'expected_new_variant_id':addition['id'],
          'expected_new_text':addition['text'],'expected_new_pack_version':new['version']}
    out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    server.access_control=AccessController(password_record('ui-test-only-question-review'))
    print(json.dumps({'fixture_file':str(out),'pid':os.getpid(),'port':args.port,'public_bank_unchanged':banksha}),flush=True)
    try:server.serve_forever()
    finally:server.server_close()
