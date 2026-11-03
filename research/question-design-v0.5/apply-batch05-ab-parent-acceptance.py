"""Five explicit comparison/purchase decisions after the independent full read."""
import ast
import base64
import hashlib
import importlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from question_authoring import SIGNALS,validate
from build_question_packs_v05 import BEHAVIORS
from youge import v04

EXPECTED={'question_batch05_a':'122b45604dca2379e22e980cbaea894bf08a16a56d7bcd4ee1ae2e89bf29e452',
 'question_batch05_b':'6b8fce0a150327ddfc9ef9fa01fca7be1ec2b05196ff96f8923bab200b7a0756'}
DECISIONS={'G5V502.VERSUS.V1':'compare_available_setup','GTAVEV502.V1':'compare_available_setup',
 'GTAVEV502.ONLINE.V1':'compare_available_setup','HD2V506.V1':'compare_available_setup',
 'HD2V506.ALT1':'purchase_available_upgrade'}

def main():
    rp=ROOT/'research/question-design-v0.5/batch05-ab-parent-acceptance.json';assert not rp.exists()
    ep=ROOT/'research/question-design-v0.5/batch05-ab-strict-signal-editorial-review.json'
    e=json.loads(ep.read_text(encoding='utf8'))
    assert hashlib.sha256(ep.read_bytes()).hexdigest()=='e95978568141b07d45c5eed64cbaf0f121a02d2f4e0dfce96d6114780fc1afa2'
    report={'status':'parent_accepted_pending_uniform_runtime_build','date':'2026-10-30','reviewer':'root',
     'independent_editor_report':str(ep.relative_to(ROOT)),'independent_full_variants_read_before_and_after':288,
     'independent_options_read':1152,
     'parent_review_scope':'核对全部288变体与冻结快照；全文复读最终4项自定规则、6项持续经营、2项身份维持的全部情境与选项；逐项读62个剩余构筑选项和完整题干。主审未冒称再次全文通读所有288变体。',
     'parent_additional_decisions':DECISIONS,'modules':[],'human_player_trial':False}
    seen=set()
    for name,sha in EXPECTED.items():
        path=ROOT/'scripts'/(name+'.py');raw=path.read_bytes()
        assert hashlib.sha256(raw).hexdigest()==sha,'Already revised; do not rerun'
        m=importlib.import_module(name);before_packs=m.PACKS;before_sources=m.SOURCES
        before={v['id']:v for p in m.PACKS for s in p['slots'] for v in s['variants']}
        erows={r['id']:r['after'] for r in e['variant_reviews'] if Path(r['module']).stem==name}
        assert before==erows,(name,len(before),len(erows))
        text_ids={v['text']:i for i,v in before.items()};assert len(text_ids)==len(before)
        offsets=[0]
        for line in raw.splitlines(keepends=True):offsets.append(offsets[-1]+len(line))
        edits=[]
        def span(n):return offsets[n.lineno-1]+n.col_offset,offsets[n.end_lineno-1]+n.end_col_offset
        def repl(n,value):
            a,b=span(n);edits.append((a,b,repr(value).encode('utf8')))
        for node in ast.walk(ast.parse(raw.decode('utf8'))):
            if not isinstance(node,ast.Call) or not isinstance(node.func,ast.Name) or node.func.id!='Q':continue
            alt=node.args[7];mid=text_ids[ast.literal_eval(node.args[2])];aid=text_ids[ast.literal_eval(alt.elts[0])]
            ms=ast.literal_eval(node.args[4]).split()
            als=ast.literal_eval(alt.elts[2]).split() if len(alt.elts)==3 else list(ms)
            changed=False
            for i,tokens in [(mid,ms),(aid,als)]:
                if i not in DECISIONS:continue
                idx=[j for j,x in enumerate(tokens) if SIGNALS.get(x,x)=='build_alchemist'];assert len(idx)==1
                tokens[idx[0]]=DECISIONS[i];seen.add(i);changed=True
            if changed:
                repl(node.args[4],' '.join(ms))
                if len(alt.elts)==3:repl(alt.elts[2],' '.join(als))
                else:
                    a,b=span(alt);edits.append((b-1,b-1,(', '+repr(' '.join(als))).encode('utf8')))
                repl(node.args[5],ast.literal_eval(node.args[5])+' 仅比较可选方案、尚未实际装配的选项只记配置比较；一次解锁未说明具体互动的选项只记购买，不强计构筑或成长动机。')
        new=raw
        for a,b,val in sorted(edits,reverse=True):new=new[:a]+val+new[b:]
        compile(new.decode('utf8'),str(path),'exec');path.write_bytes(new)
        importlib.invalidate_caches();m=importlib.reload(m)
        validate(m.PACKS,m.SOURCES,{p['id'] for p in v04.config()['personas']}|set(BEHAVIORS))
        after={v['id']:v for p in m.PACKS for s in p['slots'] for v in s['variants']}
        assert set(before)==set(after)
        for identifier in set(DECISIONS)&set(before):
            old=next(o for o in before[identifier]['options'] if o['signal']=='build_alchemist')
            new_choice=next(o for o in after[identifier]['options'] if o['id']==old['id'])
            assert old['label']==new_choice['label'] and new_choice['signal']==DECISIONS[identifier]
        report['modules'].append({'module':name,'before_source_sha256':sha,
         'before_source_raw_base64':base64.b64encode(raw).decode(),'before_packs':before_packs,'before_sources':before_sources,
         'after_source_sha256':hashlib.sha256(new).hexdigest(),'after_packs':m.PACKS,'after_sources':m.SOURCES,
         'changes':[{'id':i,'before':before[i],'after':after[i]} for i in before if before[i]!=after[i]]})
    assert seen==set(DECISIONS)
    report['all288_frozen_variants_match_current_imports_before_revision']=True
    report['all_ids_modes_and_source_objects_preserved']=True
    report['known_signal_and_source_validation']=True
    report['remaining_runtime_history_baseline']='reports/fixtures/before-batch05-final-signal-review.json'
    rp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'decisions':len(DECISIONS),'sources':[{'module':x['module'],'sha':x['after_source_sha256'],'changed':len(x['changes'])} for x in report['modules']]},ensure_ascii=False))

if __name__=='__main__':main()
