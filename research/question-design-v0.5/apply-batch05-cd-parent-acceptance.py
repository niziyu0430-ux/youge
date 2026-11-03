"""Additional explicit decisions after the independent editor froze batch05c/d."""
import ast
import base64
from collections import Counter
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

COMPARE='''SE5SC07.V1 DMC5SC01.ALT1 DMC5SC03.ALT1 DMC5SC05.V1 DMC5SC05.ALT1 DMC5SC06.V1 DMC5SC06.ALT1
DMC4SC02.ALT1 DMC4SC05.V1 DMC4SC05.ALT1 BAYOSC02.ALT1 BAYOSC04.V1 BAYOSC04.ALT1 TLOU1V501.ALT1
VANV506.V1 MGRV508.V1 HIFIV507.V1 HIFIV507.ALT1 NIERAV504.V1 NIERAV504.ALT1 NIERRV504.V1 NIERRV504.ALT1'''.split()
PURCHASE='DMC5SC07.V1 DMC5SC07.ALT1 DMC4SC01.ALT1 BAYOSC05.V1 BAYOSC05.ALT1 HIFIV504.V1'.split()
DECISIONS={i:'compare_available_setup' for i in COMPARE}|{i:'purchase_available_upgrade' for i in PURCHASE}
EXPECTED={'question_batch05_c':'f45e72b030b0674b1c5f7ccdf8d6d4f5b7f593264a0a96032078a7f6d6991950',
 'question_batch05_d':'0b8fe487f28c982bd0343abc62ee85ef40f36550d8cb37c0dd3a14981b180a0c'}

def main():
    editor_path=ROOT/'research/question-design-v0.5/batch05-cd-strict-signal-editorial-review.json'
    editor=json.loads(editor_path.read_text(encoding='utf8'))
    assert hashlib.sha256(editor_path.read_bytes()).hexdigest()=='5232013159415d44f9e36c2cd5e98796f9ecc7ce6f6de46e4e7caa78a25ffe2e'
    report={'status':'parent_accepted_pending_uniform_runtime_build','date':'2026-10-30','reviewer':'root',
     'independent_editor_report':str(editor_path.relative_to(ROOT)),
     'independent_editor_full_variants_read':312,
     'parent_review_scope':'主审原先逐字审137项自创玩法；本轮对最终13条规则、1项栽培、2项身份维持连同完整四选项复读，并逐项读全部107个剩余构筑选项及其完整题干；机械核对全部312变体快照和当前源码。未冒称第三次主审全文重读312。',
     'parent_targeted_final_rule_ids':[r['variant_id'] for r in editor['retained_13_rule_feasibility_reviews']],
     'editorial_decisions':['仅比较当前可选配置，不等于已经装配或验证互动，按本轮新增compare_available_setup只记比较行为。','一次购买未说清具体功能互补，不强推构筑，也不因结果永久就替原选项补成长动机；只记purchase_available_upgrade。','新增两个行为尚未发布；不改任何既有行为文案，旧答卷保留原版本。','个人栽培循环保留系统经营；熟悉浇水照看须明确正向安定体验。'],
     'human_player_trial':False,'modules':[]}
    seen=set();all_before={};all_after={}
    for name,expected in EXPECTED.items():
        path=ROOT/'scripts'/f'{name}.py';raw=path.read_bytes()
        assert hashlib.sha256(raw).hexdigest()==expected,'Already revised; do not rerun'
        module=importlib.import_module(name)
        ed=next(x for x in editor['modules'] if x['module']==name)
        assert ed['after_sha256']==expected and ed['after_packs']==module.PACKS and ed['after_sources']==module.SOURCES
        before_packs=module.PACKS;before_sources=module.SOURCES
        before={v['id']:v for p in module.PACKS for s in p['slots'] for v in s['variants']};all_before.update(before)
        text_ids={v['text']:i for i,v in before.items()}
        offsets=[0]
        for line in raw.splitlines(keepends=True):offsets.append(offsets[-1]+len(line))
        edits=[]
        def span(n):return offsets[n.lineno-1]+n.col_offset,offsets[n.end_lineno-1]+n.end_col_offset
        def replace(n,value):
            a,b=span(n);edits.append((a,b,repr(value).encode('utf8')))
        for node in ast.walk(ast.parse(raw.decode('utf8'))):
            if not isinstance(node,ast.Call) or not isinstance(node.func,ast.Name) or node.func.id!='Q':continue
            alt=node.args[7];mid=text_ids[ast.literal_eval(node.args[2])];aid=text_ids[ast.literal_eval(alt.elts[0])]
            ms=ast.literal_eval(node.args[4]).split();als=ast.literal_eval(alt.elts[2]).split() if len(alt.elts)==3 else list(ms)
            changed=False
            for i,tokens in [(mid,ms),(aid,als)]:
                if i not in DECISIONS:continue
                indices=[n for n,x in enumerate(tokens) if SIGNALS.get(x,x)=='build_alchemist']
                assert len(indices)==1,(i,tokens)
                tokens[indices[0]]=DECISIONS[i];seen.add(i);changed=True
            if changed:
                replace(node.args[4],' '.join(ms))
                if len(alt.elts)==3:replace(alt.elts[2],' '.join(als))
                else:
                    a,b=span(alt);edits.append((b-1,b-1,(', '+repr(' '.join(als))).encode('utf8')))
                purpose=ast.literal_eval(node.args[5])+' 本轮仅比较可选方案或一次购入而未说明具体互动作用的选项，只记录相应行为，不强计构筑或成长动机。'
                replace(node.args[5],purpose)
            if mid=='NIERRV505.V1':
                labels=ast.literal_eval(node.args[3]).split('|');index=next(n for n,x in enumerate(ms) if SIGNALS.get(x,x)=='cozy_resident')
                labels[index]='即使可以继续冒险，仍因喜欢熟悉浇水照看的安定过程，先留在家旁按原节奏照看一轮'
                replace(node.args[3],'|'.join(labels))
        edited=raw
        for a,b,value in sorted(edits,reverse=True):edited=edited[:a]+value+edited[b:]
        compile(edited.decode('utf8'),str(path),'exec');path.write_bytes(edited)
        importlib.invalidate_caches();module=importlib.reload(module)
        validate(module.PACKS,module.SOURCES,{p['id'] for p in v04.config()['personas']}|set(BEHAVIORS))
        after={v['id']:v for p in module.PACKS for s in p['slots'] for v in s['variants']};all_after.update(after)
        assert set(before)==set(after)
        report['modules'].append({'module':name,'before_source_sha256':expected,'before_raw_base64':base64.b64encode(raw).decode(),
         'before_packs':before_packs,'before_sources':before_sources,'after_source_sha256':hashlib.sha256(edited).hexdigest(),
         'after_packs':module.PACKS,'after_sources':module.SOURCES,
         'changes':[{'id':i,'before':before[i],'after':after[i]} for i in before if before[i]!=after[i]]})
    assert seen==set(DECISIONS)
    for i,signal in DECISIONS.items():
        old=next(o for o in all_before[i]['options'] if o['signal']=='build_alchemist')
        new=next(o for o in all_after[i]['options'] if o['id']==old['id'])
        assert new['label']==old['label'] and new['signal']==signal
    assert Counter(o['signal'] for q in all_after.values() for o in q['options'])['play_inventor']==13
    report['explicit_signal_decisions']=DECISIONS
    report['zero_point_comparison_choices']=len(COMPARE);report['zero_point_purchase_choices']=len(PURCHASE)
    report['all312_ids_and_modes_preserved']=True;report['all_source_snapshots_match_imports']=True
    report['old_2200_history_fixture']='reports/fixtures/before-batch05-final-signal-review.json'
    (ROOT/'research/question-design-v0.5/batch05-cd-parent-acceptance.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'decisions':len(DECISIONS),'modules':[{'module':x['module'],'sha':x['after_source_sha256'],'changed':len(x['changes'])} for x in report['modules']]},ensure_ascii=False))

if __name__=='__main__':main()
