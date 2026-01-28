# 问题三 —— 资料手工作指南

> 本文档面向资料手Person2，指导完成思路图绘制和参考文献查找工作。

---

## 一、需要绘制的思路图

### 思路图1：问题三建模流程图

```
┌─────────────────────────────────────────────────────────────────┐
│           Problem 3: Result Distribution Prediction              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐                                            │
│  │ Historical Data   │ 359 words with result distributions       │
│  │ (Training Set)    │                                           │
│  └────────┬─────────┘                                            │
│           │                                                       │
│           ▼                                                       │
│  ┌────────────────────────────────────────────────────┐         │
│  │              Feature Extraction                     │         │
│  │  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │         │
│  │  │ Vowels: 4   │  │ Repeated: 2 │  │ Letter     │  │         │
│  │  │ Ratio: 80%  │  │ (3 E's)     │  │ Frequency  │  │         │
│  │  └─────────────┘  └─────────────┘  └────────────┘  │         │
│  └────────────────────────┬───────────────────────────┘         │
│                           │                                       │
│                           ▼                                       │
│  ┌────────────────────────────────────────────────────┐         │
│  │         Random Forest Multi-Output Regression       │         │
│  │                                                      │         │
│  │   Input: 10 features  →  Output: 7 percentages      │         │
│  │   (word attributes)      (try_1 to try_6, try_x)    │         │
│  └────────────────────────┬───────────────────────────┘         │
│                           │                                       │
│                           ▼                                       │
│  ┌────────────────────────────────────────────────────┐         │
│  │              Bootstrap Uncertainty                  │         │
│  │                                                      │         │
│  │   200 resamples → 95% Confidence Intervals          │         │
│  └────────────────────────┬───────────────────────────┘         │
│                           │                                       │
│                           ▼                                       │
│  ┌──────────────────────────────────────────────────────┐       │
│  │                  EERIE Prediction                     │       │
│  │  ┌─────────────────────────────────────────────────┐ │       │
│  │  │ Try 3: 29.2% [18.4%, 33.4%]                     │ │       │
│  │  │ Try 4: 29.8% [25.6%, 32.8%]                     │ │       │
│  │  │ Try X:  2.2% [ 0.5%,  8.0%]                     │ │       │
│  │  └─────────────────────────────────────────────────┘ │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 思路图2：不确定性来源分析图

```
┌───────────────────────────────────────────────────────────┐
│              Uncertainty Sources Analysis                  │
├───────────────────────────────────────────────────────────┤
│                                                            │
│   ┌─────────────────────────────────────────────────┐     │
│   │          Total Prediction Uncertainty            │     │
│   └─────────────────────┬───────────────────────────┘     │
│                         │                                  │
│          ┌──────────────┼──────────────┐                  │
│          ▼              ▼              ▼                  │
│   ┌────────────┐ ┌────────────┐ ┌────────────┐           │
│   │ Aleatoric  │ │ Epistemic  │ │ Data       │           │
│   │ (Random)   │ │ (Model)    │ │ Coverage   │           │
│   └─────┬──────┘ └─────┬──────┘ └─────┬──────┘           │
│         │              │              │                   │
│         ▼              ▼              ▼                   │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│   │ Twitter  │  │ Feature  │  │ Few words │               │
│   │ sampling │  │ coverage │  │ like      │               │
│   │ bias     │  │ limited  │  │ EERIE     │               │
│   └──────────┘  └──────────┘  └──────────┘               │
│                                                            │
└───────────────────────────────────────────────────────────┘
```

**绘图要点**：
- 整体使用从上到下的流程结构
- Random Forest模型用蓝色框强调
- EERIE预测结果用绿色框突出
- 不确定性分析用橙色标注

---

## 二、参考文献检索指南

### 2.1 检索关键词

| 主题 | 英文关键词 | 中文关键词 |
|------|-----------|-----------|
| 多输出回归 | multi-output regression, multivariate regression | 多输出回归、多元回归 |
| 随机森林 | random forest, ensemble learning | 随机森林、集成学习 |
| Bootstrap | bootstrap resampling, confidence interval | Bootstrap、置信区间 |
| 不确定性量化 | uncertainty quantification, prediction interval | 不确定性量化、预测区间 |
| 游戏分析 | game analytics, player behavior | 游戏分析、玩家行为 |

### 2.2 推荐数据库与来源

| 数据库 | 适用内容 | 网址 |
|--------|---------|------|
| Google Scholar | 综合学术搜索 | scholar.google.com |
| IEEE Xplore | 机器学习方法 | ieeexplore.ieee.org |
| JMLR | 机器学习理论 | jmlr.org |

### 2.3 推荐引用格式（IEEE格式）

**随机森林**：
```
L. Breiman, "Random forests," Machine Learning, vol. 45, no. 1, pp. 5-32, 2001.
```

**Bootstrap方法**：
```
B. Efron and R. J. Tibshirani, An Introduction to the Bootstrap. 
New York: Chapman & Hall/CRC, 1994.
```

**多输出回归**：
```
H. Borchani, G. Varando, C. Bielza, and P. Larrañaga, "A survey on multi-output 
regression," Wiley Interdisciplinary Reviews: Data Mining and Knowledge Discovery, 
vol. 5, no. 5, pp. 216-233, 2015.
```

---

## 三、图片文件交付清单

### Coder已导出的图片（共7张）

| 序号 | 文件名 | 描述 | 格式 |
|------|--------|------|------|
| 1 | fig1_distribution_boxplot.pdf | 结果分布箱线图 | PDF |
| 2 | fig2_average_distribution.pdf | 平均结果分布柱状图 | PDF |
| 3 | fig3_feature_target_correlation.pdf | 特征-目标相关性热力图 | PDF |
| 4 | fig4_model_comparison.pdf | 模型MAE对比 | PDF |
| 5 | fig5_feature_importance.pdf | 特征重要性 | PDF |
| 6 | fig6_eerie_prediction.pdf | EERIE预测vs历史平均 | PDF |
| 7 | fig7_bootstrap_distribution.pdf | Bootstrap预测分布（7合1） | PDF |

### 需要Person2绘制的图

| 序号 | 图名 | 内容 | 工具建议 |
|------|------|------|---------|
| 1 | 问题三建模流程图 | 按上述ASCII图绘制 | Draw.io / PPT |
| 2 | 不确定性来源分析图 | 三类不确定性分解 | Draw.io / PPT |

**绘图规范**：
- 尺寸：宽度不超过论文单栏宽度
- 配色：主色调使用蓝色系，结果用绿色突出
- 字体：英文Arial，数字清晰可读
- 导出格式：PDF（矢量图）
