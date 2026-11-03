"""Deterministic four-choice local instrument. No runtime generative model."""
from collections import Counter
from copy import deepcopy
from functools import lru_cache
import hashlib
import json
from pathlib import Path

from .engine import InputError

ROOT=Path(__file__).resolve().parents[1]


@lru_cache(maxsize=1)
def config():
    return json.loads((ROOT/'config/youge.v0.4.0.json').read_text(encoding='utf-8'))


@lru_cache(maxsize=1)
def _catalog_snapshot(modified_ns):
    return json.loads((ROOT/'config/games.v0.5.0.json').read_text(encoding='utf-8'))


def catalog():
    path=ROOT/'config/games.v0.5.0.json'
    return _catalog_snapshot(path.stat().st_mtime_ns)


def find_game(game_id):
    game=next((g for g in catalog()['games'] if g['id']==game_id),None)
    # Keep saved v0.4 responses readable while unverified names leave the public picker.
    if game is None and game_id in catalog().get('legacy_game_ids',[]):
        game=next((g for g in catalog().get('candidates',[]) if g['id']==game_id),None)
    if not game:raise InputError('这款作品尚未收录，请选择库内确实玩过并喜欢的作品。')
    return game


def questionnaire(game_id):
    game=find_game(game_id);c=config()
    source=c['packs'].get(game.get('question_pack')) or c['families'][game['mechanic_family']]
    items=deepcopy(source+c['common'])
    overrides=c.get('anchor_context',{}).get(game.get('question_pack'),{})
    for i,item in enumerate(items):
        if item['id'] in overrides:
            item['text'],labels=overrides[item['id']]
            for option,label in zip(item['options'],labels):option['label']=option['report']=label
        item['text']=item['text'].format(game=game['title'])
        item['order']=i+1
    return items


def public_question(item):
    return {k:deepcopy(item[k]) for k in ('id','text','scope','order') if k in item}|{'options':[{'id':o['id'],'label':o['label']} for o in item['options']]}


def bootstrap():
    c=config();lib=catalog()
    people=[]
    for p in c['personas']:
        copy={k:p[k] for k in ('id','name','central_pull','game_personality','portrait')}
        copy['personality_profile']=deepcopy(c['personality_portraits']['personas'][p['id']])
        copy['game_personality']=copy['personality_profile']['headline']
        people.append(copy)
    public_fields=('id','title','original_title','aliases','category_ids','platforms','version_type','version_label','work_id','work_title','name_status','related_games')
    public=lambda game:{key:deepcopy(game[key]) for key in public_fields if key in game}
    archived=[public(game) for game in lib.get('candidates',[]) if game['id'] in lib.get('legacy_game_ids',[])]
    return {'versions':c['versions'],'catalogue_release':lib['version'],'reference':c['reference'],'personas':people,'categories':lib['categories'],'games':[public(game) for game in lib['games']],'archived_games':archived,'featured':lib['featured'],'rules':{'base_count':16,'max_extra':2,'compatible_report_versions':c.get('compatible_report_versions',[c['versions']['report_rules']]),'report_only_question_ids':[q['id'] for q in c['common'] if all(not o['weights'] for o in q['options'])]}}


def normalize(raw):
    if not isinstance(raw,dict):raise InputError('需要一份有效的游格答卷。')
    current=config()['versions']
    compatible=[current|{'report_rules':version} for version in config().get('compatible_report_versions',[current['report_rules']])]
    if raw.get('versions') not in compatible:raise InputError('答卷与新版题库版本不同，请使用对应版本查看。')
    if not isinstance(raw.get('game_id'),str):raise InputError('请先选择一款作品。')
    find_game(raw['game_id'])
    answers=raw.get('answers',{})
    extra=raw.get('extra_answers',[])
    if not isinstance(answers,dict) or not isinstance(extra,list) or len(extra)>2:raise InputError('只接受单选四选一答卷，补问最多两题。')
    ids={q['id'] for q in questionnaire(raw['game_id'])}
    if set(answers)-ids:raise InputError('答卷含有不属于当前题包的问题。')
    if any(not isinstance(a,str) or a not in ('A','B','C','D') for a in answers.values()):raise InputError('每题请选择A、B、C、D中的一个答案。')
    for e in extra:
        if not isinstance(e,dict) or set(e)!={'question_id','answer'} or not isinstance(e['question_id'],str) or e['answer'] not in ('A','B','C','D'):raise InputError('补问答案不完整。')
    name=raw.get('display_name','玩家')
    if not isinstance(name,str) or len(name)>24:raise InputError('档案名字请控制在24个字以内。')
    rid=raw.get('respondent_id','local-player')
    if not isinstance(rid,str) or len(rid)>100:raise InputError('答卷标识不正确。')
    return {'versions':deepcopy(config()['versions']),'respondent_id':rid,'display_name':name.strip() or '玩家','game_id':raw['game_id'],'answers':deepcopy(answers),'extra_answers':deepcopy(extra),'fictional':raw.get('fictional') is True}


def rank(points,anchor_counts,last_choice=None):
    order={p['id']:p['order'] for p in config()['personas']}
    return sorted(order,key=lambda p:(-points[p],-anchor_counts[p],-(p==last_choice),order[p]))


def tie_question(candidates,index):
    digest=hashlib.sha256('|'.join(candidates).encode()).hexdigest()[:10]
    return {'id':f'T{index+1:02d}.{digest}','text':['放眼你玩过的游戏，现在更想把时间留给哪件事？','再做一个取舍，你更想接着体验哪件事？'][index],'scope':'cross','order':17+index,'options':[{'id':chr(65+i),'label':config()['tie_actions'][p][index],'weights':{p:config()['rules']['tie_bonus']},'habit':None,'report':config()['tie_actions'][p][index]} for i,p in enumerate(candidates)]}


def score(raw):
    response=normalize(raw);items=questionnaire(response['game_id'])
    if len(response['answers'])!=16:raise InputError('请先完成16道正式题目。')
    points=Counter({p['id']:0 for p in config()['personas']});anchor=Counter();registry={};selected=[];habits={}
    def apply(item,answer):
        option=next(o for o in item['options'] if o['id']==answer)
        points.update(option['weights'])
        if item['scope']=='anchor':anchor.update({p:1 for p,w in option['weights'].items() if w>0})
        ref='answer:'+item['id']
        registry[ref]={'question_id':item['id'],'question':item['text'],'answer':answer,'label':option['label'],'scope':item['scope'],'weights':deepcopy(option['weights'])}
        selected.append((item,option,ref))
        if option.get('habit'):habits[item['topic']]=option['habit']
        return next(iter(option['weights']),None)
    for item in items:apply(item,response['answers'][item['id']])
    trace=[];last=None
    for index in range(2):
        ordered=rank(points,anchor,last)
        close=points[ordered[0]]-points[ordered[1]]<=config()['rules']['close_gap_points']
        if not close:
            if len(response['extra_answers'])>index:raise InputError('补问与当前答案不匹配，请重新生成。')
            break
        item=tie_question(ordered[:4],index)
        if len(response['extra_answers'])<=index:
            return {'complete':False,'next_question':public_question(item),'answered':16+index,'response':response}
        saved=response['extra_answers'][index]
        if saved['question_id']!=item['id']:raise InputError('前面的答案已经变化，请重新回答补问。')
        before=deepcopy(dict(points));last=apply(item,saved['answer']);items.append(item)
        trace.append({'question_id':item['id'],'candidate_ids':ordered[:4],'choice':saved['answer'],'points_before':before,'bonus':config()['rules']['tie_bonus']})
    ordered=rank(points,anchor,last)
    return {'complete':True,'response':response,'points':dict(points),'anchor_counts':dict(anchor),'ordered':ordered,'evidence':registry,'selected':selected,'habits':habits,'tie_trace':trace,'items':items}


ADVICE=config()['report_copy']['advice']


def personality_sections(persona_id,habits):
    """Original archetype essay plus a concise, answer-specific relationship paragraph."""
    c=config();source=c['personality_portraits'];p=deepcopy(source['personas'][persona_id])
    core=list(p['inner_world']);relations=list(p['with_others'])
    guide={'guide_mechanics':'交流玩法时，你愿意借资料弄清机制和规则','guide_completion':'交流玩法时，你会关心遗漏的位置和想补齐的内容','guide_hint':'遇到卡点，你希望先得到提示，再留一点自己想通的空间','guide_independent':'遇到新内容，你通常希望先给自己留出摸索的空间'}[habits['guide']]
    spoiler={'spoiler_hint':'具体结果和完整解法，先保留到你愿意知道的时候','spoiler_rules':'通用规则可以讲清，尚未体验的具体内容先留给自己','spoiler_open':'你也接受把未体验的内容或解法直接讲清，再亲自去感受','spoiler_ask':'提前讲到哪里，最好先确认你的进度和这次的意愿'}[habits['spoiler']]
    failure={'failure_retry':'受挫后想继续尝试时，可以先约好这一段投入到什么时候','failure_adjust':'受挫后想先调整做法时，可以请同伴留一点重新准备的时间','failure_switch':'受挫后想换些内容时，提前留一个大家都接受的替代安排会更舒服','failure_pause':'受挫后想先停下来时，约好下次从哪里接着来，会更容易放松离开'}[habits['failure']]
    relations.append(guide+'；'+spoiler+'。'+failure+'。')
    practical=[]
    if habits['replay']=='replay_time_limited':practical.append('你有重温的兴趣，安排时仍需要为现实时间留位置')
    elif habits['replay']=='replay_new_first':practical.append('新的作品更能吸引你，约共同时间时可以先从新体验谈起')
    if habits['mod']=='mod_limited':practical.append('Mod的使用受平台、版本或安装条件限制，同游前先确认可行性即可')
    elif habits['mod']=='mod_original':practical.append('你更想保留原版体验，共同内容和版本可以提前约好')
    if practical:relations.append('；'.join(practical)+'。')
    sections=[{'id':'character','title':source['sections'][0],'paragraphs':core,'kind':'original_archetype_interpretation'},{'id':'relations','title':source['sections'][1],'paragraphs':relations,'kind':'archetype_and_explicit_habits'}]
    return p,sections


def report(raw):
    state=score(raw)
    if not state['complete']:return state
    c=config();response=state['response'];game=find_game(response['game_id']);personas={p['id']:p for p in c['personas']};winner=state['ordered'][0]
    persona=deepcopy(personas[winner]);selected=state['selected'];evidence=state['evidence']
    def claim(rule,text,refs,scope='gaming',condition=None):
        return {'rule_id':rule,'rule_version':c['versions']['report_rules'],'text':text,'evidence_refs':refs,'scope':scope,'condition_snapshot':condition or {'selected_answers':{evidence[r]['question_id']:evidence[r]['answer'] for r in refs}}}
    supporting=[(i,o,r) for i,o,r in selected if winner in o['weights']]
    primary_refs=[r for i,o,r in supporting[:3]]
    # Every leading-persona claim has actual answer support, including a discriminator when needed.
    if not primary_refs:raise InputError('画像没有对应答案依据。')
    primary_text=c['report_copy']['persona_details'][winner] if len(primary_refs)>=2 else c['report_copy']['single_evidence_prefix']+evidence[primary_refs[0]]['label']+'。这是本次称号采用的一条具体线索。'
    primary=claim('P_PRIMARY',primary_text,primary_refs,scope='gaming' if len(primary_refs)>=2 else 'specific_scenario',condition={'persona_id':winner,'points':state['points'][winner],'support_count':len(supporting)})
    insights=[primary]
    second=next((p for p in state['ordered'][1:] if state['points'][p]>0),None)
    if second:
        refs=[r for i,o,r in selected if second in o['weights']][:2]
        detail=c['report_copy']['persona_details'][second] if len(refs)>=2 else c['report_copy']['single_evidence_prefix']+evidence[refs[0]]['label']+'。这条记录保留了称号之外的一处玩法细节。'
        insights.append(claim('P_SECOND_DETAIL',detail,refs,scope='gaming' if len(refs)>=2 else 'specific_scenario'))
    guide=state['habits']['guide'];replay=state['habits']['replay'];mod=state['habits']['mod']
    focus='replay' if replay=='replay_time_limited' else 'guide'
    refs=[r for i,o,r in selected if i.get('topic')==focus]
    insights.append(claim('H_DETAIL',ADVICE[focus][state['habits'][focus]],refs,scope='specific_habit'))
    attraction_rows=[(i,o,r) for i,o,r in selected if i['id'] in ('G01','G02','G03','G04')]
    attractions=[claim('GAME_ATTRACTION',o['report'],[r],scope='this_game') for i,o,r in attraction_rows]
    cross=[(i,o,r) for i,o,r in selected if i['scope']=='cross' and i['id'].startswith('X')]
    repeated=[]
    for p in state['ordered']:
        ar=[r for i,o,r in attraction_rows if p in o['weights']];cr=[r for i,o,r in cross if p in o['weights']]
        if ar and cr:repeated.append(claim('CROSS_ECHO',f'在本命作品和跨游戏选择中，你都选到了“{personas[p]["central_pull"]}”相关体验。',ar[:1]+cr[:1]))
    advice=[]
    for topic,data in ADVICE.items():
        value=response['answers'].get('X14') if topic=='coop' else state['habits'].get(topic)
        refs=[r for i,o,r in selected if i.get('topic')==topic]
        advice.append({'topic':topic,'title':data['title'],**claim('ADVICE_'+topic.upper(),data[value],refs,scope='specific_habit')})
    drains=[]
    if state['habits']['spoiler'] in ('spoiler_hint','spoiler_rules'):
        refs=[r for i,o,r in selected if i.get('topic')=='spoiler']
        drains.append(claim('D_SPOILER','你明确希望保留尚未体验的具体内容或解法。未经确认就直接揭晓，会越过这次表达的边界。',refs,'specific_habit'))
    if replay=='replay_new_first':
        drains.append(claim('D_REPLAY','你把新作品放在重温之前。同游安排若默认反复体验旧流程，需要先与你确认。',['answer:G09'],'specific_habit'))
    tags=[{'text':{'guide_mechanics':'攻略看机制','guide_completion':'攻略补遗漏','guide_hint':'要提示留解法','guide_independent':'先自己摸索'}[guide],'evidence_refs':['answer:G07']},{'text':{'replay_willing':'愿意重温','replay_time_limited':'想重玩但缺时间','replay_new_first':'新作品优先','replay_not_yet':'二刷暂未到阶段'}[replay],'evidence_refs':['answer:G09']},{'text':{'mod_use':'有条件会用Mod','mod_original':'原版体验优先','mod_limited':'Mod条件受限','mod_unknown':'Mod尚未接触'}[mod],'evidence_refs':['answer:G10']}]
    audit={'points':state['points'],'anchor_support_count':state['anchor_counts'],'rank':state['ordered'],'tie_trace':state['tie_trace'],'tie_rule':c['rules']['tie_order'],'result_role':'single product category, not an accuracy estimate'}
    fingerprint=hashlib.sha256(json.dumps(response,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    profile,sections=personality_sections(winner,state['habits'])
    result={'versions':deepcopy(c['versions']),'fictional':response['fictional'],'display_name':response['display_name'],'persona':persona,'game':{k:game[k] for k in ('id','title','original_title','category_ids')},'one_line':profile['headline'],'personality_profile':profile,'report_sections':sections,'insights':insights,'attractions':attractions,'cross_echo':repeated[:2],'behavior_tags':tags,'advice':advice,'drains':drains,'evidence':evidence,'audit':audit,'question_count':len(selected),'response':response,'fingerprint':fingerprint,'scope_note':c['personality_portraits']['scope_note']}
    verify(result)
    return {'complete':True,'response':response,'report':result}


def verify(result):
    claims=result['insights']+result['attractions']+result['cross_echo']+result['advice']+result['drains']+result['behavior_tags']
    for item in claims:
        if not item['evidence_refs'] or any(r not in result['evidence'] for r in item['evidence_refs']):raise InputError('报告缺少对应的实际答案。')
    assert len(result['persona']['id'])>0
    return True


def compare(left,right):
    l=report(left);r=report(right)
    if not l['complete'] or not r['complete']:raise InputError('请先完成两份答卷的补问。')
    a,b=l['report'],r['report'];rows=[]
    for la,ra in zip(a['advice'],b['advice']):
        av=[a['evidence'][ref]['answer'] for ref in la['evidence_refs']];bv=[b['evidence'][ref]['answer'] for ref in ra['evidence_refs']]
        rows.append({'topic':la['topic'],'title':la['title'],'status':'已有共同选择' if av==bv else '需要协调','left':la,'right':ra})
    same=a['game']['id']==b['game']['id']
    return {'versions':deepcopy(config()['versions']),'contains_fictional':a['fictional'] or b['fictional'],'left':a,'right':b,'same_game':same,'common_game':a['game'] if same else None,'coordination':rows,'note':'一款本命作品的对照，不代表完整游戏口味清单。不同选择是协商线索，不换算契合度。'}


def demo(case='A'):
    games=catalog()['featured'];targets={'A':('systems_builder',games[0]),'B':('wanderer',games[0]),'C':('wanderer',games[1])}
    if case not in targets:raise InputError('没有这份示例。')
    target,gid=targets[case];items=questionnaire(gid)
    raw={'versions':deepcopy(config()['versions']),'respondent_id':'fictional-v04-'+case,'display_name':'虚构示例'+case,'game_id':gid,'answers':{},'extra_answers':[],'fictional':True}
    for i in items:
        best=max(i['options'],key=lambda o:o['weights'].get(target,0))
        raw['answers'][i['id']]=best['id']
    if case=='C':
        raw['answers']['G09']='B'
        raw['answers']['G10']='C'
    for _ in range(3):
        state=report(raw)
        if state['complete']:return state
        tie=state['next_question']
        # Public option text is deterministic and uniquely identifies each candidate's action.
        preferred=config()['tie_actions'][target][len(raw['extra_answers'])]
        selected=next((o for o in tie['options'] if o['label']==preferred),tie['options'][0])
        raw['extra_answers'].append({'question_id':tie['id'],'answer':selected['id']})
    raise InputError('示例未能完成。')
