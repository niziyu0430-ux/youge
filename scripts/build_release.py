"""Generate reviewable content artifacts from the frozen JSON configuration.

Normal builds are offline and only write this package's generated files.
"""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from youge import build_report,compare_reports,load_config
from youge.render import write_report,write_comparison


def write(path,text):
    target=ROOT/path
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(text,encoding="utf-8")


def option_lines(question,*,codes=True):
    return [f"- {('`'+str(o['value'])+'`：') if codes else '□ '}{o['label']}" for o in question["options"]]


def questionnaire(config):
    dims={d["id"]:d for d in config["dimensions"]}
    lines=["# 游格完整题库与适用条件","",f"题库版本：{config['manifest']['versions']['instrument']}。本文件由完整配置生成。","",
           "## 统一说明与选项","",config["instructions"]["reference"],"",config["instructions"]["clarification"],""]
    lines+=option_lines(config["answer_scale"])
    lines += ["- `null`：无法判断／不适用；缺失原因单独记录。","","## 32道核心题 固定交错顺序",""]
    for q in sorted(config["core_questions"],key=lambda x:x["display_order"]):
        lines += [f"### {q['display_order']:02} {q['id']} {dims[q['dimension']]['name']}","",q["text"],"",
                  f"主要目标：{q['measurement_target']}。","",f"情境：{q['context']}。计分：本维等权、1—5正向映射。","",f"适用条件：{q['applicability']}",""]
    lines += ["## 作品口味档案","","默认三款，允许零至五款；每款最多两项吸引点。名称和类型均不计分。","",
              "每项字段：作品名称、可选作品ID、版本、亲玩状态、吸引点、可选原话。未知作品保留自填名，不自动猜测系列或类型。","","### 亲玩状态",""]
    lines+=option_lines({"options":config["taste"]["experience_options"]})
    lines += ["","### 吸引点 最多两项",""]
    lines += [f"- `{x['id']}`：{x['label']}（不计分）" for x in config["taste"]["attractions"]]
    lines += ["","### 可选未喜欢作品","","最多一款，必须亲玩；选择1—2项原因。拥有、时长、通关和中途退出均不直接等于喜爱或厌恶。",""]
    lines+=option_lines({"options":config["taste"]["negative_reasons"]})
    lines += ["","## 补充体验清单","",config["supplement"]["text"],""]
    lines+=option_lines(config["supplement"])
    lines += ["","## 背景与接触机会 核心题之后",""]
    for q in config["background_questions"]:
        lines += [f"### {q['id']}","",q["text"],""]+option_lines(q)+[""]
    lines += ["## 条件追问的适用性入口","",config["branch_applicability"]["question"],"",
              "五个模块分别填写：攻略、二刷、同游、起步方式、Mod。",""]
    lines+=option_lines({"options":config["branch_applicability"]["statuses"]})
    lines += ["","未声明时为not_provided；未适用、未触发、未回答和明确不喜欢分别记录。","","## 12道条件追问 全部不计分",""]
    for q in config["followup_questions"]:
        lines += [f"### {q['id']}","",q["text"],"",f"入口：{q['module']}模块声明适用。",""]
        if q.get("depends_on"):
            dep=q["depends_on"]
            lines += [f"前置：{dep['question_id']}选择`{'、'.join(dep['accepted'])}`时触发。",""]
        if q.get("basis_options"):
            lines += ["先选择依据：",""]+option_lines({"options":q["basis_options"]})+[""]
        lines+=option_lines(q)+[""]
        if q.get("max_selections"):
            lines += [f"最多选择{q['max_selections']}项。",""]
        if q.get("exclusive_options"):
            lines += ["通常不借助和随内容改变均为独占选项，不与其他项混选。",""]
        if q["id"]=="R02":
            lines += ["愿意或有条件愿意时显示新路线、练习、补全、重温、陪同等原因；更想新作或不愿意时显示新作、已有体验足够等原因；其他原因可补充原话。",""]
        if q["id"]=="M02":
            lines += ["实际用途仅在M01确认用过时可填写；其他可用分支只能记录假设意愿。同一回答内不混填两种依据。",""]
    return "\n".join(lines)


def player_form(config):
    lines=["# 游格玩家偏好问卷","",config["instructions"]["reference"],"",config["instructions"]["clarification"],"",
           "评分：1非常不符合，2比较不符合，3中立，4比较符合，5非常符合。无法判断／不适用单独选择。","",
           "请先完成下面的问题，再填写喜欢作品。这里没有正确答案。","","## 通常的游戏体验",""]
    for q in sorted(config["core_questions"],key=lambda x:x["display_order"]):
        lines += [f"{q['display_order']}. {q['text']}","","   □1　□2　□3　□4　□5　□无法判断／不适用",""]
    lines += ["## 喜欢的作品","","请写真正喜欢的作品，默认三款，允许少填或跳过，最多五款。拥有、玩得久或通关不一定代表喜欢。","",
              "每款：名称______　版本可选______　□亲玩过 □未亲玩 □无法确认","","最吸引你的部分最多选两项：",""]
    lines += ["、".join(x["label"] for x in config["taste"]["attractions"]),"","可选补充原话______。","",
              "可选：一款亲自玩过但没喜欢起来的作品______，原因最多两项：",""]
    lines += ["、".join(x["label"] for x in config["taste"]["negative_reasons"]),"","## 补充体验清单","",config["supplement"]["text"],""]
    lines+=option_lines(config["supplement"],codes=False)+["","## 背景与适用经历",""]
    for q in config["background_questions"]:
        lines += [q["text"],""]+option_lines(q,codes=False)+[""]
    lines += ["对攻略、二刷、同游、起步方式和Mod五组场景，分别选：□适用 □缺乏经历 □不适用 □跳过。只填写你确认适用的部分。","","## 按需补充",""]
    names={"guide":"攻略与剧透","replay":"再次游玩","coop":"一起玩的安排","approach":"接触新系统","mod":"Mod条件与用途"}
    previous=None
    for q in config["followup_questions"]:
        if q["module"]!=previous:
            lines += [f"### {names[q['module']]}",""]
            previous=q["module"]
        if q["id"]=="R02":
            lines += ["意愿明确时填写原因：愿意再次体验时看前五项；更想新作或不想再次体验时看接下来的两项。其他原因均可补充。",""]
        if q["id"]=="M02":
            lines += ["已经用过或能明确表达用途时填写；不知道用途或没有使用意愿时可以跳过。",""]
        if q.get("exclusive_options"):
            lines += ["选择通常不借助或随作品改变时，请单独选择该项。",""]
        lines += [q["text"],""]
        if q.get("basis_options"):
            lines+=option_lines({"options":q["basis_options"]},codes=False)+[""]
        lines+=option_lines(q,codes=False)+[""]
    lines += ["填写结束。你可以跳过无法判断的部分，报告会保留资料不足，而不会把它算成低偏好。",""]
    return "\n".join(lines)


def readable_condition(condition,config):
    dims={d["id"]:d["name"] for d in config["dimensions"]}
    qindex={q["id"]:q for q in config["followup_questions"]}
    if "all" in condition:
        return "（"+" 且 ".join(readable_condition(c,config) for c in condition["all"])+"）"
    if "any" in condition:
        return "（"+" 或 ".join(readable_condition(c,config) for c in condition["any"])+"）"
    if "not" in condition:
        return "不满足"+readable_condition(condition["not"],config)
    path=condition["fact"].split(".")
    value=condition["value"]
    if path[0]=="scores":
        label=dims[path[1]]+"分"
    elif path[0]=="positive_counts":
        label=dims[path[1]]+"的4/5分题数"
    else:
        label=".".join(path[1:])
        q=qindex.get(path[1])
        if q and len(path)==2:
            labels={o["value"]:o["label"] for o in q["options"]}
            if isinstance(value,list):
                value="／".join(labels.get(v,v) for v in value)
            elif isinstance(value,str):
                value=labels.get(value,value)
    operators={"gte":"≥","lte":"≤","eq":"＝","in":"属于","contains":"包含","exists":"有值＝"}
    return f"{label}{operators[condition['op']]}{value}"


def handbook(config):
    lines=["# 游格八原型手册与确定性报告文案","","基础原型是连续画像的摘要。称号按计分展示规则产生；具体判断另需实际答案支持，不自动沿用手册里的所有描述。","",
           "## 八个基础原型",""]
    for d in config["dimensions"]:
        a=d["archetype"]
        lines += [f"### {a['name']} 对应{d['name']}","",a["one_line"],"",a["portrait"],"",
                  f"维度定义：{d['definition']}","","可能承载这种偏好的情境：",""]
        lines += [f"- {s}" for s in a["example_situations"]]
        lines += ["",f"同游时仍需直接确认：{'、'.join(a['co_play_focus'])}。","",
                  f"解释边界：不从该维推断{d['must_not_infer']}。相对低分只表示这些题目没有得到较高认同，不自动等于能力不足或厌恶。","",
                  "题目覆盖："+"；".join(q["context"] for q in config["core_questions"] if q["dimension"]==d["id"])+"。",""]
    lines += ["## 单人报告固定模板","",
              "1. 原型名称、一句话、副偏好及最多三个行为标签；敏感或缺失时弱化称号。",
              "2. 最多三条具体判断；每条附题号、实际选择、触发规则和适用范围。证据不足时少于三条。",
              "3. 八维横向条形图，固定0—100坐标、有效题数，缺失维度显示资料不足。",
              "4. 作品及自填原因，区分亲玩与期待，解释共同点或不同需求。",
              "5. 有支持的吸引点、明确负面原因或回避边界。低分本身不生成消耗点。",
              "6. 七项同游建议；未回答时只作为待确认事项。",
              "7. 最多两项现实习惯自我核对，不计分、不作人格结论。",
              "8. 审计附录：原始答案、逐维复算、追问状态、敏感性变化和版本。","",
              "## 条件化判断 文案和证据",""]
    for rule in sorted(config["report_rules"],key=lambda r:(r["section"],-r["priority"],r["id"])):
        lines += [f"### {rule['id']} {rule['section']}","","触发："+readable_condition(rule["condition"],config)+"。","",rule["text"],"",
                  "证据选择：`"+json.dumps(rule["evidence"],ensure_ascii=False,separators=(",",":"))+"`。","",
                  f"优先级{rule['priority']}；去重分组`{rule.get('dedup_group','')}`。",""]
    lines += ["## 派生判断的触发和边界",""]
    for rule in config["derived_report_rules"]:
        lines += [f"### {rule['id']}","","触发：`"+json.dumps(rule["trigger"],ensure_ascii=False,separators=(",",":"))+"`。","",f"证据：{rule['evidence']}。",""]
        if rule.get("template_key"):
            lines += ["模板："+config["system_templates"][rule["template_key"]],""]
    lines += ["## 同游建议的条件化文字",""]
    for topic in config["advice_topics"]:
        lines += [f"### {topic['title']} 依据{topic['question_id']}","","未提供明确回答："+topic["fallback"],""]
        if topic["by_answer"]:
            q=next(q for q in config["followup_questions"] if q["id"]==topic["question_id"])
            labels={o["value"]:o["label"] for o in q["options"]}
            lines += ["| 实际选择 | 建议模板 |","|---|---|"]
            lines += [f"| {labels[key]} | {value} |" for key,value in topic["by_answer"].items()]
            lines.append("")
        else:
            lines += [config["system_templates"]["guide_advice"],""]
    lines += ["## 呈现与证据复核","","相同优先级以规则ID稳定排序；组合已经覆盖的维度不再重复占据前三条。保留规则快照及原始答案，不能只留下名称和赞美。新增或修改文字条件后，更新文案版本并重建全部模拟报告。",""]
    return "\n".join(lines)


def response_schema(config):
    def choice(q):
        values=[o["value"] for o in q["options"]]
        if q["response_type"]=="single":
            result={"type":"string","enum":values}
        else:
            selected={"type":"array","items":{"type":"string","enum":values},"minItems":1,"uniqueItems":True,"maxItems":q.get("max_selections",len(values))}
            if q["response_type"]=="multi_with_basis":
                result={"type":"object","required":["basis","purposes"],"properties":{"basis":{"enum":["actual","hypothetical"]},"purposes":selected},"additionalProperties":False}
            else:
                result=selected
        return {"anyOf":[result,{"type":"null"}]}
    string={"type":"string"}
    game_properties={"title":{"type":"string","minLength":1},"game_id":string,"edition":{"type":"string","minLength":1},"experience":{"enum":["yes","no","unknown"]},"note":string,
                     "attractions":{"type":"array","maxItems":2,"uniqueItems":True,"items":{"enum":[a["id"] for a in config["taste"]["attractions"]]}}}
    favorite={"type":"object","required":["title","experience"],"properties":game_properties}
    negative={"type":"object","required":["title","experience","reasons"],"properties":{**game_properties,"experience":{"const":"yes"},"reasons":{"type":"array","minItems":1,"maxItems":2,"uniqueItems":True,"items":{"enum":[a["value"] for a in config["taste"]["negative_reasons"]]}}}}
    return {"$schema":"https://json-schema.org/draft/2020-12/schema","title":"游格v0.2原始答卷","description":"字段形状约束；跨字段分支、版本及重复语义由参考实现检查。",
            "type":"object","required":["versions","core"],"properties":{
                "versions":{"const":config["manifest"]["versions"]},"respondent_id":string,"display_name":string,"fictional":{"type":"boolean"},
                "core":{"type":"object","properties":{q["id"]:{"type":["integer","null"],"minimum":1,"maximum":5} for q in config["core_questions"]},"additionalProperties":False},
                "core_missing_reasons":{"type":"object","propertyNames":{"enum":[q["id"] for q in config["core_questions"]]},"additionalProperties":{"enum":[x["value"] for x in config["answer_scale"]["missing_reasons"]]}},
                "favorites":{"type":"array","maxItems":5,"items":favorite},"disliked":{"anyOf":[negative,{"type":"null"}]},
                "supplement":{"type":"array","uniqueItems":True,"items":{"enum":[x["value"] for x in config["supplement"]["options"]]}},
                "background":{"type":"object","properties":{q["id"]:{"type":"array","uniqueItems":True,"items":{"enum":[o["value"] for o in q["options"]]}} for q in config["background_questions"]},"additionalProperties":False},
                "applicability":{"type":"object","properties":{m:{"enum":[s["value"] for s in config["branch_applicability"]["statuses"]]+["not_provided"]} for m in config["branch_applicability"]["modules"]},"additionalProperties":False},
                "followups":{"type":"object","properties":{q["id"]:choice(q) for q in config["followup_questions"]},"additionalProperties":False}}}


def main():
    if hasattr(sys.stdout,"reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    cfg=load_config()
    write("docs/02-questionnaire.md",questionnaire(cfg))
    write("docs/02-player-form.md",player_form(cfg))
    write("docs/04-archetypes-and-reports.md",handbook(cfg))
    write("config/answer.schema.json",json.dumps(response_schema(cfg),ensure_ascii=False,indent=2)+"\n")
    reports={}
    for case in ("A","B","C"):
        raw=json.loads((ROOT/"examples"/f"{case}.json").read_text(encoding="utf-8"))
        report=build_report(raw,cfg)
        write_report(report,cfg,ROOT/"reports",case)
        reports[case]=report
    for l,r in (("A","B"),("A","C")):
        write_comparison(compare_reports(reports[l],reports[r],cfg),cfg,ROOT/"reports",f"{l}-{r}")
    lines=["# 游格专项边界答卷","","以下答卷全部虚构，只用于规则验收，不是研究样本。","","| 答卷 | 基础分类 | 最终摘要 | 有效题数 | 主型单题稳定 | 副偏好单题稳定 |","|---|---|---|---:|---|---|"]
    special_files=sorted((ROOT/"examples"/"special").glob("*.json"))
    for file in special_files:
        report=build_report(json.loads(file.read_text(encoding="utf-8")),cfg)
        write_report(report,cfg,ROOT/"reports"/"special",file.stem)
        stable=lambda value:'资料不足' if value is None else ('是' if value else '否')
        lines.append(f"| [{file.stem}](special/{file.stem}.md) | {report['classification']['category']} | {report['display']['title']} | {report['quality']['valid_n']}/32 | {stable(report['sensitivity']['primary_stable'])} | {stable(report['sensitivity']['secondary_stable'])} |")
    lines += ["","`all_neutral`与`all_missing`会得到不同结果：前者八维为50分，后者八维均资料不足。`many_neutral_signal`保留少量但明确的局部高偏好。`fractional_gap`和`fractional_outside`分别验证约8.3333分、10.4167分的门槛内外分差。","",
              "原始答卷在examples/special；每份Markdown末尾含逐维算式与变化示例，同名JSON保存完整证据和敏感性列表。",""]
    write("reports/boundaries.md","\n".join(lines))
    print(f"已生成完整问卷、参与者版、原型文案、结构约束、三份报告、两份双人对照及{len(special_files)}份边界报告。")
    if "--no-verify" not in sys.argv:
        subprocess.run([sys.executable,str(ROOT/"scripts"/"verify_release.py")],cwd=ROOT,check=True)


if __name__=="__main__":
    main()
