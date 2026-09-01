# MathModelHub Documentation Hub Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将现有比赛运行时仓库改造成只包含 Markdown 的数学建模资源 Hub。

**Architecture:** Hub 只维护导航、选型、方法论和质量门禁文档。图表模板与两套建模工作流继续由三个兄弟仓库独立维护，Hub 通过经过整理的文档链接到它们。

**Tech Stack:** Markdown、Git、shell 链接检查。

## Global Constraints

- 删除所有比赛和模拟内容。
- 不复制上游代码、Skill 包、图片或二进制模板。
- 保留并重写可复用的方法论。
- 最终直接提交并推送 `origin/main`。

---

### Task 1: 删除运行时资产

**Files:** 删除所有比赛、模拟、个人笔记、数据、模板、代码和旧产品文件。

- [ ] 删除 `competitions/`、`Simulation/`、`past_problems/`。
- [ ] 删除 Notebook、数据、图片、PDF、Word、模板和 Python 文件。
- [ ] 删除本地 IDE、虚拟环境和缓存目录。
- [ ] 确认用户要求删除的未跟踪比赛产物一并移除。

### Task 2: 建立文档信息架构

**Files:** 创建 `README.md`、`CONTRIBUTING.md` 与 `docs/` 下的导航、工作流、图表、指南和维护文档。

- [ ] 写入口 README 和文档索引。
- [ ] 写两套 mathmodel-skill 的独立说明和选择指南。
- [ ] 写图表目录与图表选型指南。
- [ ] 写生命周期、证据可复现和论文质量检查指南。
- [ ] 写上游资源与维护规则。

### Task 3: 验证纯文档约束

**Files:** 检查整个工作树。

- [ ] 列出所有 Git 跟踪文件，确认没有禁止格式。
- [ ] 搜索旧比赛路径、年份目录和个人角色残留。
- [ ] 检查 Markdown 相对链接均指向现有文件。
- [ ] 检查 Git diff，确认没有保留比赛运行时资产。

### Task 4: 发布

**Files:** Git 提交与远程分支。

- [ ] 创建一个完整迁移提交。
- [ ] 推送到 `origin/main`。
- [ ] 核对本地 HEAD 与远程 `origin/main` 一致。
