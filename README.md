# 游格 · 本命游戏玩家人格 v0.4

## GitHub 与线上部署

源码仓库：<https://github.com/niziyu0430-ux/youge>。网站需要 Python 后端，不能直接用 GitHub Pages 运行。Render 免费验证版配置见 `render.yaml`；登录密码在 Render 的 `YOUGE_ACCESS_PASSWORD` 秘密环境变量中设置，不随源码公开。完整部署、域名切换与后续题库同步见[部署维护说明](docs/19-deployment.md)。

本仓库保留在用网页、人物素材、作品目录、所有题包历史、源码、文档和维护脚本。下载缓存、临时输出、批量审查中间文件及大体积生成报告留在本地，不影响现有网站运行。

人格侧写已更新为 **0.4.1**：16种人格分别展开动机、思考方式、相处期待与可能的摩擦；结果页和下载长图统一为“你的性格底色”“与你相处的方式”两部分，移除答案依据与计分明细的展示。旧答卷可直接查看新版侧写，问卷与计分仍为0.4.0。

[16个人格完整侧写](docs/15-v0.4.1-personality-portraits.md) · [两部分报告示例](reports/v0.4.1/A.md) · [公开参考与写作取舍](research/personality-writing-v0.4.1.md)

网站已实现，可以先在本机完整测试。双击 [启动游格.cmd](启动游格.cmd)，或运行 `python -m youge.web --port 8765`，然后打开 **http://127.0.0.1:8765**。

选择一款本命游戏 → 16道四选一 → 必要时最多2道补问 → 一个明确的玩家外号与专属3D卡通角色。已经移除旧版五选项、多选清单和条件表单。选项只写具体行动，不附人格、维度或计分提示。

作品库已扩充为 **v0.5：59类、每类不设数量上限**。以原生PC游戏为主，保留知名主机作品；支持中文名、英文名、简称、简繁体和版本区分。无可核实中文名但有至少50篇中文评测的圈层作品采用原名加中文说明；证据不足的作品先放候选。最新计数见[分类清单](exports/游格-游戏分类清单.md)，维护口径见[扩充说明](docs/16-v0.5-catalogue.md)。8款熟悉作品的专用情境题和原有答卷继续兼容。

当前完整专属题已覆盖195条游戏记录，共194套作品题包、2328个基础题位，含模式与替代题6292个情境。每次12道专属题＋4道跨游戏题，最多2道补问；旧答卷按原版本读取。[当前全部题目](exports/游格-已重写游戏题库.md) · [使用与版本说明](docs/18-game-specific-questionnaires.md) · [全库重写进度](exports/游格-专属题重写进度.md)。正式库另1,983条仍待逐款重写，候选库1,546条待核实与编写。

2026-10-31本轮重写后已逐条核对实际取题内容：2,178条正式记录中，195条完整专属、1,983条未达完整标准；候选库另行记录。[逐游戏检查清单](exports/游格-逐游戏专属题检查清单.md) · [全部剩余待办](research/question-design-v0.5/rewrite-queue.json)。只替换游戏名或打乱选项顺序不算专属题。

| 新版交付 | 入口 |
|---|---|
| 本地使用、续答、导出、双人对照 | [网站说明](docs/08-local-website.md) |
| 不限分类容量的完整目录与来源 | [作品目录](docs/12-v0.4-games.md)、[待核实候选](exports/游格-待核实游戏候选清单.md) |
| 完整题目、条件、唯一人格与计分 | [题库与计分](docs/13-v0.4-questionnaire-and-scoring.md) |
| 16个人格与角色设定 | [人格手册](docs/10-v0.4-personas.md) |
| 理解测试、120人试用、两周重测 | [试测与研究](docs/14-v0.4-trial-and-review.md) |
| 可逐题相加复核的虚构A/B/C | [新版模拟报告](reports/v0.4/README.md) |
| 网站直接读取的内容与作品配置 | [旧题库JSON](config/youge.v0.4.0.json)、[专属题JSON](config/question-packs.v0.5.0.json)、[作品JSON](config/games.v0.5.0.json) |
| 16幅原创人物的完整生成提示词与出处 | [素材清单](design/v0.4/portraits-manifest.json) |

原版文档、题库和答卷继续保留，网站另有 `index.v03.html` 旧版入口。各版记录分开保存，不按新题义解释旧答案。v0.4是原创探索版，仍待真人试测；称号描述游戏选择，不推断现实人格或能力。

## v0.2 原始内容包

这套内容用独立的情境题描绘游戏偏好，再用作品及其吸引点解释口味。它围绕三个问题展开：喜欢的不同游戏有什么共同点，同一作品为什么有不同玩法，以及哪些选择在不同情境中相对稳定。

本包已提供完整题库、确定性计分和报告规则、八个原型、双人对照、结构化配置、三份完整模拟报告与专项边界答卷。八维及展示阈值均为待试测模型；尚未招募真实玩家，也未验证口味与现实人格的关系。

## 从这里阅读

| 内容 | 文件 |
|---|---|
| 完整实施规格与验收映射 | [产品规格](docs/01-product-spec.md) |
| 32道完整核心题、作品表单、清单与12道追问 | [完整问卷](docs/02-questionnaire.md) |
| 计分、并列、缺失、中立与单题敏感性 | [计分规则](docs/03-scoring.md) |
| 八原型手册、报告模板与条件化文案 | [原型与报告手册](docs/04-archetypes-and-reports.md) |
| 作品、吸引点、画像及七项同游协商 | [双人规格](docs/05-comparison.md) |
| 12人理解测试、120人试用、40人重测及后续研究 | [试测与研究方案](docs/06-research.md) |
| 答卷、配置、证据与版本的数据契约 | [数据契约](docs/07-data-contract.md) |
| 真实执行的检查结果 | [验收记录](reports/verification.md) |

## 先看三份完整模拟报告

- [玩家A](reports/A.md)：探索与攻略并存，挑战与舒缓并存，有二刷兴趣但时间受限。
- [玩家B](reports/B.md)：与A喜欢同样三款作品，但吸引点、八维画像与同游安排不同。
- [玩家C](reports/C.md)：与A喜欢不同作品，核心画像相同；Mod条件受限，且二刷受明显时间限制。
- [A与B双人对照](reports/A-B.md)、[A与C双人对照](reports/A-C.md)。
- [边界答卷总览](reports/boundaries.md)：全高、全低、并列、中立、缺失和容易翻转的称号。

模拟玩家和答卷均为虚构。真实作品名只用于演示填写和对齐，不预置游戏与人格的对应标签。

## 交给后续网站使用

- [完整配置](config/youge.v0.2.0.json)：32道核心题、12道追问、八维、原型、条件化文案、作品选项和版本。
- [空白答卷](config/answer-template.json)：可填入自己的答案；核心题缺失用null。
- [答卷结构约束](config/answer.schema.json)：字段形状；跨字段语义由参考实现检查。
- [示例原始答卷](examples/A.json)与[对应机器可读报告](reports/A.json)：每条判断保留触发快照与实际证据。
- [独立IPIP研究源文件](research/ipip50.zh-Hant.source-v1.json)：公开繁体译文50题和核对过的计分键，不进入游格计分。

后续实现应复用配置与确定性算法。改动题义、计分或文案条件时更新对应版本，保留旧版本答卷和报告。

## 本地复算

计分、报告判断和测试使用Python标准库；生成PNG图表额外使用Pillow。已生成的报告可直接阅读。

```powershell
python scripts/build_release.py
python -m unittest discover -s tests -v
python -m youge report config/answer-template.json --output my-report --stem my-result
python -m youge compare examples/A.json examples/B.json --output my-report --stem pair
```

空白答卷不含任何分数，直接运行会得到资料不足的局部画像。填写1—5整数后即可重新生成。PNG所需版本列在`requirements-render.txt`；无Pillow或中文字库时保留SVG图表。

独立研究源文件已经冻结，正常生成不联网。只有明确需要更新来源时才运行`freeze_ipip.py`，该命令拒绝覆盖已有冻结版本。


## 人物换装 V2（2026-10-28）

16位V2服装已接入本地网站，减少绿色主色与重复鞋款。人格图鉴和结果页可切回完整V1；导出长图使用当前造型。全套对照：`http://127.0.0.1:8765/wardrobe.html`。图片来源、完整提示词、配色与回退说明见 [design/v0.4.2/README.md](design/v0.4.2/README.md)。


## 首页与手机适配（2026-10-28）

16人人物栏已移到导航与主视觉之间，匀速循环，只显示画像和名字；旧四人卡片、三步流程及首页数量／进度说明已移除。其他页面与弹窗可返回首页，草稿保留。支持手机宽度、触控、暂停、键盘与减少动态效果。实现与验证见 [design/v0.4.3/README.md](design/v0.4.3/README.md)。



## 共用密码登录版（2026-10-28）

打开网站必须先输入共用访问密码，当前页面内可不限次测试，刷新后重新登录。初始密码见 `.local/access-password.txt`；修改密码运行 `python -m youge.access set-password`。说明见 [docs/17-shared-password-login.md](docs/17-shared-password-login.md)。
