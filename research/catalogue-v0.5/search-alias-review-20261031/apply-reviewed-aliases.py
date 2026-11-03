"""Dry-build, reject every unrelated change, then apply the two reviewed aliases."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import hashlib
import json
import sys

ROOT=Path.cwd()
sys.path.insert(0,str(ROOT/'scripts'))
import build_expanded_catalogue as builder

path=ROOT/'config/games.v0.5.0.json'
before=json.loads(path.read_text(encoding='utf8'))
original_write=builder.write
original_exports=builder.write_exports
outputs={}
builder.write=lambda p,d:outputs.__setitem__(Path(p).resolve(),deepcopy(d))
builder.write_exports=lambda d:None
builder.main()
after=outputs[path.resolve()]
oldrows={g['id']:g for field in ('games','candidates') for g in before[field]}
newrows={g['id']:g for field in ('games','candidates') for g in after[field]}
assert oldrows.keys()==newrows.keys()
changes=[]
for gid in oldrows:
    if oldrows[gid]!=newrows[gid]:
        fields={key for key in oldrows[gid].keys()|newrows[gid].keys()
                if oldrows[gid].get(key)!=newrows[gid].get(key)}
        changes.append({'game_id':gid,'fields':sorted(fields)})
assert {row['game_id'] for row in changes}=={'steam-233450','steam-1245560'},changes[:15]
assert all(set(row['fields'])<={'aliases','name_evidence','alias_evidence'} for row in changes),changes
assert {key:value for key,value in before.items() if key not in ('games','candidates')}=={
    key:value for key,value in after.items() if key not in ('games','candidates')}
assert [g['id'] for g in before['games']]==[g['id'] for g in after['games']]
assert [g['id'] for g in before['candidates']]==[g['id'] for g in after['candidates']]
added={gid:[a for a in newrows[gid]['aliases'] if a not in oldrows[gid]['aliases']]
       for gid in ('steam-233450','steam-1245560')}
assert added=={'steam-233450':['监狱建筑师','監獄建築師'],
              'steam-1245560':['帕夏灵田','帕夏靈田']},added
for gid in added:
    assert newrows[gid]['alias_evidence'][:len(oldrows[gid]['alias_evidence'])]==oldrows[gid]['alias_evidence']
    new_evidence=newrows[gid]['alias_evidence'][len(oldrows[gid]['alias_evidence']):]
    assert all(x['kind']=='script_variant' and x['value'] in added[gid] for x in new_evidence)

report={
    'checked_at_utc':datetime.now(timezone.utc).isoformat(),
    'status':'source_reviewed_alias_only_diff_accepted_pending_runtime_search_and_history',
    'before_catalogue_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
    'game_count_unchanged':len(before['games']),'candidate_count_unchanged':len(before['candidates']),
    'changed_fields':changes,'added_aliases':added,
    'before_affected_records':{gid:oldrows[gid] for gid in added},
    'after_affected_records':{gid:newrows[gid] for gid in added},
    'display_names_versions_classification_and_eligibility_all_unchanged':True,
    'source_evidence':'research/catalogue-v0.5/search-alias-evidence.json',
    'primary_reading':[
        'Live official Steam PA Chinese translated review195/197 andoriginal2015identity26/99 actuallyread; commonaliasobserved, notofficialChineseproducttitle.',
        'Current HTTP200 official RootsPachaChineseAbout fullyread, uses帕夏灵田; productnameRoots of Pacha andexistingdisplay帕夏时代preserved.'],
    'qualification':'Only reviewed search aliases andtheir evidence. No title,mode,question,score,inclusion change. All4660actualoldreportpairs andrealbrowsersearch stillrequired.'}
report_path=ROOT/'reports/catalogue-reviewed-search-aliases-20261031.json'
assert not report_path.exists()
original_write(path,after)
original_exports(after)
report['after_catalogue_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'changed':changes,'added_aliases':added,'oldnames_preserved':True},ensure_ascii=False))
