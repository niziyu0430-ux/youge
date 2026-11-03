"""Portable Markdown reports and fixed-scale static horizontal charts."""

from __future__ import annotations

import html
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


def _escape(value):
    return str(value).replace("|", "\\|").replace("\n", " ").replace("<", "&lt;").replace(">", "&gt;")


def _number(value):
    return "资料不足" if value is None else format(Decimal(str(value)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP), "f")


def _evidence_lines(refs, registry):
    lines = []
    for ref in refs:
        ev = registry[ref]
        if ev["source"] == "core":
            lines.append(f"{ev['question_id']}「{ev['context']}」＝{ev['value']}（{ev['label']}）")
        elif ev["source"] == "dimension":
            lines.append(f"{ev['name']}＝{_number(ev['score'])}，有效{ev['valid_n']}/4题")
        elif ev["source"] == "followup":
            lines.append(f"{ev['question_id']}：{ev['label']}")
        elif ev["source"] in ("attraction", "negative_game"):
            lines.append(f"《{ev['title']}》：{ev['label']}")
        elif ev["source"] == "supplement":
            lines.append(f"补充清单：{ev['label']}")
    return "；".join(lines)


def _claim_markdown(claim, evidence):
    text = _escape(claim["text"])
    basis = _escape(_evidence_lines(claim["evidence_refs"], evidence))
    return [text, "", f"依据：{basis}。", "", f"规则：`{claim['rule_id']}`。", ""]


def report_markdown(report, config, chart_path=None):
    evidence = report["evidence"]
    name = _escape(report["display_name"])
    lines = [f"# 游格玩家偏好报告 {name}", ""]
    if report["fictional"]:
        lines += ["**虚构模拟报告：玩家、答卷及其口味原因均为人工构造，不是研究样本。**", ""]
    lines += [f"版本：题库 {report['versions']['instrument']}；计分 {report['versions']['scoring']}；文案 {report['versions']['report_rules']}；作品字典 {report['versions']['catalog']}。", "",
              "## 原型摘要", "", f"**{report['display']['title']}**", "", report["display"]["one_line"], ""]
    if report["display"]["secondary_names"]:
        lines += ["副偏好：" + "、".join(report["display"]["secondary_names"]) + "。", ""]
    if report["display"]["secondary_candidate_names"]:
        lines += ["副偏好候选（不排序）：" + "、".join(report["display"]["secondary_candidate_names"]) + "。", ""]
    for note in report["display"]["notes"]:
        lines += [note, ""]
    if report["behavior_tags"]:
        lines += ["行为标签：" + "；".join(_escape(t["text"]) for t in report["behavior_tags"]) + "。", ""]
        for tag in report["behavior_tags"]:
            lines += [f"- {_escape(tag['text'])}：{_escape(_evidence_lines(tag['evidence_refs'], evidence))}。", ""]
    lines += ["摘要依据：下方八维分数与有效题数；称号仅为连续画像的展示摘要。", ""]
    lines += ["## 具体判断与答案依据", ""]
    for i, claim in enumerate(report["insights"], 1):
        lines += [f"### 判断 {i}", "", *_claim_markdown(claim, evidence)]
    if report["insight_gap"]:
        lines += [config["system_templates"]["insight_gap"], ""]
    lines += ["## 八维问卷偏好分", "", "固定0—100坐标；分数不是百分位、能力分或人格准确率。", ""]
    if chart_path:
        lines += [f"![八维横向条形图]({chart_path})", ""]
    lines += ["| 维度 | 分数 | 有效题数 |", "|---|---:|---:|"]
    for dim in config["dimensions"]:
        row = report["scores"][dim["id"]]
        lines.append(f"| {dim['name']} | {_number(row['score'])} | {row['valid_n']}/4 |")
    lines += ["", "## 你喜欢的这些游戏有什么共同点", "", report["taste"]["note"], ""]
    exp_labels = {"yes": "亲自体验过", "no": "未亲自体验", "unknown": "亲玩状态无法确认"}
    tag_labels = {x["id"]: x["label"] for x in config["taste"]["attractions"]}
    if report["response"]["favorites"]:
        lines += ["| 喜欢的作品 | 体验状态 | 自填吸引点 |", "|---|---|---|"]
        for game in report["response"]["favorites"]:
            lines.append(f"| {_escape(game['title'])} | {exp_labels[game['experience']]} | {'、'.join(tag_labels[t] for t in game['attractions']) or '未填写'} |")
        lines.append("")
    for claim in [*report["taste"]["claims"], *report["taste"]["alignment"]]:
        lines += _claim_markdown(claim, evidence)
    for raw in report["taste"]["free_text"]:
        lines += [f"玩家原话《{_escape(raw['title'])}》：“{_escape(raw['text'])}”", "", raw["policy"] + "。", ""]
    lines += ["## 容易享受的体验与需要留意的体验", "", "### 有明确支持的吸引点", ""]
    if report["enjoyments"]:
        for claim in report["enjoyments"]:
            lines += _claim_markdown(claim, evidence)
    else:
        lines += ["本次尚无满足多场景证据条件的维度吸引点，保留具体回答供核对。", ""]
    if report["supplement"]:
        lines += ["补充体验清单：", ""]
        for claim in report["supplement"]:
            lines += [f"- {_escape(claim['text'])}（依据：补充清单明确选择；不计入八维）。", ""]
    lines += ["### 有明确依据的消耗点或条件", ""]
    if report["drains"]:
        for claim in report["drains"]:
            lines += _claim_markdown(claim, evidence)
    else:
        lines += [config["system_templates"]["no_drains"], ""]
    lines += ["## 具体同游建议", "", "有直接回答时，建议按这些边界协商；资料不足的项目只是待确认事项。", ""]
    for advice in report["advice"]:
        lines += [f"### {advice['title']}", "", advice["text"], ""]
        if advice["basis"] == "explicit_answer":
            lines += ["依据：" + _escape(_evidence_lines(advice["evidence_refs"], evidence)) + "。", ""]
        else:
            lines += ["资料状态：未提供明确的可用选择；这不是对你的偏好判断。", ""]
    lines += ["## 现实习惯自我核对", "", "下面仅是自我核对问题，不计分，也不直接形成现实人格结论。", ""]
    if report["self_checks"]:
        for claim in report["self_checks"]:
            lines += _claim_markdown(claim, evidence)
    else:
        lines += ["当前没有足够依据生成个性化核对问题。", ""]
    lines += ["## 原始答卷与逐维复算", "", "只用有效核心答案求平均。每维至少三题有效；null不计入分母。", "",
              "| 维度 | 四题原始答案，按01—04 | 有效总和／题数 | 平均分 | 25×平均分减25 |", "|---|---|---:|---:|---:|"]
    for dim in config["dimensions"]:
        row = report["scores"][dim["id"]]
        raw = "，".join(f"{qid}={row['answers'][qid] if row['answers'][qid] is not None else 'null'}" for qid in dim["question_ids"])
        mean = f"{row['mean']:.6f}".rstrip("0").rstrip(".") if row["mean"] is not None else "—"
        lines.append(f"| {dim['name']} | {raw} | {row['sum']}/{row['valid_n']} | {mean} | {_number(row['score'])} |")
    lines += ["", "### 条件追问原始选择", "", "| 题号 | 状态 | 实际答案 |", "|---|---|---|"]
    status_labels = {"answered": "已回答", "unanswered": "适用但未回答", "not_triggered": "前置条件未触发", "not_provided": "未声明适用性", "no_experience": "缺乏经历", "not_applicable": "不适用", "prefer_skip": "选择跳过"}
    for q in config["followup_questions"]:
        ev = evidence.get(f"answer:{q['id']}")
        lines.append(f"| {q['id']} | {status_labels[report['response']['branch_status'][q['id']]]} | {_escape(ev['label']) if ev else '—'} |")
    if report["response"]["disliked"]:
        negative = report["response"]["disliked"]
        labels = {x["value"]: x["label"] for x in config["taste"]["negative_reasons"]}
        lines += ["", f"未喜欢作品：《{_escape(negative['title'])}》；亲自体验；原因：{'、'.join(labels[r] for r in negative['reasons'])}。", ""]
    if report['sensitivity']['applicable']:
        sensitivity_text=f"枚举了{report['sensitivity']['tested_changes']}个合法单题变化；主型或领先组{'保持不变' if report['sensitivity']['primary_stable'] else '可能改变'}；副偏好{'保持不变' if report['sensitivity']['secondary_stable'] else '可能改变'}。"
    else:
        sensitivity_text=f"枚举了{report['sensitivity']['tested_changes']}个有效答案的合法单题变化；完整画像仍有缺失，本次不评价完整称号是否稳定。"
    lines += ["", "### 单题敏感性与答题分布", "", sensitivity_text, "",
              report["sensitivity"]["interpretation"], "",
              f"有效核心答案{report['quality']['valid_n']}/32；中立答案{report['quality']['neutral_n']}；1—5分分布：{json.dumps(report['quality']['response_distribution'], ensure_ascii=False)}。", ""]
    if report["quality"]["many_neutral"]:
        lines += [config["system_templates"]["neutral_note"], ""]
    if report["quality"]["same_option_repeated"]:
        lines += [config["system_templates"]["repeat_note"], ""]
    if report["sensitivity"]["changes"]:
        lines += ["可人工核对的变化示例：", "", "| 题号 | 原答案→新答案 | 主型或领先组改变 | 副偏好改变 |", "|---|---|---|---|"]
        for change in report["sensitivity"]["changes"][:8]:
            lines.append(f"| {change['question_id']} | {change['from']}→{change['to']} | {'是' if change['primary_changed'] else '否'} | {'是' if change['secondary_changed'] else '否'} |")
        lines += ["", "完整变化列表保存在同名JSON报告中。", ""]
    lines += ["## 解释范围", ""]
    lines += [f"- {text}" for text in report["limitations"]]
    lines += ["", f"答卷与版本指纹：`{report['answer_fingerprint']}`。", ""]
    return "\n".join(lines)


def comparison_markdown(comparison, config, chart_path=None):
    if comparison["status"] != "comparable":
        return "# 游格双人对照\n\n" + comparison["text"] + "\n"
    lines = [f"# 游格双人对照 {comparison['left_name']}与{comparison['right_name']}", ""]
    if comparison["fictional"]:
        lines += ["**虚构模拟对照；不代表真实玩家、研究数据或契合度验证。**", ""]
    lines += [comparison["note"], "", "## 共同喜欢的作品与各自原因", ""]
    if comparison["common_games"]:
        lines += ["| 作品 | 左侧玩家的吸引点 | 右侧玩家的吸引点 | 共同吸引点 |", "|---|---|---|---|"]
        for game in comparison["common_games"]:
            lines.append(f"| {_escape(game['title'])} | {'、'.join(game['left_attractions']) or '未填写'} | {'、'.join(game['right_attractions']) or '未填写'} | {'、'.join(game['shared_attractions']) or '当前未重合'} |")
        lines += ["", "亲玩依据：", ""]
        exp = {"yes": "亲自体验", "no": "未亲自体验", "unknown": "状态未确认"}
        for game in comparison["common_games"]:
            lines += [f"- 《{_escape(game['title'])}》：左侧{exp[game['left_experience']]}；右侧{exp[game['right_experience']]}。", ""]
    else:
        lines += ["本次清单没有同作品同版本的重合；不能据此推断双方口味相反或性格不同。", ""]
    if comparison["related_editions"]:
        lines += ["同作不同版本记录：", ""]
        for game in comparison["related_editions"]:
            lines += [f"- 《{_escape(game['title'])}》：{_escape(game['left_edition'])}／{_escape(game['right_edition'])}，单独保留，不计作同版本共同作品。", ""]
    lines += ["## 独立测得的八维画像", "", "分数只来自双方各自的核心题。差异不是合作能力评价。", ""]
    if chart_path:
        lines += [f"![双人八维横向条形图]({chart_path})", ""]
    lines += ["| 维度 | 左侧分数／有效题数 | 右侧分数／有效题数 |", "|---|---:|---:|"]
    for row in comparison["profile_rows"]:
        lines.append(f"| {row['name']} | {_number(row['left_score'])} / {row['left_valid_n']} | {_number(row['right_score'])} / {row['right_valid_n']} |")
    lines += ["", "## 一起玩之前的协商事项", ""]
    for topic in comparison["coordination"]:
        lines += [f"### {topic['title']}：{topic['status_label']}", "",
                  f"左侧：{_escape(topic['left_answer'])}。", "", f"右侧：{_escape(topic['right_answer'])}。", "",
                  topic["recommendation"], "", f"规则：`{topic['rule_id']}`；证据：{'、'.join(topic['evidence_refs']) or '资料不足，先确认'}。", ""]
    return "\n".join(lines)


def _chart_rows(report, config):
    return [{"name": d["name"], "values": [report["scores"][d["id"]]["score"]], "valid": [report["scores"][d["id"]]["valid_n"]]} for d in config["dimensions"]]


def chart_svg(rows, names):
    pair = len(names) == 2
    row_height = 86 if pair else 58
    width, left, plot_width = 900, 155, 580
    height = 85 + len(rows) * row_height
    colors = ["#246B68", "#B46A3C"]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
           '<rect width="100%" height="100%" fill="#ffffff"/>',
           '<g font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif" fill="#263833">']
    out.append('<text x="24" y="28" font-size="17">问卷偏好分 · 固定0—100坐标</text>')
    for j, name in enumerate(names):
        out.append(f'<text x="{left+j*220}" y="50" fill="{colors[j]}" font-size="14">{html.escape(name)}</text>')
    for tick in (0, 25, 50, 75, 100):
        x = left + plot_width * tick / 100
        out += [f'<line x1="{x}" y1="70" x2="{x}" y2="{height-20}" stroke="#e6ece8"/>',
                f'<text x="{x}" y="67" text-anchor="middle" font-size="12">{tick}</text>']
    for i, row in enumerate(rows):
        y = 83 + i * row_height
        out.append(f'<text x="24" y="{y+18}" font-size="16">{html.escape(row["name"])}</text>')
        for j, value in enumerate(row["values"]):
            by = y + j * 29
            out.append(f'<rect x="{left}" y="{by}" width="{plot_width}" height="19" rx="3" fill="#f0f4f1"/>')
            if value is not None:
                out.append(f'<rect x="{left}" y="{by}" width="{plot_width*value/100:.4f}" height="19" rx="3" fill="{colors[j]}"/>')
            label = f'{_number(value)}  ({row["valid"][j]}/4)'
            out.append(f'<text x="{left+plot_width+14}" y="{by+15}" font-size="14">{label}</text>')
    return "\n".join(out + ["</g>", "</svg>", ""])


def _chart_png(rows, names, path):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return False
    fonts = [Path("C:/Windows/Fonts/msyh.ttc"), Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")]
    font_path = next((p for p in fonts if p.exists()), None)
    if font_path is None:
        return False
    pair = len(names) == 2
    row_height = 86 if pair else 58
    width, height, left, plot_width = 900, 85 + len(rows) * row_height, 155, 580
    scale = 2
    image = Image.new("RGB", (width*scale, height*scale), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(str(font_path), 15*scale)
    small = ImageFont.truetype(str(font_path), 13*scale)
    colors = ["#246B68", "#B46A3C"]
    def text(x, y, value, fill="#263833", small_text=False):
        draw.text((x*scale,y*scale), value, font=small if small_text else font, fill=fill)
    text(24, 7, "问卷偏好分 · 固定0—100坐标")
    for j, name in enumerate(names):
        text(left+j*220, 31, name, colors[j], True)
    for tick in (0,25,50,75,100):
        x=left+plot_width*tick/100
        draw.line((x*scale,74*scale,x*scale,(height-20)*scale), fill="#e6ece8", width=scale)
        text(x-8, 53, str(tick), small_text=True)
    for i,row in enumerate(rows):
        y=83+i*row_height
        text(24,y-1,row["name"])
        for j,value in enumerate(row["values"]):
            by=y+j*29
            draw.rounded_rectangle((left*scale,by*scale,(left+plot_width)*scale,(by+19)*scale),radius=3*scale,fill="#f0f4f1")
            if value is not None and value>0:
                draw.rounded_rectangle((left*scale,by*scale,(left+plot_width*value/100)*scale,(by+19)*scale),radius=3*scale,fill=colors[j])
            text(left+plot_width+14,by-2,f"{_number(value)}  ({row['valid'][j]}/4)",small_text=True)
    image.save(path)
    return True


def write_report(report, config, output_dir, stem):
    output_dir=Path(output_dir)
    charts=output_dir/"charts"
    charts.mkdir(parents=True,exist_ok=True)
    rows=_chart_rows(report,config)
    (charts/f"{stem}.svg").write_text(chart_svg(rows,[report["display_name"]]),encoding="utf-8")
    png=_chart_png(rows,[report["display_name"]],charts/f"{stem}.png")
    image=f"charts/{stem}.{'png' if png else 'svg'}"
    (output_dir/f"{stem}.md").write_text(report_markdown(report,config,image),encoding="utf-8")
    (output_dir/f"{stem}.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def write_comparison(comparison, config, output_dir, stem):
    output_dir=Path(output_dir)
    output_dir.mkdir(parents=True,exist_ok=True)
    chart_path=None
    if comparison["status"]=="comparable":
        charts=output_dir/"charts"
        charts.mkdir(exist_ok=True)
        rows=[{"name":r["name"],"values":[r["left_score"],r["right_score"]],"valid":[r["left_valid_n"],r["right_valid_n"]]} for r in comparison["profile_rows"]]
        names=[comparison["left_name"],comparison["right_name"]]
        (charts/f"{stem}.svg").write_text(chart_svg(rows,names),encoding="utf-8")
        png=_chart_png(rows,names,charts/f"{stem}.png")
        chart_path=f"charts/{stem}.{'png' if png else 'svg'}"
    (output_dir/f"{stem}.md").write_text(comparison_markdown(comparison,config,chart_path),encoding="utf-8")
    (output_dir/f"{stem}.json").write_text(json.dumps(comparison,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
