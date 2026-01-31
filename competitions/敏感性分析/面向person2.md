# 敏感性分析 —— 资料手工作指南

> 本文档面向资料手Person2，指导完成参考文献查找和图片整理工作。

## 一、需要绘制的思路图

本部分无需额外绘制思路图，敏感性分析的可视化已由Coder完成。

---

## 二、参考文献检索指南

### 2.1 检索关键词

| 领域 | 英文关键词 |
|------|------------|
| 敏感性分析 | sensitivity analysis, robustness testing |
| 参数优化 | parameter optimization, grid search |
| 模型验证 | model validation, cross-validation |

### 2.2 推荐参考文献

1. Saltelli, A., et al. (2008). *Global sensitivity analysis: the primer*. John Wiley & Sons.
   - **相关性**：敏感性分析方法论

---

## 三、图片文件交付清单

| 文件名 | 内容 | 状态 |
|--------|------|------|
| `fig1_q1_sensitivity.pdf` | 问题一敏感性 | ✅ |
| `fig2_q2_sensitivity.pdf` | 问题二敏感性 | ✅ |
| `fig3_q3_sensitivity.pdf` | 问题三敏感性 | ✅ |
| `fig4_q4_sensitivity.pdf` | 问题四敏感性 | ✅ |

### 数据文件

| 文件名 | 内容 |
|--------|------|
| `q1_noise_sensitivity.csv` | 噪声敏感性数据 |
| `q1_sample_sensitivity.csv` | 抽样敏感性数据 |
| `q3_ridge_sensitivity.csv` | Ridge参数敏感性 |
| `q4_alpha_sensitivity.csv` | 动态权重参数敏感性 |
| `sensitivity_summary.csv` | 汇总结果 |

---

## 四、研究框架图提示词（供AI画图工具）

基于项目的研究框架信息，生成学术研究流程架构图。

### 项目框架信息

**任务模块划分**：共4个核心任务+1个敏感性分析，分5列展示：

- **Task 1: Fan Vote Estimation**
  - 输入：Judge Scores + Elimination Results
  - 核心步骤：Softmax Model → Constrained Optimization → Bootstrap Uncertainty
  - 输出：Estimated Vote Shares + Certainty Index

- **Task 2: Voting Method Comparison**
  - 输入：Estimated Votes + Method Rules
  - 核心步骤：Rank Method → Percentage Method → Counterfactual Analysis
  - 输出：Method Comparison + Controversial Case Studies

- **Task 3: Factor Impact Analysis**
  - 输入：Celebrity Features + Pro Dancer Data
  - 核心步骤：ANOVA → Regression → Random Forest
  - 输出：Feature Importance + Impact Quantification

- **Task 4: New System Design**
  - 输入：Analysis Results + Design Objectives
  - 核心步骤：Dynamic Weight Design → Threshold Mechanism → Tiebreaker Rules
  - 输出：DWVS System Specification

- **Sensitivity Analysis**
  - 输入：All Model Parameters
  - 核心步骤：Parameter Sweep → Cross-Validation → Grid Search
  - 输出：Robustness Assessment

### 提示词

```
Create an academic research workflow diagram with 5 columns:

Column 1 - "Task 1: Fan Vote Estimation":
- Input box: "Judge Scores + Elimination Results" (with table icon)
- Process boxes in blue: "Softmax Voting Model" → "Constrained Optimization" → "Bootstrap Uncertainty"
- Output box: "Estimated Votes + Certainty"

Column 2 - "Task 2: Method Comparison":
- Input box: "Estimated Votes + Rules"
- Process boxes in blue: "Rank Method" → "Percentage Method" → "Counterfactual Analysis"
- Output box: "Method Comparison Report"

Column 3 - "Task 3: Factor Analysis":
- Input box: "Celebrity Features + Pro Data"
- Process boxes in blue: "ANOVA" → "Regression" → "Random Forest"
- Output box: "Feature Importance"

Column 4 - "Task 4: System Design":
- Input box: "Analysis Results + Objectives"
- Process boxes in blue: "Dynamic Weights" → "Threshold" → "Tiebreaker"
- Output box: "DWVS Specification"

Column 5 - "Sensitivity Analysis":
- Input box: "All Parameters"
- Process boxes in green: "Parameter Sweep" → "Cross-Validation"
- Output box: "Robustness Report"

Style: Academic, clean, no decorations. Blue for main methods, green for validation. Black text, white background.
```
