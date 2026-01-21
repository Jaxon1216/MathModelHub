---
name: academic-writing
description: MCM/ICM数学建模论文写作指南。用于论文结构设计、摘要写作、模型描述、结果分析、图表引用、LaTeX排版等场景。当用户提到论文写作、摘要、introduction、LaTeX、图表引用、润色、academic writing、paper structure时触发。
---

# MCM论文写作指南

## 1. 标准论文结构

基于O奖论文分析，推荐以下结构和篇幅占比：

| 章节 | 篇幅占比 | 核心功能 |
|------|----------|----------|
| **Summary/Abstract** | 1页 | 最重要！概述问题、方法、结果、结论 |
| **1. Introduction** | 8-12% | 问题背景、重述、研究内容概述 |
| **2. Assumptions** | 3-4% | 模型假设及合理性说明 |
| **3. Notations** | 3-4% | 符号定义表 |
| **4-5. Models** | 40-50% | 核心建模章节，按问题分节 |
| **6. Sensitivity Analysis** | 4-8% | 参数敏感性验证 |
| **7. Model Evaluation** | 4-8% | 优势与局限性分析 |
| **8. Conclusion** | 3-5% | 总结与建议 |
| **References** | 1页 | 参考文献 |
| **Appendix** | 可选 | 代码、补充图表 |

---

## 2. 各章节写作要点

### Summary (摘要) - 最重要！

**结构**：背景（1-2句）→ 方法（2-3句）→ 结果（2-3句）→ 结论（1-2句）

**必须包含**：
- 研究问题是什么
- 用了什么核心方法/模型
- 主要发现/预测结果
- 关键结论和建议

**关键词**：3-5个，涵盖核心方法和研究对象

### Introduction (引言)

**三段式结构**：
1. **Problem Background**：研究背景和意义
2. **Restatement of Problem**：问题重述（用自己的话）
3. **Our Work**：研究内容和方法概述

**常用句式**：
```
背景引入：
- In recent years, [topic] has attracted considerable attention due to [reason].
- The [event/phenomenon] presents a significant challenge for [stakeholder].

问题重述：
- The problem requires us to [task 1], [task 2], and [task 3].
- We are asked to develop a model that [objective].

研究概述：
- To address these challenges, we develop a comprehensive framework that...
- Our approach integrates [method 1] and [method 2] to achieve [goal].
```

### Assumptions (假设)

**格式**：每个假设 + Justification说明

```latex
\textbf{Assumption 1:} [假设内容]

\textbf{Justification:} [合理性说明，为什么这样假设是合理的]
```

**常见假设类型**：
- 数据可靠性假设
- 外部因素排除假设
- 参数稳定性假设

### Model Chapters (建模章节)

**每个问题的标准结构**：
1. 问题分析
2. 模型构建（含公式推导）
3. 求解方法
4. 结果展示（图表）
5. 结果分析

**模型描述句式**：
```
We develop/construct/establish a [模型名称] to [目的].

The model is based on [理论/方法], which [优势说明].

The objective function is defined as: [公式]

where [符号] represents [含义].
```

### Sensitivity Analysis (敏感性分析)

**验证内容**：
- 关键参数变化对结果的影响
- 模型在不同条件下的稳健性

**句式**：
```
To verify the robustness of our model, we conduct sensitivity analysis on [参数].

The results show that [结论], indicating that [模型性质].
```

### Strengths and Weaknesses (模型评估)

**Strengths常见角度**：
- 算法创新性
- 预测精度高
- 可解释性强
- 泛化能力好

**Weaknesses常见角度**：
- 数据局限性
- 计算复杂度
- 假设简化导致的偏差

**句式**：
```
Strengths:
- The model achieves [性能], demonstrating [优势].
- By integrating [方法], we ensure [效果].

Weaknesses:
- Due to [原因], the model may [局限].
- Future work could incorporate [改进方向] to address this limitation.
```

---

## 3. 图表引用规范

### 引用句式

```
引入图表：
- As illustrated in Fig. X, [图表核心内容].
- Table X presents the [数据类型] of [研究对象].

解读图表：
- Fig. X shows/depicts/demonstrates that [趋势/关系].
- From Fig. X, we can observe that [观察结果].
- The [图表类型] in Fig. X confirms that [结论].

数据对比：
- As can be seen from Table X, [变量] is [数值], which indicates [结论].
- Compared with [对比对象], [研究对象] achieves [结果].
```

### 图表标注规范

- 图：`Fig. 1`, `Figs. 2(a)-(b)`
- 表：`Table 1`
- 公式：`Eq. (1)`, `Eqs. (1)-(3)`

### LaTeX图表模板

```latex
% 单图
\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{figures/fig1.pdf}
\caption{Description of the figure.}
\label{fig:fig1}
\end{figure}

% 双图并排
\begin{figure}[h]
\centering
\subfigure[Left figure caption]{
    \includegraphics[width=0.45\textwidth]{figures/fig2a.pdf}
}
\subfigure[Right figure caption]{
    \includegraphics[width=0.45\textwidth]{figures/fig2b.pdf}
}
\caption{Overall caption for both figures.}
\label{fig:fig2}
\end{figure}

% 表格
\begin{table}[h]
\centering
\caption{Model performance comparison.}
\label{tab:performance}
\begin{tabular}{lccc}
\hline
Model & R² & MAE & RMSE \\
\hline
Linear Regression & 0.85 & 3.2 & 4.5 \\
Random Forest & 0.91 & 2.1 & 3.2 \\
\hline
\end{tabular}
\end{table}
```

---

## 4. 常用过渡词

| 类型 | 过渡词 |
|------|--------|
| 递进 | Furthermore, Moreover, Additionally, In addition |
| 因果 | Therefore, Thus, Consequently, As a result, Due to |
| 转折 | However, Nevertheless, In contrast, On the other hand |
| 举例 | For example, For instance, Specifically, As illustrated by |
| 总结 | In summary, To conclude, Overall, In essence |

---

## 5. 写作风格要点

### 语态选择
- **被动语态为主**：强调客观性
  - `The model was trained using 10-fold cross-validation.`
  - `PCA was employed to reduce dimensionality.`
- **主动语态**：强调研究贡献
  - `We develop a novel framework...`
  - `Our findings suggest that...`

### 时态选择
- **现在时**：描述模型、公式、一般性结论
- **过去时**：描述实验过程、数据处理步骤
- **将来时**：讨论未来工作

### 避免事项
- 避免口语化表达（如 "a lot of" → "numerous"）
- 避免主观评价词（如 "very good" → 用数据支撑）
- 避免过长句子（建议每句不超过30词）

---

## 6. LaTeX常用片段

### 公式
```latex
% 带编号
\begin{equation}
L(\theta) = \sum_{i=1}^{n} l(y_i, \hat{y}_i) + \lambda \Omega(\theta)
\label{eq:loss}
\end{equation}

% 不带编号
\[
R^2 = 1 - \frac{\sum(y_i - \hat{y}_i)^2}{\sum(y_i - \bar{y})^2}
\]

% 分段函数
\[
p_j = \begin{cases}
0, & \text{if } j \text{ is odd} \\
r!(-1)^{j/2}, & \text{if } j \text{ is even}
\end{cases}
\]
```

### 列表
```latex
% 无序列表
\begin{itemize}
\item First point
\item Second point
\end{itemize}

% 有序列表
\begin{enumerate}
\item Step one
\item Step two
\end{enumerate}
```

### 加粗与斜体
```latex
\textbf{Bold text}
\emph{Italic text}
\textbf{\textit{Bold italic}}
```

---

## 7. 深度参考

本目录下的O奖论文分析包含详细的写作模式和句式：

- [reference/25-C-1.md](reference/25-C-1.md) - 2025年C题O奖论文1分析
- [reference/25-C-2.md](reference/25-C-2.md) - 2025年C题O奖论文2分析
- [reference/24-C-1.md](reference/24-C-1.md) - 2024年C题O奖论文1分析
- [reference/24-C-2.md](reference/24-C-2.md) - 2024年C题O奖论文2分析

每个参考文件包含：
1. 结构分析（章节标题和篇幅占比）
2. 写作风格（过渡词、句式）
3. 专业表达（术语、固定句式）
4. 论证逻辑（假设引出、模型选择说明、局限性讨论）

**LaTeX模板**：[templates/latex/mcmthesis/](templates/latex/mcmthesis/)
