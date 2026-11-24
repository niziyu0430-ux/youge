"""Compare actual historical forms and reports across an authored-bank revision."""
from concurrent.futures import ProcessPoolExecutor
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


def capture(previous=None, verification=None):
    bank=v05.bank()
    bank_sha=digest(bank)
    pack_versions={p['id']:p['version'] for p in bank['packs']}
    reusable_packs=set()
    previous_rows={}
    if previous is not None:
        assert verification['passed'] is True
        assert previous['fictional_fixtures_only'] is True
        assert verification['fixture_sha256']==digest(previous)
        assert verification['current_bank_sha256']==bank_sha
        assert verification['historical_form_and_report_pairs']==len(previous['rows'])
        previous_versions=previous['pack_versions']
        reusable_packs={key for key,version in previous_versions.items() if pack_versions.get(key)==version}
        assert set(verification['preserved_pack_ids'])==reusable_packs
        assert set(verification['changed_pack_ids'])==set(previous_versions)-reusable_packs
        for row in previous['rows']:
            if row['pack_id'] not in reusable_packs:
                continue
            key=(row['pack_id'],row['game_id'],row['mode_id'],row['variant_id'])
            assert key not in previous_rows
            previous_rows[key]=row
    rows=[]
    for pack in bank['packs']:
        gid=pack['game_ids'][0]
        for mode in pack['modes']:
            form=None
            for slot in pack['slots']:
                for variant in slot['variants']:
                    if variant.get('modes') and mode['id'] not in variant['modes']:
                        continue
                    key=(pack['id'],gid,mode['id'],variant['id'])
                    if pack['id'] in reusable_packs:
                        rows.append(previous_rows.pop(key))
                        continue
                    if form is None:
                        form=questionnaires.questions(gid,mode_id=mode['id'])
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
    assert not previous_rows, '已验证基线中有未保留的历史题目'
    return {'fictional_fixtures_only':True,'bank_sha256':bank_sha,
            'pack_versions':pack_versions,'rows':rows}


def check_row(row):
    assert row['raw']['fictional'] is True
    form=questionnaires.questions(raw=deepcopy(row['raw']))
    assert digest(form['questions'])==row['form_sha256'],row['variant_id']+'旧题内容改变'
    report=finish(deepcopy(row['raw']))
    assert digest(report)==row['report_sha256'],row['variant_id']+'旧报告改变'


def check(fixture, workers=1):
    assert fixture['fictional_fixtures_only'] is True
    bank=v05.bank()
    bank_sha=digest(bank)
    if workers==1:
        for row in fixture['rows']:
            check_row(row)
    else:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            for _ in pool.map(check_row,fixture['rows'],chunksize=120):
                pass
    assert digest(v05.bank())==bank_sha,'The bank changed during historical verification.'
    current={p['id']:p['version'] for p in bank['packs']}
    return {'passed':True,'historical_form_and_report_pairs':len(fixture['rows']),
            'fixture_sha256':digest(fixture),'current_bank_sha256':bank_sha,
            'changed_pack_ids':[p for p,v in fixture['pack_versions'].items() if current.get(p)!=v],
            'preserved_pack_ids':[p for p,v in fixture['pack_versions'].items() if current.get(p)==v],
            'qualification':'Exact historical forms, evidence, signals and full deterministic reports; no player data written.'}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['capture','check']);parser.add_argument('fixture')
    parser.add_argument('--output')
    parser.add_argument('--workers',type=int,default=1,help='Verify history rows in parallel')
    parser.add_argument('--reuse-verified',nargs=2,metavar=('BASELINE','CHECK_REPORT'),
                        help='Reuse historical rows only after a full check against the current bank')
    args=parser.parse_args();path=report_path(args.fixture)
    if args.reuse_verified and args.mode!='capture':
        parser.error('--reuse-verified requires capture')
    if args.workers<1 or (args.mode=='capture' and args.workers!=1):
        parser.error('--workers must be positive and is only used for check')
    if args.mode=='capture':
        assert not path.exists(),'不要覆盖已保存的历史校验基线'
        inputs=[json.loads(report_path(name).read_text(encoding='utf-8')) for name in (args.reuse_verified or [])]
        result=capture(*inputs);path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({'captured':len(result['rows']),'packs':len(result['pack_versions'])}))
    else:
        result=check(json.loads(path.read_text(encoding='utf-8')),args.workers)
        if args.output:
            report_path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
