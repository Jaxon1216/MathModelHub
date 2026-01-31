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

### 1.1 问题本质

分析影响选手成绩的因素：
- **专业舞伴效应**：不同舞伴是否带来不同成绩？
- **明星特征**：行业、年龄、国籍是否影响表现？
- **外部因素**：知名度（pageviews）是否相关？

### 1.2 建模策略

采用**多层次分析方法**：
1. **描述统计**：各因素的分布和差异
2. **ANOVA**：检验组间差异显著性
3. **回归分析**：量化各因素影响
4. **随机森林**：特征重要性排序

---

## 二、模型介绍与公式

### 2.1 ANOVA（方差分析）

检验不同行业选手成绩是否有显著差异：

$$F = \frac{MS_{between}}{MS_{within}} = \frac{\sum_{i=1}^{k} n_i(\bar{x}_i - \bar{x})^2 / (k-1)}{\sum_{i=1}^{k} \sum_{j=1}^{n_i} (x_{ij} - \bar{x}_i)^2 / (N-k)}$$

其中：
- $k$：组数（行业数）
- $n_i$：第$i$组样本量
- $\bar{x}_i$：第$i$组均值
- $\bar{x}$：总体均值

### 2.2 多元回归模型

$$\text{Placement}_i = \beta_0 + \beta_1 \cdot \text{Age}_i + \beta_2 \cdot \text{JudgeScore}_i + \epsilon_i$$

### 2.3 随机森林特征重要性

基于基尼不纯度减少量：

$$\text{Importance}(X_j) = \frac{1}{N_{trees}} \sum_{t=1}^{N_{trees}} \sum_{n \in N_t(j)} p(n) \cdot \Delta i(n)$$

---

## 三、结果解读

### 3.1 行业影响

| 行业 | 平均名次 | 胜率 | 样本数 |
|------|---------|------|--------|
| Athlete | 6.3 | 11.6% | 95 |
| TV Personality | 6.7 | 9.0% | 67 |
| Actor/Actress | 6.8 | 6.2% | 128 |
| Singer/Rapper | 6.9 | 6.6% | 61 |
| Other | 7.0 | 9.8% | 41 |
| Comedian | 8.8 | 0.0% | 12 |
| Model | 8.9 | 5.9% | 17 |

**ANOVA结果**：F=1.784, p=0.1010（行业差异不显著）

**关键发现**：
- 运动员表现最佳，可能因为身体协调性和训练经历
- 喜剧演员和模特表现较差
- 但统计上差异不显著（p>0.05）

### 3.2 年龄影响

| 年龄组 | 平均名次 | 冠军数 | 样本数 |
|--------|---------|--------|--------|
| <25 | 4.8 | 9 | 67 |
| 25-35 | 5.6 | 17 | 135 |
| 35-45 | 7.1 | 6 | 100 |
| 45+ | 9.1 | 2 | 119 |

**相关性**：r=0.433（年龄越大，名次越靠后）

**关键发现**：
- 年轻选手表现显著更好
- 25岁以下选手平均第5名，45岁以上平均第9名
- 这可能反映了舞蹈对身体素质的要求

### 3.3 专业舞伴影响

| 舞伴 | 平均名次 | 冠军数 | 合作次数 |
|------|---------|--------|---------|
| Derek Hough | 2.9 | 6 | - |
| Mark Ballas | 3.8 | 2 | - |
| Val Chmerkovskiy | 4.2 | 2 | - |

**关键发现**：
- 专业舞伴差异显著
- Derek Hough是最成功的舞伴（6次冠军）
- 好的舞伴可以平均提升3-4名

### 3.4 特征重要性

| 特征 | 重要性 |
|------|--------|
| avg_score（评委得分）| 0.876 |
| season | 0.074 |
| age | 0.028 |
| industry | 0.019 |
| is_us | 0.004 |

**关键发现**：
- 评委得分是最重要的预测因素（占87.6%）
- 其他因素影响相对较小
- 说明「实力」是决定因素，但外部因素通过影响粉丝投票间接作用

### 3.5 回归模型

$$\text{Placement} = \beta_0 + 0.004 \times \text{Age} - 2.25 \times \text{JudgeScore}$$

- R² = 0.648（模型解释64.8%的方差）
- 评委得分系数显著（p<0.001）
- 年龄系数不显著（p=0.69）

### 3.6 随机森林模型评估指标（5折交叉验证）

| 指标 | 值 | 解读 |
|------|-----|------|
| R² | 0.488 | 模型解释48.8%的名次方差 |
| RMSE | 2.688 | 均方根误差，约2.7个名次 |
| MAE | 2.090 | 平均绝对误差，约2个名次 |

**解读**：
- RMSE > MAE 说明存在一些较大的预测偏差（异常值）
- MAE=2.09 意味着平均预测误差约为2个名次，对于1-13名的预测是合理的
- 这些指标与R²互补，提供了误差的绝对规模

---

## 四、论文撰写建议

### 4.1 建议章节结构

```
5. Factor Impact Analysis
   5.1 Professional Dancer Effect
   5.2 Celebrity Industry Analysis
   5.3 Age Impact Assessment
   5.4 Feature Importance Ranking
   5.5 Regression Model and Interpretation
```

### 4.2 关键公式LaTeX

```latex
% ANOVA
F = \frac{MS_{between}}{MS_{within}}

% 相关系数
r = \frac{\sum(x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum(x_i - \bar{x})^2 \sum(y_i - \bar{y})^2}}

% 回归模型
\text{Placement} = \beta_0 + \beta_1 \cdot \text{Age} + \beta_2 \cdot \text{JudgeScore}
```

### 4.3 常用英文表达

- "We employ ANOVA to test whether industry categories significantly affect placement."
- "The correlation coefficient r=0.433 indicates a moderate positive relationship between age and placement."
- "Feature importance analysis reveals that judge scores dominate the prediction (87.6%)."
- "Younger contestants (<25) achieve significantly better placements (mean=4.8) compared to older contestants (45+, mean=9.1)."

---

## 五、图片列表与插入位置

| 编号 | 文件名 | 内容 | 建议插入章节 |
|------|--------|------|-------------|
| 1 | fig1_industry_impact.pdf | 行业影响（平均名次、胜率） | 5.2 |
| 2 | fig2_age_impact.pdf | 年龄影响（散点图、箱线图） | 5.3 |
| 3 | fig3_feature_importance.pdf | 特征重要性条形图 | 5.4 |
| 4 | fig4_pro_dancer_impact.pdf | 专业舞伴影响（冠军数、平均名次） | 5.1 |

### 图片引用示例

```latex
As shown in Fig. 3, judge scores account for 87.6% of the feature importance 
in predicting final placement, indicating that actual dancing performance 
remains the dominant factor despite the influence of fan voting.
```
