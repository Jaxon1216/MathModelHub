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

### 1.1 问题理解

问题二要求：
1. 判断单词属性（元音数量、重复字母数、字母频率等）是否影响**困难模式玩家占比**
2. 若有影响，需量化说明
3. 若无影响，需解释原因

### 1.2 建模思路

采用**多层次统计分析**方法：

```
数据准备 → 相关性分析 → 多元回归 → 特征重要性 → 得出结论
```

**分析逻辑**：
1. **相关性分析**：计算各属性与目标变量的Pearson/Spearman相关系数
2. **显著性检验**：通过p值判断相关性是否具有统计意义
3. **回归分析**：评估多个属性的联合解释能力（R²）
4. **特征重要性**：使用随机森林评估非线性关系

**类比理解**：
- 这就像研究「身高是否影响考试成绩」——我们收集数据、计算相关系数、做显著性检验
- 如果相关系数接近0且p值很大，说明两者没有显著关联

---

## 二、模型介绍与公式

### 2.1 Pearson相关系数

$$r = \frac{\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^{n}(x_i - \bar{x})^2} \cdot \sqrt{\sum_{i=1}^{n}(y_i - \bar{y})^2}}$$

| 范围 | 解读 |
|------|------|
| r ≈ 0 | 无相关 |
| \|r\| < 0.3 | 弱相关 |
| 0.3 ≤ \|r\| < 0.7 | 中等相关 |
| \|r\| ≥ 0.7 | 强相关 |

### 2.2 多元线性回归

$$y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + ... + \beta_k x_k + \varepsilon$$

- $y$：困难模式占比（hard_mode_ratio）
- $x_1, x_2, ..., x_k$：单词属性特征
- $\beta_i$：回归系数（标准化后可比较大小）
- $R^2$：决定系数，表示模型解释的方差比例

### 2.3 显著性检验

- **原假设 H₀**：$\beta_i = 0$（特征对目标无影响）
- **备择假设 H₁**：$\beta_i \neq 0$
- **判断标准**：p < 0.05 则拒绝原假设，认为影响显著

---

## 三、结果解读

### 3.1 关键发现

| 分析方法 | 结果 | 结论 |
|----------|------|------|
| Pearson相关 | 所有特征 \|r\| < 0.06 | 无显著相关 |
| 显著性检验 | 所有特征 p > 0.05 | 均不显著 |
| 多元回归 | R² = 0.0133 | 几乎无解释力 |
| 随机森林 | CV R² < 0 | 预测能力为负 |

### 3.2 核心统计量

| 统计量 | 数值 | 解读 |
|--------|------|------|
| 困难模式占比均值 | 7.76% | 约8%玩家选择困难模式 |
| 困难模式占比标准差 | 5.06% | 变异相对较小 |
| 回归R² | 0.0133 | 单词属性仅解释1.3%的变异 |
| F检验p值 | 0.91 | 整体模型不显著 |
| 显著特征数 | 0/10 | 无任何特征显著 |

### 3.3 最终结论

**单词属性对困难模式占比没有显著影响。**

### 3.4 原因解释（行为学角度）

1. **模式选择先于单词出现**
   - 玩家在游戏开始前就选择了普通/困难模式
   - 此时尚未看到当日目标单词
   - 因此单词属性不可能影响模式选择

2. **个人偏好主导**
   - 困难模式选择反映的是玩家的「挑战意愿」和「游戏风格」
   - 这是一种稳定的个人特质，不随单词变化

3. **时间稳定性**
   - 困难模式占比在全年保持相对稳定（CV≈65%）
   - 说明困难模式玩家群体是固定的

---

## 四、论文撰写建议

### 4.1 建议章节结构

```
4.2 Problem 2: Word Attributes and Hard Mode Ratio
    4.2.1 Problem Description
    4.2.2 Correlation Analysis
    4.2.3 Multiple Linear Regression
    4.2.4 Random Forest Feature Importance
    4.2.5 Conclusion and Explanation
```

### 4.2 关键公式LaTeX格式

```latex
% Pearson相关系数
r = \frac{\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})}
         {\sqrt{\sum_{i=1}^{n}(x_i - \bar{x})^2} \cdot 
          \sqrt{\sum_{i=1}^{n}(y_i - \bar{y})^2}}

% 多元回归
y = \beta_0 + \sum_{j=1}^{k} \beta_j x_j + \varepsilon

% R-squared
R^2 = 1 - \frac{SS_{res}}{SS_{tot}}
```

### 4.3 常用英文表达

**描述分析方法**：
- "We employ Pearson correlation analysis to examine the linear relationship between word attributes and hard mode ratio."
- "A multiple linear regression model is constructed to quantify the joint effect of all word features."

**报告结论**：
- "None of the word attributes show statistically significant correlation with hard mode ratio (all p > 0.05)."
- "The regression model yields an R² of only 0.013, indicating that word attributes explain merely 1.3% of the variance in hard mode ratio."

**解释原因**：
- "This finding can be explained by the game mechanics: players select their mode before seeing the target word."
- "The choice of hard mode reflects personal preference rather than word-specific difficulty."

---

## 五、图片列表与插入位置

| 编号 | 文件名 | 内容 | 建议插入章节 |
|------|--------|------|-------------|
| 图1 | fig1_hard_mode_distribution.pdf | 困难模式占比分布与时间趋势 | 4.2.1 数据描述 |
| 图2 | fig2_word_features_distribution.pdf | 单词属性特征分布（6合1） | 4.2.1 特征描述 |
| 图3 | fig3_correlation_heatmap.pdf | 相关性热力图 | 4.2.2 相关分析 |
| 图4 | fig4_correlation_barplot.pdf | 相关系数柱状图（含显著性） | 4.2.2 相关分析 |
| 图5 | fig5_regression_coefficients.pdf | 回归系数及95%置信区间 | 4.2.3 回归分析 |
| 图6 | fig6_feature_importance.pdf | 随机森林特征重要性 | 4.2.4 特征重要性 |
| 图7 | fig7_scatter_plots.pdf | 关键特征散点图（4合1） | 4.2.2 关系可视化 |

### 图片引用示例

```latex
As shown in Fig. \ref{fig:correlation}, none of the word attributes exhibit 
statistically significant correlation with hard mode ratio (all |r| < 0.06, 
p > 0.05).

The regression analysis (Fig. \ref{fig:regression}) confirms this finding, 
with an R² of only 0.013 and no significant coefficients.
```
