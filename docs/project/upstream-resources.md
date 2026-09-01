# 上游资源

MathModelHub 只维护稳定说明和选型入口。安装、版本、许可证和具体命令始终以上游仓库为准。

## mma-chart-templates

- 远程仓库：[Jaxon1216/mma-chart-templates](https://github.com/Jaxon1216/mma-chart-templates)
- `mma` 工作区路径：`../mma-chart-templates`
- 定位：数学建模常见数据图的模板与人工审核样张。
- 在 Hub 中的入口：[图表资源目录](../charts/index.md)

适合已经知道分析目标、希望快速取得一致论文风格的团队。模板解决的是表现层，不替代统计方法选择和结果解释。

## MathModel-Skill

- 远程仓库：[yushui2022/MathModel-Skill](https://github.com/yushui2022/MathModel-Skill)
- `mma` 工作区路径：`../mathmodel-skill/MathModel-Skill`
- 定位：面向正式竞赛交付的完整 Agent-native 工作流。
- 在 Hub 中的入口：[正式交付型工作流](../workflows/formal-delivery.md)

适合需要阶段恢复、证据门禁、正式 Word 和格式验收的任务。选择 Standard、Lite 或其他分支前，应阅读上游的版本说明。

## MathModeling-skills

- 远程仓库：[zhnnky329/MathModeling-skills](https://github.com/zhnnky329/MathModeling-skills)
- `mma` 工作区路径：`../mathmodel-skill/MathModeling-skills`
- 定位：强调人工决策、风险探针、冻结数字和独立审计的工作流。
- 在 Hub 中的入口：[人在环审计型工作流](../workflows/human-in-the-loop.md)

适合不希望 AI 自动替代建模判断，并要求每个阶段留下可检查证据的团队。

## 同步原则

上游更新时，Hub 只同步影响选择和使用边界的信息。脚本名、Skill 数量、命令或目录结构若变化频繁，应链接到上游，不在 Hub 中维护易过期副本。
