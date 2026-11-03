"""Build readable specifications, full fictional examples and independent arithmetic checks."""
from collections import Counter
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from youge import v04
from scripts.build_expanded_catalogue import write_exports


def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(value,encoding='utf-8')


def md_report(result):
    r=result['report'];state=v04.score(result['response']);c=v04.config()
    rows=['# '+r['display_name']+' · '+r['persona']['name'],'','**虚构模拟答卷，不能作为模型有效的证据。**','','本命作品：《'+r['game']['title']+'》。'+r['one_line'],'','## 完整原始答卷','','```json',json.dumps(result['response'],ensure_ascii=False,indent=2),'```','','## 逐题复算','','A—D表示不同做法，不是1—4分。以下为被选选项的实际计分点。','','| 题号 | 问题 | 选择 | 计分点 |','|---|---|---|---|']
    totals=Counter({p['id']:0 for p in c['personas']})
    for item,option,ref in state['selected']:
        totals.update(option['weights'])
        weights='；'.join(f'{next(p["name"] for p in c["personas"] if p["id"]==pid)} +{weight}' for pid,weight in option['weights'].items()) or '0（只解释行为）'
        rows.append(f'| {item["id"]} | {item["text"]} | {option["id"]} · {option["label"]} | {weights} |')
    assert dict(totals)==r['audit']['points']
    rows+=['','| 人格 | 合计点 | 本命题支持数 |','|---|---:|---:|']
    rows += [f'| {p["name"]} | {totals[p["id"]]} | {r["audit"]["anchor_support_count"].get(p["id"],0)} |' for p in c['personas']]
    rows+=['',f'共{r["question_count"]}题，补问{r["question_count"]-16}题。最后按固定规则输出：**{r["persona"]["name"]}**。','', '## 最终报告','']
    for heading,key in [('三条具体线索','insights'),('本命作品里的吸引力','attractions'),('跨情境呼应','cross_echo'),('同游建议','advice'),('明确边界','drains')]:
        rows+=['### '+heading,'']
        for claim in r[key]:
            rows += [claim.get('title','')+'：'+claim['text'] if claim.get('title') else claim['text'],'','依据：'+'；'.join(f'{r["evidence"][ref]["question_id"]}={r["evidence"][ref]["answer"]}（{r["evidence"][ref]["label"]}）' for ref in claim['evidence_refs']),'']
    rows+=['## 完整触发与版本记录','','```json',json.dumps({'versions':r['versions'],'audit':r['audit'],'fingerprint':r['fingerprint']},ensure_ascii=False,indent=2),'```','']
    return '\n'.join(rows)


def main():
    c=v04.config();lib=v04.catalog();byid={g['id']:g for g in lib['games']}
    write_exports(lib)
    lines=['# 游格 v0.4 · 完整题库与计分','','正式路径固定16题：G01—G12本命作品，X13—X16跨游戏。每题4个行动选项，单选。先根据作品机制适配内容，不增加第五项或后续多选。','','## 选项计分与唯一人格','','游戏名、分类、时长和拥有情况不直接给任何人格加分。作品只选择适用题包；实际选项按配置累加语义点。A—D不是程度分，位置不代表高低。Mod、攻略、剧透、重玩、推进方式、受挫安排与起步方式只生成行为解释，不计人格点。','','分类步骤：','','1. 先累计16题的实际选项权重。主吸引点通常2点；少量有独立依据的附加点1点；行为解释项0点。','2. 第一名与第二名分差不超过2点时，进入四选一补问。候选为当前前4名，选项只显示具体活动，不显示人格名称。选中的候选加4点。','3. 重新检查，必要时再补1题，总计最多18题。','4. 始终输出一个称号。最终依次按总点、本命题支持数、最后补问所选候选、配置固定顺序排序；最后一项只为保证唯一可重复。','5. 不完整答卷只保存，不出人格结果。只接受A—D；数组、E、缺失伪填、未知游戏和不同版本均拒绝。修改正式答案后清除旧补问并重新判断。','','2点接近门槛、4点补问权重和固定顺序都是待试测产品参数，不是科学界限。各题包的可获得计分机会不同，原始点仅用于本题包内分类，不能跨玩家当作能力、常模、人格强度或百分位比较。','','## 唯一称号与具体报告','','报告固定给一个人格名称、对应原创角色、3个性格特征词和两个侧写板块。规则ID、触发快照与实际选择在内部记录中保留，不进入结果页或长图。多情境概括至少两个问题支持，只有一个依据时只描述该情境。低点不生成消耗点。','','同游报告比较受挫之后、新机制、攻略、提前告知、重玩、Mod、推进节奏和一起玩的安排，共8项。难度档位、剧情停留的具体设置如果没有直接回答，不从称号推断，实际同游仍需单独确认。','','以下先列8款专用题包的完整16题；其余作品使用16种机制模板，完整配置包含所有模板。G05、G06、G07和G12在8款专用题包另有具体玩法适配。','','## 8款作品完整题目','']
    for gid in lib['featured']:
        g=byid[gid];lines+=['### '+g['title'],'']
        for q in v04.questionnaire(gid):
            lines += ['**'+q['id']+' · '+q['text']+'**','']+[o['id']+'. '+o['label'] for o in q['options']]+['']
    lines += ['## 其他作品的机制模板','','适用关系由每款作品的 `mechanic_family` 字段固定，不能在运行时由生成模型猜测。首次试测重点检查模板与作品是否吻合；有不适用选项则修题或为作品补专用题，不能把不适用当低偏好。','']
    for name,questions in c['families'].items():
        lines+=['### '+name,'']
        for q in questions:lines+=['**'+q['id']+' · '+q['text']+'**','']+[o['id']+'. '+o['label'] for o in q['options']]+['']
    lines+=['## 两轮补问的全部动作词条','','具体显示当前前4名对应词条；两轮题干分别是“放眼你玩过的游戏，现在更想把时间留给哪件事？”和“再做一个取舍，你更想接着体验哪件事？”。候选顺序和哈希题号固定。','', '| 人设（仅审查文档可见） | 第一轮 | 第二轮 |','|---|---|---|']
    lines += [f'| {p["name"]} | {c["tie_actions"][p["id"]][0]} | {c["tie_actions"][p["id"]][1]} |' for p in c['personas']]
    write(ROOT/'docs/13-v0.4-questionnaire-and-scoring.md','\n'.join(lines)+'\n')
    for case in 'ABC':
        result=v04.demo(case)
        if case=='C':
            raw=result['response'];raw['answers']['G09']='B';raw['answers']['G10']='C';result=v04.report(raw)
            assert result['complete']
        write(ROOT/f'examples/v0.4/{case}.json',json.dumps(result['response'],ensure_ascii=False,indent=2)+'\n')
        write(ROOT/f'reports/v0.4/{case}.json',json.dumps(result['report'],ensure_ascii=False,indent=2)+'\n')
        write(ROOT/f'reports/v0.4/{case}.md',md_report(result))
    a,b,cc=[json.loads((ROOT/f'examples/v0.4/{x}.json').read_text(encoding='utf-8')) for x in 'ABC']
    for left,right,name in [(a,b,'A-B'),(a,cc,'A-C')]:
        pair=v04.compare(left,right);write(ROOT/f'reports/v0.4/{name}.json',json.dumps(pair,ensure_ascii=False,indent=2)+'\n')
    write(ROOT/'reports/v0.4/README.md','# v0.4完整虚构模拟报告\n\nA与B都选文明6，但分别得到赛博包工头与电子街溜子；C选荒野大镖客2，仍得到电子街溜子。C另覆盖有重玩兴趣但时间不足、Mod条件受限。\n\n每份报告包含原始答卷、逐题权重、16人设合计、补问记录、最终文案和实际证据，可以独立手工相加核对。全部为虚构，不是研究样本。\n')
    print('Built catalogue document, complete question bank and three manually summable fictional reports.')


if __name__=='__main__':main()
