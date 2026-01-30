# 问题一建模分析 —— 写作指南

> 本文档面向写作手Person1，帮助理解建模方法、公式符号，并指导论文撰写。

## 目录
1. [问题分析与建模思路](#一问题分析与建模思路)
2. [模型介绍与公式](#二模型介绍与公式)
3. [结果解读](#三结果解读)
4. [论文撰写建议](#四论文撰写建议)
5. [图片列表与插入位置](#五图片列表与插入位置)

---

## 一、问题分析与建模思路

### 1.1 问题本质

问题一要求**反向推断观众投票**。这是一个典型的**逆问题（Inverse Problem）**：
- **已知**：评委得分 $J_i$、淘汰结果、投票结合规则
- **未知**：观众投票比例 $V_i$

核心约束是：**被淘汰者的综合得分必须是最低的**（对于百分比制）或**综合排名必须是最高的**（对于排名制）。

### 1.2 为什么选择约束优化方法

1. **符合问题结构**：淘汰结果提供了硬性约束条件
2. **可解释性强**：满足约束的解都是"合理"的投票分布
3. **无需假设具体分布**：不像统计模型需要假设投票服从某种分布

### 1.3 解决思路

```
对于每一周：
1. 获取当周所有选手的评委得分
2. 找出实际被淘汰的选手
3. 根据投票结合规则（排名制/百分比制）
4. 求解满足"淘汰者综合得分最低"约束的投票分布
5. 用Bootstrap量化不确定性
```

---

## 二、模型介绍与公式

### 2.1 投票结合规则

**排名制**（S1-2, S28-34）：
$$R_{total,i} = R_{judge,i} + R_{fan,i}$$

其中 $R_{judge,i}$ 是选手 $i$ 的评委得分排名（1=最高），$R_{fan,i}$ 是观众投票排名。综合排名 $R_{total}$ **最高者淘汰**。

**百分比制**（S3-27）：
$$P_{total,i} = P_{judge,i} + P_{fan,i} = \frac{J_i}{\sum_j J_j} + V_i$$

其中 $V_i$ 是选手 $i$ 获得的投票比例，$\sum_i V_i = 1$。综合百分比 $P_{total}$ **最低者淘汰**。

### 2.2 约束优化模型（百分比制）

**目标函数**：最小化与均匀分布的偏差（最大熵原则）
$$\min \sum_{i=1}^{n} \left( V_i - \frac{1}{n} \right)^2$$

**约束条件**：
1. 归一化：$\sum_{i=1}^{n} V_i = 1$
2. 非负性：$V_i \geq 0$
3. 淘汰约束：对于被淘汰者 $e$ 和所有其他选手 $j$：
   $$P_{judge,e} + V_e \leq P_{judge,j} + V_j - \epsilon$$

其中 $\epsilon$ 是一个小的margin（如0.001），确保淘汰者确实是综合得分最低。

### 2.3 确定性指标

我们定义综合确定性指标：
$$C = 0.3 \times (1 - H_{norm}) + 0.3 \times 5 \times G + 0.4 \times \frac{\rho + 1}{2}$$

其中：
- $H_{norm}$ = 归一化熵，衡量投票分布的集中度
- $G$ = 最低投票与次低投票的差距
- $\rho$ = 投票排名与得分排名的Spearman相关系数

---

## 三、结果解读

### 3.1 一致性检验结果（核心！）

| 指标 | 数值 | 解读 |
|------|------|------|
| **总体准确率** | **93.9%** | 模型能正确预测93.9%周的淘汰结果 |
| 百分比制准确率 | 98.5% | 25个赛季，几乎完美 |
| 排名制准确率 | 80.3% | 9个赛季，准确率较低 |

**关键结论**：百分比制下的投票估算更可靠，排名制存在更多不确定性。

### 3.2 不确定性分析

| 指标 | 数值 |
|------|------|
| 平均确定性 | 0.273 |
| 确定性标准差 | 0.142 |

确定性较低的原因：存在多组投票分布都能满足约束，说明问题本身存在解的不唯一性。

### 3.3 投票与得分关系

- **相关系数** r = 0.371
- 投票与评委得分正相关，但相关性不强
- 说明观众投票受到评委得分以外的因素影响（如明星人气）

### 3.4 争议选手分析

| 选手 | 赛季 | 评委排名 | 投票排名 | 差距 |
|------|------|----------|----------|------|
| Jerry Rice | S2 | 4.8 | 5.2 | -0.5 |
| Billy Ray Cyrus | S4 | 6.6 | 6.1 | +0.5 |
| Bristol Palin | S11 | 6.0 | 5.4 | +0.6 |
| **Bobby Bones** | S27 | **7.2** | **6.6** | **+0.7** |

**关键发现**：Bobby Bones的投票排名比评委排名好0.7位，但差距并不大。这说明他能夺冠主要靠**稳定获得足够多的投票**，而非特别高的投票。

---

## 四、论文撰写建议

### 4.1 建议章节结构

```
3. Task 1: Fan Vote Estimation Model
   3.1 Problem Formulation
   3.2 Methodology
       3.2.1 Rank-based Method (Seasons 1-2, 28-34)
       3.2.2 Percentage-based Method (Seasons 3-27)
   3.3 Consistency Verification
   3.4 Uncertainty Quantification
   3.5 Results and Analysis
```

### 4.2 关键公式LaTeX格式

```latex
% 百分比制综合得分
P_{total,i} = \frac{J_i}{\sum_{j=1}^{n} J_j} + V_i

% 约束优化目标
\min_{V} \sum_{i=1}^{n} \left( V_i - \frac{1}{n} \right)^2
\quad \text{s.t.} \quad \sum_i V_i = 1, \; V_i \geq 0

% 确定性指标
C = 0.3(1-H_{norm}) + 1.5G + 0.2(\rho + 1)
```

### 4.3 常用英文表达

| 中文 | 英文表达 |
|------|----------|
| 反向推断 | inverse inference / backward estimation |
| 约束优化 | constrained optimization |
| 一致性检验 | consistency verification |
| 不确定性量化 | uncertainty quantification |
| 准确率 | accuracy / consistency rate |
| 置信区间 | confidence interval |

### 4.4 论文句式示例

**方法描述**：
> We formulate the fan vote estimation as a constrained optimization problem, where the elimination outcome serves as the constraint to ensure that the estimated votes correctly identify the eliminated contestant.

**结果描述**：
> The model achieves an overall consistency rate of 93.9%, demonstrating high reliability in reconstructing the fan voting patterns. Notably, the percentage-based method (Seasons 3-27) yields a higher accuracy of 98.5% compared to 80.3% for the rank-based method.

**争议选手分析**：
> For Bobby Bones (Season 27), our model estimates that his average fan vote rank (6.6) was 0.7 positions better than his average judge rank (7.2), suggesting moderate fan support rather than overwhelmingly high votes.

---

## 五、图片列表与插入位置

| 编号 | 文件名 | 内容 | 建议插入章节 |
|------|--------|------|-------------|
| 1 | fig1_consistency_analysis.pdf | 按赛季/选手数的一致性分析 | 3.3 Consistency Verification |
| 2 | fig2_accuracy_by_method.pdf | 两种投票方式的准确率对比 | 3.3 Consistency Verification |
| 3 | fig3_certainty_distribution.pdf | 确定性指标分布 | 3.4 Uncertainty Quantification |
| 4 | fig4_vote_score_relationship.pdf | 投票与得分关系散点图 | 3.5 Results and Analysis |
| 5 | fig5_controversial_analysis.pdf | 争议选手排名对比 | 3.5.2 Controversial Cases |

### 图片引用示例

> As illustrated in Fig. 1(a), the consistency rate varies across seasons, with most seasons achieving above 80% accuracy. Fig. 1(b) shows that the consistency rate is relatively stable across different numbers of contestants.

> Fig. 2 compares the consistency rates between the two voting methods. The percentage-based method (98.5%) significantly outperforms the rank-based method (80.3%), suggesting that our optimization approach is more suitable for the percentage combination rule.

---

## 六、数据引用速查

供论文直接引用的关键数据：

```
- 总体一致性准确率: 93.9% (248/264周)
- 百分比制准确率: 98.5% (n=198)
- 排名制准确率: 80.3% (n=66)
- 平均确定性: 0.273 ± 0.142
- 投票-得分相关系数: r = 0.371
- Bobby Bones排名差距: +0.7 (投票更好)
```
