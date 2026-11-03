"""Run actual forms, every mode/variant, replacement and report evidence for a batch."""
from collections import Counter
from copy import deepcopy
from datetime import datetime,timezone,timedelta
from pathlib import Path
import argparse
import hashlib
import importlib
import json
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from youge import v04,v05,questionnaires
from question_authoring import validate
from check_game_question_coverage import inspect_form,template_keys


def finish(raw):
    for _ in range(3):
        result=questionnaires.report(raw)
        if result['complete']:return result['report']
        raw['extra_answers'].append({'question_id':result['next_question']['id'],'answer':'C'})
    raise AssertionError('超过两道补问仍未完成')


def verify(names,include_initial_six=False):
    sources=[];packs=[]
    for name in names:
        assert re.fullmatch(r'question_batch\d{2}(?:_[a-z0-9]+)?',name)
        module=importlib.import_module(name);packs+=module.PACKS;sources+=module.SOURCES
    if include_initial_six:
        from build_question_packs_v05 import initial_packs
        draft=json.loads((ROOT/'config/question-packs.v0.5.draft.json').read_text(encoding='utf-8'))
        packs=initial_packs(draft,{p['id'] for p in v04.config()['personas']})+packs
        sources=json.loads((ROOT/'research/question-design-v0.5/sources.json').read_text(encoding='utf-8'))['sources']+sources
    validate(packs,sources,{p['id'] for p in v04.config()['personas']}|set(v05.bank()['behavior_copy']))
    templates=template_keys(v04.config());rows=[];reports=0
    shared=[v04.public_question(q) for q in v04.config()['common'] if q['scope']=='cross']
    for declared in packs:
        pack=v05.pack_for(declared['game_ids'][0])
        assert pack and pack['id']==declared['id'],'题包尚未实际接入：'+declared['id']
        assert {k:v for k,v in pack.items() if k!='version'}==declared,'运行题包与当前已审源稿不一致：'+declared['id']
        for gid in declared['game_ids']:
            form=questionnaires.questions(gid)
            assert form['pack']['id']==pack['id'] and form['versions']['instrument']=='0.5.0'
            old=questionnaires.questions(gid,instrument='0.4.0')
            assert old['questions']==[v04.public_question(q) for q in v04.questionnaire(gid)]
        authored={q['id'] for s in pack['slots'] for q in s['variants']}
        kinds=Counter();variants=0
        for mode in pack['modes']:
            form=questionnaires.questions(pack['game_ids'][0],mode_id=mode['id'])
            finding=inspect_form(form['questions'],pack['title'],templates,authored)
            assert len(finding['dedicated_ids'])==12 and not finding['errors']
            assert not finding['template_ids'] and not finding['uncertain_ids']
            assert [q['options'] for q in form['questions'][12:]]==[q['options'] for q in shared]
            kinds.clear()
            for slot in pack['slots']:
                initial=next(q for q in form['questions'] if q.get('slot_id')==slot['id'])
                assert initial['can_replace'],'缺少适用替代：'+initial['id']
                actual=next(v for v in slot['variants'] if v['id']==initial['id'])
                kinds[actual['question_type']]+=1
                replaced=v05.replace_question(form['response'],initial['id'])
                restored=v05.replace_question(replaced['response'],replaced['questions'][slot['number']-1]['id'],undo=True)
                assert restored['questions']==form['questions'],'撤销未恢复原题'
                for variant in slot['variants']:
                    if variant.get('modes') and mode['id'] not in variant['modes']:continue
                    raw=deepcopy(form['response']);raw['fictional']=True
                    raw['question_variants'][slot['id']]=variant['id']
                    current=questionnaires.questions(raw=raw)
                    raw['answers']={q['id']:q['options'][(i+variants)%len(q['options'])]['id'] for i,q in enumerate(current['questions'])}
                    report=finish(raw);reports+=1;variants+=1
                    assert report['question_count']<=18
                    evidence=report['evidence']['answer:'+variant['id']]
                    assert evidence['question']==variant['text']
                    assert evidence['label']==next(o['label'] for o in variant['options'] if o['id']==raw['answers'][variant['id']])
            assert kinds=={'situational_action':8,'experience_reflection':4},(pack['id'],mode['id'],kinds)
        rows.append({'pack_id':pack['id'],'title':pack['title'],'game_ids':pack['game_ids'],
                     'pack_version':pack['version'],'modes':len(pack['modes']),'verified_variants':variants,'passed':True})
    return {'checked_at':datetime.now(timezone(timedelta(hours=8))).isoformat(),
            'modules':names,'packs':len(rows),'game_records':sum(len(p['game_ids']) for p in packs),
            'actual_reports_verified':reports,'passed':True,'results':rows,
            'initial_six_included':include_initial_six,
            'runtime_sha256':hashlib.sha256((ROOT/'config/question-packs.v0.5.0.json').read_bytes()).hexdigest(),
            'qualification':'Runtime and evidence checks; does not replace source editorial review or human player trial.'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('modules',nargs='*');parser.add_argument('--output')
    parser.add_argument('--include-initial-six',action='store_true')
    args=parser.parse_args()
    if not args.modules and not args.include_initial_six:parser.error('请指定批次或初始六款')
    result=verify(args.modules,args.include_initial_six)
    if args.output:
        target=(ROOT/args.output).resolve()
        assert target.is_relative_to((ROOT/'reports').resolve()),'验证结果应留在reports中'
        target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('results','runtime_sha256','qualification')},ensure_ascii=False))


if __name__=='__main__':main()
