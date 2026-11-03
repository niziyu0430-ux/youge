"""Publish reader essays and sources separately from internal answer/audit records."""
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from youge import v04


def main():
    c=v04.config();folder=ROOT/'reports/v0.4.1';folder.mkdir(parents=True,exist_ok=True)
    manual=['# 游格16人格侧写 v0.4.1','','本轮只调整人格侧写和结果展示，题目、选项权重、人格归类与角色图片保留。报告统一为两个主板块，移除页面、人物介绍和下载长图中的答案依据、四区分栏与计分明细。','','描述从游戏动机展开为自主感、意义感、掌握感、秩序、连接等性格主题，包含思考方式、关系期待与可能的摩擦；它是供自我对照的原创类型侧写，不把游戏偏好当作现实人格已经得到验证的证据。','','旧0.4.0答卷只更新文案版本为0.4.1，核心题库、计分、作品版本仍为0.4.0；原答案、补问题号及归类保留。内部结构化答案与计分记录继续供维护使用，不进入结果页或长图。','']
    for p in c['personas']:
        profile=c['personality_portraits']['personas'][p['id']]
        manual+=['## '+p['name'],'',profile['headline'],'',' / '.join(profile['traits']),'','> '+profile['credo'],'','### 你的性格底色','',*sum(([t,''] for t in profile['inner_world']),[]),'### 与你相处的方式','',*sum(([t,''] for t in profile['with_others']),[])]
    for case in 'ABC':
        d=v04.demo(case);r=d['report'];lines=['# '+r['display_name']+' · '+r['persona']['name'],'','**虚构示例，仅用于展示格式。**','',r['one_line'],'','本命作品：《'+r['game']['title']+'》。','','> '+r['personality_profile']['credo'],'']
        for s in r['report_sections']:lines+=['## '+s['title'],'',*sum(([p,''] for p in s['paragraphs']),[])]
        lines += [r['scope_note'],'']
        (folder/(case+'.md')).write_text('\n'.join(lines),encoding='utf-8')
        (folder/(case+'.json')).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'docs/15-v0.4.1-personality-portraits.md').write_text('\n'.join(manual),encoding='utf-8')
    types=[('INTJ','Architect','动机如何形成判断，并影响相处'),('INTP','Logician','把思考过程写成连贯的行动方式'),('ENTJ','Commander','追求、行动与协作代价来自同一习惯'),('ENTP','Debater','尝试可能性，也讨论完成与承诺'),('INFJ','Advocate','价值需要与关系边界一起展开'),('INFP','Mediator','连接认同、意义和实际行动'),('ENFJ','Protagonist','关心与介入之间有需要协商的边界'),('ENFP','Campaigner','外在活力之后仍有深层需要'),('ISTJ','Logistician','从约定和实践写出持续的行为逻辑'),('ISFJ','Defender','细节与长期投入，以及付出的边界'),('ESTJ','Executive','结构可以支持行动，也需要接纳差异'),('ESFJ','Consul','重视回应，同时允许不同期待'),('ISTP','Virtuoso','直接经验、个人节奏与沟通方式'),('ISFP','Adventurer','表达、自主与他人评价的关系'),('ESTP','Entrepreneur','即时行动与后果之间的取舍'),('ESFP','Entertainer','共同感受与长线安排的联系')]
    sources=['# 人格侧写的公开参考与写作取舍','','查阅日期：2026-10-27。','','参考了 [Myers & Briggs Foundation类型概览](https://www.myersbriggs.org/my-mbti-personality-type/the-16-mbti-personality-types/) 以及下列16Personalities公开介绍。Architect等外号来自16Personalities，未把其测量框架、MBTI或游格16类一一对应。学习的是叙述如何展开动机、思考、关系和代价；游格正文围绕自己的游戏动机原创，没有翻译或替换原文人格名。','','| 查阅的介绍 | 留意的写作方式 |','|---|---|']
    sources += [f'| [{code} · {name}](https://www.16personalities.com/{code.lower()}-personality) | {note} |' for code,name,note in types]
    sources += ['','落地结构为“你的性格底色”“与你相处的方式”两个主板块；各人格同时保留动机、选择方式、值得留意的代价与相处建议。问卷中的明确习惯只作简短个性化补充，不堆回攻略、Mod、二刷等独立卡片。','','表达中避免天生聪明、道德高低、职业命定、诊断、现实关系结论等无依据断言。游戏中的投入方式提供解读视角，现实中的自己可以认同、修正或保留不同意见。','']
    (ROOT/'research/personality-writing-v0.4.1.md').write_text('\n'.join(sources),encoding='utf-8')
    print('Built all 16 essays, 3 fictional two-chapter reports and 17 primary reference links.')


if __name__=='__main__':main()
