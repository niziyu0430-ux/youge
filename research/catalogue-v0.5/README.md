# 作品库 v0.5 研究资料

本目录是 2026-10-28 扩充工作的可复查资料，当前运行文件为 `config/games.v0.5.0.json`。

| 文件或目录 | 用途 |
|---|---|
| manifest.json | 发现计划与用户确认的 50 篇中文评测门槛；种子中的拟议名称须核对身份，不直接变成公开名称 |
| searches/、discovered.json | Steam 公开搜索结果冻结；搜索返回也可能含相近作品，不直接当成最终分类依据 |
| products/ | 官方商店产品身份、英文与中文名、类型、PC 平台、标签、发行状态和汇总数据 |
| tag-definitions.json | Steam 中文标签定义 |
| chinese-reviews/ | 简体或简繁中文评测汇总，只保留数字、口径、日期和来源 |
| native-seeds.json、publishers/ | 原生 PC 端游与独立客户端的发行方线索、网页标题和匹配结果 |
| manual-native-evidence.json | 本轮通过网页工具核对的补充来源；区别于自动采集成功 |
| name-evidence*.json | 中英文名称对应的中文资料使用证据 |
| relationships.json | 明确核对的原版、重制版等关系；不按标题相似度自动合并 |
| identity-issues.json | 拟议种子与实际产品身份不符的线索；这些名称不会应用到错误作品 |
| excluded-products.json | 未验证为游戏、未验证原生 PC 或尚未发行等不进入本轮公开库的产品线索 |
| build-summary.json | 最新构建计数、名称状态和各分类容量 |

批量身份来自 Steam 的 `IStoreBrowseService/GetItems` 公开返回；语言评测的补充核对使用 [IUserReviewsService 官方文档](https://partner.steamgames.com/doc/webapi/IUserReviewsService)所列接口。身份判断和名称判断分别保存：英文种子的 ID 不匹配时，忽略拟议别名，不把别款作品的资料移植过来。

中文名称、中文受众与 PC 平台是不同的证据。达到评测门槛代表本轮允许展示，不代表整体市场份额、好评程度或 97% 偏好覆盖率。原版与版本条目保留独立 ID，因此本目录的条目数也不等于全部独立作品的去重总数。

数据构建默认离线。采集是显式维护动作，不在用户答题时执行。正常维护入口及验收说明见 `docs/16-v0.5-catalogue.md`。
