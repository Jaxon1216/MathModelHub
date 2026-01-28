# 问题一 —— 资料手工作指南

> 本文档面向资料手Person2，指导完成思路图绘制和参考文献查找工作。建模思路在面向person1的文件里自行查阅。

---

## 一、需要绘制的思路图

### 思路图1：问题一建模流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Problem 1: Modeling Flow                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────┐    ┌──────────────┐    ┌─────────────────┐        │
│  │Raw Data  │───▶│Log Transform │───▶│Stationarity Test│        │
│  │(359 days)│    │  y = ln(x)   │    │   ADF Test      │        │
│  └──────────┘    └──────────────┘    └────────┬────────┘        │
│                                                │                  │
│                         ┌──────────────────────┘                  │
│                         ▼                                         │
│  ┌──────────────────────────────────────────────────────┐       │
│  │          Time Series Decomposition (STL)              │       │
│  │  ┌─────────┐  ┌──────────┐  ┌──────────┐             │       │
│  │  │ Trend   │  │ Seasonal │  │ Residual │             │       │
│  │  │ (98.3%) │  │  (0.6%)  │  │  (1.1%)  │             │       │
│  │  └─────────┘  └──────────┘  └──────────┘             │       │
│  └──────────────────────────────────────────────────────┘       │
│                         │                                         │
│                         ▼                                         │
│  ┌──────────────────────────────────────────────────────┐       │
│  │              SARIMA(1,1,1)(1,1,1)₇                    │       │
│  │  ┌───────────────┐    ┌───────────────────┐          │       │
│  │  │ ACF/PACF      │───▶│ Parameter         │          │       │
│  │  │ Analysis      │    │ Selection (AIC)   │          │       │
│  │  └───────────────┘    └───────────────────┘          │       │
│  └──────────────────────────────────────────────────────┘       │
│                         │                                         │
│                         ▼                                         │
│  ┌──────────────────────────────────────────────────────┐       │
│  │              Model Validation                         │       │
│  │  R² = 0.967  │  MAE = 7,881  │  MAPE = 9.43%         │       │
│  └──────────────────────────────────────────────────────┘       │
│                         │                                         │
│                         ▼                                         │
│  ┌──────────────────────────────────────────────────────┐       │
│  │           Prediction: March 1, 2023                   │       │
│  │  ┌──────────────┐    ┌────────────────────┐          │       │
│  │  │Point Estimate│    │ 95% Confidence     │          │       │
│  │  │   13,270     │    │ Interval           │          │       │
│  │  │              │    │ [6,445 - 27,322]   │          │       │
│  │  └──────────────┘    └────────────────────┘          │       │
│  │                              │                        │       │
│  │                    ┌─────────┴─────────┐              │       │
│  │                    │ Bootstrap (n=1000)│              │       │
│  │                    │ Uncertainty       │              │       │
│  │                    │ Quantification    │              │       │
│  │                    └───────────────────┘              │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

**绘图要点**：
- 整体使用从上到下的流程结构
- 关键方法模块（Log Transform, SARIMA, Bootstrap）用**浅蓝色高亮**
- 数据/结果模块用普通白色框
- 添加小图标：时序数据用折线图图标，分解结果用柱状图标

---

## 二、参考文献检索指南

### 2.1 检索关键词

| 主题 | 英文关键词 | 中文关键词 |
|------|-----------|-----------|
| 时间序列预测 | time series forecasting, ARIMA, SARIMA | 时间序列预测、自回归移动平均 |
| 季节性调整 | seasonal adjustment, seasonal decomposition, STL | 季节性调整、季节分解 |
| 预测区间 | prediction interval, confidence interval, uncertainty quantification | 预测区间、置信区间、不确定性量化 |
| Bootstrap方法 | bootstrap resampling, bootstrap prediction | 自助法、Bootstrap抽样 |
| 社交媒体趋势 | social media trend, viral content decay, hotspot evolution | 社交媒体趋势、病毒式传播衰减 |

### 2.2 推荐数据库与来源

| 数据库 | 适用内容 | 网址 |
|--------|---------|------|
| Google Scholar | 综合学术搜索 | scholar.google.com |
| IEEE Xplore | 工程/计算机方法 | ieeexplore.ieee.org |
| arXiv | 预印本/最新方法 | arxiv.org |
| Statsmodels文档 | Python实现参考 | statsmodels.org |

### 2.3 推荐引用格式（IEEE格式）

**ARIMA/SARIMA原始文献**：
```
G. E. P. Box and G. M. Jenkins, Time Series Analysis: Forecasting and Control. 
San Francisco: Holden-Day, 1970.
```

**STL分解方法**：
```
R. B. Cleveland, W. S. Cleveland, J. E. McRae, and I. Terpenning, 
"STL: A seasonal-trend decomposition procedure based on loess," 
J. Official Statistics, vol. 6, no. 1, pp. 3-73, 1990.
```

**Bootstrap方法**：
```
B. Efron and R. J. Tibshirani, An Introduction to the Bootstrap. 
New York: Chapman & Hall, 1993.
```

---

## 三、图片文件交付清单

### Coder已导出的图片（共9张）

| 序号 | 文件名 | 描述 | 格式 |
|------|--------|------|------|
| 1 | fig1_time_series_trend.pdf | 报告数量时间序列趋势图 | PDF |
| 2 | fig2_weekly_pattern.pdf | 周末效应分析图 | PDF |
| 3 | fig3_monthly_trend.pdf | 月度变化趋势柱状图 | PDF |
| 4 | fig4_stl_decomposition.pdf | STL时间序列分解图 | PDF |
| 5 | fig5_acf_pacf.pdf | ACF/PACF自相关分析图 | PDF |
| 6 | fig6_residual_diagnostics.pdf | 残差诊断图（4合1） | PDF |
| 7 | fig7_model_fit.pdf | 模型拟合效果对比图 | PDF |
| 8 | fig8_forecast.pdf | 预测结果可视化图 | PDF |
| 9 | fig9_bootstrap_distribution.pdf | Bootstrap预测分布图 | PDF |

### 需要Person2绘制的图

| 序号 | 图名 | 内容 | 工具建议 |
|------|------|------|---------|
| 1 | 问题一建模流程图 | 按上述ASCII图绘制 | Draw.io / PPT |

**绘图规范**：
- 尺寸：宽度不超过论文单栏宽度
- 配色：主色调使用蓝色系，突出显示用橙色
- 字体：英文Arial，数字清晰可读
- 导出格式：PDF（矢量图）
