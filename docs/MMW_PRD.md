# MathModelWorkspace（MMW）— PRD & Technical Design

> AI-Native Mathematical Modeling Workspace
>
> 本文档定义 V1 的产品范围、技术架构、Skills 体系、验收标准与里程碑。

---

## 0. 文档元信息

| 项目 | 内容 |
|------|------|
| 项目名称 | **MathModelWorkspace** |
| 仓库名称 | `math-model-workspace`（新建独立仓库） |
| 交互方式 | Agent 驱动（零 CLI） |
| 原型参考 | `MathModelHub`（旧仓库不动，作为实战归档与素材来源） |
| 目标赛事 | 美赛（MCM/ICM）+ 国赛（CUMCM），兼容校赛与科研训练 |
| 核心原则 | IDE-first · Human-in-the-loop · Docker-native |

---

## 1. 项目定位

### 1.1 一句话

把数学建模从"临时拼凑环境 + 碎片化 AI 使用"升级为 **可复现、可协作、AI 增强的工程化工作流**。

### 1.2 是什么

- Docker 一键可复现运行环境
- IDE Skills 协同系统（Cursor / Claude Code / VS Code / Gemini CLI）
- Markdown → Typst → PDF 论文流水线
- Notebook 建模工作台 + 自动化验收
- 可选 Agent 自主模式：AI 按 workflow 自主推进

### 1.3 不是什么

- 不是"一键生成论文"的自动化工厂
- 不是自建模型 API / SaaS 平台
- 不替代人的建模判断、假设设计与结论解释

---

## 2. 核心理念

### 2.1 Human-in-the-loop

| AI 负责 | 人负责 |
|---------|--------|
| 题型归类与模型候选推荐 | 选题决策与路线确认 |
| 结构化 Notebook 模板生成 | 假设设计与参数选择依据 |
| 图表整理、格式检查、checklist | 结果解释与结论撰写 |
| 论文草稿骨架与润色建议 | 最终审核与提交 |
| workflow 引导与验收自动化 | 策略决策（简化还是深化） |

### 2.2 IDE-first

AI 能力来源于用户本机已安装的 IDE / CLI 工具：

- Cursor（订阅或兼容方案）
- Claude Code（+ ccswitch 等）
- VS Code + Agent 插件
- Gemini CLI
- Codex

**本项目交付的是 Skills / Rules / Prompts / Runtime / Templates**，不交付统一模型网关。

用户在 IDE 对话框输入 `/` 即可看到并调用项目内置的 Skills。

> **关于模型成本**：建议用户先用低成本模型（如 DeepSeek）做草稿和初步分析，再用高质量模型做润色和关键决策。中转站 / 聚合 API 属于用户自建基础设施，V1 仓库不内置。

### 2.3 Docker-native

```bash
docker compose up
```

启动后终端输出 ASCII Banner + 环境就绪信息：

```text
===============================================================================
  __  __       _   _     __  __           _      _
 |  \/  | __ _| |_| |__ |  \/  | ___   __| | ___| |
 | |\/| |/ _` | __| '_ \| |\/| |/ _ \ / _` |/ _ \ |
 | |  | | (_| | |_| | | | |  | | (_) | (_| |  __/ |
 |_|  |_|\__,_|\__|_| |_|_|  |_|\___/ \__,_|\___|_|
 __        __         _                                
 \ \      / /__  _ __| | _____ _ __   __ _  ___ ___   
  \ \ /\ / / _ \| '__| |/ / __| '_ \ / _` |/ __/ _ \  
   \ V  V / (_) | |  |   <\__ \ |_) | (_| | (_|  __/  
    \_/\_/ \___/|_|  |_|\_\___/ .__/ \__,_|\___\___|  
                              |_|                      
===============================================================================
  JupyterLab  : http://localhost:8888
  Python      : 3.10 + scientific stack ready
  Typst       : installed
  Pandoc      : installed
  Skills      : 9 skills loaded
===============================================================================
```

启动后即获得：

- Python 3.10 + 全部建模依赖
- JupyterLab
- Typst + Pandoc
- 可视化工具链（matplotlib / seaborn / plotly）
- 模板系统与 Skills

环境目标：新机器克隆 → `docker compose up` → 15 分钟内可用。

**V1 不启动后端 / 前端 / Redis 等服务**——纯运行环境。核心用户是竞赛队伍，4 天出论文，不需要仪表盘。验收由各 Skill 的 `validate.py` 脚本覆盖，Agent 自动调用。如果 V2 做进度仪表盘，那时再加 compose profile。

---

## 3. 用户画像

### 3.1 核心用户

**数学建模竞赛队伍**（3 人制为典型）：

| 角色 | 主要职责 |
|------|----------|
| 建模手（Modeler） | 模型选择、假设设计、数学推导 |
| 编程手（Coder） | 数据处理、模型实现、图表生成、工程兜底 |
| 写作手（Writer） | 论文撰写、流程图绘制、翻译润色、最终排版 |

> 小团队场景下角色可合并（如 Coder 兼任 Modeler）。

### 3.2 次级用户

- 科研训练 / 课程大作业用户
- Typst 论文工作流爱好者
- AI Agent Workflow 开发者

---

## 4. 要解决的核心问题

| 问题域 | 现状痛点 | MMW 对策 |
|--------|----------|----------|
| **环境** | Python/Notebook 版本漂移，队友跑不通，LaTeX 安装困难 | Docker 固化全部依赖，一条命令启动 |
| **协作** | 文件命名混乱，图表 DPI/格式不统一，Git 使用不规范 | Agent 自动创建规范目录结构 + Reviewer Skill |
| **AI 使用** | Prompt 碎片化，缺少 workflow，输出不可复用 | Skills 内置仓库 + 阶段化 workflow + 可追溯 checklist |
| **文档** | LaTeX 学习成本高，编译慢，AI 生成效果差 | 默认 Typst 流水线（快、模板化、AI 友好）；LaTeX 作为可选 |

---

## 5. 产品目标与路线图

### V1（MVP）

构建 **AI 数学建模工作空间**：

- Docker Runtime（一键环境 + ASCII Banner）
- Skills System（阶段化 workflow + Agent 自主模式）
- Typst Pipeline（论文流水线，含完整可用模板）
- Competition Workspace Generator（脚手架，通过 `docker compose up` 自动初始化）
- 自动化验收系统

### V1.1

- 参数化 Notebook 模板生成
- 增强 `review` Skill（图表命名、摘要结构、数据一致性）

### V2（单独立项）

- `docker compose --profile local-llm up`（Ollama / LiteLLM 仅本地开发，默认不启用）
- `docker compose --profile dashboard up`（进度仪表盘 + Skills 管理 UI）
- 增强 Agent 自主模式（条件分支、回溯、多 Agent 协作）

---

## 6. MVP 功能与验收标准

### 6.1 Docker Workspace

**交付物：**

- `Dockerfile` + `docker-compose.yml`（根目录，非子目录）
- 固定 Python 3.10，依赖锁定（`requirements.txt` 或 `pyproject.toml`）
- 内置：JupyterLab、Typst、Pandoc、Python 科学栈
- entrypoint 脚本：打印 ASCII Banner → 启动 Jupyter

**依赖清单（容器内预装）：**

| 类别 | 包 |
|------|----|
| 数据计算 | numpy, pandas, scipy, sympy |
| 建模 | scikit-learn, statsmodels, xgboost |
| 优化/图论 | pulp, cvxpy, networkx |
| 可视化 | matplotlib, seaborn, plotly, graphviz |
| 文档 | typst, pandoc |
| Notebook | jupyterlab |
| 工具 | requests, beautifulsoup4, tqdm, openpyxl |

**Docker Compose 配置：**

```yaml
services:
  workspace:
    build: .
    ports:
      - "8888:8888"
    volumes:
      - .:/workspace
    # entrypoint 打印 ASCII Banner → 启动 JupyterLab

  # 可选 Profile：传统 LaTeX 支持（体积大）
  # texlive:
  #   profiles: ["texlive"]
  #   ...
```

**验收：**

- [ ] 新机器 `git clone` + `docker compose up` 可在 15 分钟内打开 Jupyter
- [ ] 容器内 `typst compile`、`pandoc --version`、`python -c "import sklearn"` 均可用
- [ ] 启动时终端输出 ASCII Banner + 工具就绪状态
- [ ] `entrypoint.sh` 启动时打印工具就绪状态

---

### 6.2 Competition Workspace Generator

**初始化方式：**

Agent 驱动。用户告诉 Agent 竞赛名称，Agent 自动创建目录结构：

```bash
# Agent 执行（用户无需手动操作）：
mkdir -p competitions/<id>/{data,notebooks,figures,report,out,results,references}
cp templates/typst/mcm-paper.typ competitions/<id>/report/paper.typ
```

**生成目录：**

```text
competitions/<id>/
├── data/               # 原始数据 + 题目 PDF
├── notebooks/          # 建模 Notebook（按顺序编号）
│   ├── 00_preprocess.ipynb
│   └── ...             # 后续按题目动态添加
├── figures/            # 图表输出（PDF 矢量图，300dpi）
├── report/             # Markdown / Typst 源文件
├── out/                # 构建产物（PDF）
├── references/         # 参考文献
├── results/            # 结果 CSV（供论文引用核对）
└── README.md           # 本轮分工、进度、关键决策记录
```

**验收：**

- [ ] 命令执行后目录结构完整
- [ ] README.md 含时间轴模板和分工占位符
- [ ] `.gitignore` 自动排除 `out/`、大数据文件

---

### 6.3 Skills System

#### 6.3.1 调用方式

用户在 IDE 对话框输入 `/` 时，IDE 自动展示项目内已安装的 Skills 列表。选择对应 Skill 即可进入该阶段的工作流。

**两种使用模式：**

| 模式 | 调用方式 | 适用场景 |
|------|---------|----------|
| **手动逐步模式** | 用户依次输入 `/skill-name` | 需要精细控制、学习流程、新手 |
| **Agent 自主模式** | 用户输入 `/agent-mode` | 让 AI 自动按 workflow 推进，遇到决策节点暂停请求人工确认 |

#### 6.3.2 Skills 拆分策略

**按阶段拆分，建模 Skill 内含完整的"数据处理 + 模型 + Notebook 产出"一体化流程。**

做题时不硬编码 problem-1/2/3/4（因为题目数量不固定），而是**逐题调用建模 Skill**，每次调用时指定当前要解决的子问题。

#### 6.3.3 Skills 清单（V1）

| Skill 名称 | 触发关键词 | 职责 | 阶段验收 |
|------------|-----------|------|----------|
| **problem-analyze** | 分析题目、读题、题型 | 解析题目 PDF，输出题型分类、子问题拆解、候选模型列表、数据需求清单 | 自动：检查输出文件存在 |
| **data-preprocess** | 预处理、清洗、缺失值 | 全局数据加载、清洗、EDA、特征工程；产出处理后 CSV + 质量报告 | 自动：验证无缺失值、文件存在、行数合理 |
| **modeling** | 建模、预测、分类、回归、优化 | 针对当前子问题：模型选择→实现→训练→评估→图表→结果 CSV；产出 Notebook + figures/ + results/ + 面向写作手的指南 | 自动：Notebook JSON 合法、figures/ 非空、results_summary.csv 存在 |
| **sensitivity** | 敏感性、鲁棒性、稳定性 | 全题统一敏感性分析：参数扰动、交叉验证、Bootstrap | 自动：检查图表和结论输出 |
| **academic-writing** | 写作、论文、摘要、润色 | 论文结构生成、各章节撰写、润色、图表引用规范 | 自动：检查 report/ 下文件、摘要字数 |
| **typst-build** | 编译、导出、PDF | Markdown → Typst → PDF 构建 + 格式检查 | 自动：PDF 生成、页数检查 |
| **ai-report** | AI 报告、披露 | 生成 AI 工具使用报告，格式合规 | 自动：检查格式和必填项 |
| **review** | 检查、核对、验收 | 全文一致性检查：数据 vs 论文数字、图表完整性、引用格式、摘要四问 | 自动：输出不一致项列表 |
| **agent-mode** | 自主模式、全自动、autopilot | 按 workflow 自动依次执行各 Skill，遇到需要人工决策的节点暂停 | 自动：逐步验收 + 进度报告 |

#### 6.3.4 建模 Skill（modeling）的逐题工作流

由于题目数量不固定，**每次调用 modeling Skill 时指定当前子问题**：

```text
用户：/modeling 第一问：估算粉丝投票分布

Skill 自动执行：
1. 在 notebooks/ 下创建 01_problem1_fan_vote.ipynb
2. 引导用户完成：模型选择 → 数据准备 → 实现 → 评估 → 图表
3. 产出：
   - notebooks/01_problem1_fan_vote.ipynb
   - figures/p1_*.pdf
   - results/p1_summary.csv
   - report/p1_guide.md（面向写作手的指南）
4. 运行验收脚本

用户：/modeling 第二问：比较两种投票方式

Skill 自动执行：
1. 在 notebooks/ 下创建 02_problem2_voting_methods.ipynb
2. ...同上流程
```

Notebook 文件名格式：`{序号}_{问题简述}.ipynb`，序号自动递增。

#### 6.3.5 Agent 自主模式（agent-mode）

Agent 自主模式通过一个 `agent-mode` Skill 实现——本质是一个大型 SKILL.md，将 §7 的完整 workflow 编排为 AI 可自主执行的序列。

**工作机制：**

```text
用户：/agent-mode

Agent 执行流程：
1. 读取 competitions/<当前竞赛>/README.md 获取进度状态
2. 自动判断下一步应执行哪个 Skill
3. 执行该 Skill
4. 运行自动验收
5. 更新 README.md 进度标记
6. 循环到下一步
7. 遇到以下节点时暂停，请求人工确认：
   - 模型选择（推荐候选列表，等待用户确认）
   - 假设设计
   - 结论解释
   - 最终论文审核
```

**为什么不用 OpenSpec / Agent Protocol：**

- V1 阶段 workflow 是线性的，一个 SKILL.md 完全够用
- OpenSpec 等规范目前生态不成熟，引入增加复杂度但无实际收益
- V2 如果需要条件分支、多 Agent 协作，再考虑结构化编排

**实现成本：** 仅一个 SKILL.md 文件，无需额外基础设施。

#### 6.3.6 每个 Skill 的验收机制

**每次 Skill 执行完毕后，自动运行验收脚本并输出结果：**

```text
===============================================================================
  Skill Validation Report: modeling (Problem 1)
===============================================================================
  [PASS] Notebook file exists and JSON is valid
  [PASS] Notebook runs without errors
  [PASS] figures/ contains 4 PDF charts
  [PASS] results/p1_summary.csv exists and is non-empty
  [PASS] Chart data feature outputs exist (print statements)
  [FAIL] report/p1_guide.md is missing
===============================================================================
  Passed 5/6 | Fix 1 item
===============================================================================
```

验收脚本位于 `scripts/validate_skill.py`，按 Skill 名称分发检查逻辑。

#### 6.3.7 Skills 目录结构与安装

**Cursor 用户：零配置。** Skills 直接放在仓库 `.cursor/skills/` 目录下，Cursor 自动检测。

**其他 IDE 用户：** 运行安装脚本，自动检测 IDE 并映射。

```text
.cursor/skills/                 # Cursor 直接读取（零配置）
├── problem-analyze/
│   └── SKILL.md
├── data-preprocess/
│   └── SKILL.md
├── modeling/
│   └── SKILL.md
├── sensitivity/
│   └── SKILL.md
├── academic-writing/
│   ├── SKILL.md
│   └── reference/             # O 奖论文分析
├── typst-build/
│   └── SKILL.md
├── ai-report/
│   └── SKILL.md
├── review/
│   └── SKILL.md
└── agent-mode/
    └── SKILL.md

AGENTS.md                       # Claude Code 读取（自动生成或手写）

skills/
├── shared/                     # 跨 IDE 共享资源
│   ├── prompts/                # Prompt 模板
│   ├── workflows/              # 工作流定义
│   ├── checklists/             # 检查清单
│   └── templates/              # 代码/文档模板片段
└── adapters/                   # IDE 适配器
    ├── claude/                 # Claude Code Rules（映射同名 Skill）
    └── vscode/                 # VS Code Agent Rules
```

**Skills 安装：**

```bash
python scripts/install_skills.py
```

安装脚本行为（自动探测平台）：

1. **自动检测**已安装的 IDE（Cursor / Claude Code / VS Code / Gemini CLI / Codex）
2. **Cursor**：检查 `.cursor/skills/` 已存在则跳过（零配置），否则创建符号链接
3. **Claude Code**：自动生成 `AGENTS.md` + 将 Skill 内容适配到 `.claude/` 目录
4. **VS Code**：复制到对应 Agent 插件配置目录
5. **Gemini CLI / Codex**：输出配置引导说明
6. **未安装的 IDE**：跳过并打印原因，不报错

安装脚本同时检查 Docker / Typst / Pandoc / Python 等运行时依赖，输出就绪状态报告。

**Skills 创建与维护：**

使用 Cursor 内置的 `/create-skill` 技能创建新 Skill。该技能会：

1. 引导填写 Skill 的用途、触发场景、领域知识
2. 生成符合 SKILL.md 规范的文件（frontmatter + body < 500 行）
3. 可选生成验收脚本（`scripts/validate.py`）
4. 支持渐进式披露（主文件 + `reference.md` + `examples.md`）

> 详见 Cursor 内置 Skill：`/create-skill`，遵循标准目录结构 `skill-name/SKILL.md`。

**验收：**

- [ ] Cursor 用户：克隆仓库后输入 `/` 即可看到所有 Skills
- [ ] 非 Cursor 用户：运行 `python scripts/install_skills.py` 后，对应 IDE 可用
- [ ] 未安装任何 IDE 的机器上脚本不报错（跳过并打印原因）
- [ ] 安装脚本输出工具就绪状态报告

---

### 6.4 Typst Pipeline

#### 6.4.1 流程

```text
report/*.md  →  pandoc  →  report/*.typ  →  （可选人工修订）  →  typst compile  →  out/*.pdf
```

**构建命令（Agent 直接调用）：**

```bash
pandoc report/paper.md -t typst -o report/paper.typ
typst compile report/paper.typ out/paper.pdf --root .
```

#### 6.4.2 Typst 模板设计（对标 ourlatex/main.tex）

**V1 直接交付可用的 Typst 模板文件。**

模板文件：`templates/typst/mcm-template.typ`（函数库）+ `templates/typst/mcm-paper.typ`（论文骨架）

**必须包含的元素（从 ourlatex/main.tex 迁移）：**

| LaTeX 元素 | Typst 对应实现 |
|-----------|---------------|
| `\mcmsetup{tcn, problem}` | 模板顶部变量：`#let team-number = "0000000"` / `#let problem = "C"` |
| Summary Sheet（首页） | Typst 函数 `#summary-sheet()` |
| 页眉（Page X of Y + Team #） | `#set page(header: ...)` |
| 目录 | `#outline()` |
| 摘要 + Keywords | `#abstract-block()` |
| 三线表（booktabs） | `#table()` + `stroke` 设置 |
| 图注 `Fig. X` | `#figure()` + 自动编号 |
| 公式编号 `Eq. (X)` | `$ ... $ <label>` |
| 参考文献 | `#bibliography()` 或手动 |
| Memorandum 格式 | `#memo()` 自定义函数 |
| 占位符系统 `【标题_PLACEHOLDER】` | Typst 变量 + 注释标记 |
| 首行缩进 `\setlength{\parindent}{1.5em}` | `#set par(first-line-indent: 1.5em)` |
| 页码从第 2 页开始 | `#counter(page).update(2)` |
| AI Report 独立页 | `#pagebreak()` + `#ai-report-section()` |

**模板结构预览：**

```typst
// ============ 竞赛信息（必改）============
#let team-number = "0000000"
#let problem = "C"
#let paper-title = "Your Paper Title"
#let keywords = ("keyword1", "keyword2", "keyword3")

// ============ 导入模板函数 ============
#import "mcm-template.typ": *

// ============ 页面设置 ============
#set page(paper: "us-letter", margin: (x: 1in, y: 1in))
#set page(header: make-header(team-number))

// ============ Summary Sheet ============
#summary-sheet(team-number, problem, paper-title, keywords)

// ============ 目录 ============
#outline(indent: auto)
#pagebreak()

// ============ 正文 ============
= Introduction
== Problem Background
// ...

== Problem Restatement
// ...

== Our Approach
// ...

= Preparation for Modeling
== Model Assumptions
*Assumption 1:* ...

*Justification:* ...

== Notations
// 符号表（Typst table）

== Data Overview and Preprocessing
// ...

= Problem 1: ...
// ...按问题展开

= Sensitivity Analysis
// ...

= Model Evaluation and Discussion
// ...

= Memorandum
#memo(
  to: "...",
  from: "MCM Team #" + team-number,
  subject: "...",
)
// ...

= References
// ...

// ============ AI Report（独立页）============
#pagebreak()
#ai-report-section()
```

#### 6.4.3 已知 Pandoc 转换弱点（需在 Skill 中说明）

| 元素 | 问题 | 解决方案 |
|------|------|----------|
| `#horizontalrule` | Typst 无内置 | 模板预定义 `#let horizontalrule = line(length: 100%)` |
| 复杂表格（合并单元格） | 转换丢失 | 手写 Typst `#table()` |
| 交叉引用（Fig/Eq） | Pandoc 不生成 Typst label | 手动添加 `<label>` |
| 参考文献 | 需 `.bib` + Typst bibliography | 提供配置模板 |
| 图片路径 | 大小写敏感 | 验收脚本检查路径存在性 |

**验收：**

- [ ] 提供最小示例论文（含公式、图、表）能 `pandoc` + `typst compile` 生成 PDF
- [ ] PDF 含页眉页脚、控制号、目录、图表编号

---

### 6.5 Agent 系统提示（`agent.md`）

> **注**：原 CLI（`mmw`）已移除。所有功能由 Agent 直接完成，用户无需记忆任何命令。

**定位**：放在仓库根目录的 `agent.md`，作为 Cursor Rules 级别的系统提示，给 AI Agent 提供项目上下文和行为准则。

**内容覆盖**：

| 章节 | 内容 |
|------|------|
| 项目定位 | AI-Native 数学建模工作空间 |
| 环境 | Dev Containers + Skills 位置 + 竞赛目录结构 |
| 工作流 | 10 步流程精简描述 |
| 行为准则 | 主动创建工作区、每步验证、决策点暂停、零命令行 |
| 构建 PDF | pandoc + typst compile 命令 |
| Skills 清单 | 触发词 + 产出速查表 |

**原 CLI 功能去向**：

| 原命令 | 新归属 |
|--------|--------|
| `mmw init <id>` | Agent 检测到无竞赛目录时自动创建（`problem-analyze` 前置检查） |
| `mmw doctor` | `entrypoint.sh` 启动时打印工具状态 |
| `mmw build` | `typst-build` Skill 直接调用 `pandoc` + `typst compile` |
| `mmw validate` | 各 Skill 完成后 Agent 自动调用 `scripts/validate.py` |
| `mmw install-skills` | 保留为独立脚本 `scripts/install_skills.py`（非 Cursor IDE 用户用） |

---

## 7. 核心 Workflow（比赛全流程）

### 7.1 手动逐步模式

```text
Step 0: 环境启动
    在 Cursor 中 "Reopen in Container"
    → Dev Containers 就绪

Step 1: 初始化（Agent 自动完成）
    Agent 检测到无竞赛目录 → 询问竞赛名称 → 创建目录结构
    → 生成竞赛目录

Step 2: 读题分析
    /problem-analyze
    → 输入：题目 PDF
    → 输出：题型分类、子问题拆解、候选模型、数据需求
    → 验收：✅ 自动检查输出文件

Step 3: 数据预处理
    /data-preprocess
    → 加载全部数据 → 清洗 → EDA → 特征工程
    → 产出：处理后 CSV + 质量报告 + Notebook
    → 验收：✅ 自动检查数据完整性

Step 4: 逐题建模（循环，题目数量不固定）
    /modeling 第一问：xxx
    → Notebook + figures + results + 写作指南
    → 验收：✅ 自动检查全部产出

    /modeling 第二问：xxx
    → ...

    /modeling 第N问：xxx
    → ...

Step 5: 敏感性分析
    /sensitivity
    → 全题统一敏感性 + 交叉验证
    → 验收：✅ 自动检查图表和结论

Step 6: 论文撰写
    /academic-writing
    → 基于各题 results + 写作指南 → 论文 Markdown 初稿
    → 验收：✅ 检查结构完整性和摘要

Step 7: 构建 PDF
    /typst-build
    → pandoc + typst compile → PDF
    → 验收：✅ PDF 生成、页数、格式

Step 8: AI 报告
    /ai-report
    → 生成合规的 AI 使用报告
    → 验收：✅ 格式和必填项

Step 9: 全文检查
    /review
    → 数据 vs 论文数字一致性、图表齐全、引用格式
    → 验收：✅ 输出不一致项列表

Step 10: 人工最终审核 → 提交
```

### 7.2 Agent 自主模式

```text
用户：/agent-mode

→ Agent 读取 README.md 进度
→ 自动执行 Step 2 → Step 9
→ 每完成一步输出验收报告
→ 遇到决策节点（模型选择 / 假设设计 / 结论）暂停等待确认
→ 用户确认后继续
→ 最终 Step 10 人工审核
```

---

## 8. 技术架构

### 8.1 逻辑分层

```text
┌─────────────────────────┐
│       IDE Layer         │  用户自备：Cursor / Claude Code / VS Code / Gemini CLI
│  输入 / 调用 Skills     │
└───────────┬─────────────┘
            │ 读取仓库内 Skills / Rules / Prompts
            ▼
┌─────────────────────────┐
│      Skills Layer       │  workflow 引导 · prompt 模板 · reviewer 规则
│  阶段化 + 逐题建模      │  图表规范 · 论文结构 · 验收清单
│  Agent 自主模式编排      │  agent-mode Skill
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│    Workspace Layer      │  competitions/ · notebooks/ · figures/ · report/
│  竞赛目录 + 产出物       │  results/ · references/ · templates/
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│    Docker Runtime       │  Python 3.10 · JupyterLab · Typst · Pandoc
│  一键启动，跨平台统一    │  全部建模/可视化/文档依赖 · ASCII Banner
└─────────────────────────┘
```

### 8.2 关键设计决策

| 决策 | 选择 | 原因 |
|------|------|------|
| 项目名称 | MathModelWorkspace | "Workspace" 强调完整工作空间定位，避嫌同名项目 |
| 默认排版工具 | Typst | 编译快、模板化、AI 友好 |
| LaTeX 支持 | 可选 compose profile | 兼容传统赛队（体积大，默认不装） |
| AI 网关 | V1 不提供 | 降低合规与运维面；IDE BYOK |
| 后端服务 | V1 不启动 | 竞赛用户不需要仪表盘；验收由 Agent 自动调用验证脚本 |
| Skills 存放 | `.cursor/skills/`（Cursor 零配置）+ 安装脚本（其他 IDE） | 与 runtime 版本同步，Cursor 用户零配置 |
| Notebook 模板 | 静态模板（V1）→ 参数化生成（V1.1） | MVP 先交付，迭代增强 |
| 做题粒度 | 按题调用 modeling Skill，不硬编码题号 | 适配不同赛事的题目数量 |
| Agent 模式 | SKILL.md 实现（V1）→ 结构化编排（V2） | 实现成本极低，一个文件即可 |
| Typst 模板 | V1 直接交付可用模板 | 已验证可行性，不拖到后续版本 |

### 8.3 仓库目录结构

```text
math-model-workspace/
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh                # ASCII Banner + 工具就绪检查
├── agent.md                     # Agent 系统提示（项目上下文 + 行为准则）
├── scripts/
│   ├── install_skills.py        # Skills 安装器（非 Cursor IDE）
│   └── validate_skill.py        # 验收脚本
├── .cursor/
│   └── skills/                  # Cursor 自动检测（零配置）
│       ├── problem-analyze/
│       │   └── SKILL.md
│       ├── data-preprocess/
│       │   └── SKILL.md
│       ├── modeling/
│       │   └── SKILL.md
│       ├── sensitivity/
│       │   └── SKILL.md
│       ├── academic-writing/
│       │   ├── SKILL.md
│       │   └── reference/
│       ├── typst-build/
│       │   └── SKILL.md
│       ├── ai-report/
│       │   └── SKILL.md
│       ├── review/
│       │   └── SKILL.md
│       └── agent-mode/
│           └── SKILL.md
├── AGENTS.md                    # Claude Code 读取
├── skills/
│   ├── shared/                  # 跨 IDE 共享资源
│   │   ├── prompts/
│   │   ├── workflows/
│   │   ├── checklists/
│   │   └── templates/
│   └── adapters/
│       ├── claude/
│       └── vscode/
├── templates/
│   ├── typst/
│   │   ├── mcm-template.typ    # 美赛 Typst 模板函数库
│   │   ├── mcm-paper.typ       # 美赛论文骨架（带占位符）
│   │   └── cumcm-template.typ  # 国赛 Typst 模板
│   ├── notebooks/
│   │   ├── preprocess.ipynb
│   │   ├── modeling.ipynb
│   │   └── sensitivity.ipynb
│   └── latex/                   # 传统 LaTeX 模板（可选引用）
│       └── mcmthesis/
├── competitions/                # 竞赛工作区（Agent 自动生成）
├── docs/                        # 仓库内文档（非文档站）
│   └── dev-notes.md
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 9. 从 MathModelHub 迁移的资产清单

> **原则：旧仓库 MathModelHub 不动。** 以下资产拷贝到新仓库后改造。

| 旧仓库资产 | 新仓库位置 | 改造要求 |
|-----------|-----------|----------|
| `.cursor/skills/data-preprocess/SKILL.md` | `.cursor/skills/data-preprocess/SKILL.md` | 补充自动验收 section |
| `.cursor/skills/math-modeling/SKILL.md` | `.cursor/skills/modeling/SKILL.md` | 重命名 + 补充逐题调用说明 |
| `.cursor/skills/academic-writing/SKILL.md` + `reference/` | `.cursor/skills/academic-writing/` | 将 LaTeX 模板引用改为 Typst |
| `.cursor/skills/ai-report/SKILL.md` | `.cursor/skills/ai-report/SKILL.md` | 基本不变 |
| `templates/ourlatex/main.tex` | `templates/typst/mcm-template.typ` + `mcm-paper.typ` | **重写为 Typst 原生模板** |
| `templates/latex/mcmthesis/` | `templates/latex/mcmthesis/` | 保留作为可选 |
| `requirements.txt` | `requirements.txt` | 补充 jupyterlab 等 |
| `algorithms/algorithms_reference.md` | `skills/shared/templates/` | 作为 modeling Skill 的参考嵌入 |
| `data_analysis/visualization/` | `templates/notebooks/` | 精选模板化 |
| `competitions/` 实战产出 | 不迁移 | 旧仓库归档，可作为示例引用 |

---

## 10. V1 开发优先级

### P0（必须交付，阻塞其它）

1. Docker 环境（Dockerfile + compose + entrypoint + ASCII Banner）
2. Dev Containers 配置（`.devcontainer/`）
3. Typst 模板（完整可用的 `mcm-template.typ` + `mcm-paper.typ`）

### P1（核心体验）

4. 4 个核心 Skill（data-preprocess / modeling / academic-writing / typst-build）
5. Agent 系统提示（`agent.md`）
6. 验收脚本框架（`validate_skill.py`）
7. agent-mode Skill

### P2（完善）

8. 剩余 Skills（problem-analyze / sensitivity / ai-report / review）
9. `install_skills.py`（非 Cursor IDE 适配）
10. AGENTS.md（Claude Code 适配）

---

## 11. 文档站规划

新建独立文档站（建议用 VitePress / Docusaurus / MkDocs），内容结构：

| 章节 | 内容 | 来源 |
|------|------|------|
| **Quick Start** | 克隆仓库 → 安装 Docker → `docker compose up` → 打开 Jupyter | 新写 |
| **环境配置** | Docker 安装（Mac/Win/Linux）、镜像加速、常见问题 | 新写 |
| **IDE Agent 选择指南** | Cursor / Claude Code / VS Code / Gemini CLI 的对比表 + 各自配置方式 + Skills 安装 | 新写，可引用 §2.2 |
| **完整 Workflow 演示** | 从 Agent 建模到提交 PDF 的全流程，含截图/GIF/示例对话 | 复用 §7 |
| **Skills 参考手册** | 每个 Skill 的触发词、输入、输出、验收标准、示例对话 | 复用 §6.3 |
| **Typst 模板指南** | 模板结构说明、自定义方法、与 LaTeX 的对应关系 | 复用 §6.4 |
| **Agent 配置** | `agent.md` 说明 + 行为准则 | 复用 §6.5 |
| **FAQ / Troubleshooting** | 常见错误、Docker 问题、Typst 编译问题 | 新写 |
| **贡献指南** | 如何新增 Skill、如何贡献模板 | 新写 |

> 大量内容可直接从本 PRD 提取，不需要重复写。文档站主要增加截图/GIF 演示和面向新手的步骤化引导。

---

## 12. 风险与合规

| 风险 | 应对 |
|------|------|
| **学术诚信** | README 和 Skills 内显著声明 AI 使用边界；AI Report Skill 内置合规模板 |
| **数据版权** | 外部数据集版权由队伍自担；不提供"自动抓取付费库"功能 |
| **API 密钥** | `.env.example` + `.gitignore` 模板；Skills 中提示勿提交 Key |
| **Docker 镜像体积** | 基础镜像用 `python:3.10-slim`；Typst 二进制约 30MB；无 TeXLive 时总体 < 2GB |

---

## 13. 与原始 PRD 草稿的变更摘要

| 版本 | 变更 |
|------|------|
| v1 → v2 | 项目命名：`math-model-agent` → `math-model-workspace`，避嫌同名开源项目 |
| v1 → v2 | Skills 目录：`skills/cursor/` → `.cursor/skills/`（Cursor 零配置） |
| v1 → v2 | 新增 agent-mode Skill（AI 自主按 workflow 推进） |
| v1 → v2 | 明确 V1 不起后端/前端/Redis，纯 Docker 运行环境 |
| v1 → v2 | Docker 启动增加 ASCII Banner + 工具就绪信息输出 |
| v1 → v2 | 竞赛目录创建由 Agent 自动完成，用户无需手动执行 |
| v1 → v2 | Typst 模板 V1 直接交付可用文件（不推迟） |
| v1 → v2 | 新增 §11 文档站规划 |
| v1 → v2 | 迁移资产清单补充：明确旧仓库不动，新仓库路径用 `.cursor/skills/` |
| 原始 | "无限续杯插件" 等灰色工具描述 → 删除 |
| 原始 | Skills 按 IDE 分四大类 → Cursor 零配置 + adapters/ 适配其他 IDE |
| 原始 | 做题 Skills 命名未定 → 不按题号硬编码，用 `modeling` Skill + 参数 |
| 原始 | compose up 前置条件 → 一条命令搞定全部环境 |
| 原始 | 验收方式未定 → 自动脚本优先 |

---

## 14. Skills 生成：参考资料清单与测试样例

### 14.1 必须借鉴的本项目（MathModelHub）资料

以下资料是 Skills 内容的核心输入，迁移时应完整保留并改造：

| 资源路径 | 行数 | Skill 目标 | 改造要点 |
|---------|------|-----------|---------|
| `.cursor/skills/data-preprocess/SKILL.md` | 314 | data-preprocess | 补充自动验收 section；万能 Prompt 模板保留 |
| `.cursor/skills/math-modeling/SKILL.md` | 934 | modeling | 重命名；补充逐题调用说明；图表数据特征输出规范保留（核心价值） |
| `.cursor/skills/academic-writing/SKILL.md` | 485 | academic-writing | 将 LaTeX 引用改为 Typst；润色规则、论文结构、逻辑漏洞检查清单保留 |
| `.cursor/skills/academic-writing/reference/*.md` | 656 (6 files) | academic-writing 参考 | O 奖论文分析（24C/25C），直接放入 `reference/` |
| `.cursor/skills/ai-report/SKILL.md` | 211 | ai-report | 基本不变 |
| `algorithms/algorithms_reference.md` | 1400 | modeling 参考 | 模型选择决策树 + 代码片段 + 美赛 C 题历年总结，嵌入 `skills/shared/templates/` |
| `docs/team_workflow.md` | 1064 | agent-mode + 文档 | 角色分工、五天时间轴、协作流程，提取精华嵌入 agent-mode Skill 和文档站 |

### 14.2 关于借鉴 mathmodelagent 项目

**结论：不借鉴其代码架构，仅参考其 workflow 编排思路。**

两个项目定位不同：

| 维度 | mathmodelagent | MMW |
|------|---------------|-----|
| 架构 | 全栈应用（FastAPI + Vue + Redis + WebSocket） | IDE-first 工作空间（Skills + Docker + 模板） |
| AI 调用 | 自建 LiteLLM 网关 + 多 Agent 编排 | 用户 IDE 自带的模型（BYOK） |
| 后端 | 有（协调 Agent、任务管理、WebSocket 推送） | 无（V1 纯运行环境） |
| Skills | 无 SKILL.md，逻辑写在 Python 代码里 | SKILL.md 为核心，Cursor 原生读取 |

**可参考的一点：** 其 `flows.py` 的阶段编排（题目分析 → 假设 → 符号 → EDA → 逐题编码 → 敏感性 → 章节撰写）与本项目 §7 workflow 高度一致，验证了我们的 workflow 设计合理性。

### 14.3 测试样例

采用 mathmodelagent 项目的 `2025五一杯C题` 作为端到端测试样例：

**来源：** `mathmodelagent/backend/app/example/example/2025五一杯C题/`

**内容：**

| 文件 | 说明 |
|------|------|
| `questions.txt` | 完整 C 题题目文本（社交媒体用户-创作者互动分析，4 个子问题） |
| `附件1 (Attachment 1).csv` | 平台交互日志数据 |
| `附件2 (Attachment 2).csv` | 特定日期行为数据 |

**选择理由：**

1. 国赛类型题目，补充"美赛 + 国赛并重"定位
2. 含原始数据（CSV），可完整跑通 data-preprocess → modeling 流程
3. 4 个子问题，测试逐题建模 Skill 的循环调用
4. 仅含输入素材（题目 + 数据），无生成产出物，不涉及版权
5. 数据量适中，适合作为 CI / 演示 / 文档站示例

**放置位置：**

```text
tests/
└── fixtures/
    └── 2025-wuyibei-c/
        ├── questions.txt
        ├── attachment1.csv
        └── attachment2.csv
```

### 14.4 Skills 生成方式

使用 Cursor 内置 `/create-skill` 技能生成每个 Skill。生成流程：

```text
1. 在新仓库中打开 Cursor
2. 对话框输入: /create-skill
3. 告知 Skill 用途、触发场景、领域知识
4. 将上述 §14.1 的对应资料作为输入（附上原始 SKILL.md 内容）
5. /create-skill 自动生成：
   - SKILL.md（< 500 行，含 frontmatter）
   - reference.md（详细参考，如算法手册、O 奖论文分析）
   - scripts/validate.py（验收脚本）
6. 人工审核 → 提交
```

**生成顺序（按依赖关系）：**

1. `data-preprocess`（无前置依赖）
2. `modeling`（依赖 algorithms_reference.md）
3. `sensitivity`（依赖 modeling 产出）
4. `academic-writing`（依赖 modeling + sensitivity 产出）
5. `typst-build`（依赖 academic-writing 产出）
6. `ai-report`（无前置依赖，可并行）
7. `review`（依赖所有产出）
8. `problem-analyze`（无前置依赖，可并行）
9. `agent-mode`（依赖所有 Skill 定义完毕）
