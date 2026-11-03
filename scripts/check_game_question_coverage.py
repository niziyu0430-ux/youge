"""Audit every catalogue record against the actual default question route and text."""
from collections import Counter,defaultdict
from datetime import datetime,timedelta,timezone
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys
import unicodedata

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from youge import v04,v05,questionnaires

LABELS={
    'complete_dedicated':'完整专属',
    'partial_dedicated':'部分定制',
    'generic_template':'通用模板',
    'needs_review':'需核实',
    'invalid_route':'题包或路由异常',
}
INPUTS=['config/games.v0.5.0.json','config/youge.v0.4.0.json',
        'config/question-packs.v0.5.0.json','youge/questionnaires.py','youge/v04.py','youge/v05.py']


def text_key(value,title=''):
    value=unicodedata.normalize('NFKC',str(value))
    if title:value=value.replace(unicodedata.normalize('NFKC',title),'{game}')
    return re.sub(r'\s+','',value).casefold()


def question_key(question,title=''):
    # Shuffling A-D or changing only the selected game's name is not authorship.
    return (text_key(question['text'],title),
            tuple(sorted(text_key(o['label'],title) for o in question['options'])))


def template_keys(config):
    items=[q for group in config['families'].values() for q in group]
    items += [q for q in config['common'] if q['scope']=='anchor']
    return {question_key(q) for q in items}


def form_fingerprint(items,title):
    visible=[question_key(q,title) for q in items if q.get('scope')=='anchor']
    return hashlib.sha256(json.dumps(visible,ensure_ascii=False).encode()).hexdigest()


def inspect_form(items,title,templates,authored_ids):
    errors=[]
    if not isinstance(items,list):return {'errors':['题目不是列表'],'dedicated_ids':[],'template_ids':[],'uncertain_ids':[]}
    if len(items)!=16:errors.append(f'实际{len(items)}题，应为16题')
    ids=[q.get('id') for q in items]
    if len(ids)!=len(set(ids)):errors.append('题目ID重复')
    anchors=[q for q in items if q.get('scope')=='anchor']
    shared=[q for q in items if q.get('scope')=='cross']
    if len(anchors)!=12:errors.append(f'作品题{len(anchors)}道，应为12道')
    if len(shared)!=4:errors.append(f'跨游戏题{len(shared)}道，应为4道')
    dedicated=[];generic=[];uncertain=[]
    for q in items:
        options=q.get('options',[])
        if not 2<=len(options)<=4 or [o.get('id') for o in options]!=list('ABCD'[:len(options)]):errors.append(str(q.get('id'))+'选项应为连续的2至4项')
        if len({o.get('label') for o in options})!=len(options):errors.append(str(q.get('id'))+'选项重复或缺失')
        if not q.get('text') or '{game}' in q.get('text',''):errors.append(str(q.get('id'))+'题干缺失或未展开')
        if q.get('scope')!='anchor':continue
        if question_key(q,title) in templates:generic.append(q['id'])
        elif q['id'] in authored_ids:dedicated.append(q['id'])
        else:uncertain.append(q['id'])
    return {'errors':errors,'dedicated_ids':dedicated,'template_ids':generic,'uncertain_ids':uncertain,
            'shared_ids':[q['id'] for q in shared],'question_ids':ids,
            'form_fingerprint':form_fingerprint(items,title)}


def status_for(forms,errors):
    if errors or any(f['errors'] for f in forms):return 'invalid_route'
    if any(f['uncertain_ids'] for f in forms):return 'needs_review'
    dedicated=min(len(f['dedicated_ids']) for f in forms)
    if dedicated==12:return 'complete_dedicated'
    if dedicated>0:return 'partial_dedicated'
    return 'generic_template'


def input_hashes():
    return {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in INPUTS}


def audit(checked_at):
    before=input_hashes();catalog=v04.catalog();legacy=v04.config();active=v05.bank()
    templates=template_keys(legacy);claims=defaultdict(list)
    for p in active['packs']:
        for gid in p['game_ids']:claims[gid].append(p)
    all_ids={g['id'] for g in catalog['games']+catalog['candidates']}
    source_ids={s['id'] for s in active['sources']}
    old_pack_users=defaultdict(list)
    for g in catalog['games']+catalog['candidates']:
        if g.get('question_pack') in legacy['packs']:
            old_pack_users[g['question_pack']].append({'game_id':g['id'],'title':g['title']})
    rows=[];groups=defaultdict(list);total_routes=0
    for number,game in enumerate(catalog['games'],1):
        gid=game['id'];declared=claims.get(gid,[]);pack=declared[0] if declared else None
        old_pack=game.get('question_pack');errors=[];forms=[]
        if len(declared)>1:errors.append('同一游戏被多个运行题包同时声明')
        if pack:
            authored_ids={q['id'] for s in pack['slots'] for q in s['variants']}
            if len(pack['slots'])!=12:errors.append('运行题包不是12个专属题位')
            for slot in pack['slots']:
                for q in slot['variants']:
                    if not q.get('source_ids') or set(q['source_ids'])-source_ids:
                        errors.append(q['id']+'缺少可定位的机制资料')
            modes=pack['modes']
            pack_key=pack['id'];basis='authored_game_pack'
        else:
            authored_ids={q['id'] for q in legacy['packs'].get(old_pack,[])}
            authored_ids |= set(legacy.get('anchor_context',{}).get(old_pack,{}))
            modes=[{'id':'default','label':'默认'}]
            pack_key=old_pack if old_pack in legacy['packs'] else game.get('mechanic_family')
            basis='partly_custom_legacy_pack' if old_pack in legacy['packs'] else 'generic_mechanic_template'
        for index,mode in enumerate(modes):
            total_routes+=1
            try:
                # The same adapter is called by GET /api/v4/questions. The first call
                # has no instrument override: an old saved form cannot disguise the new route.
                result=questionnaires.questions(gid,mode_id=mode['id'] if index else None)
                items=result['questions'];instrument=result['versions']['instrument']
                if result['game']['id']!=gid:errors.append('默认路由返回了另一款游戏')
                if pack and instrument!='0.5.0':errors.append('声明了专属题，但实际仍走旧模板')
                if pack and result.get('pack',{}).get('id')!=pack['id']:errors.append('实际题包与声明不符')
                finding=inspect_form(items,game['title'],templates,authored_ids)
                finding.update(mode_id=mode['id'],mode_label=mode['label'],instrument=instrument,
                               pack_version=result.get('pack',{}).get('version'),
                               replacement_available=all(q.get('can_replace',False) for q in items[:12]) if pack else False)
                forms.append(finding)
                if not index:groups[finding['form_fingerprint']].append(gid)
            except Exception as exc:
                errors.append(f'{mode["id"]}: {type(exc).__name__}: {exc}')
        if not forms:errors.append('没有可用正式题卷')
        status=status_for(forms,errors) if forms else 'invalid_route'
        count=min((len(f['dedicated_ids']) for f in forms),default=0)
        missing=list(dict.fromkeys(q for f in forms for q in f['template_ids']+f['uncertain_ids']))
        rows.append({'number':number,'game_id':gid,'title':game['title'],
                     'original_title':game.get('original_title'),'status':status,'status_label':LABELS[status],
                     'has_complete_dedicated_form':status=='complete_dedicated',
                     'dedicated_count':count,'required_dedicated_count':12,
                     'missing_dedicated_count':12-count,'missing_dedicated_question_ids':missing,
                     'actual_pack':pack_key,'declared_basis':basis,
                     'shared_pack_with':([{'game_id':x,'title':next(g['title'] for g in catalog['games'] if g['id']==x)} for x in pack['game_ids'] if x!=gid] if pack else
                                         [x for x in old_pack_users.get(old_pack,[]) if x['game_id']!=gid]),
                     'mode_count':len(modes),'forms':forms,'errors':errors})
    row_by_id={r['game_id']:r for r in rows}
    for row in rows:
        for f in row['forms']:
            f['same_default_form_game_count']=len(groups.get(f['form_fingerprint'],[]))
    generic_groups=[]
    for digest,members in groups.items():
        generic=[gid for gid in members if row_by_id[gid]['status']=='generic_template']
        if generic:generic_groups.append({'fingerprint':digest,'count':len(generic),
                                         'pack':row_by_id[generic[0]]['actual_pack'],
                                         'sample_titles':[row_by_id[gid]['title'] for gid in generic[:5]],'game_ids':generic})
    candidates=[]
    for number,game in enumerate(catalog['candidates'],1):
        gid=game['id'];readable=gid in catalog['legacy_game_ids']
        old=game.get('question_pack');dedicated_ids=set()
        declared=claims.get(gid,[])
        if declared:dedicated_ids={q['id'] for s in declared[0]['slots'] for q in s['variants']}
        elif old in legacy['packs']:
            dedicated_ids={q['id'] for q in legacy['packs'][old]}|set(legacy.get('anchor_context',{}).get(old,{}))
        finding=None;error=None
        if readable:
            total_routes+=1
            try:
                result=questionnaires.questions(gid)
                finding=inspect_form(result['questions'],game['title'],templates,dedicated_ids)
            except Exception as exc:error=type(exc).__name__+': '+str(exc)
        candidates.append({'number':number,'game_id':gid,'title':game['title'],
                           'publicly_selectable':False,'has_declared_dedicated_pack':bool(dedicated_ids),
                           'legacy_answers_readable':readable,'legacy_form_inspection':finding,
                           'error':error,'status':'候选未展示，仅兼容旧答卷' if readable else '候选未展示，未接入正式题包'})
    counts=Counter(r['status'] for r in rows);after=input_hashes()
    return {'checked_at':checked_at,'scope':'all published records plus all candidate records',
            'criteria':{'required_dedicated':12,'allowed_shared':4,
                        'template_detection':'Title-normalized question text and sorted option labels; checked against all runtime family/common templates.',
                        'complete_means':'All configured mode forms have 12 non-template items with per-game authoring records and a valid 16-item runtime route.',
                        'limit':'Content/routing coverage audit, not a fresh gameplay-fact or psychometric validity review.'},
            'published_count':len(rows),'candidate_count':len(candidates),'reviewed_record_count':len(rows)+len(candidates),
            'runtime_routes_checked':total_routes,'published_mode_routes_checked':sum(r['mode_count'] for r in rows),
            'published_status_counts':dict(counts),'complete_percentage':round(counts['complete_dedicated']/len(rows)*100,4),
            'published_records_not_complete':len(rows)-counts['complete_dedicated'],
            'published_forms_structurally_valid':sum(not r['errors'] and all(not f['errors'] for f in r['forms']) for r in rows),
            'dedicated_slots_missing':sum(r['missing_dedicated_count'] for r in rows),
            'candidate_legacy_forms_checked':sum(r['legacy_answers_readable'] for r in candidates),
            'candidate_legacy_forms_structurally_valid':sum(r['legacy_answers_readable'] and r['legacy_form_inspection'] is not None and not r['legacy_form_inspection']['errors'] and not r['error'] for r in candidates),
            'candidate_declared_dedicated_packs':sum(r['has_declared_dedicated_pack'] for r in candidates),
            'duplicate_game_ids':sorted(gid for gid,n in Counter(g['id'] for g in catalog['games']+catalog['candidates']).items() if n>1),
            'orphan_authored_game_ids':sorted(set(claims)-all_ids),
            'inputs_sha256':before,'inputs_unchanged_during_audit':before==after,
            'generic_template_groups':sorted(generic_groups,key=lambda g:-g['count']),
            'games':rows,'candidates':candidates}


def cell(value):
    return str(value).replace('|','\\|').replace('\n',' ').replace('\r',' ')


def write_report(report):
    folder=ROOT/'research/question-design-v0.5';folder.mkdir(parents=True,exist_ok=True)
    (folder/'per-game-question-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    counts=report['published_status_counts'];lines=['# 游格逐游戏专属题检查清单','',
        f'检查日期：{report["checked_at"]}。逐条检查{report["published_count"]:,}条公开游戏记录，另检查{report["candidate_count"]:,}条候选记录。游戏记录包含原版、重制版等不同版本。','',
        f'结论：尚未做到每款游戏都有完整专属题。完整专属{counts.get("complete_dedicated",0)}条，部分定制{counts.get("partial_dedicated",0)}条，通用模板{counts.get("generic_template",0):,}条；仍有{report["published_records_not_complete"]:,}条未达到完整标准。','',
        '## 检查标准','',
        '每款应有12道围绕作品编写的专属题，另4道跨游戏题按已确认的设计保留，不算缺项。逐条调用网站默认取题使用的路由，检查题数、选项、实际题包和各配置模式；对比题干与选项，将只替换游戏名或调换选项顺序的通用题识别出来。草稿、旧答卷兼容和候选库不冒充新测试的专属题。','',
        f'共检查{report["runtime_routes_checked"]:,}条实际取题路径，其中公开库{report["published_mode_routes_checked"]:,}条、旧候选兼容{report["candidate_legacy_forms_checked"]}条。公开库{report["published_forms_structurally_valid"]:,}条均能取得16道四选一，但“有题可答”不等于“12道都是专属”。检查期间输入文件'+('未变化。' if report['inputs_unchanged_during_audit'] else '发生变化，结果需重新检查。'),'',
        '| 判定 | 记录数 | 含义 |','|---|---:|---|']
    for status in LABELS:
        if counts.get(status):lines.append(f'| {LABELS[status]} | {counts[status]:,} | '+{
            'complete_dedicated':'12道作品题均有逐款内容并接入实际路由',
            'partial_dedicated':'部分作品题已经定制，其余仍为通用问法',
            'generic_template':'12道作品题均沿用机制模板，只替换作品名',
            'needs_review':'存在无法确认编写依据的题目',
            'invalid_route':'题包声明、题数或实际路由存在异常'}[status]+' |')
    lines.extend(['','## 完整专属的游戏','',
                  '| 游戏 | 游戏ID | 专属题 | 模式数 |','|---|---|---:|---:|'])
    for row in report['games']:
        if row['status']=='complete_dedicated':lines.append(f'| {cell(row["title"])} | {row["game_id"]} | {row["dedicated_count"]}/12 | {row["mode_count"]} |')
    lines.extend(['','## 部分定制的游戏',''])
    if counts.get('partial_dedicated'):
        lines.extend(['以下游戏存在独立的旧题包记录，但仍缺完整的12道专属题。原版与导演剪辑版若共用题包，会逐条列出。','',
                      '| 游戏 | 游戏ID | 专属题 | 仍使用通用问法的题位 | 实际题包 |','|---|---|---:|---|---|'])
    else:
        lines.extend(['当前没有部分定制记录；本轮最初发现的9条已接入完整专属题包。'])
    for row in report['games']:
        if row['status']=='partial_dedicated':lines.append(f'| {cell(row["title"])} | {row["game_id"]} | {row["dedicated_count"]}/12 | {"、".join(row["missing_dedicated_question_ids"])} | {row["actual_pack"]} |')
    lines.extend(['','## 通用模板的复用情况','',
                  '| 模板 | 使用记录数 | 示例 |','|---|---:|---|'])
    for group in report['generic_template_groups']:
        lines.append(f'| {group["pack"]} | {group["count"]} | {cell("、".join(group["sample_titles"]))} |')
    lines.extend(['','## 公开游戏逐条清单','',
                  '按游戏库当前顺序逐条列出。这里的专属题数不包含4道跨游戏题。','',
                  '| 序号 | 游戏 | 游戏ID | 判定 | 专属题/12 | 实际题包 |','|---:|---|---|---|---:|---|'])
    for row in report['games']:
        lines.append(f'| {row["number"]} | {cell(row["title"])} | {row["game_id"]} | {row["status_label"]} | {row["dedicated_count"]}/12 | {row["actual_pack"]} |')
    lines.extend(['','## 候选游戏逐条清单','',
                  f'候选库{report["candidate_count"]:,}条不在新测试的选择器中，声明逐款专属题的记录有{report["candidate_declared_dedicated_packs"]}条；其中{report["candidate_legacy_forms_checked"]}条仅保留旧答卷兼容，不能算正式专属题已经完成。','',
                  '| 序号 | 候选游戏 | 游戏ID | 状态 |','|---:|---|---|---|'])
    for row in report['candidates']:
        lines.append(f'| {row["number"]} | {cell(row["title"])} | {row["game_id"]} | {row["status"]} |')
    lines.extend(['','## 检查依据','',
                  '- 网站实际取题路由：youge/questionnaires.py。',
                  '- 当前作品库：config/games.v0.5.0.json。',
                  '- 独立专属题：config/question-packs.v0.5.0.json。',
                  '- 旧版专用题、情境覆盖与16种机制模板：config/youge.v0.4.0.json。',
                  '- 逐模式题目ID、模板命中、相同题卷分组与输入文件校验值：[机器可读检查结果](../research/question-design-v0.5/per-game-question-audit.json)。','',
                  '本轮核对题目覆盖与实际接入，不将结构通过等同于逐款攻略复核、选项设计质量或测量效果已经验证。',''])
    path=ROOT/'exports/游格-逐游戏专属题检查清单.md'
    path.write_text('\n'.join(lines),encoding='utf-8')
    return path


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--date',default=datetime.now(timezone(timedelta(hours=8))).date().isoformat())
    args=parser.parse_args();datetime.strptime(args.date,'%Y-%m-%d')
    result=audit(args.date);path=write_report(result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('games','candidates','generic_template_groups','inputs_sha256','criteria')},ensure_ascii=False))
    print(str(path))


if __name__=='__main__':main()
