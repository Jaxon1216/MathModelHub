# 问题三建模分析 —— 写作指南

> 本文档面向写作手Person1，帮助理解建模方法、公式符号，并指导论文撰写。

## 目录
1. [问题分析与建模思路](#一问题分析与建模思路)
2. [模型介绍与公式](#二模型介绍与公式)
3. [结果解读](#三结果解读)
4. [论文撰写建议](#四论文撰写建议)
5. [图片列表与插入位置](#五图片列表与插入位置)

---

## 一、问题分析与建模思路

### 1.1 问题理解

问题三要求：
1. 针对未来某日期的目标单词，建立模型预测**结果分布**（1-6次猜对及X的百分比）
2. 分析模型**不确定性来源**
3. 以2023年3月1日目标单词「EERIE」为例给出**具体预测**
4. 评估**模型置信度**

### 1.2 建模思路

采用**多输出回归模型**方法：

```
特征提取 → 多输出回归 → Bootstrap → 预测+置信区间
```

**核心思想**：
- **输入**：单词属性特征（元音数量、重复字母、字母频率等）
- **输出**：7个百分比（try_1, try_2, ..., try_6, try_x）
- **约束**：7个百分比之和应接近100%

**类比理解**：
- 这就像根据学生特征（学习时间、智商等）预测各科成绩分布
- 不同的是，这里的「成绩」是7个比例，且它们之和固定

---

## 二、模型介绍与公式

### 2.1 多输出回归模型

$$\mathbf{y} = f(\mathbf{x}) + \boldsymbol{\varepsilon}$$

其中：
- $\mathbf{x} = (x_1, x_2, ..., x_{10})^T$：10维特征向量
- $\mathbf{y} = (y_1, y_2, ..., y_7)^T$：7维输出（7个百分比）
- $f$：随机森林多输出回归模型

### 2.2 随机森林回归

随机森林通过集成多棵决策树进行预测：

$$\hat{y}_j = \frac{1}{B} \sum_{b=1}^{B} T_b(\mathbf{x})$$

其中：
- $B = 200$：决策树数量
- $T_b$：第 $b$ 棵决策树
- $\hat{y}_j$：第 $j$ 个目标的预测值

### 2.3 Bootstrap不确定性估计

通过Bootstrap方法估计预测的置信区间：

1. 从原始数据有放回抽样 $n$ 次
2. 在每个Bootstrap样本上训练模型
3. 对目标单词进行预测
4. 取预测分布的2.5%和97.5%分位数作为95%置信区间

$$CI_{95\%} = [\hat{y}_{2.5\%}, \hat{y}_{97.5\%}]$$

---

## 三、结果解读

### 3.1 EERIE特征分析

| 特征 | 值 | 解读 |
|------|-----|------|
| 字母组成 | E-E-R-I-E | 3个E，高重复 |
| 元音数量 | 4 | 极高（正常1-2个） |
| 元音占比 | 80% | 非常高 |
| 重复字母数 | 2 | 高（E出现3次） |
| 平均字母频率 | 10.21 | 较高（E和I高频） |

### 3.2 EERIE预测结果

| 猜测次数 | 预测值 | 95%置信区间 |
|----------|--------|-------------|
| 1次 | 0.5% | [0.0%, 0.9%] |
| 2次 | 13.0% | [6.3%, 17.1%] |
| 3次 | **29.2%** | [18.4%, 33.4%] |
| 4次 | **29.8%** | [25.6%, 32.8%] |
| 5次 | 17.6% | [14.9%, 23.4%] |
| 6次 | 8.4% | [5.1%, 17.9%] |
| X (失败) | 2.2% | [0.5%, 8.0%] |

### 3.3 与历史平均对比

| 指标 | EERIE预测 | 历史平均 | 差异 |
|------|-----------|----------|------|
| 3次猜对 | 29.2% | ~23% | +6.2% |
| 4次猜对 | 29.8% | ~34% | -4.2% |
| 失败率 | 2.2% | ~2% | 相近 |

**解读**：EERIE的结果分布与历史平均接近，略偏向更多尝试次数。

### 3.4 不确定性来源

| 来源 | 类型 | 说明 |
|------|------|------|
| 数据随机性 | Aleatoric | Twitter样本的代表性有限 |
| 模型不确定性 | Epistemic | 单词属性未能完全解释结果分布 |
| 特征不完全 | Epistemic | EERIE为非常规单词，参考有限 |
| 玩家行为变化 | Aleatoric | 不同日期玩家群体差异 |

---

## 四、论文撰写建议

### 4.1 建议章节结构

```
4.3 Problem 3: Predicting Result Distribution
    4.3.1 Problem Description
    4.3.2 Feature Engineering
    4.3.3 Multi-Output Regression Model
    4.3.4 EERIE Prediction
    4.3.5 Uncertainty Analysis
    4.3.6 Model Confidence Evaluation
```

### 4.2 关键公式LaTeX格式

```latex
% 多输出回归
\mathbf{y} = f(\mathbf{x}) + \boldsymbol{\varepsilon}

% 随机森林集成
\hat{y}_j = \frac{1}{B} \sum_{b=1}^{B} T_b(\mathbf{x})

% Bootstrap置信区间
CI_{95\%} = [\hat{y}_{2.5\%}, \hat{y}_{97.5\%}]

% 预测约束
\sum_{j=1}^{7} y_j \approx 100\%
```

### 4.3 常用英文表达

**描述模型**：
- "We employ a Random Forest multi-output regression model to simultaneously predict the distribution of results across all seven categories."
- "Bootstrap resampling (n=200) is used to quantify prediction uncertainty and construct 95% confidence intervals."

**描述EERIE**：
- "EERIE presents unique challenges due to its unusual structure: 3 repeated E's and 80% vowel ratio."
- "The model predicts that approximately 29% of players will solve EERIE in 3 attempts, with a 95% CI of [18.4%, 33.4%]."

**讨论不确定性**：
- "The primary sources of uncertainty include: (1) sampling bias in Twitter data, (2) incomplete feature coverage, and (3) the rarity of words similar to EERIE in our training data."

### 4.4 EERIE预测表格模板

```latex
\begin{table}[h]
\centering
\caption{Predicted Result Distribution for EERIE (March 1, 2023)}
\begin{tabular}{lccc}
\hline
\textbf{Tries} & \textbf{Prediction} & \textbf{95\% CI} & \textbf{Hist. Avg.} \\
\hline
1 & 0.5\% & [0.0\%, 0.9\%] & 0\% \\
2 & 13.0\% & [6.3\%, 17.1\%] & 3\% \\
3 & 29.2\% & [18.4\%, 33.4\%] & 23\% \\
4 & 29.8\% & [25.6\%, 32.8\%] & 34\% \\
5 & 17.6\% & [14.9\%, 23.4\%] & 25\% \\
6 & 8.4\% & [5.1\%, 17.9\%] & 11\% \\
X & 2.2\% & [0.5\%, 8.0\%] & 2\% \\
\hline
\end{tabular}
\end{table}
```

---

## 五、图片列表与插入位置

| 编号 | 文件名 | 内容 | 建议插入章节 |
|------|--------|------|-------------|
| 图1 | fig1_distribution_boxplot.pdf | 结果分布箱线图 | 4.3.1 数据描述 |
| 图2 | fig2_average_distribution.pdf | 平均结果分布柱状图 | 4.3.1 数据描述 |
| 图3 | fig3_feature_target_correlation.pdf | 特征-目标相关性热力图 | 4.3.2 特征分析 |
| 图4 | fig4_model_comparison.pdf | 模型MAE对比 | 4.3.3 模型选择 |
| 图5 | fig5_feature_importance.pdf | 特征重要性 | 4.3.3 模型分析 |
| 图6 | fig6_eerie_prediction.pdf | EERIE预测vs历史平均 | 4.3.4 预测结果 |
| 图7 | fig7_bootstrap_distribution.pdf | Bootstrap预测分布（7合1） | 4.3.5 不确定性分析 |

### 图片引用示例

```latex
Figure \ref{fig:eerie_pred} shows the predicted result distribution for EERIE 
compared to the historical average. The model predicts a higher proportion of 
3-try solves (29.2\%) compared to the historical average (23\%), likely due 
to EERIE's unusual letter pattern.

The Bootstrap distributions (Fig. \ref{fig:bootstrap}) illustrate the 
uncertainty in our predictions. The widest confidence intervals are observed 
for try\_3 and try\_6, reflecting greater model uncertainty in these regions.
```
