# 问题二建模分析 —— 写作指南

> 本文档面向写作手Person1，帮助理解两种投票方式的比较分析。

## 目录
1. [问题分析与建模思路](#一问题分析与建模思路)
2. [模型介绍与公式](#二模型介绍与公式)
3. [结果解读](#三结果解读)
4. [论文撰写建议](#四论文撰写建议)
5. [图片列表与插入位置](#五图片列表与插入位置)

---

## 一、问题分析与建模思路

### 1.1 问题核心

问题二要求比较两种投票结合方式的差异：
- **排名制 (Rank-based)**：S1-2, S28-34使用
- **百分比制 (Percentage-based)**：S3-27使用

需要回答：
1. 两种方式的结果差异有多大？
2. 哪种方式更偏向观众/评委？
3. 争议选手在两种方式下结果是否不同？
4. 评委决胜规则有何影响？

### 1.2 分析思路

```
1. 将两种方式应用到所有264周
2. 比较淘汰结果是否一致
3. 分析淘汰者的「评委排名」vs「投票排名」特征
4. 模拟评委决胜规则的影响
5. 给出推荐
```

---

## 二、模型介绍与公式

### 2.1 排名制 (Rank-based)

计算每位选手的：
- 评委排名 $R_{judge,i}$（得分越高排名越靠前，数值越小）
- 观众排名 $R_{fan,i}$

综合排名：
$$R_{total,i} = R_{judge,i} + R_{fan,i}$$

**淘汰规则**：$R_{total}$ 最高者淘汰

### 2.2 百分比制 (Percentage-based)

计算每位选手的：
- 评委百分比 $P_{judge,i} = \frac{J_i}{\sum_j J_j}$
- 观众百分比 $P_{fan,i} = \frac{V_i}{\sum_j V_j}$

综合百分比：
$$P_{total,i} = P_{judge,i} + P_{fan,i}$$

**淘汰规则**：$P_{total}$ 最低者淘汰

### 2.3 偏向性指标

定义偏向指标：
$$Bias = \frac{R_{judge,elim} - R_{fan,elim}}{n}$$

- 正值 = 淘汰者评委排名更差 → 偏向评委
- 负值 = 淘汰者投票排名更差 → 偏向观众

### 2.4 评委决胜规则

S28起采用：
1. 计算综合排名/百分比，确定Bottom 2
2. 由评委从Bottom 2中选择淘汰对象
3. 假设：评委倾向于淘汰「评委得分更低」的选手

---

## 三、结果解读

### 3.1 两种方式一致性（核心发现）

| 指标 | 数值 |
|------|------|
| 分析周数 | 264 |
| **一致率** | **89.8%** |
| 不一致周数 | 27周 |

**结论**：两种方式在约90%的情况下给出相同的淘汰结果。

### 3.2 偏向性分析

| 方式 | 平均偏向 | 解读 |
|------|----------|------|
| 排名制 | 0.0390 | 轻微偏向评委 |
| 百分比制 | 0.0938 | 更偏向评委 |

**结论**：百分比制相对更偏向评委意见（淘汰者的评委排名更差）。

### 3.3 与实际结果一致率

| 方式 | 一致率 |
|------|--------|
| 排名制 | 64.4% |
| **百分比制** | **67.0%** |
| 排名制+评委决胜 | 30.7% |
| 百分比制+评委决胜 | 30.3% |

**关键发现**：
- 百分比制与实际结果一致性更高
- 评委决胜规则反而**降低**了一致率（因为我们假设评委选得分更低者，但实际可能选得分更高者以保护节目效果）

### 3.4 争议选手分析

| 选手 | 赛季 | 排名制淘汰次数 | 百分比制淘汰次数 |
|------|------|----------------|------------------|
| Jerry Rice | S2 | 3 | 3 |
| Billy Ray Cyrus | S4 | 1 | 1 |
| Bristol Palin | S11 | 0 | 0 |
| Bobby Bones | S27 | 0 | 0 |

**关键发现**：
- 对于Bristol Palin和Bobby Bones，两种方式都**不会**导致他们被淘汰
- 这说明他们的观众投票确实足够高，无论采用哪种方式都能存活
- 争议的核心不是投票方式，而是**观众投票与评委意见的分歧本身**

### 3.5 评委决胜规则影响

| 方式 | 改变率 |
|------|--------|
| 排名制 | 43.2% |
| 百分比制 | 38.3% |

**结论**：评委决胜规则会改变约40%的淘汰结果，影响显著。

---

## 四、论文撰写建议

### 4.1 建议章节结构

```
4. Task 2: Voting Method Analysis
   4.1 Methodology
       4.1.1 Rank-based Method
       4.1.2 Percentage-based Method
   4.2 Method Comparison
       4.2.1 Agreement Rate
       4.2.2 Bias Analysis
   4.3 Controversial Cases Analysis
   4.4 Judge Tiebreaker Rule Analysis
   4.5 Recommendations
```

### 4.2 关键公式LaTeX

```latex
% 排名制
R_{total,i} = R_{judge,i} + R_{fan,i}

% 百分比制
P_{total,i} = \frac{J_i}{\sum_{j=1}^{n} J_j} + \frac{V_i}{\sum_{j=1}^{n} V_j}

% 偏向性指标
Bias = \frac{R_{judge,elim} - R_{fan,elim}}{n}
```

### 4.3 推荐结论写法

**推荐采用百分比制**：

> Based on our analysis, we recommend the percentage-based method for future seasons. This method achieves a higher consistency rate (67.0%) with actual elimination results compared to the rank-based method (64.4%). Additionally, the percentage-based method provides a more transparent combination of judge scores and fan votes.

**关于评委决胜规则**：

> While the judge tiebreaker rule was introduced to prevent controversial outcomes, our analysis shows that it would change approximately 40% of elimination results. However, the rule's effectiveness depends on judges' actual decision criteria, which may not always favor the lower-scoring contestant.

### 4.4 常用英文表达

| 中文 | 英文 |
|------|------|
| 排名制 | rank-based method |
| 百分比制 | percentage-based method |
| 一致率 | agreement rate / consistency rate |
| 偏向性 | bias |
| 评委决胜 | judge tiebreaker |
| 争议选手 | controversial contestant |

---

## 五、图片列表与插入位置

| 编号 | 文件名 | 内容 | 建议插入章节 |
|------|--------|------|-------------|
| 1 | fig1_method_comparison.pdf | 偏向性分布+按赛季一致率 | 4.2 Method Comparison |
| 2 | fig2_controversial_methods.pdf | 争议选手两种方式对比 | 4.3 Controversial Cases |
| 3 | fig3_tiebreaker_analysis.pdf | 评委决胜规则影响 | 4.4 Judge Tiebreaker |

---

## 六、数据引用速查

```
- 两种方式一致率: 89.8%
- 不一致周数: 27/264
- 排名制偏向: 0.0390
- 百分比制偏向: 0.0938
- 排名制与实际一致率: 64.4%
- 百分比制与实际一致率: 67.0%
- 评委决胜改变率(排名制): 43.2%
- 评委决胜改变率(百分比制): 38.3%
```
