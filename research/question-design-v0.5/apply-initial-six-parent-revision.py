"""Explicit editorial corrections after root read all 172 frozen variants.

This one-time migration contains handwritten edits, never generates game prose.
The source hashes prevent replay against a later editorial revision.
"""
import ast
import base64
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
draft_path=ROOT/'config/question-packs.v0.5.draft.json'
alt_path=ROOT/'scripts/question_variants_v05.py'
expected={draft_path:'73c2b2bdd9de11d1f04259bd65181ea03ae0390755951c16e70fd41b5cd69ac9',
          alt_path:'7ecb3ac35a2a78b1edda659e989ebe02a0e6d0922ddf623b70f9849524556056'}
raw={p:p.read_bytes() for p in expected}
for p,h in expected.items():assert hashlib.sha256(raw[p]).hexdigest()==h,str(p)
draft=json.loads(raw[draft_path])
spec=importlib.util.spec_from_file_location('initial_alts_for_parent',alt_path)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
alts=deepcopy(module.VARIANTS)
before_draft=deepcopy(draft);before_alts=deepcopy(alts)
entries={}
for p in draft['packs']:
 for q in p['questions']:
  entries[q['id']+'.V1']=q
  for i,v in enumerate(q['alternatives'],1):entries[q['id']+f'.DRAFTALT{i}']=v
  for v in alts[p['id']][q['number']]:entries[q['id']+'.'+v['key']]=v
assert len(entries)==172
edits=[]

def option(identifier,old_signal,label,new_signal=None):
 v=entries[identifier];before=deepcopy(v)
 if 'options' in v:
  targets=[o for o in v['options'] if o['proposed_signal']==old_signal]
  assert len(targets)==1,(identifier,old_signal)
  targets[0]['label']=label
  if new_signal:targets[0]['proposed_signal']=new_signal
 else:
  i=v['signals'].index(old_signal);v['labels'][i]=label
  if new_signal:v['signals'][i]=new_signal
 edits.append({'id':identifier,'old_signal':old_signal,'new_signal':new_signal or old_signal,
               'before':before,'after':deepcopy(v)})

def text(identifier,words):
 v=entries[identifier];before=deepcopy(v);v['text']=words
 edits.append({'id':identifier,'field':'text','before':before,'after':deepcopy(v)})

# An unfamiliar permutation alone is not evidence of inventing play rules.
option('GI02.V1','play_inventor','给这小场定每名角色只准出手一次、必须切到下一名后才许继续攻击的规则，实际试轮流限制的打法')
option('GI02.CORE','play_inventor','规定这小场每名现有角色出手一次就必须切人，不许一人连续进攻，实际试这种轮流限制')
option('GI05.V1','play_inventor','自定这场禁用普攻、只许已有角色战技与躲避的规则，实际试出限制后的打法')
option('GI05.CORE','play_inventor','规定这小场不用普攻、只许已有角色战技和躲避，亲自试这种限制怎样改变战斗')
option('GI09.DRAFTALT1','cozy_resident','当时仍有精力，各自在自己的世界重走熟悉安全小路，边随意聊边享受已有环境带来的安定')

# League variants share a mode-independent rule only where that action exists.
option('LOL01.CORE','play_inventor','在可自由尝试的这一段，自定只许普攻和移动、不准主动技能的限制，亲自试它怎样改变这波处理')
option('LOL02.V1','play_inventor','给眼前练习定只用普攻与移动、禁用主动技能的限制，试这名英雄在限制下会怎样打')
option('LOL02.ARAM','play_inventor','在这段允许自由尝试的自定义大乱斗里，自定只用普攻和移动、不准主动技能的限制，实际试本局英雄')
text('LOL02.ARAM','当前在可自由尝试的普通大乱斗自定义局，英雄已经确定，自己仍在出发前商店，能看技能说明并购买可负担装备。现在先做什么？')
option('LOL02.CORE','play_inventor','给眼前练习定每次普攻后必须先横移一次、才许下次攻击的规则，实际试它改变了哪些距离选择')
option('LOL05.V1','play_inventor','留在当前练习里，规定每次普攻后必须先横移再攻击，亲自试自己加的新限制')
text('LOL05.ARAM','当前在真人熟人同意自由尝试的普通大乱斗自定义局，英雄已经确定，自己仍在开局准备位置，能查看说明或交流。先做什么？')
option('LOL05.ARAM','play_inventor','在这段自由尝试里规定只用普攻与移动、禁用主动技能，亲自试本局英雄在限制下的打法')
option('LOL05.CORE','play_inventor','规定这段练习每次普攻后必须先横移、不能站定连打，试自己新增限制带来的变化')
option('LOL06.CORE','play_inventor','在允许自由试用的这段，规定只用普攻与移动处理兵线、不准主动技能，实际试限制后的处理')
text('LOL06.CORE','不要求真人队友或真人对手。当前在允许自由尝试的练习或自定义场合，一波兵线到眼前，自己的技能与装备可用。先做什么？')
text('LOL07.V1','当前在允许自由试用的峡谷自定义或练习里，已经回到商店，金币足够在几件熟悉装备中选择，英雄技能也已了解。先怎样选并使用？')
option('LOL07.V1','play_inventor','给接下来这段定每次普攻后先横移、再许下一次进攻的规则，按这限制选可负担装备并出发实际试用')
text('LOL07.ARAM','当前在真人同伴同意自由试用的普通大乱斗自定义局，刚在出生处获得购买机会，金币能买几件熟悉装备，尚未离开商店。先怎样选？')
option('LOL07.ARAM','play_inventor','为接下来一段定只许普攻与移动、不准主动技能的限制，按这规则选择可买装备，再出发实际试用')
text('LOL07.CORE','当前在允许自由试用的练习或自定义场合，已获得本模式允许的购买机会，金币能买几件熟悉装备；不要求真人对手。先怎样选并试用？')
option('LOL07.CORE','play_inventor','为这段定每次普攻后先横移、不许站定连打的规则，按这限制选可用装备并实际试一段')
option('LOL08.CORE','play_inventor','给当前练习定每次普攻后必须先横移、不能站定连打的规则，实际试这个新限制')
option('LOL09.V1','play_inventor','在双方同意自由尝试的自定义局里，两人约好一小段都不使用主动技能，只靠普攻与移动，实际试出了新打法')
option('LOL09.ARAM','play_inventor','在双方同意自由尝试的自定义大乱斗里，两人用已确定英雄约好只许普攻与移动、禁用主动技能，并实际试过一段')
option('LOL09.CORE','play_inventor','在允许自由试用的场合，给自己定每次普攻后先横移、不能站定连打的规则，并亲自试过一段')
option('LOL10.CORE','play_inventor','在可自由尝试的场合规定一小段只准普攻和移动、不准主动技能，并实际试过限制下的交火')
option('LOL11.V1','play_inventor','在允许自由试用的场合，给熟悉英雄定一段只许普攻与移动、禁用主动技能的规则，并亲自试出了限制后的处理')
option('LOL11.ARAM','play_inventor','在允许自由尝试的自定义大乱斗里，规定这段只用普攻与移动、不用主动技能，并用当局英雄真正实行')
option('LOL11.CORE','play_inventor','在允许自由试用的场合，规定每次普攻后先横移、不能站定连打，并用熟悉英雄亲自试过一段')
option('LOL12.V1','play_inventor','在允许自由尝试的自定义局里，为一小段设只许普攻与移动、不准主动技能的限制，并真正试过其变化')
option('LOL12.ARAM','play_inventor','在允许自由尝试的自定义大乱斗里，用已确定英雄实行只许普攻与移动、不准主动技能的限制，亲自试过一段')
option('LOL12.CORE','play_inventor','在允许自由试用的场合给自己定每次普攻后先横移、不能站定连打的规则，并实际试出限制后的变化')

# Merely explaining a past loadout is different from actually composing one.
option('LOL03.V1','build_alchemist','根据刚才技能与装备的相互作用，选出现有可用的一组互补，再到可练习场合亲手试一小段')
option('LOL03.ARAM','build_alchemist','从刚才技能与装备的关系中选一组现有可用配合，再到手边可练习场合亲手试它的相互作用')
option('LOL03.CORE','build_alchemist','根据当时技能与装备的关系重新选一组现有可用配合，并在随后能练习的场合亲手验证互补')

# A different entry direction remains a scoped route choice, not play invention.
option('CS201.BASIC','play_inventor','给这段练习定每次开火后必须退回起手掩体、重新出身位才能再开火的规则，亲自试这种限制的变化')
option('CS202.V1','play_inventor','从另一条当前可达支路接近这个点，试一次自己较少用的进入方向','route_choice')
option('CS202.CORE','play_inventor','改从另一条当前可达通路进入，试一次自己较少用的接近方向','route_choice')
option('CS202.BASIC','play_inventor','改沿通道另一侧接近，试一次自己较少用的进入方向','route_choice')
option('CS203.BASIC','play_inventor','规定这一小段每次开火后必须回到起手遮挡，再许下次开火，亲自试新增限制后的节奏')
option('CS204.V1','play_inventor','用枪火暂时扰动眼前烟雾，再换站位对照可见区域，验证烟雾与视线怎样变化','puzzle_breaker')
option('CS204.CORE','play_inventor','从另一条当前可达路线经过转角，试一次平时较少用的进入方向','route_choice')
option('CS204.BASIC','play_inventor','从当前可达的另一侧绕入，试一次平时较少用的进入方向','route_choice')
option('CS205.CORE','play_inventor','给这段交火定只能在自己选定的两处可达位置开火、其他地方禁射的规则，实际试这种限制')
option('CS205.BASIC','play_inventor','给这段练习圈定两处当前可达位置，规定只能在这两处开火，亲自试新增限制后的变化')
option('CS207.CORE','play_inventor','给自己定这小段只许蹲姿开火、站立时禁射的规则，用手中可用枪实际试这种限制')
option('CS207.BASIC','play_inventor','规定这段只准蹲姿开火、站立时不能射击，用本次可用枪试自己加的新限制')
option('CS208.V1','play_inventor','改走一条当前可达但自己较少用的进点路线，实际试这次接近方式','route_choice')
option('CS208.CORE','play_inventor','从当前可达的另一侧接近交火，实际试一次较少用的进入方向','route_choice')
option('CS208.BASIC','play_inventor','改从眼前转角另一条可达路线经过，实际试一次较少用的进入方向','route_choice')
option('CS210.CORE','play_inventor','给自己定过一小段只准蹲姿开火、站立时禁射的规则，并亲自试出了限制后的变化')
option('CS210.BASIC','play_inventor','规定过一小段只能在自己圈定的两处可达位置开火，并实际试过限制怎样改变这段交火')
option('CS211.V1','play_inventor','给自己定过一小段每次开火后必须换到另一处可达遮挡、不能留原位连打的规则，并在当时实际试过')
option('CS211.CORE','play_inventor','给自己定过这小段只准蹲姿开火、站立时禁射的规则，并用当时枪械真正试过')
option('CS211.BASIC','play_inventor','给自己定过只能在选定两处可达位置开火的短段规则，并在当时亲自实行')
option('CS212.BASIC','play_inventor','自定过一小段只准蹲姿开火、站立时禁射的规则，并真正按这项限制试过')

# A solo practice itinerary is evidence of this practice workflow only.
option('CS203.CORE','systems_builder','把想练的路段、观察点和动作排成几个接得上的步骤，再按这个安排出发','practice_route_plan')
option('CS203.BASIC','systems_builder','先排清要走的路段、观察点与练习动作，再按这个安排开始','practice_route_plan')
option('CS206.CORE','systems_builder','把下一段要走的路、停的位置和练习动作排成顺序，再照安排开始','practice_route_plan')
option('CS206.BASIC','systems_builder','把接下来路段、观察点和练习动作排好先后，再照安排尝试','practice_route_plan')
option('CS210.CORE','systems_builder','把当时要走的路段、观察点和动作排清先后，并按这套练习安排实际完成','practice_route_plan')
option('CS210.BASIC','systems_builder','把路段、观察点与练习动作先排成步骤，再按这套练习安排实际完成','practice_route_plan')
option('CS212.CORE','systems_builder','把地图路段、观察点与练习动作排清先后，并按这套练习安排实际完成','practice_route_plan')
option('CS212.BASIC','systems_builder','把地图路段、观察点与动作先排成步骤，并按这套练习安排实际实行','practice_route_plan')

# Recording an already owned item/known place is not acquiring a collection gap.
option('CS209.V1','collector','对照自己的外观记录清单，补记已有但尚未记录的物品与截图','game_recording')
option('CS209.CORE','collector','对照自己的枪械与地点记录清单，补拍已经体验但未留记录的内容','game_recording')
option('CS209.SOLO','collector','对照自己的枪械和地点记录清单，补拍已经体验但尚未留图的内容','game_recording')
option('ER03.V1','collector','把这件新取得兵器的名称、说明与当前外观补进自己的旅途记录','game_recording')
option('ER03.CORE','collector','把已找到但还没记下的兵器名称、说明与当前外观补进自己的旅途记录','game_recording')
option('ER08.V1','collector','把当前已经听到的人物信息或已取得物品补进自己的旅途记录','game_recording')
option('ER08.CORE','collector','把已经听过的人物信息或已取得物品补进自己的旅途记录','game_recording')
option('ER11.V1','collector','把当时已经取得的装备名称、说明与自己的搭配补进旅途记录','game_recording')
option('SV11.CORE','collector','对照自己的作物或采集物收藏清单，亲自取回当时尚未收齐的实物，补入自己的收藏箱')
option('SV10.V1','play_inventor','共同约好这一天禁用商店买种，只用当时现有种子与可采材料，并实际试过这条新种植规则')
option('SV10.CORE','play_inventor','自定这一天不买种子、只用现有种子与可采材料的限制，并在那天真正试过它改变的安排')
option('ER07.V1','play_inventor','选一只已有且会主动进攻的骨灰，规定自己必须等它先出手才许进攻，实际试这种限制下的配合')

# Do not force invention points into ordinary BG3 choices and rule inspection.
option('BG302.CORE','play_inventor','离开当前交涉，走进旁边尚未去过的可达入口，亲眼看看另一处未知空间','wanderer')
option('BG303.V1','play_inventor','对照升级说明、现有职业资源与当前装备，先弄懂一项能力的触发条件，再确认当前合法选项','puzzle_breaker')
option('BG303.CORE','play_inventor','选一处自己仍不熟的移动到遮挡后再出手，在眼前这场逐回合亲手练到更可控','practice_seeker')
option('BG305.V1','play_inventor','规定这场自己每次攻击后都必须换到另一处可达落点、下回合不能在原处继续出手，实际试限制后的战斗')
option('BG305.CORE','play_inventor','给这场加每次攻击后必须换到另一处可达落点、下回合不能留原处出手的规则，亲自试这种限制')
option('BG307.V1','play_inventor','对照当前可选能力的消耗、恢复与触发条件，弄懂一项规则后再确认合法配置','puzzle_breaker')
option('BG307.CORE','play_inventor','对照当前目标高度、视线和能力范围，选当前合法动作验证一次遮挡或落点关系','puzzle_breaker')
option('BG308.V1','play_inventor','离开这段交谈，走向旁边已确认能够继续当前去向的入口，实际换条推进路径','seek_other_route')
option('BG308.CORE','play_inventor','先结束眼前交谈，走向旁边已确认可继续当前去向的入口，实际换条推进路径','seek_other_route')
option('BG310.V1','play_inventor','在双方都同意的可行一段里，约好禁用直接武器攻击、只用当时合法投掷或环境互动，并真正试过这项限制')
option('BG310.CORE','play_inventor','自己投掷、跳跃或推移物件时，环境与画面立刻回应操作，当时享受的就是这段直接反馈','feedback_engine')
option('BG312.V1','play_inventor','给一段当时可行的交手定不准直接武器攻击、只用已有可投掷物与环境互动的限制，并真正试过')
option('BG312.CORE','play_inventor','给一段当时可行的交手定只用已有可投掷物、不做直接武器攻击的限制，并真正按规则尝试过')

def shared_raw(words):
 start=words.index('"shared_questions"');start=words.index(':',start)+1
 while words[start].isspace():start+=1
 _,n=json.JSONDecoder().raw_decode(words[start:]);return start,start+n,words[start:start+n]
old_shared=shared_raw(raw[draft_path].decode('utf-8'))[2]
draft_words=json.dumps(draft,ensure_ascii=False,indent=2)+'\n'
a,b,_=shared_raw(draft_words);draft_words=draft_words[:a]+old_shared+draft_words[b:]
assert json.loads(draft_words)['shared_questions']==before_draft['shared_questions']
assert shared_raw(draft_words)[2]==old_shared
draft_path.write_text(draft_words,encoding='utf-8')

old_text=raw[alt_path].decode('utf-8')
prefix=old_text[:old_text.index('# Genshin:')]
lines=[prefix.rstrip(),'','']
for group,numbered in alts.items():
 for n,items in numbered.items():
  for v in items:
   fields=[repr(group),str(n),repr(v['text']),repr(v['labels']),repr(' '.join(v['signals']))]
   if v['key']!='CORE':fields.append('key='+repr(v['key']))
   if v['modes']:fields.append('modes='+repr(tuple(v['modes'])))
   fields.append('note='+repr(v['note']))
   lines.append('add('+', '.join(fields)+')')
alt_words='\n'.join(lines)+'\n';ast.parse(alt_words)
alt_path.write_text(alt_words,encoding='utf-8')

report={'status':'parent_editorial_revision_completed_pending_uniform_runtime_build',
 'reviewed_by':'root','checked_at':'2026-10-30','independent_full_variants_read':172,
 'before_files':{str(p.relative_to(ROOT)):{'sha256':hashlib.sha256(raw[p]).hexdigest(),'bytes_base64':base64.b64encode(raw[p]).decode()} for p in raw},
 'after_files':{str(p.relative_to(ROOT)):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in raw},
 'before_draft':before_draft,'after_draft':draft,'before_alternatives':before_alts,'after_alternatives':alts,
 'explicit_edits':edits,'edit_operations':len(edits),'edited_variants':len({e['id'] for e in edits}),
 'shared_raw_preserved':True,'shared_value_sha256':hashlib.sha256(old_shared.encode()).hexdigest(),
 'new_behavior_signals':['route_choice','practice_route_plan','game_recording'],
 'reasoning':['普通改次序、换路径或技能分组不自动计创造玩法；保留i者明确玩家新增限制。',
  '个人枪法练习路线不硬推经营系统；已知物品补记不硬推收藏。',
  'LoL自定规则限定为允许自由尝试的练习/自定义场合，避免把正常比赛临时限制当普遍建议。',
  'BG3普通检视规则、选择旁路与练习分别用p、行为证据和t，不硬凑i。'],
 'player_trial_performed':False,'runtime_built':False}
(ROOT/'research/question-design-v0.5/initial-six-parent-editorial-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'operations':len(edits),'variants_edited':report['edited_variants'],'shared_raw_preserved':True,'sha':report['after_files']},ensure_ascii=False))
