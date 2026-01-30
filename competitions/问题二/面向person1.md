# 问题二建模分析 —— 写作指南

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

DWTS使用了两种投票结合方式：
1. **排名法**（S1-2, S28-34）：评委排名 + 粉丝排名
2. **百分比法**（S3-27）：评委得分% + 粉丝投票%

需要分析：
- 两种方法产生的结果差异
- 哪种方法更偏向粉丝投票
- 争议选手在不同方法下的命运
- 评委打破平局规则的影响

### 1.2 建模策略

采用**反事实分析**：
1. 用问题一估算的投票，同时应用两种方法到所有季
2. 比较两种方法产生的淘汰结果
3. 分析争议选手的案例
4. 模拟评委打破平局规则

---

## 二、模型介绍与公式

### 2.1 排名法（Rank-Based Method）

**综合排名计算**：
$$C_i^{rank} = R_i^{judge} + R_i^{fan}$$

其中：
- $R_i^{judge}$：评委得分排名（1=最高）
- $R_i^{fan}$：粉丝投票排名（1=最高）
- 综合排名最高者被淘汰

### 2.2 百分比法（Percentage-Based Method）

**综合百分比计算**：
$$C_i^{pct} = P_i^{judge} + P_i^{fan} = \frac{s_i}{\sum_j s_j} + \frac{v_i}{\sum_j v_j}$$

其中：
- $P_i^{judge}$：评委得分占比
- $P_i^{fan}$：粉丝投票占比
- 综合百分比最低者被淘汰

### 2.3 方法偏向性度量

**粉丝影响力指标**：
$$\text{Fan Influence} = \text{corr}(v_i, C_i)$$

正值表示粉丝投票高的选手综合得分更高（方法偏向粉丝）

### 2.4 评委打破平局规则

从第28季开始，综合得分最低的两位选手中，由评委投票决定淘汰：
$$\text{Eliminated} = \arg\min_{i \in \text{Bottom 2}} s_i$$

---

## 三、结果解读

### 3.1 方法比较结果

| 指标 | 数值 | 解读 |
|------|------|------|
| 两种方法结果一致率 | 95.5% | 绝大多数情况下两种方法产生相同淘汰 |
| 不一致周次数 | 15 / 335 | 约4.5%的周次两种方法结果不同 |
| 排名法粉丝影响力 | 负相关 | 粉丝投票高→综合排名好 |
| 百分比法粉丝影响力 | 正相关 | 粉丝投票高→综合百分比高 |

**分析**：
- 95.5%的高一致率表明在大多数情况下，两种方法的淘汰决策一致
- 当选手间差距明显时，方法选择影响较小
- 差异主要出现在选手得分接近时（约4.5%的情况）

### 3.2 争议选手分析

| 选手 | 最终名次 | 排名法淘汰次数 | 百分比法淘汰次数 |
|------|---------|---------------|-----------------|
| Jerry Rice | 第2名 | 3次 | 3次 |
| Billy Ray Cyrus | 第5名 | 3次 | 3次 |
| Bristol Palin | 第3名 | 7次 | 7次 |
| Bobby Bones | 第1名 | 2次 | 2次 |

**关键发现**：
- Bristol Palin在14周中有7周处于「应淘汰」位置，但最终获得第3名
- Bobby Bones作为冠军，也有2周处于淘汰边缘
- 这些选手的高人气补偿了评委低分

### 3.3 评委打破平局规则影响

| 指标 | 数值 |
|------|------|
| 改变结果比例 | 3.9% |
| 改变周次数 | 13 / 333 |

**分析**：
- 评委打破平局规则在约4%的情况下改变了淘汰结果
- 该规则给予评委最终决定权，增加了专业性权重
- 在选手综合得分接近时，评委意见起到了关键作用

---

## 四、论文撰写建议

### 4.1 建议章节结构

```
4. Voting Method Comparison
   4.1 Rank-Based vs Percentage-Based Methods
   4.2 Method Bias Analysis
   4.3 Controversial Contestant Case Studies
   4.4 Impact of Judge Tiebreaker Rule
   4.5 Recommendations for Future Seasons
```

### 4.2 关键公式LaTeX

```latex
% 排名法
C_i^{rank} = R_i^{judge} + R_i^{fan}

% 百分比法
C_i^{pct} = \frac{s_i}{\sum_j s_j} + \frac{v_i}{\sum_j v_j}

% 粉丝影响力
\text{Fan Influence} = \text{corr}(v_i, C_i)
```

### 4.3 常用英文表达

- "We apply counterfactual analysis to compare the two voting methods."
- "The rank-based method treats all position differences equally."
- "The percentage-based method is more sensitive to score magnitudes."
- "Controversial contestants demonstrate a significant judge-fan discrepancy."
- "The tiebreaker rule gives judges final authority in close eliminations."

---

## 五、图片列表与插入位置

| 编号 | 文件名 | 内容 | 建议插入章节 |
|------|--------|------|-------------|
| 1 | fig1_method_comparison.pdf | 方法比较（一致性、偏向性） | 4.1-4.2 |
| 2 | fig2_controversial_methods.pdf | 争议选手两种方法对比 | 4.3 |
| 3 | fig3_tiebreaker_analysis.pdf | 评委打破平局分析 | 4.4 |

### 推荐使用的结论

**方法选择建议**：
> Based on our analysis, we recommend the **percentage-based method** for future seasons because:
> 1. It provides a more nuanced evaluation of performance differences
> 2. It naturally balances judge expertise with fan engagement
> 3. Combined with the tiebreaker rule, it ensures professional input in close calls
