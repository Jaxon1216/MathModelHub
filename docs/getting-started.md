# 快速开始

MathModelHub 不要求安装依赖。先判断自己当前需要解决的问题，再进入对应入口。

## 1. 选择任务入口

### 我要完整推进一道赛题

先阅读[工作流选择](workflows/index.md)。

- 目标是形成正式 Word 成稿、强调固定阶段和格式门禁：选择 [MathModel-Skill](workflows/formal-delivery.md)。
- 希望每个关键判断都由团队确认、强调风险探针和审计：选择 [MathModeling-skills](workflows/human-in-the-loop.md)。

不要同时把两套完整工作流安装到同一个比赛目录。它们都有自己的目录契约、状态文件和流程控制，同时使用会产生职责冲突。

### 我只需要绘制结果图

直接阅读[图表选择指南](charts/selection-guide.md)，根据“比较、趋势、关系、分布、敏感性”等分析目的选择图形，再前往 `mma-chart-templates` 取得模板。

### 我正在制定团队流程

阅读[数学建模生命周期](guides/modeling-lifecycle.md)，把比赛拆成问题理解、路线决策、实现、证据冻结、写作和审计六个阶段。

### 我正在提交前验收

依次使用：

1. [证据与可复现性](guides/evidence-and-reproducibility.md)
2. [论文质量清单](guides/paper-quality-checklist.md)

## 2. 安装上游项目

Hub 不固定上游版本，也不代替上游安装说明。进入[上游资源](project/upstream-resources.md)，选择项目后按其 README 安装。

## 3. 建立自己的比赛工作区

比赛文件应放在单独的私有或团队仓库中，不要提交回 MathModelHub。工作区至少区分：

```text
problem/     # 原始题目和附件，只读
planning/    # 题意、假设、符号、模型路线
code/        # 可运行实现
results/     # 机器生成结果与图表
paper/       # 论文源文件
reviews/     # 检查报告与修改记录
```

具体目录以所选上游工作流为准。上面的结构只表达职责边界，不应覆盖上游项目的正式约定。
