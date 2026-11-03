# 游格配置 答卷与证据数据契约

所有文件为UTF-8 JSON。主配置`config/youge.v0.2.0.json`是题目、选项、原型和文案的内容来源；说明文档中的题库与规则目录从它生成。

## 版本和输入

`versions`保存instrument、scoring、report_rules、catalog四项。本版均为0.2.0。完整答卷必须与所用配置匹配，不静默拿新规则重算旧答卷。研究IPIP源文件有独立版本，不与游格混用。

| 字段 | 类型 | 含义 |
|---|---|---|
| respondent_id、display_name | 字符串 | 玩家代号和展示名；模拟样例不含真实身份 |
| fictional | 布尔值 | 模拟样例为true |
| versions | 四项版本对象 | 对应生成时使用的配置 |
| core | 题号到整数或null的对象 | 32道核心题；缺少的题号归为未回答，未知题号报错 |
| core_missing_reasons | 题号到原因代码 | 只能引用真实缺失题，不能覆盖已有数值 |
| favorites | 0—5项作品记录 | 每项含title、experience、最多两项attractions，可有game_id、edition和note |
| disliked | null或单项作品记录 | 必须亲玩，含1—2项明确原因 |
| supplement | 代码列表 | 十项补充体验中的选择；空列表不表示厌恶 |
| background | B01和B02的多选值 | 平台与接触机会，不计分 |
| applicability | 五模块到状态的对象 | 适用、缺乏经历、不适用、跳过或未提供 |
| followups | 题号到选择的对象 | 只允许已适用且前置条件满足的答案 |

单选使用选项代码，多选使用不重复代码列表。M02使用`{"basis":"actual或hypothetical","purposes":["用途代码"]}`。没有实际经历时不得标actual；同一条回答不混合实际经历与假设意愿。

追问没有选择时省略该题或传null；多选追问一旦提供则至少有一项。补充体验清单的空列表只表示没有记录所选体验，不生成负面判断。

R02根据R01进入愿意／有条件愿意或更想新作／不愿意分支。正向原因与不愿意原因分开呈现；R01不明确时R02不触发。R03独立记录时间约束，不能反向改写意愿。

## 模块状态

完整报告中的`branch_status`由入口及前置答案重新计算，不能用调用方传入的隐藏状态覆盖：answered已回答；unanswered适用但未答；not_triggered前置条件未触发；no_experience缺乏经历；not_applicable不适用；prefer_skip选择跳过；not_provided未声明适用性。

明确不喜欢由具体选项保存，例如R01的not_interested和M01的not_interested。它们与任何跳过或未触发状态都不同。未适用却夹带追问答案时报错，避免使用隐藏的陈旧选择。

## 作品身份与重复

字典只是模拟用最小别名集，不包含真实作品的玩家人格标签。已知别名按作品ID归并；未知作品保留原名称，生成确定的custom: ID，不猜测系列或游戏类型。

同作品同版本重复填写时合并，保留原话。亲玩状态冲突或吸引点合并后超过两项时要求先澄清该记录，不静默丢弃选择。同一作品的不同版本可以保留，但不能当成两款不同作品凑成共同吸引的证据。续作与重制应建立各自作品ID及系列信息。

## 规则和文案

`report_rules`中的条件支持all、any、not组合，以及eq、in、contains、gte、lte、exists运算。可读取scores、positive_counts和followups；文案规则不能回写计分。

每条规则包含id、section、priority、condition、evidence、text，以及去重分组和可选覆盖维度。多场景证据选择器指定维度、最低题目值和最少题数。先按优先级，再按规则ID稳定排序；已被组合覆盖的单维判断不重复占据前三条。

作品重复、摘要和双人协商等派生规则登记在`derived_report_rules`；实际文字在`system_templates`和`advice_topics`。派生算法的精确行为由本版参考实现与边界样例共同约束。

## 报告证据

每条具体判断保留rule_id、condition_snapshot、evidence_refs和scope。证据包括实际核心答案、维度的算式及全部题号、具体追问、作品吸引点、明确负面原因或补充选择。

证据引用不存在或把缺失核心答案当成直接偏好证据时，报告生成失败。一般协商建议允许没有答案依据，但必须标为needs_confirmation，不能声称已经知道玩家的选择。

报告还保存规范化答卷、未舍入分、基础分类、呈现分类、完整敏感性变化及版本指纹。指纹只检查答卷和版本是否相同，不是测量有效性的证据，也不用于推断身份。

## 可读取的入口

`score_core`只接收核心答案；`build_report`接收完整答卷；`compare_reports`接收两份报告。研究距离位于独立的research模块，不被单人或双人报告调用。

答卷JSON结构约束负责字段形状；跨字段的版本、分支、重复身份和条件检查以参考实现为准。后续网站移植时必须运行同一套样例和预期结果，不能仅重新绘制页面。
