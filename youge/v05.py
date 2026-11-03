"""Versioned, authored game forms with explicit replacement history and evidence."""
from collections import Counter
from copy import deepcopy
from functools import lru_cache
import hashlib
import json
from pathlib import Path

from .engine import InputError
from . import v04

ROOT=Path(__file__).resolve().parents[1]
VERSIONS={'instrument':'0.5.0','scoring':'0.5.0','report_rules':'0.5.0','catalog':'0.5.0'}


@lru_cache(maxsize=1)
def _bank(stamp):
    return json.loads((ROOT/'config/question-packs.v0.5.0.json').read_text(encoding='utf-8'))


def bank():
    path=ROOT/'config/question-packs.v0.5.0.json'
    return _bank(path.stat().st_mtime_ns)


def pack_for(game_id,version=None):
    current=next((p for p in bank()['packs'] if game_id in p['game_ids']),None)
    if current is None or version is None or current['version']==version:return current
    entry=next((e for e in bank()['pack_history'] if game_id in e['game_ids'] and e['version']==version),None)
    if entry:return json.loads((ROOT/entry['path']).read_text(encoding='utf-8'))
    return None


def compatible(versions):
    return versions==VERSIONS


def descriptor(pack):
    return {k:deepcopy(pack[k]) for k in ('id','version','game_ids','modes')}


def mode_for(pack,mode_id=None):
    mode_id=mode_id or pack['modes'][0]['id']
    mode=next((m for m in pack['modes'] if m['id']==mode_id),None)
    if mode is None:raise InputError('请选择这款游戏支持的体验范围。')
    return mode


def _form(pack,mode,variants,history):
    slots={q['id']:q for q in pack['slots']}
    if not isinstance(variants,dict) or not isinstance(history,dict):raise InputError('题目替换记录不完整。')
    if (set(variants)|set(history))-set(slots):raise InputError('替换记录含有其他题包的问题。')
    result=[]
    for order,slot in enumerate(pack['slots'],1):
        available=[q for q in slot['variants'] if not q.get('modes') or mode['id'] in q['modes']]
        lookup={q['id']:q for q in available}
        initial=mode.get('initial_variants',{}).get(slot['id'],available[0]['id'])
        chosen=variants.get(slot['id'],initial)
        rejected=history.get(slot['id'],[])
        if not isinstance(rejected,list) or any(not isinstance(q,str) for q in rejected):raise InputError('换题记录格式不正确。')
        if len(rejected)!=len(set(rejected)) or any(q not in lookup for q in rejected):raise InputError('换题记录含有不适用的情境。')
        if not isinstance(chosen,str) or chosen not in lookup or chosen in rejected:raise InputError('当前题目与换题记录不一致。')
        item=deepcopy(lookup[chosen]);item.update(slot_id=slot['id'],order=order,scope='anchor',
            can_replace=any(q not in rejected and q!=chosen for q in lookup),can_undo_replace=bool(rejected))
        result.append(item)
    for order,item in enumerate(deepcopy(bank()['shared_questions']),13):
        item.update(order=order,scope='cross',can_replace=False,can_undo_replace=False)
        result.append(item)
    return result


def public_question(item):
    fields=('id','text','scope','order','slot_id','can_replace','can_undo_replace')
    return {k:deepcopy(item[k]) for k in fields if k in item}|{'options':[{'id':o['id'],'label':o['label']} for o in item['options']]}


def normalize(raw):
    if not isinstance(raw,dict) or not compatible(raw.get('versions')):raise InputError('答卷与专属题版本不同，请使用原版本查看。')
    gid=raw.get('game_id');pack=pack_for(gid,raw.get('pack_version'))
    if pack is None:raise InputError('这款游戏尚未接入本版专属题。')
    if raw.get('pack_version')!=pack['version']:raise InputError('这份答卷的题包版本不匹配，不能用新题重算。')
    mode=mode_for(pack,raw.get('mode_id'))
    variants=raw.get('question_variants',{});history=raw.get('replacement_history',{})
    form=_form(pack,mode,variants,history)
    answers=raw.get('answers',{});extra=raw.get('extra_answers',[])
    if not isinstance(answers,dict) or not isinstance(extra,list) or len(extra)>2:raise InputError('答卷格式不正确，补问最多两题。')
    if set(answers)-{q['id'] for q in form}:raise InputError('答卷含有未展示或已被替换的问题。')
    if any(not isinstance(a,str) or a not in 'ABCD' or len(a)!=1 for a in answers.values()):raise InputError('每题请选择A、B、C、D中的一个答案。')
    allowed={q['id']:{o['id'] for o in q['options']} for q in form}
    if any(answer not in allowed[qid] for qid,answer in answers.items()):raise InputError('请选择该题实际显示的选项。')
    for e in extra:
        if not isinstance(e,dict) or set(e)!={'question_id','answer'} or not isinstance(e['question_id'],str) or e['answer'] not in ('A','B','C','D'):raise InputError('补问记录不正确。')
    name=raw.get('display_name','玩家');rid=raw.get('respondent_id','local-player')
    if not isinstance(name,str) or len(name)>24 or not isinstance(rid,str) or len(rid)>100:raise InputError('档案称呼或标识不正确。')
    return {'versions':deepcopy(VERSIONS),'pack_version':pack['version'],'mode_id':mode['id'],
            'question_variants':deepcopy(variants),'replacement_history':deepcopy(history),
            'respondent_id':rid,'display_name':name.strip() or '玩家','game_id':gid,
            'answers':deepcopy(answers),'extra_answers':deepcopy(extra),'fictional':raw.get('fictional') is True}


def questions(game_id=None,raw=None,mode_id=None):
    if raw is None:
        pack=pack_for(game_id)
        if pack is None:raise InputError('这款游戏尚未接入本版专属题。')
        raw={'versions':deepcopy(VERSIONS),'pack_version':pack['version'],'game_id':game_id,'mode_id':mode_id}
    response=normalize(raw);pack=pack_for(response['game_id'],response['pack_version']);mode=mode_for(pack,response['mode_id'])
    form=_form(pack,mode,response['question_variants'],response['replacement_history'])
    return {'versions':deepcopy(VERSIONS),'game':v04.find_game(response['game_id']),
            'pack':descriptor(pack),'response':response,'questions':[public_question(q) for q in form]}


def _replacement_expansion(pack,game_id):
    """Return a published append-only expansion without reinterpreting old work.

    Resume and reports never call this. An explicit replacement may use a newer
    pack only if every old scene, choice, signal and mode remains identical.
    """
    latest=pack_for(game_id)
    if latest is None or latest['version']==pack['version']:return None
    if any(latest.get(key)!=pack.get(key) for key in ('id','title','scope','game_ids')):return None
    latest_modes={mode['id']:mode for mode in latest['modes']}
    if any(latest_modes.get(mode['id'])!=mode for mode in pack['modes']):return None
    if [(slot['id'],slot['number']) for slot in latest['slots']]!=[(slot['id'],slot['number']) for slot in pack['slots']]:return None
    for old_slot,new_slot in zip(pack['slots'],latest['slots']):
        newer={variant['id']:variant for variant in new_slot['variants']}
        if len(newer)!=len(new_slot['variants']):return None
        if any(newer.get(variant['id'])!=variant for variant in old_slot['variants']):return None
    return latest


def replace_question(raw,question_id,undo=False):
    response=normalize(raw);pack=pack_for(response['game_id'],response['pack_version']);mode=mode_for(pack,response['mode_id'])
    form=_form(pack,mode,response['question_variants'],response['replacement_history'])
    current=next((q for q in form if q['id']==question_id and q['scope']=='anchor'),None)
    if current is None:raise InputError('只可替换当前作品的专属情境题。')
    key=current['slot_id'];history=response['replacement_history'].setdefault(key,[])
    slot=next(q for q in pack['slots'] if q['id']==key)
    if undo:
        if not history:raise InputError('这道题还没有换过情境。')
        chosen=history.pop()
    else:
        available=[q for q in slot['variants'] if not q.get('modes') or mode['id'] in q['modes']]
        chosen=next((q['id'] for q in available if q['id']!=question_id and q['id'] not in history),None)
        if chosen is None:
            expanded=_replacement_expansion(pack,response['game_id'])
            if expanded is not None:
                expanded_slot=next(q for q in expanded['slots'] if q['id']==key)
                candidates=[q for q in expanded_slot['variants'] if not q.get('modes') or mode['id'] in q['modes']]
                chosen=next((q['id'] for q in candidates if q['id']!=question_id and q['id'] not in history),None)
                if chosen is not None:
                    slot=expanded_slot
                    response['pack_version']=expanded['version']
        if chosen is None:raise InputError('这道题暂时没有其他适用情境。可以撤销换题或暂存进度，未体验不会被计成答案。')
        history.append(question_id)
    response['question_variants'][key]=chosen
    # Only the actual selected variant can have an answer. Changing the form invalidates ties.
    for item in slot['variants']:response['answers'].pop(item['id'],None)
    response['extra_answers']=[]
    return questions(raw=response)


def _points(selected,tie_points):
    people=[p['id'] for p in v04.config()['personas']]
    raw=Counter({p:0 for p in people});anchors=Counter();cross=Counter()
    for item,option,_ in selected:
        signal=option.get('signal')
        if signal not in people:continue
        raw[signal]+=2
        if item['scope']=='anchor':anchors[signal]+=1
        else:cross[signal]+=2
    # Repeated variants/topics cannot create arbitrarily many persona points.
    points=Counter({p:min(anchors[p],2)*2+cross[p]+tie_points[p] for p in people})
    return points,raw,anchors


def score(raw):
    response=normalize(raw);pack=pack_for(response['game_id'],response['pack_version']);mode=mode_for(pack,response['mode_id'])
    items=_form(pack,mode,response['question_variants'],response['replacement_history'])
    if len(response['answers'])!=16:raise InputError('请完成16道适用题目；没有体验过的情境可以换题。')
    selected=[];evidence={}
    def apply(item,answer):
        option=next(o for o in item['options'] if o['id']==answer);ref='answer:'+item['id']
        selected.append((item,option,ref))
        evidence[ref]={'question_id':item['id'],'slot_id':item.get('slot_id'),
                      'question':item['text'],'label':option['label'],'answer':answer,
                      'scope':item['scope'],'signal':option.get('signal'),
                      'pack_version':pack['version']}
        return option.get('signal')
    for item in items:apply(item,response['answers'][item['id']])
    base_selected=list(selected);bonus=Counter();trace=[];last=None
    points,raw_points,anchors=_points(base_selected,bonus)
    for index in range(2):
        ordered=v04.rank(points,Counter({p:min(n,2) for p,n in anchors.items()}),last)
        if points[ordered[0]]-points[ordered[1]]>2:
            if len(response['extra_answers'])>index:raise InputError('正式答案已变化，请重新生成补问。')
            break
        candidates=ordered[:4]
        signature=json.dumps({'candidates':candidates,'answers':response['answers'],
                              'variants':response['question_variants'],'mode':mode['id'],
                              'history':response['replacement_history'],'pack':pack['version'],'index':index},sort_keys=True)
        digest=hashlib.sha256(signature.encode()).hexdigest()[:14]
        item={'id':f'T{index+1:02d}.v05.{digest}',
              'text':['放眼你玩过的游戏，现在更想把时间留给哪件事？','再做一个取舍，你更想接着体验哪件事？'][index],
              'scope':'cross','order':17+index,'options':[{'id':chr(65+i),'label':v04.config()['tie_actions'][p][index],'signal':p} for i,p in enumerate(candidates)]}
        if len(response['extra_answers'])<=index:return {'complete':False,'next_question':public_question(item),'answered':16+index,'response':response}
        answer=response['extra_answers'][index]
        if answer['question_id']!=item['id']:raise InputError('题目或答案已变化，请重新回答补问。')
        before=dict(points);last=apply(item,answer['answer']);bonus[last]+=4
        trace.append({'question_id':item['id'],'candidate_ids':candidates,'choice':answer['answer'],'points_before':before,'bonus':4})
        points,_,_=_points(base_selected,bonus)
    return {'complete':True,'response':response,'selected':selected,'evidence':evidence,
            'points':dict(points),'raw_points':dict(raw_points),'anchor_counts':dict(anchors),
            'ordered':v04.rank(points,Counter({p:min(n,2) for p,n in anchors.items()}),last),'tie_trace':trace}


COOP_COPY={
    'A':'一起玩时，可以给聊天与临时改变安排留出空间，不必把每段共同时间都排成任务。',
    'B':'一起玩时，先说清共同目标、分工和推进时间，会更贴近你这次表达的期待。',
    'C':'一起玩时，可以保留各自的节奏，再约一个愿意交流的时刻。',
    'D':'一起玩时，可以先聊各自想扮演的角色和经历，让共同故事有展开的空间。'}


def report(raw):
    state=score(raw)
    if not state['complete']:return state
    response=state['response'];c=v04.config();winner=state['ordered'][0]
    persona=deepcopy(next(p for p in c['personas'] if p['id']==winner))
    profile=deepcopy(c['personality_portraits']['personas'][winner]);evidence=state['evidence']
    def claim(rule,text,refs,scope='this_game'):
        return {'rule_id':rule,'rule_version':VERSIONS['report_rules'],'text':text,
                'evidence_refs':refs,'scope':scope,'condition_snapshot':{'selected_answers':{evidence[r]['question_id']:evidence[r]['answer'] for r in refs}}}
    refs=[r for item,o,r in state['selected'] if o.get('signal')==winner]
    text=c['report_copy']['persona_details'][winner] if len(refs)>=2 else c['report_copy']['single_evidence_prefix']+evidence[refs[0]]['label']+'。'
    insights=[claim('V05_PRIMARY',text,refs[:3],'gaming' if len(refs)>=2 else 'specific_scenario')]
    anchors=[row for row in state['selected'] if row[0]['scope']=='anchor']
    attractions=[claim('V05_GAME_SCENARIO','在“'+item['scene']+'”的情境中，你更愿意：'+o['label']+'。',[r]) for item,o,r in anchors[:4]]
    coop=response['answers']['X14'];coop_claim=claim('V05_COOP',COOP_COPY[coop],['answer:X14'],'specific_habit')
    advice=[{'topic':'coop','title':'共同游戏的安排','semantic_key':coop,'comparability_key':'shared:X14:v04',**coop_claim}]
    behavior_tags=[];behavior_copy=bank()['behavior_copy']
    for item,o,ref in anchors:
        if o.get('signal') in behavior_copy:
            copy=behavior_copy[o['signal']]
            advice.append({'topic':'v05:'+item['slot_id'],'title':item['scene'],
                           'comparability_key':response['pack_version']+':'+item['id'],
                           'semantic_key':item['id']+':'+o['id'],**claim('V05_EXPLICIT_BEHAVIOR',copy['text'],[ref],'specific_scenario')})
            behavior_tags.append({'text':copy['tag'],'evidence_refs':[ref]})
    relations=deepcopy(profile['with_others'])+[COOP_COPY[coop]]
    # Only actual behavior answers can supply additional relationship copy.
    relations.extend(a['text'] for a in advice[1:2])
    sections=[{'id':'character','title':'你的性格底色','paragraphs':deepcopy(profile['inner_world']),'kind':'original_archetype_interpretation'},
              {'id':'relations','title':'与你相处的方式','paragraphs':relations,'kind':'archetype_and_explicit_answers'}]
    cross_echo=[]
    for p in state['ordered']:
        ar=[r for item,o,r in anchors if o.get('signal')==p]
        cr=[r for item,o,r in state['selected'] if item['id'].startswith('X') and o.get('signal')==p]
        if ar and cr:
            person=next(x for x in c['personas'] if x['id']==p)
            cross_echo.append(claim('V05_CROSS_ECHO','本命作品与跨游戏选择中，都出现了“'+person['central_pull']+'”相关体验。',ar[:1]+cr[:1],'gaming'))
    game=v04.find_game(response['game_id'])
    result={'versions':deepcopy(VERSIONS),'fictional':response['fictional'],'display_name':response['display_name'],
            'persona':persona,'game':{k:deepcopy(game[k]) for k in ('id','title','original_title','category_ids')},
            'one_line':profile['headline'],'personality_profile':profile,'report_sections':sections,
            'insights':insights,'attractions':attractions,'cross_echo':cross_echo[:2],
            'behavior_tags':behavior_tags,'advice':advice,'drains':[],
            'evidence':evidence,'audit':{'points':state['points'],'uncapped_semantic_points':state['raw_points'],
                                      'anchor_support_count':state['anchor_counts'],'rank':state['ordered'],
                                      'tie_trace':state['tie_trace'],'scoring_policy':bank()['scoring_policy'],
                                      'form_variants':response['question_variants'],'pack_version':response['pack_version'],
                                      'result_role':'exploratory product category; not cross-form norms'},
            'question_count':len(state['selected']),'response':response,
            'fingerprint':hashlib.sha256(json.dumps(response,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),
            'scope_note':c['personality_portraits']['scope_note']}
    v04.verify(result)
    return {'complete':True,'response':response,'report':result}
