# 游格专项边界答卷

以下答卷全部虚构，只用于规则验收，不是研究样本。

| 答卷 | 基础分类 | 最终摘要 | 有效题数 | 主型单题稳定 | 副偏好单题稳定 |
|---|---|---|---:|---|---|
| [all_high](special/all_high.md) | all_high | 多面倾向：多种体验都有吸引力 | 32/32 | 是 | 是 |
| [all_low](special/all_low.md) | all_low | 暂无明确原型：本次吸引点偏少 | 32/32 | 是 | 是 |
| [all_missing](special/all_missing.md) | partial | 局部偏好画像 | 0/32 | 资料不足 | 资料不足 |
| [all_neutral](special/all_neutral.md) | no_clear | 暂无明显主型 | 32/32 | 是 | 是 |
| [boundary](special/boundary.md) | single | 暂定偏好组合 | 32/32 | 否 | 是 |
| [exact_tie](special/exact_tie.md) | dual | 迷雾探险家 ＋ 策略规划师 | 32/32 | 是 | 是 |
| [fractional_gap](special/fractional_gap.md) | dual | 暂定偏好组合 | 30/32 | 否 | 否 |
| [fractional_outside](special/fractional_outside.md) | single | 暂定偏好组合 | 31/32 | 否 | 否 |
| [many_neutral_signal](special/many_neutral_signal.md) | single | 迷雾探险家 | 32/32 | 是 | 是 |
| [partial](special/partial.md) | partial | 局部偏好画像 | 30/32 | 资料不足 | 资料不足 |
| [three_valid](special/three_valid.md) | no_clear | 暂无明显主型 | 24/32 | 是 | 是 |

`all_neutral`与`all_missing`会得到不同结果：前者八维为50分，后者八维均资料不足。`many_neutral_signal`保留少量但明确的局部高偏好。`fractional_gap`和`fractional_outside`分别验证约8.3333分、10.4167分的门槛内外分差。

原始答卷在examples/special；每份Markdown末尾含逐维算式与变化示例，同名JSON保存完整证据和敏感性列表。
