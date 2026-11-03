"""Compare actual historical forms and reports across an authored-bank revision."""
from copy import deepcopy
from pathlib import Path
import argparse
import hashlib
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from youge import v05,questionnaires
from verify_authored_batch import finish


def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True).encode()).hexdigest()


def report_path(name):
    path=(ROOT/name).resolve()
    assert path.is_relative_to((ROOT/'reports').resolve()),'校验资料应保存在reports内'
    path.parent.mkdir(parents=True,exist_ok=True)
    return path


def capture():
    rows=[]
    for pack in v05.bank()['packs']:
        gid=pack['game_ids'][0]
        for mode in pack['modes']:
            form=questionnaires.questions(gid,mode_id=mode['id'])
            for slot in pack['slots']:
                for variant in slot['variants']:
                    if variant.get('modes') and mode['id'] not in variant['modes']:
                        continue
                    raw=deepcopy(form['response']);raw['fictional']=True
                    raw['question_variants'][slot['id']]=variant['id']
                    current=questionnaires.questions(raw=raw)
                    raw['answers']={q['id']:q['options'][(i+len(rows))%len(q['options'])]['id']
                                    for i,q in enumerate(current['questions'])}
                    report=finish(raw)
                    rows.append({'pack_id':pack['id'],'game_id':gid,'mode_id':mode['id'],
                                 'variant_id':variant['id'],'raw':raw,
                                 'form_sha256':digest(current['questions']),
                                 'report_sha256':digest(report)})
    return {'fictional_fixtures_only':True,'bank_sha256':digest(v05.bank()),
            'pack_versions':{p['id']:p['version'] for p in v05.bank()['packs']},
            'rows':rows}


def check(fixture):
    assert fixture['fictional_fixtures_only'] is True
    for row in fixture['rows']:
        assert row['raw']['fictional'] is True
        form=questionnaires.questions(raw=deepcopy(row['raw']))
        assert digest(form['questions'])==row['form_sha256'],row['variant_id']+'旧题内容改变'
        report=finish(deepcopy(row['raw']))
        assert digest(report)==row['report_sha256'],row['variant_id']+'旧报告改变'
    current={p['id']:p['version'] for p in v05.bank()['packs']}
    return {'passed':True,'historical_form_and_report_pairs':len(fixture['rows']),
            'changed_pack_ids':[p for p,v in fixture['pack_versions'].items() if current.get(p)!=v],
            'preserved_pack_ids':[p for p,v in fixture['pack_versions'].items() if current.get(p)==v],
            'qualification':'Exact historical forms, evidence, signals and full deterministic reports; no player data written.'}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['capture','check']);parser.add_argument('fixture')
    parser.add_argument('--output');args=parser.parse_args();path=report_path(args.fixture)
    if args.mode=='capture':
        assert not path.exists(),'不要覆盖已保存的历史校验基线'
        result=capture();path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({'captured':len(result['rows']),'packs':len(result['pack_versions'])}))
    else:
        result=check(json.loads(path.read_text(encoding='utf-8')))
        if args.output:
            report_path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
