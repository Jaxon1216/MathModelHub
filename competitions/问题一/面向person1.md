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
观众投票数是保密信息，但我们知道：
1. 每周被淘汰的是综合得分最低者
2. 综合得分 = 评委得分 + 观众投票（通过特定方式结合）
3. 评委得分已知

**逆问题本质**：已知淘汰结果，反推投票分布

### 1.2 建模策略

采用**约束优化 + Softmax投票模型**：

1. **Softmax假设**：粉丝投票与选手「人气」正相关，人气与评委得分存在基础关联
2. **人气因子**：引入参数 $\alpha_i$ 表示选手相对于基础预期的人气偏离
3. **约束条件**：估算的投票必须使被淘汰者综合得分最低

### 1.3 为什么选择这种方法

| 方法 | 优点 | 缺点 |
|------|------|------|
| 贝叶斯MCMC | 提供后验分布 | 计算复杂，需先验假设 |
| 线性规划 | 精确满足约束 | 解空间可能不唯一 |
| **约束优化** | 灵活、可解释 | 局部最优 |

我们选择约束优化因为：
- 可直接编码淘汰约束
- 人气因子提供可解释性
- Bootstrap提供不确定性估计

---

## 二、模型介绍与公式

### 2.1 投票估算模型

**符号定义**：
- $s_i$：选手 $i$ 的评委总得分
- $\alpha_i$：选手 $i$ 的人气因子（待估参数）
- $v_i$：选手 $i$ 的投票份额

**投票份额计算（Softmax模型）**：

$$v_i = \frac{\exp\left(\frac{s_i(1+\alpha_i)}{\bar{s}}\right)}{\sum_{j=1}^{n} \exp\left(\frac{s_j(1+\alpha_j)}{\bar{s}}\right)}$$

其中 $\bar{s}$ 是当周平均得分（归一化因子）。

### 2.2 综合得分计算

**排名法**（S1-2, S28-34）：
$$C_i = R_i^{judge} + R_i^{fan}$$

**百分比法**（S3-27）：
$$C_i = P_i^{judge} + P_i^{fan} = \frac{s_i}{\sum_j s_j} + v_i$$

### 2.3 约束优化问题

$$\min_{\alpha} \sum_{i=1}^{n} \alpha_i^2$$

**约束**：被淘汰者 $k$ 的综合得分必须最低
- 排名法：$C_k = \max_i C_i$
- 百分比法：$C_k = \min_i C_i$

**参数范围**：$\alpha_i \in [-1, 2]$

### 2.4 不确定性估计

使用**Bootstrap方法**：
1. 对评委得分添加随机扰动（$\sigma = 0.05 \times \text{std}(s)$）
2. 重复估算投票 $B=100$ 次
3. 计算投票份额的均值、标准差、置信区间

**确定性指标**：
$$\text{Certainty} = 1 - \frac{\sigma_v}{\mu_v}$$

---

## 三、结果解读

### 3.1 一致性分析

| 指标 | 数值 | 解读 |
|------|------|------|
| 总体一致率 | 80.7% | 模型大部分周次与淘汰一致 |
| 一致周次数 | 221 / 274 | 符合约束的淘汰事件数 |
| 排名法一致率 | 38.4% | S1-2, S28-34（整数排名限制） |
| 百分比法一致率 | 96.0% | S3-27（连续优化空间大） |
| 确定性指标 | 0.995 | 估算高度稳定 |

**分析**：
- 80.7%的总体一致率表明模型能够很好地捕捉投票-淘汰关系
- 百分比法一致率(96.0%)远高于排名法(38.4%)，因为连续空间提供更多优化自由度
- 排名法一致率较低是因为整数排名限制了调整空间
- 约19%的不一致主要来自排名法季节，反映了离散排名的固有限制
- 模型成功为大部分淘汰事件找到了合理的投票分布解释

### 3.2 确定性分析

| 指标 | 数值 | 解读 |
|------|------|------|
| 平均确定性 | 0.995 | 估算高度稳定 |
| 确定性标准差 | 0.002 | 波动极小 |

**分析**：
- 高确定性表明在给定评委得分下，投票分布相对确定
- Bootstrap扰动对结果影响微小

### 3.3 争议选手分析

| 选手 | 季数 | 平均投票份额 | 平均评委排名 | 特点 |
|------|------|-------------|-------------|------|
| Jerry Rice | S2 | 0.165 | 4.6 | 高人气弥补技术不足 |
| Billy Ray Cyrus | S4 | 0.107 | 6.5 | 名人效应明显 |
| Bristol Palin | S11 | 0.127 | 7.2 | 政治人物争议 |
| Bobby Bones | S27 | 0.112 | 7.0 | 广播名人粉丝基础 |

### 3.4 争议选手量化定义与整体分析（新增亮点）

**量化定义**：
$$\text{Controversy Score}_i = \text{Judge Rank}_i - \text{Final Placement}_i \geq 3$$

即：选手最终排名比裁判评估排名高出3位以上，视为"争议选手"。

**筛选结果**：共识别出 **32名争议选手**（占421人的7.6%）

| 指标 | 争议选手 (n=32) | 普通选手 (n=389) |
|------|-----------------|------------------|
| 平均最终排名 | 5.53 | 6.92 |
| 平均裁判分数 | 22.05 | 24.34 |
| 平均争议度 | +3.88 | -0.34 |

**关键发现**：
- 争议选手获得**更好排名（5.53 vs 6.92）**但**更低裁判分（22.05 vs 24.34）**
- 这证实了模型的popularity factor α_i：争议选手需要更高的α_i值来解释其"低分高名"现象
- 该量化定义使分析更客观，避免主观挑选

---

## 四、论文撰写建议

### 4.1 建议章节结构

```
3. Fan Vote Estimation Model
   3.1 Problem Formulation
   3.2 Softmax Voting Model
   3.3 Constrained Optimization
   3.4 Uncertainty Quantification
   3.5 Consistency Validation
   3.6 Case Study: Controversial Contestants
```

### 4.2 关键公式LaTeX

```latex
% 投票份额
v_i = \frac{\exp\left(\frac{s_i(1+\alpha_i)}{\bar{s}}\right)}{\sum_{j=1}^{n} \exp\left(\frac{s_j(1+\alpha_j)}{\bar{s}}\right)}

% 百分比法综合得分
C_i = \frac{s_i}{\sum_j s_j} + v_i

% 确定性指标
\text{Certainty} = 1 - \frac{\sigma_v}{\mu_v}
```

### 4.3 常用英文表达

- "We formulate fan vote estimation as a constrained optimization problem."
- "The Softmax function naturally models the competitive allocation of votes."
- "Consistency rate measures how well our estimates align with actual eliminations."
- "The high certainty index indicates stable vote share estimates under perturbation."
- "Controversial contestants exhibit a notable discrepancy between judge rankings and fan support."

---

## 五、图片列表与插入位置

| 编号 | 文件名 | 内容 | 建议插入章节 |
|------|--------|------|-------------|
| 1 | fig1_consistency_analysis.pdf | 一致性分析（按季、按方法） | 3.5 Consistency Validation |
| 2 | fig2_uncertainty_analysis.pdf | 不确定性分析（分布、与得分关系） | 3.4 Uncertainty Quantification |
| 3 | fig3_controversial_analysis.pdf | 争议选手投票与排名对比 | 3.6 Case Study |
| 4 | fig4_vote_score_relationship.pdf | 投票与得分关系、人气因子分布 | 3.2 Softmax Voting Model |
| 5 | fig5_certainty_distribution.pdf | 确定性按季/周分布 | 3.4 Uncertainty Quantification |

### 图片引用示例

```latex
As illustrated in Fig. 3, controversial contestants such as Bobby Bones 
consistently ranked low among judges (average rank: 7.0) while maintaining 
moderate fan support (average vote share: 0.112), indicating a significant 
judge-fan discrepancy.
```
