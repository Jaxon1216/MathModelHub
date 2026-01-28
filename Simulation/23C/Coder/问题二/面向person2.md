# 问题二 —— 资料手工作指南

> 本文档面向资料手Person2，指导完成思路图绘制和参考文献查找工作。建模思路在面向person1的文件里自行查阅。

---

## 一、需要绘制的思路图

### 思路图1：问题二分析流程图

```
┌─────────────────────────────────────────────────────────────────┐
│           Problem 2: Analysis Flow                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐                                            │
│  │ Preprocessed Data │                                           │
│  │ (359 records)     │                                           │
│  └────────┬─────────┘                                            │
│           │                                                       │
│           ▼                                                       │
│  ┌────────────────────────────────────────────────────┐         │
│  │              Feature Extraction                     │         │
│  │  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │         │
│  │  │ num_vowels  │  │ repeated    │  │ letter     │  │         │
│  │  │ vowel_ratio │  │ letters     │  │ frequency  │  │         │
│  │  └─────────────┘  └─────────────┘  └────────────┘  │         │
│  └────────────────────────┬───────────────────────────┘         │
│                           │                                       │
│           ┌───────────────┼───────────────┐                      │
│           ▼               ▼               ▼                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Pearson    │  │  Multiple   │  │  Random     │              │
│  │ Correlation │  │  Linear     │  │  Forest     │              │
│  │  Analysis   │  │ Regression  │  │  Feature    │              │
│  │             │  │             │  │ Importance  │              │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
│         │                │                │                      │
│         ▼                ▼                ▼                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │ All |r|<0.06│  │  R²=0.013   │  │  CV R²<0    │              │
│  │ All p>0.05  │  │  No sig.    │  │  No predict │              │
│  │             │  │  features   │  │  power      │              │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
│         │                │                │                      │
│         └────────────────┼────────────────┘                      │
│                          ▼                                        │
│  ┌──────────────────────────────────────────────────────┐       │
│  │                    Conclusion                         │       │
│  │   Word attributes have NO significant effect on       │       │
│  │   hard mode ratio (player choice is preference-based) │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

**绘图要点**：
- 整体使用从上到下的流程结构
- 三种分析方法并行展示（蓝色高亮）
- 最终结论用绿色框强调
- 添加关键数值（R²、相关系数等）

---

## 二、参考文献检索指南

### 2.1 检索关键词

| 主题 | 英文关键词 | 中文关键词 |
|------|-----------|-----------|
| 相关性分析 | correlation analysis, Pearson correlation, Spearman correlation | 相关性分析、皮尔逊相关 |
| 显著性检验 | significance test, p-value, hypothesis testing | 显著性检验、假设检验 |
| 多元回归 | multiple regression, OLS regression | 多元回归、最小二乘 |
| 特征重要性 | feature importance, random forest | 特征重要性、随机森林 |
| 玩家行为 | player behavior, gaming choice, user preference | 玩家行为、用户偏好 |

### 2.2 推荐数据库与来源

| 数据库 | 适用内容 | 网址 |
|--------|---------|------|
| Google Scholar | 综合学术搜索 | scholar.google.com |
| JSTOR | 统计学方法 | jstor.org |
| ACM Digital Library | 游戏研究 | dl.acm.org |

### 2.3 推荐引用格式（IEEE格式）

**Pearson相关**：
```
K. Pearson, "Notes on regression and inheritance in the case of two parents," 
Proceedings of the Royal Society of London, vol. 58, pp. 240-242, 1895.
```

**多元回归**：
```
D. C. Montgomery, E. A. Peck, and G. G. Vining, Introduction to Linear 
Regression Analysis, 5th ed. Hoboken, NJ: Wiley, 2012.
```

**随机森林**：
```
L. Breiman, "Random forests," Machine Learning, vol. 45, no. 1, pp. 5-32, 2001.
```

---

## 三、图片文件交付清单

### Coder已导出的图片（共7张）

| 序号 | 文件名 | 描述 | 格式 |
|------|--------|------|------|
| 1 | fig1_hard_mode_distribution.pdf | 困难模式占比分布与时序图 | PDF |
| 2 | fig2_word_features_distribution.pdf | 单词属性分布（6合1） | PDF |
| 3 | fig3_correlation_heatmap.pdf | 相关性热力图 | PDF |
| 4 | fig4_correlation_barplot.pdf | 相关系数柱状图 | PDF |
| 5 | fig5_regression_coefficients.pdf | 回归系数及置信区间 | PDF |
| 6 | fig6_feature_importance.pdf | 随机森林特征重要性 | PDF |
| 7 | fig7_scatter_plots.pdf | 关键特征散点图（4合1） | PDF |

### 需要Person2绘制的图

| 序号 | 图名 | 内容 | 工具建议 |
|------|------|------|---------|
| 1 | 问题二分析流程图 | 按上述ASCII图绘制 | Draw.io / PPT |

**绘图规范**：
- 尺寸：宽度不超过论文单栏宽度
- 配色：主色调使用蓝色系，结论用绿色突出
- 字体：英文Arial，数字清晰可读
- 导出格式：PDF（矢量图）
