"""One-time edits from a complete independent reading of the 144 scenes."""
from pathlib import Path
from collections import Counter
import ast
import hashlib
import importlib
import json
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from question_authoring import SIGNALS,validate
from build_question_packs_v05 import BEHAVIORS
from youge import v04

# Every choice below was read in its complete scene.  These are editorial
# decisions, not rules for manufacturing prose for other games.
CHOICES={}
def change(identifier,old_signal,label,new_signal=None):
    assert (identifier,old_signal) not in CHOICES
    CHOICES[identifier,old_signal]=(label,new_signal or old_signal)

for identifier,signal in {
 'MIRCATV503.V1':'mission_preparation_plan',
 'MIRCATV504.V1':'combat_resource_cycle',
 'MIRCATV506.V1':'platform_route_plan',
 'MIRCATV510.V1':'mission_preparation_plan',
 'CUPBASEV502.V1':'combat_resource_cycle',
 'CUPBASEV503.V1':'mission_preparation_plan',
 'CUPBASEV509.V1':'mission_preparation_plan',
}.items():
    change(identifier,'systems_builder',None,signal)

for identifier,label in {
 'MIRORIGV506.V1':'先从安全平台查看滑索落点和出口附近的连接，再继续已知路线',
 'MIRORIGV506.ALT1':'先在安全边缘查看可通行的平台连接，再走已知出口',
 'MIRORIGV512.V1':'先从安全处查看过滑索落点与屋顶连接，之后才走向已知出口',
 'MIRORIGV512.ALT1':'先查看过附近平台连接，然后才向已知出口走',
 'MIRCATV508.V1':'先步行查看安全屋附近已经可达的屋顶连接，再去原本可直达的目标',
 'MIRCATV508.ALT1':'先查看安全屋外已经可通行的屋顶连接，再去已知目标',
 'MIRCATV512.V1':'先步行查看过安全屋外的屋顶连接，然后才走向原本已知的目标',
 'MIRCATV512.ALT1':'先查看过附近可通行的屋顶连接，再向已知目标走',
}.items():
    change(identifier,'role_player',label,'scene_inspection')

# Replace recurring turn/crouch/empty-swing filler with actual movement or
# route choices.  The few retained constraints concern this game's tools.
RULE_CHOICES={
 'MIRORIGV502.V1':('play_inventor','给这段已确认只借矮物也可通过的路线加上禁用蹬墙的限制，实际按新条件跑到出口'),
 'MIRORIGV502.ALT1':('try_action_variant','换一趟翻过矮墙后接起跳的时点，亲手体验另一种已经会用的衔接'),
 'MIRORIGV503.V1':('play_inventor','这趟自定禁止Skillroll，只走旁边已确认不用翻滚也可安全经过的矮台路线'),
 'MIRORIGV503.ALT1':('try_action_variant','换一趟落地后接小跑和起跳的先后，亲手体验不同动作节奏'),
 'MIRORIGV507.V1':('try_action_variant','这趟换一处已经会用的助跳与抓边接法，亲手体验不同动作怎样串过这条路线'),
 'MIRORIGV507.ALT1':('try_action_variant','换一趟翻过矮障碍后接起跑的时点，亲手体验另一种已有动作接法'),
 'MIRORIGV510.V1':('play_inventor','给当时确认不用蹬墙也可通过的小段加过禁用蹬墙的限制，并实际按它跑过'),
 'MIRORIGV510.ALT1':('try_action_variant','自己换过矮台起跳与落地后转向的衔接，亲手体验过另一种已有动作接法'),
 'MIRORIGV511.V1':('play_inventor','给当时确认不用翻滚也可安全经过的短段加过禁用Skillroll的限制，并实际遵守过'),
 'MIRORIGV511.ALT1':('try_action_variant','自己换过抓边翻上后接下一跳的时点，亲手体验过不同动作节奏'),
 'MIRCATV502.V1':('play_inventor','这趟自定禁用原本可用的Shift，只靠已确认可过的基础跑跳路线继续'),
 'MIRCATV502.ALT1':('try_action_variant','换一次抓边翻上后接起跳的时点，亲手体验不同的已有动作衔接'),
 'MIRCATV504.ALT1':('try_action_variant','换一趟翻过矮台后接起跑与转向的先后，亲手感受不同动作接法'),
 'MIRCATV507.V1':('play_inventor','给这趟Dash新增禁止Shift的限制，只跑已经确认不用它也能到终点的路线'),
 'MIRCATV507.ALT1':('try_action_variant','这趟换一次抓边后接起跑的时点，亲手体验已经会用的动作怎样换着接起来'),
 'MIRCATV510.ALT1':('try_action_variant','自己换过翻上矮台后接跑跳的时点，亲手体验过不同的已有动作衔接'),
 'MIRCATV511.V1':('play_inventor','给当时确认不用Shift也能通过的熟段加过禁用Shift的限制，并实际遵守过'),
 'MIRCATV511.ALT1':('try_action_variant','自己换过基础抓边、翻上与起跑的先后，亲手体验过另一种动作接法'),
 'LITT1V502.V1':('play_inventor','这轮自定不点原本可用的打火机，只借当前已有灯光辨认椅子和门把，再按新限制通过'),
 'LITT1V502.ALT1':('try_action_variant','换一趟爬上箱台后接起跳的时点，亲手体验不同动作接法'),
 'LITT1V508.V1':('try_action_variant','先走一趟眼前可双向回钻的小口，再从熟悉出口离开，体验另一种已有动作的行进顺序'),
 'LITT1V508.ALT1':('try_action_variant','换一次爬上矮台后蹲行、起身与跑动的衔接，亲手体验不同动作节奏'),
 'LITT1V510.V1':('play_inventor','为当时确认已有照明且可安全经过的短段定过不点打火机的限制，并实际遵守过'),
 'LITT1V510.ALT1':('try_action_variant','自己换过爬台后接蹲行与起身的先后，亲手体验过另一种已有动作衔接'),
 'LITT1V512.V1':('try_action_variant','自己改变过钻小口与走向出口的先后，亲手体验过另一趟已有路线的行进过程'),
 'LITT2V501.V1':('try_action_variant','换个当前可达的安全投掷起点，亲手体验松果触发后再跨过的动作接法'),
 'LITT2V501.ALT1':('try_action_variant','换一次推箱后爬上与起跳的衔接，亲手体验另一种已有动作接法'),
 'LITT2V505.ALT1':('try_action_variant','换个已经可达的安全站位投鞋，再亲手体验接着跨过的动作过程'),
 'LITT2V510.V1':('try_action_variant','自己换过投出鞋或松果后接移动的时点，亲手体验过另一种已有动作接法'),
 'LITT2V510.ALT1':('try_action_variant','自己换过推箱、爬上与起跳的衔接，亲手体验过不同动作节奏'),
 'CUPBASEV502.ALT1':('try_action_variant','换一个当前可用的起跳位置，亲手体验另一种跳向粉色物的接法'),
 'CUPBASEV504.ALT1':('play_inventor','对已确认不用冲刺也能通过的短段新增禁止冲刺的限制，只用跳跃和Peashooter实际玩这一段'),
 'CUPBASEV505.V1':('play_inventor','给已确认可躲开的这段新增禁止射击的限制，只用缩放和移动到约定位置，再恢复射击'),
 'CUPBASEV505.ALT1':('try_action_variant','换一趟跳开、冲刺与转身射击的先后，亲手体验已有动作的另一种接法'),
 'CUPBASEV506.ALT1':('try_action_variant','换一次落地后接射击与下一跳的时点，亲手体验不同出手节奏'),
 'CUPBASEV507.ALT1':('try_action_variant','换一个已经可用的起跳点再跳向粉色物，亲手体验不同位置的招架接法'),
 'CUPBASEV510.ALT1':('try_action_variant','自己换过跳落、射击与下一跳的先后，亲手体验过另一种已有动作衔接'),
 'CUPBASEV511.ALT1':('try_action_variant','自己换过躲开来物后转身射击的时点，亲手体验过不同出手节奏'),
 'KZEROV501.V1':('play_inventor','给确认可行的小房新增每次出刀前必须先完成一次翻滚的限制，实际按新规则处理这一房'),
 'KZEROV501.ALT1':('play_inventor','在已确认只靠刀与翻滚也可通过的这房，自定禁止拾取投掷物，按新增限制实际玩一遍'),
 'KZEROV502.ALT1':('try_action_variant','换一次翻滚后接斩击的时点，亲手体验不同的已有动作衔接'),
 'KZEROV505.V1':('mission_preparation_plan','先把三个已开放布景楼层的处理顺序排好，再按自己的行程逐层寻找任务卡'),
 'KZEROV505.ALT1':('try_action_variant','换一次翻滚、转向与出刀的先后，亲手体验另一种已经会用的接法'),
 'KZEROV506.V1':('play_inventor','回到已开且确认不用慢动作也能完成的熟房，自定禁止启用慢动作，再按新限制玩一遍'),
 'KZEROV506.ALT1':('play_inventor','给当前已确认不靠慢动作也可完成的熟房新增禁用慢动作的限制，只靠刀与翻滚实际试一轮'),
 'KZEROV507.ALT1':('try_action_variant','换一次跳斩接翻滚的先后，亲手体验不同的已有动作衔接'),
 'KZEROV509.V1':('play_inventor','给确认可行的熟房定过每次出刀前必须先翻滚的新限制，并真按这条自定规则玩过'),
 'KZEROV509.ALT1':('try_action_variant','自己换过翻滚后接出刀的时点，亲手体验过另一种已有动作接法'),
}
for identifier,(signal,label) in RULE_CHOICES.items():
    change(identifier,'play_inventor',label,signal)

for identifier,label in {
 'MIRORIGV508.V1':'因为喜欢熟悉屋顶的安定脚步与开阔感，先慢走一段，主动享受这会儿不赶目标的时间',
 'MIRORIGV508.ALT1':'先在熟悉安全的宽台慢走一会，享受已经认得的脚步与屋顶氛围',
 'MIRORIGV512.V1':'精力足、没有追逐且主路可走，仍因喜欢熟悉屋顶的安定感，自愿慢行过一段',
 'MIRORIGV512.ALT1':'当时精力充足且前路可走，仍主动慢行过熟悉宽台，享受认得的屋顶氛围',
 'MIRCATV508.V1':'先沿熟悉安全屋和近处小段慢走，享受回到认得路线时的安定感',
 'MIRCATV508.ALT1':'先沿熟悉安全的小段慢走一会，喜欢这些已认得的屋顶和脚步带来的安定感',
 'MIRCATV512.V1':'精力足、无追踪无计时且目标可继续，仍在熟悉安全屋附近慢走过一会，享受回到熟路的安定感',
 'MIRCATV512.ALT1':'精力充足、没被追踪且前路可走，仍主动慢行过熟悉安全小段，因为这段已认得的路线让人安定',
 'LITT1V508.V1':'先在灯已亮、走熟的小房慢行一会，喜欢这处认得的脚步与安定氛围',
 'LITT1V508.ALT1':'先慢走一段已经认得的安全地面，享受熟悉小房里安定的脚步与灯光',
 'LITT1V512.V1':'精力足、无追逐无倒计时且出口可走，仍因喜欢熟悉安全小房的安定感，主动慢行过一会',
 'LITT1V512.ALT1':'精力充足且前路可走，仍自愿慢行过熟悉安全小段，享受已认得的脚步和环境',
 'LITT2V512.V1':'精力足、无追赶无倒计时且出口可走，仍在熟悉安全小房慢行过一会，喜欢回到已认得环境的安定感',
 'LITT2V512.ALT1':'精力充足、前路可走且无追赶，仍自愿慢行过熟悉安全小段，享受认得的脚步和环境',
 'CUPBASEV508.V1':'先沿熟悉岛屿小路慢走一段，享受已经认得的地图音乐与安定路线',
 'CUPBASEV508.ALT1':'先在走熟的第一岛小路慢行片刻，喜欢这段熟悉音乐和路线带来的安定感',
 'CUPBASEV512.V1':'精力足、没有倒计时且关卡可进，仍主动慢行过熟悉地图，享受认得的音乐与安定路线',
 'CUPBASEV512.ALT1':'精力充足、基础关可继续，仍沿熟悉岛屿小路慢走过，喜欢这段已认得的音乐与环境',
 'KZEROV508.V1':'先在熟悉公寓小段慢走一会，享受回到这处认得环境的安定感，暂不坐下结束当天',
 'KZEROV512.V1':'本人精力足、公寓可结束当天且无异常触发，仍自愿慢行过熟悉小段，享受回到认得环境的安定感',
}.items():
    change(identifier,'cozy_resident',label)

change('LITT1V502.V1','puzzle_breaker','先猜椅子离门多远能让自己跃起抓住门把，再移动并跳一次核对')
change('LITT1V510.V1','puzzle_breaker','挪过椅子或箱子的位置，亲自验证了物件摆位与可抓边缘的关系')
change('KZEROV507.V1','practice_seeker','练自己跳斩后落到上层平台的一拍，只看自身动作改善')
for identifier,label in {
 'KZEROV504.V1':'用当前已出现且能收尾的回应结束这段，再回已开放动作房，专练自己翻滚后转身出刀的一拍',
 'KZEROV504.ALT1':'用当前可收尾的回应完成通话，再到随后动作房专练自己翻滚接出刀的一小段',
 'KZEROV511.V1':'用当时可收尾的回应结束问答后，回已开放动作房专练过自己翻滚后转身出刀的一拍',
 'KZEROV511.ALT1':'结束当时已有电话后，在随后动作房专练过自己翻滚接出刀的一小段，只看自身改善',
}.items():
    change(identifier,'practice_seeker',label)

TEXTS={
 'MIRORIGV502.V1':'原版屋顶上有能助跳的矮物和可蹬的墙；你已走通过一条只借矮物的路线，也会助跳后接墙，能从安全平台再试。现在更想怎样跑一遍？',
 'MIRORIGV503.V1':'原版屋顶有一处已会用Skillroll承受的落差，也有不用翻滚就能安全经过的矮台路线；两边都已走通过，当前没有追逐。你现在先做什么？',
 'MIRCATV502.V1':'你在Catalyst熟悉的屋顶转角前，Shift已可用；这一小段也确认不用Shift就能基础跑跳通过，能从宽敞安全地面重新起跑。此刻先怎样试一段？',
 'MIRCATV507.V1':'Catalyst当前这条Dash已开放，也有自己的先前结果可比；眼前选的路线已确认不用Shift也能到终点，红箭头和另一条可行近路都能走。现在先跑哪一轮？',
 'LITT1V502.V1':'Prison里有能拖动的椅子和高处门把，出口关系已经看清；这里已有照明，不点打火机也能辨认物件，当前能从安全地面重新试。你现在先怎么动手？',
}

PURPOSES={
 'MIRORIGV502':'原版助跳和蹬墙的不同已会接法可试用；只有明确禁用原本可用的蹬墙动作才支持自定规则，替代的普通动作变化只记当次行为。',
 'MIRORIGV506':'原版滑索松开后接回屋顶有手册支持；可达连接的查看只记scene_inspection，不由“巡线员”称呼推角色扮演。',
 'MIRORIGV510':'本人动作改善、反馈、关系验证和具体新增禁令分开；普通动作换序只记当次试用，不把实际水平计人格。',
 'MIRORIGV511':'只回顾已开放内容；Speed Run不虚构幽灵，纪录与练习分开，普通动作变化不计自创玩法。',
 'MIRORIGV512':'普通查看平台连接只记现场查看；舒缓要有精力、可推进和对熟悉安定过程的正向投入。',
 'MIRCATV502':'Shift属于Catalyst；明确自禁已可用的Shift才是新增规则，基础动作换序只记当次行为。',
 'MIRCATV503':'实际点数解锁保留能力支持成长；点数、目标与返回菜单的个人次序只记mission_preparation_plan。',
 'MIRCATV504':'Focus是当场交手资源循环，只记combat_resource_cycle，不当长期成长或持续经营；不混原版慢动作与拾枪。',
 'MIRCATV506':'Fragile Delivery的剩余时间、耐久和落脚次序只记platform_route_plan，不因此推持续系统经营；限时过程不记舒缓。',
 'MIRCATV508':'已得文件录音可为叙事重读；普通安全屋外查看只记scene_inspection，舒缓要有精力且正向享受熟悉过程。',
 'MIRCATV510':'实际花点解锁为保留成长；个人XP目标和返菜单次序只记准备，临时Focus与手动熟练不记成长。',
 'MIRCATV511':'仅单人本地计时目标；明确新增禁用Shift才支持规则，普通动作变化只记当次试用，不以实际用时判能力。',
 'MIRCATV512':'查看已可通行屋顶连接只记scene_inspection；舒缓排除被追、限时和疲劳，并要求正向享受熟路。',
 'LITT1V502':'拖椅到门把是原作真实操作；不把椅距说成改变跳跃高度。已有照明的短段明确自禁打火机才支持规则，普通爬跳变化只记当次行为。',
 'LITT1V508':'有精力且出口可走时正向享受熟悉安全小房才支持舒缓；钻小口与出发次序的变化仅记当次试用。',
 'LITT1V510':'回顾真实操作；不把重复次数和解得快慢解释成能力，只有有照明短段的具体自订禁令支持规则。',
 'LITT1V512':'舒缓不是被迫休息，要正向享受已认得环境；普通行进次序变化不计自创玩法。',
 'LITT2V501':'松果触发陷阱、推箱靠近岩壁均有实际流程支持；普通站位与动作变化仅记当次试用。',
 'LITT2V510':'仅回顾已体验过的投掷或基础箱台动作；不同站位与已有动作变化不因此支持自创玩法。',
 'CUPBASEV502':'EX与已取得Super之间的当场卡槽安排仅记combat_resource_cycle；不计持续经营或成长。',
 'CUPBASEV503':'本体两Shot与一Charm确有远近及冲刺互补；真实购买为保留成长，个人预算次序只记准备，明确缺币才计收藏。',
 'CUPBASEV509':'保留成长、实际组件互补、个人购买预算和明确缺币分开；预算只记mission_preparation_plan，不把购买或通关表现判能力。',
 'KZEROV504':'对话等待、打断与局部反馈不直接推品德、身份或练习；练习选项要实际回到可用动作房专练具体衔接。',
 'KZEROV505':'三个电影布景楼层可自选先后；排楼层与取任务卡的个人行程只记准备，不计收藏或自创规则。',
 'KZEROV506':'正常速度录像不支持主动倒带；回已开放房间重玩，具体禁慢动作只在已确认可过熟房，不含必须慢动作的风扇段。',
 'KZEROV507':'Prism Key为真实早期收藏，剑仍需之后实验室；跳斩到高台说落台而非虚构抓边攀爬。',
 'KZEROV511':'不由对话态度推品德、固定身份不计角色扮演；只有实际回到动作房专练才支持练习，不把普通等待选项计作训练。',
}

def main():
    path=ROOT/'scripts/question_batch07_e.py';raw=path.read_bytes()
    expected='b4ce8ec28a2a7e987450dd46360b90660ff7fbda924127bf60999d52b4c0d543'
    assert hashlib.sha256(raw).hexdigest()==expected,'Already revised; do not rerun'
    module=importlib.import_module('question_batch07_e')
    before={v['id']:v for p in module.PACKS for s in p['slots'] for v in s['variants']}
    text_ids={v['text']:k for k,v in before.items()};assert len(text_ids)==144
    report_path=ROOT/'research/question-design-v0.5/batch07-e-parent-review.json'
    report=json.loads(report_path.read_text(encoding='utf8'))
    assert report['before_source_sha256']==expected and report['before_packs']==module.PACKS
    offsets=[0]
    for line in raw.splitlines(keepends=True):offsets.append(offsets[-1]+len(line))
    edits=[];seen=set();text_seen=set();purpose_seen=set()
    def span(n):return offsets[n.lineno-1]+n.col_offset,offsets[n.end_lineno-1]+n.end_col_offset
    def replace(n,value):
        a,b=span(n);edits.append((a,b,repr(value).encode('utf8')))
    for node in ast.walk(ast.parse(raw.decode('utf8'))):
        if not isinstance(node,ast.Call) or not isinstance(node.func,ast.Name) or node.func.id!='Q':continue
        alt=node.args[7];mid=text_ids[ast.literal_eval(node.args[2])];aid=text_ids[ast.literal_eval(alt.elts[0])]
        main_signals=ast.literal_eval(node.args[4]).split()
        alt_signals=ast.literal_eval(alt.elts[2]).split() if len(alt.elts)==3 else list(main_signals)
        signal_changed=False
        for identifier,label_node,tokens,text_node in [(mid,node.args[3],main_signals,node.args[2]),(aid,alt.elts[1],alt_signals,alt.elts[0])]:
            labels=ast.literal_eval(label_node).split('|');changed=False
            for old in list(tokens):
                key=(identifier,SIGNALS.get(old,old))
                if key not in CHOICES:continue
                assert sum(SIGNALS.get(x,x)==key[1] for x in tokens)==1
                index=next(i for i,x in enumerate(tokens) if SIGNALS.get(x,x)==key[1])
                label,signal=CHOICES[key]
                if label is not None:labels[index]=label
                tokens[index]=signal;seen.add(key);changed=True
            if changed:replace(label_node,'|'.join(labels));signal_changed=True
            if identifier in TEXTS:replace(text_node,TEXTS[identifier]);text_seen.add(identifier)
        if signal_changed:
            replace(node.args[4],' '.join(main_signals))
            if len(alt.elts)==3:replace(alt.elts[2],' '.join(alt_signals))
            else:
                a,b=span(alt);edits.append((b-1,b-1,(', '+repr(' '.join(alt_signals))).encode('utf8')))
        slot_id=mid.split('.')[0]
        if slot_id in PURPOSES:replace(node.args[5],PURPOSES[slot_id]);purpose_seen.add(slot_id)
    assert seen==set(CHOICES) and text_seen==set(TEXTS) and purpose_seen==set(PURPOSES)
    edited=raw
    for a,b,value in sorted(edits,reverse=True):edited=edited[:a]+value+edited[b:]
    compile(edited.decode('utf8'),str(path),'exec');path.write_bytes(edited)
    importlib.invalidate_caches();module=importlib.reload(module)
    known={p['id'] for p in v04.config()['personas']}|set(BEHAVIORS)
    validate(module.PACKS,module.SOURCES,known)
    after={v['id']:v for p in module.PACKS for s in p['slots'] for v in s['variants']}
    assert set(before)==set(after)
    assert len(after)==144
    for p in module.PACKS:
        initial=[s['variants'][0] for s in p['slots']]
        assert Counter(v['question_type'] for v in initial)=={'situational_action':8,'experience_reflection':4}
    for (identifier,old),(label,signal) in CHOICES.items():
        old_choice=next(o for o in before[identifier]['options'] if o['signal']==old)
        new_choice=next(o for o in after[identifier]['options'] if o['id']==old_choice['id'])
        assert new_choice['signal']==signal
        assert label is None or new_choice['label']==label
    report.update({'full_variants_read_so_far':144,'full_variants_read':144,'full_options_read':576,
      'status':'parent_editorial_accepted_pending_uniform_runtime_build',
      'editorial_findings':['七项个人升级预算、Focus、EX与递送路线不支持持续系统经营，只保留为具体零分行为。','八项普通屋顶连接查看没有实质身份维持，移除巡线员称呼并降为现场查看。','逐项重设计原48项自创玩法选项，去掉跨游戏反复出现的转身、蹲一下与出口空挥填充；普通现有动作变化不计自创，少量保留禁用该作已可用工具的真实限制。','20项熟悉停留增加具体正向体验，不能仅凭不添目标或慢走推断舒缓。','武士零四个对话时机选项不冒称操作训练；改为实际返回已可用动作房专练。','修正小小梦魇椅距与门把的可达关系、武士零跳斩落台措辞。'],
      'after_source_sha256':hashlib.sha256(edited).hexdigest(),'after_packs':module.PACKS,'after_sources':module.SOURCES,
      'changes':[{'id':i,'before':before[i],'after':after[i]} for i in before if before[i]!=after[i]],
      'explicit_choice_decisions':[{'id':i,'before_signal':old,'after_signal':sig,'label':label} for (i,old),(label,sig) in CHOICES.items()],
      'before_signal_counts':dict(Counter(o['signal'] for v in before.values() for o in v['options'])),
      'after_signal_counts':dict(Counter(o['signal'] for v in after.values() for o in v['options'])),
      'all_ids_and_mode_maps_preserved':True,'all_six_forms_eight_action_four_past':True,'all_slots_have_alternatives':True,
      'parent_firsthand_source_checks':[
       {'url':'https://www.ea.com/amp/news/master-the-combat-of-mirrors-edge-catalyst','access':'官方开发者正文','finding':'Catalyst移动、轻重击、Focus与Shift；不混原版Reaction Time与枪械。'},
       {'url':'https://www.ea.com/amp/news/progression-in-mirrors-edge-catalyst','access':'官方制作人正文','finding':'Skill Roll等动作需点数解锁，保留成长与个人准备/临时状态分开。'},
       {'path':'research/question-design-v0.5/source-cache/batch07-e/mirrors-edge-catalyst-pc-manual.txt','access':'作者缓存的官方PDF相关段本轮读取','finding':'Focus重击消耗，MAGrope方向可控、允许松开，指定挂点与升级范围。'},
       {'path':'research/question-design-v0.5/source-cache/batch07-e/mirrors-edge-original-pc-manual.txt','access':'作者缓存的EA原版手册相关段本轮读取','finding':'原版滑索松开、蹲行、Skillroll、Reaction Time及本机幽灵；历史联网说明不作当前功能。'},
       {'url':'https://gamerwalkthroughs.com/little-nightmares/chapter-1-the-prison/','access':'玩家实玩正文','finding':'拖椅、箱子够开关、转轮门、Nome和眼睛遮挡。'},
       {'url':'https://gamerwalkthroughs.com/little-nightmares/chapter-3-the-kitchen/','access':'玩家实玩正文','finding':'肉料、香肠机关、上层小洞旁雕像与摆荡。'},
       {'url':'https://gamerwalkthroughs.com/little-nightmares-2/chapter-1-wilderness/','access':'玩家实玩正文','finding':'松果鞋触陷阱、推箱、碎影和帽子、NPC Six摇柄搭手。'},
       {'url':'https://gamerwalkthroughs.com/little-nightmares-2/chapter-2-school/','access':'玩家实玩正文及公开段落','finding':'瓷偶重锤、学校与Six被带走流程；不当真人合作。'},
       {'url':'https://steamcommunity.com/sharedfiles/filedetails/?id=1310872602','access':'玩家一手基础指南正文','finding':'本体装备栏与控制、粉色招架、地图与关卡，不带入DLC能力。'},
       {'url':'https://www.gamerevolution.com/originals/520685-katana-zero-interview','access':'开发者访谈正文','finding':'电影布景楼层可选先后、慢动作影响音乐、打断与局部叙事差异。'},
       {'url':'https://superadventuresingaming.blogspot.com/2022/05/katana-zero-pc.html','access':'本轮直开被重定向验证页，未声称重新读取正文；保留作者先前实读记录','finding':'只采用作者已核对的普通本体房、公寓与录像边界，不新加具体地图功能。'}],
      'human_player_trial':False,'known_signal_and_source_validation':True})
    report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'variants':len(after),'choice_decisions':len(CHOICES),'changed_variants':len(report['changes']),'inventor_before':report['before_signal_counts']['play_inventor'],'inventor_after':report['after_signal_counts']['play_inventor'],'sha':report['after_source_sha256']},ensure_ascii=False))

if __name__=='__main__':main()
