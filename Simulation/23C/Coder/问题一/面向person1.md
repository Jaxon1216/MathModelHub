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

### 1.1 问题理解

问题一要求：
1. **解释报告数量的波动**：理解每日Twitter分享数量的变化规律
2. **预测未来值**：给出2023年3月1日的预测**区间**（而非单点值）

### 1.2 建模思路

我们采用**时间序列分析**方法，核心思路：

```
原始数据 → 探索性分析(EDA) → 时间序列分解 → SARIMA建模 → 预测+置信区间
```

**为什么选择SARIMA？**

1. **时间序列特性**：报告数量是按日期排列的时间序列数据，天然适合时间序列模型
2. **趋势+季节性**：数据呈现明显的下降趋势和周周期特征（周末效应）
3. **自相关性**：当日数据与前几日相关，ARIMA可捕捉这种自相关
4. **预测区间**：SARIMA可直接输出置信区间，满足题目要求

**类比理解**：
- 想象你在预测每天的气温。今天的气温通常与昨天相近（自相关），但整体可能有季节变化（趋势+季节性）。SARIMA就是用数学方式描述这种"惯性+周期"的模式。

---

## 二、模型介绍与公式

### 2.1 数据预处理

**对数变换**：由于报告数量变化剧烈（2,500~360,000），我们先取对数使方差稳定：

$$y_t = \ln(x_t)$$

其中 $x_t$ 是第 $t$ 天的报告数量。

### 2.2 SARIMA模型

**模型表示**：SARIMA$(p,d,q)(P,D,Q)_s$

本研究使用：**SARIMA(1,1,1)(1,1,1)₇**

| 参数 | 含义 | 取值 | 解释 |
|------|------|------|------|
| $p$ | AR阶数 | 1 | 考虑1阶自回归 |
| $d$ | 差分阶数 | 1 | 一阶差分使序列平稳 |
| $q$ | MA阶数 | 1 | 考虑1阶移动平均 |
| $P$ | 季节AR阶数 | 1 | 季节性自回归 |
| $D$ | 季节差分 | 1 | 季节性差分 |
| $Q$ | 季节MA阶数 | 1 | 季节性移动平均 |
| $s$ | 季节周期 | 7 | 周周期（7天） |

**模型公式**：

$$\Phi_P(B^s) \phi_p(B) \nabla^d \nabla_s^D y_t = \Theta_Q(B^s) \theta_q(B) \varepsilon_t$$

**简化理解**：
- 今天的值 = 过去值的加权平均 + 季节性调整 + 随机误差
- $B$ 是后移算子：$By_t = y_{t-1}$

### 2.3 置信区间

**95%置信区间**计算：

$$CI_{95\%} = [\hat{y} - 1.96\sigma, \hat{y} + 1.96\sigma]$$

其中 $\hat{y}$ 是点预测，$\sigma$ 是预测标准误。

**Bootstrap方法**补充估计不确定性：
- 从残差中重复抽样1000次
- 每次添加随机扰动后重新预测
- 取2.5%和97.5%分位数作为区间边界

---

## 三、结果解读

### 3.1 数据特征发现

| 特征 | 发现 | 意义 |
|------|------|------|
| 时间趋势 | "先升后降"热点衰减 | 2月达峰值36万，年末降至2万 |
| 周末效应 | t检验p=0.72，不显著 | 周末与工作日分享量无显著差异 |
| 方差贡献 | 趋势98.3%，季节0.6% | 下降趋势是主要变异来源 |

### 3.2 模型性能

| 指标 | 数值 | 解读 |
|------|------|------|
| R² | 0.967 | 模型解释了96.7%的方差，拟合优秀 |
| MAE | 7,881 | 平均绝对误差约7,900条 |
| RMSE | 16,039 | 均方根误差约16,000条 |
| MAPE | 9.43% | 平均相对误差<10%，达到合格标准 |

### 3.3 预测结果

**2023年3月1日报告数量预测：**

| 方法 | 点预测 | 95%置信区间 |
|------|--------|-------------|
| SARIMA | **13,270** | [6,445, 27,322] |
| Bootstrap | **14,028** | [6,871, 26,148] |

**结果解读**：
- 预测2023年3月1日约有1.3~1.4万条Twitter分享
- 考虑不确定性，可能范围在6,500~27,000之间
- 相比2022年初的36万峰值，热度下降约96%

### 3.4 不确定性来源

1. **数据代表性**：Twitter样本可能无法代表所有玩家
2. **趋势外推**：假设2023年延续2022年末的下降趋势
3. **外部事件**：未考虑可能影响分享意愿的突发新闻/事件

---

## 四、论文撰写建议

### 4.1 建议章节结构

```
4.1 Problem 1: Modeling the Number of Reported Results
    4.1.1 Data Description and Exploratory Analysis
    4.1.2 Time Series Decomposition
    4.1.3 SARIMA Model Construction
    4.1.4 Model Validation
    4.1.5 Prediction for March 1, 2023
    4.1.6 Uncertainty Analysis
```

### 4.2 关键公式LaTeX格式

```latex
% SARIMA模型
\text{SARIMA}(1,1,1)(1,1,1)_7

% 对数变换
y_t = \ln(x_t)

% 置信区间
CI_{95\%} = [\hat{y} - 1.96\sigma, \hat{y} + 1.96\sigma]
```

### 4.3 常用英文表达

**描述趋势**：
- "The number of reported results exhibits a clear 'rise-then-fall' pattern, consistent with typical hotspot decay behavior."
- "The trend component accounts for 98.3% of the total variance, indicating that the declining popularity is the primary driver of variation."

**介绍模型**：
- "We employ a Seasonal ARIMA (SARIMA) model to capture both the temporal autocorrelation and weekly seasonality."
- "The SARIMA(1,1,1)(1,1,1)₇ model was selected based on AIC minimization and residual diagnostics."

**报告结果**：
- "The model achieves an R² of 0.967 and MAPE of 9.43%, indicating satisfactory predictive performance."
- "For March 1, 2023, we predict approximately 13,270 reported results with a 95% confidence interval of [6,445, 27,322]."

**讨论不确定性**：
- "The wide prediction interval reflects uncertainty from trend extrapolation and potential external events not captured by the model."

---

## 五、图片列表与插入位置

| 编号 | 文件名 | 内容 | 建议插入章节 |
|------|--------|------|-------------|
| 图1 | fig1_time_series_trend.pdf | 报告数量时间序列（含7天/30天移动平均） | 4.1.1 数据描述 |
| 图2 | fig2_weekly_pattern.pdf | 周末效应分析（箱线图+均值对比） | 4.1.1 周期性分析 |
| 图3 | fig3_monthly_trend.pdf | 月度变化趋势柱状图 | 4.1.1 趋势分析 |
| 图4 | fig4_stl_decomposition.pdf | STL时间序列分解（原始+趋势+季节+残差） | 4.1.2 序列分解 |
| 图5 | fig5_acf_pacf.pdf | ACF/PACF自相关分析 | 4.1.3 模型构建 |
| 图6 | fig6_residual_diagnostics.pdf | 残差诊断（时序图+直方图+Q-Q图+ACF） | 4.1.4 模型验证 |
| 图7 | fig7_model_fit.pdf | 模型拟合效果对比（实际vs预测） | 4.1.4 模型验证 |
| 图8 | fig8_forecast.pdf | 预测结果可视化（含95%置信区间） | 4.1.5 预测结果 |
| 图9 | fig9_bootstrap_distribution.pdf | Bootstrap预测分布直方图 | 4.1.6 不确定性分析 |

### 图片引用示例

```latex
As illustrated in Fig. \ref{fig:time_trend}, the number of reported results exhibits 
a clear "rise-then-fall" pattern throughout 2022, with a peak of approximately 
360,000 in early February before declining to around 20,000 by year-end.

Fig. \ref{fig:forecast} presents our prediction for March 1, 2023, showing a point 
estimate of 13,270 with a 95% confidence interval of [6,445, 27,322].
```
