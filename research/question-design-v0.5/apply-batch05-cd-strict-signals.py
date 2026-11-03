"""One-time, explicitly reviewed corrections. Does not generate question prose."""
from pathlib import Path
import ast
import base64
import hashlib
import importlib
import json
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from question_authoring import SIGNALS

# Each ID was read with its complete current scene and all four choices.
REVIEWED_IDS='''
SE5SC03.V1 SE5SC03.ALT1 SE5SC05.V1 SE5SC05.ALT1 SE5SC07.V1 SE5SC07.ALT1 SE5SC11.V1 SE5SC11.ALT1
DGSC03.V1 DGSC03.ALT1 DGSC05.V1 DGSC05.ALT1 DGSC09.ALT1 DGSC12.V1 DGSC12.ALT1
UCLEGSC02.V1 UCLEGSC02.ALT1 UCLEGSC03.ALT1 UCLEGSC05.V1 UCLEGSC05.ALT1 UCLEGSC05.LOST.V1 UCLEGSC05.LOST.ALT1 UCLEGSC06.LOST.V1 UCLEGSC06.LOST.ALT1 UCLEGSC08.V1 UCLEGSC08.ALT1 UCLEGSC09.V1 UCLEGSC09.ALT1 UCLEGSC09.LOST.V1 UCLEGSC09.LOST.ALT1
DMC5SC01.V1 DMC5SC01.ALT1 DMC5SC02.V1 DMC5SC02.ALT1 DMC5SC05.V1 DMC5SC05.ALT1 DMC5SC06.V1 DMC5SC06.ALT1 DMC5SC07.V1 DMC5SC07.ALT1 DMC5SC08.V1 DMC5SC08.ALT1 DMC5SC09.V1 DMC5SC09.ALT1 DMC5SC11.V1
DMC4SC01.V1 DMC4SC01.ALT1 DMC4SC03.V1 DMC4SC03.ALT1 DMC4SC05.V1 DMC4SC05.ALT1 DMC4SC06.V1 DMC4SC06.ALT1 DMC4SC07.V1 DMC4SC07.ALT1 DMC4SC10.V1 DMC4SC10.ALT1 DMC4SC11.V1 DMC4SC11.ALT1
BAYOSC01.V1 BAYOSC01.ALT1 BAYOSC02.V1 BAYOSC02.ALT1 BAYOSC03.V1 BAYOSC03.ALT1 BAYOSC04.V1 BAYOSC04.ALT1 BAYOSC05.V1 BAYOSC05.ALT1 BAYOSC07.V1 BAYOSC07.ALT1 BAYOSC09.V1 BAYOSC09.ALT1 BAYOSC10.V1 BAYOSC10.ALT1
TLOU1V503.V1 TLOU1V503.ALT1 TLOU1V504.V1 TLOU1V504.ALT1 TLOU1V508.V1 TLOU1V508.ALT1 TLOU1V511.V1 TLOU1V511.ALT1
VANV502.V1 VANV502.ALT1 VANV503.V1 VANV503.ALT1 VANV504.V1 VANV504.ALT1 VANV505.V1 VANV505.ALT1 VANV506.V1 VANV506.ALT1 VANV507.V1 VANV507.ALT1 VANV511.V1 VANV511.ALT1 VANV512.V1 VANV512.ALT1
MGRV501.V1 MGRV501.ALT1 MGRV503.V1 MGRV503.ALT1 MGRV504.V1 MGRV504.ALT1 MGRV505.V1 MGRV505.ALT1 MGRV511.V1 MGRV511.ALT1
HIFIV501.V1 HIFIV501.ALT1 HIFIV502.V1 HIFIV502.ALT1 HIFIV503.V1 HIFIV503.ALT1 HIFIV504.V1 HIFIV504.ALT1 HIFIV505.V1 HIFIV505.ALT1 HIFIV508.V1 HIFIV508.ALT1 HIFIV509.V1 HIFIV509.ALT1
NIERAV502.V1 NIERAV502.ALT1 NIERAV503.V1 NIERAV503.ALT1 NIERAV505.V1 NIERAV505.ALT1 NIERAV509.V1 NIERAV509.ALT1
NIERRV502.V1 NIERRV502.ALT1 NIERRV503.V1 NIERRV503.ALT1 NIERRV509.V1 NIERRV509.ALT1
'''.split()
DECISIONS={key:'try_action_variant' for key in REVIEWED_IDS}
for key in '''SE5SC03.V1 SE5SC03.ALT1 SE5SC07.V1 SE5SC11.V1 DGSC03.V1 DGSC12.V1
 UCLEGSC05.V1 UCLEGSC08.V1 DMC5SC01.V1 DMC5SC07.V1 DMC5SC07.ALT1 DMC5SC11.V1
 DMC4SC01.V1 DMC4SC01.ALT1 DMC4SC10.V1 DMC4SC10.ALT1 BAYOSC02.V1 BAYOSC05.V1 BAYOSC05.ALT1 BAYOSC10.V1
 TLOU1V503.V1 VANV502.V1 VANV503.V1 VANV503.ALT1 VANV505.V1 VANV507.V1 VANV507.ALT1 VANV511.V1
 MGRV503.V1 MGRV511.V1 HIFIV504.V1 HIFIV505.V1 NIERAV502.V1 NIERAV503.V1 NIERRV503.V1'''.split():
    DECISIONS[key]='try_available_setup'
for key in '''SE5SC11.ALT1 DGSC05.V1 UCLEGSC06.LOST.ALT1 UCLEGSC09.LOST.V1 TLOU1V504.V1 TLOU1V504.ALT1'''.split():
    DECISIONS[key]='route_choice'
for key in '''DGSC09.ALT1 UCLEGSC02.V1 UCLEGSC02.ALT1 UCLEGSC03.ALT1 UCLEGSC05.LOST.V1 UCLEGSC05.LOST.ALT1 UCLEGSC08.ALT1 UCLEGSC09.V1 UCLEGSC09.ALT1 MGRV504.V1 MGRV504.ALT1 NIERAV505.ALT1 NIERRV502.ALT1'''.split():
    DECISIONS[key]='route_variant'

# These are genuinely new prohibitions, explicitly written rather than calling
# an ordinary change of order a rule. Other unfamiliar choices stay behavior-only.
NEW_RULES={
 'SE5SC05.ALT1':'给这段新增不许主动开枪的限制，只用已有遮挡与移动经过巡逻区，亲手试这条规则',
 'DGSC05.ALT1':'规定这场不许开枪，只准已拥有的投掷物与移动，按自己新增的限制实际打一段',
 'UCLEGSC05.ALT1':'给这场新增禁止盲射与近战的限制，只准从掩体探身后开枪，按规则实际玩一段',
 'DMC5SC01.ALT1':'给下一场定下禁止主动放弃机械臂、也禁止蓄力消耗它的限制，只用这只臂的普通动作与剑枪亲自试一段',
 'DMC5SC08.ALT1':'这遍使用当前已可用的Nero，规定只许蓝玫瑰枪击与移动、不许挥红后剑，按新增限制亲自重玩这段',
 'DMC4SC07.ALT1':'规定这场禁用红后剑和蓝玫瑰，只准恶魔右腕抓投与移动，按自己新增的限制处理这些可抓小敌人',
 'BAYOSC07.ALT1':'在这段普通遭遇里禁用全部拳部攻击，只准已有脚部攻击与闪避，按新增限制亲自试一遍',
 'TLOU1V508.ALT1':'规定每次开枪前都必须换到另一处已知掩体，禁止在同一处连开第二枪，按自己新增的规则试这段',
 'VANV512.V1':'给那一遍新增禁止主动开启AR的限制，只用当前枪械、掩体与推进，亲自照规则打过',
 'MGRV505.ALT1':'规定每次出刀前必须先退回自己指定的地面位置，禁用连续斩击，按新限制在基础教学里试一轮',
 'HIFIV505.ALT1':'在训练室规定只许轻攻击、禁止重攻击与闪避，按自己新增的限制打一轮熟悉目标',
 'NIERAV502.ALT1':'给这场新增禁止近战的限制，只准当前Pod的远射与移动，亲自照规则试一段',
 'NIERRV502.V1':'规定这场禁用剑术，只准白之书当前已会的远程魔法与移动，按自己新增的规则处理魔物',
}
for key in NEW_RULES:DECISIONS[key]='play_inventor'
LABELS={
 **NEW_RULES,
 'UCLEGSC05.V1':'换用当前已有却少用的一件枪械，亲手试它在这处据点的出手体验',
 'UCLEGSC06.LOST.ALT1':'换到眼前已可到达的另一处掩体，亲手试一次从不同方向进入这场交火',
 'UCLEGSC08.V1':'换用一件当前已有却少用的枪械，亲手试它在下一段熟悉遭遇中的出手体验',
 'UCLEGSC09.LOST.V1':'自己在那场战斗改走过一条原先少用却可到达的侧路，亲手体验了不同进入方向',
 'UCLEGSC09.LOST.ALT1':'自己改过出掩体、开枪与转移的先后，亲手体验了另一种已会动作的接法',
 'DMC5SC08.V1':'这次使用已可用的Nero，换一套已有机械臂装载顺序，亲手体验熟悉关卡里不同的出手先后',
 'DMC5SC09.V1':'自己在那场战斗换过机械臂动作与剑枪的先后，亲手体验了不同的出手次序',
 'BAYOSC04.ALT1':'换一次已会拳脚动作与闪避的先后，亲手体验熟悉遭遇里不同的动作衔接',
 'BAYOSC07.V1':'在这处既有挑战允许的动作内，换一次已会攻击与闪避的先后，亲手体验不同衔接',
 'BAYOSC09.V1':'自己改过一次闪避插入与拳脚动作的先后，亲手体验了不同接法',
 'BAYOSC09.ALT1':'自己换过一次已会拳脚与闪避的先后，亲手体验了不同动作次序',
 'HIFIV505.V1':'换上一项自己已拥有却少用的芯片效果，亲手体验它在熟悉交火里怎样发挥',
 'NIERAV509.V1':'自己调过近战、回避与Pod开火的先后，亲手体验了另一种已会动作的接法',
 'NIERRV502.ALT1':'从原先少用却可达的一侧接近，亲手试一次不同进入方向',
}
TEXTS={'TLOU1V508.ALT1':'只有最早的手枪与少量物品，也知道眼前两处可达掩体和一段通路怎样走；这次先改什么？'}

def main():
    expected={'question_batch05_c':'9b34ef5a1dfd34c110b21313a3914fd49e2326df597a8aa308fd7a1974eac383',
              'question_batch05_d':'4a37cbb9428947f0c3f9602b5dde551baee196a5e577db16364b83909dfb0121'}
    report={'date':'2026-10-30','reviewer':'root','status':'source_revision_in_progress',
            'review_scope':'137 pre-existing creativity choices with their entire scenes and other choices; 312 variants previously authored/read',
            'history_baseline':'reports/fixtures/before-batch05-final-signal-review.json',
            'human_player_trial':False,'modules':[]}
    seen=set()
    for name,sha in expected.items():
        path=ROOT/'scripts'/f'{name}.py';raw=path.read_bytes()
        assert hashlib.sha256(raw).hexdigest()==sha,(name,'Already edited; do not rerun this migration')
        module=importlib.import_module(name)
        variants={v['id']:v for p in module.PACKS for s in p['slots'] for v in s['variants']}
        text_ids={v['text']:i for i,v in variants.items()};assert len(text_ids)==len(variants)
        line_offsets=[0]
        for line in raw.splitlines(keepends=True):line_offsets.append(line_offsets[-1]+len(line))
        def span(node):return line_offsets[node.lineno-1]+node.col_offset,line_offsets[node.end_lineno-1]+node.end_col_offset
        edits=[]
        def replace(node,value):
            start,end=span(node);edits.append((start,end,repr(value).encode('utf-8')))
        for node in ast.walk(ast.parse(raw.decode('utf-8'))):
            if not isinstance(node,ast.Call) or not isinstance(node.func,ast.Name) or node.func.id!='Q':continue
            main_id=text_ids[ast.literal_eval(node.args[2])];alt=node.args[7]
            alt_id=text_ids[ast.literal_eval(alt.elts[0])]
            if not ({main_id,alt_id}&set(DECISIONS)):continue
            main_signals=ast.literal_eval(node.args[4]).split()
            alt_signals=ast.literal_eval(alt.elts[2]).split() if len(alt.elts)==3 else list(main_signals)
            for identifier,label_node,tokens,text_node in ((main_id,node.args[3],main_signals,node.args[2]),(alt_id,alt.elts[1],alt_signals,alt.elts[0])):
                if identifier not in DECISIONS:continue
                seen.add(identifier)
                assert sum(SIGNALS.get(s,s)=='play_inventor' for s in tokens)==1
                index=next(i for i,s in enumerate(tokens) if SIGNALS.get(s,s)=='play_inventor')
                tokens[index]=DECISIONS[identifier]
                if identifier in LABELS:
                    labels=ast.literal_eval(label_node).split('|');labels[index]=LABELS[identifier];replace(label_node,'|'.join(labels))
                if identifier in TEXTS:replace(text_node,TEXTS[identifier])
            replace(node.args[4],' '.join(main_signals))
            if len(alt.elts)==3:replace(alt.elts[2],' '.join(alt_signals))
            else:
                start,end=span(alt);edits.append((end-1,end-1,(', '+repr(' '.join(alt_signals))).encode('utf-8')))
            purpose=ast.literal_eval(node.args[5])+' 普通换路、换配置和已会动作换序只记当次行为；只有具体新增的限制才支持自创玩法。'
            replace(node.args[5],purpose)
        edited=raw
        for start,end,value in sorted(edits,reverse=True):edited=edited[:start]+value+edited[end:]
        compile(edited.decode('utf-8'),str(path),'exec')
        report['modules'].append({'module':name,'before_sha256':sha,'before_source_raw_base64':base64.b64encode(raw).decode(),
                                  'before_packs':module.PACKS,'before_sources':module.SOURCES,'after_sha256':hashlib.sha256(edited).hexdigest()})
        path.write_bytes(edited)
    assert seen==set(DECISIONS),(set(DECISIONS)-seen)
    report['status']='written_pending_reload_and_runtime_review'
    report['explicit_decisions']={i:{'signal':DECISIONS[i],'new_label':LABELS.get(i),'new_text':TEXTS.get(i)} for i in REVIEWED_IDS}
    target=ROOT/'research/question-design-v0.5/batch05-cd-strict-signal-parent-review.json'
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print({'reviewed_creativity_choices':len(seen),'explicit_new_rules':len(NEW_RULES),'ordinary_choices_behavior_only':len(seen)-len(NEW_RULES)})

if __name__=='__main__':main()
