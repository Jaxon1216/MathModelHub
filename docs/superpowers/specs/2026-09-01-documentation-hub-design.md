# MathModelHub 纯文档化设计

## 目标

将 MathModelHub 从比赛运行时记录仓库改造成数学建模资源文档中心。仓库只保留 Markdown 文档和必要的仓库元文件，不保存比赛数据、论文、图片、代码、Notebook、模板二进制或可执行 Skill 包。

## 信息边界

MathModelHub 负责回答四类问题：

1. 数学建模任务应该采用什么工作流。
2. 两套 `mathmodel-skill` 分别适合什么团队和交付目标。
3. 常见结果应该选择什么图表，以及去哪里取得模板。
4. 如何从读题推进到建模、验证、写作和最终验收。

具体实现继续由以下独立上游项目维护：

- `mma-chart-templates`：数学建模数据图模板和样张。
- `mathmodel-skill/MathModel-Skill`：强调正式交付、证据门禁和 Word 成稿的完整工作流。
- `mathmodel-skill/MathModeling-skills`：强调人在环决策、风险探针和多重审计的工作流。

本仓库只提炼、比较和链接这些项目，不复制其源码、Skills 或资源文件。

## 最终结构

```text
MathModelHub/
├── README.md
├── CONTRIBUTING.md
├── LICENSE
└── docs/
    ├── index.md
    ├── getting-started.md
    ├── workflows/
    │   ├── index.md
    │   ├── formal-delivery.md
    │   └── human-in-the-loop.md
    ├── charts/
    │   ├── index.md
    │   └── selection-guide.md
    ├── guides/
    │   ├── modeling-lifecycle.md
    │   ├── evidence-and-reproducibility.md
    │   └── paper-quality-checklist.md
    └── project/
        ├── upstream-resources.md
        └── maintenance.md
```

`docs/superpowers/` 是本次迁移的设计与实施记录，完成后也属于项目文档。

## 删除范围

彻底删除：

- `competitions/` 与所有未提交比赛产物。
- `Simulation/`。
- `past_problems/` 中的赛题、论文和数据。
- `data_analysis/` 中的 Notebook、数据和运行示例。
- `templates/` 中的 LaTeX、Typst、Word 和编译产物。
- `notes/`、`Ada's notes/` 等个人比赛笔记。
- `.cursor/`、`.claude/`、`.vscode/`、`.venv/` 等本地运行配置。
- `setup.py`、`requirements.txt`、Python 脚本、图片和其他非文档文件。
- 面向旧比赛仓库或未落地产品的旧文档。

可复用内容不保留原文件，而是提炼进新的通用指南。

## 内容原则

- 每篇文档有明确读者和入口，避免重复描述同一流程。
- 对上游项目做能力比较，不宣称 Hub 自己实现这些能力。
- 所有路径使用父级 `mma` 工作区中的真实相对位置，并同时给出远程仓库链接。
- 不收录无法说明来源的论文、模板和二进制资产。
- 不使用比赛年份、队员姓名或某一届赛题作为导航主结构。

## 验收标准

- Git 跟踪文件除 `LICENSE`、`.gitignore` 等元文件外全部为 `.md`。
- 仓库中不存在比赛、模拟、数据、代码、Notebook、图片、PDF、Word 或模板目录。
- README 能在三次点击以内进入工作流、图表和质量检查文档。
- 两套 mathmodel-skill 的定位、选择条件和差异清晰可见。
- 15 类 mma-chart-templates 图表均在选型文档中有场景说明。
- Markdown 相对链接通过自动检查。
