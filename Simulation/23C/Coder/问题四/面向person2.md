# 问题四 —— 资料手工作指南

> 本文档面向资料手Person2，指导完成思路图绘制和参考文献查找工作。

---

## 一、需要绘制的思路图

### 思路图1：问题四建模流程图

```
┌─────────────────────────────────────────────────────────────────┐
│           Problem 4: Word Difficulty Classification              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐                                            │
│  │ Historical Data   │ 359 words with difficulty labels          │
│  │ (Training Set)    │ Easy: 32, Medium: 162, Hard: 165          │
│  └────────┬─────────┘                                            │
│           │                                                       │
│           ▼                                                       │
│  ┌────────────────────────────────────────────────────┐         │
│  │              Feature Extraction                     │         │
│  │  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │         │
│  │  │ Vowels      │  │ Repeated    │  │ Letter     │  │         │
│  │  │ Count/Ratio │  │ Letters     │  │ Frequency  │  │         │
│  │  └─────────────┘  └─────────────┘  └────────────┘  │         │
│  └────────────────────────┬───────────────────────────┘         │
│                           │                                       │
│                           ▼                                       │
│  ┌────────────────────────────────────────────────────┐         │
│  │            Random Forest Classifier                 │         │
│  │                                                      │         │
│  │   200 trees → Vote → 3-class classification         │         │
│  │   Accuracy: 66.7%, F1: 0.66                         │         │
│  └────────────────────────┬───────────────────────────┘         │
│                           │                                       │
│           ┌───────────────┼───────────────┐                      │
│           ▼               ▼               ▼                      │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│   │    Easy     │  │   Medium    │  │    Hard     │             │
│   │  avg < 4.0  │  │ 4.0 ~ 4.5   │  │  avg >= 4.5 │             │
│   └─────────────┘  └─────────────┘  └─────────────┘             │
│                           │                                       │
│                           ▼                                       │
│  ┌──────────────────────────────────────────────────────┐       │
│  │                  EERIE Prediction                     │       │
│  │  ┌─────────────────────────────────────────────────┐ │       │
│  │  │ Predicted: Medium (53.2% confidence)            │ │       │
│  │  │ Features: 4 vowels, 2 repeated, high avg_freq   │ │       │
│  │  └─────────────────────────────────────────────────┘ │       │
│  └──────────────────────────────────────────────────────┘       │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 思路图2：难度定义标准图

```
┌───────────────────────────────────────────────────────────┐
│              Difficulty Definition Based on avg_tries      │
├───────────────────────────────────────────────────────────┤
│                                                            │
│   Average Tries                                            │
│   ──────────────────────────────────────────────────►      │
│        3.5      4.0       4.5       5.0                    │
│         │        │         │         │                     │
│   ┌─────┴────┐ ┌─┴─────────┴─┐ ┌─────┴────────────┐       │
│   │   Easy   │ │   Medium    │ │      Hard        │       │
│   │  (8.9%)  │ │   (45.1%)   │ │     (46.0%)      │       │
│   │  Green   │ │   Yellow    │ │      Red         │       │
│   └──────────┘ └─────────────┘ └──────────────────┘       │
│                                                            │
└───────────────────────────────────────────────────────────┘
```

**绘图要点**：
- 使用三色区分难度（绿/黄/红）
- 标注EERIE预测结果
- 特征重要性用柱状图强调

---

## 二、参考文献检索指南

### 2.1 检索关键词

| 主题 | 英文关键词 | 中文关键词 |
|------|-----------|-----------|
| 随机森林 | random forest, ensemble classification | 随机森林、集成分类 |
| 多分类问题 | multiclass classification, one-vs-all | 多分类、一对多 |
| 特征重要性 | feature importance, Gini importance | 特征重要性、基尼重要性 |
| 混淆矩阵 | confusion matrix, classification metrics | 混淆矩阵、分类指标 |
| 文字游戏分析 | word game, puzzle difficulty | 文字游戏、谜题难度 |

### 2.2 推荐数据库与来源

| 数据库 | 适用内容 | 网址 |
|--------|---------|------|
| Google Scholar | 综合学术搜索 | scholar.google.com |
| IEEE Xplore | 机器学习分类 | ieeexplore.ieee.org |
| Scikit-learn Docs | 算法实现细节 | scikit-learn.org |

### 2.3 推荐引用格式（IEEE格式）

**随机森林**：
```
L. Breiman, "Random forests," Machine Learning, vol. 45, no. 1, pp. 5-32, 2001.
```

**分类评估指标**：
```
M. Sokolova and G. Lapalme, "A systematic analysis of performance measures for 
classification tasks," Information Processing & Management, vol. 45, no. 4, 
pp. 427-437, 2009.
```

**特征重要性**：
```
G. Louppe, L. Wehenkel, A. Sutera, and P. Geurts, "Understanding variable 
importances in forests of randomized trees," Advances in Neural Information 
Processing Systems, vol. 26, 2013.
```

---

## 三、图片文件交付清单

### Coder已导出的图片（共7张）

| 序号 | 文件名 | 描述 | 格式 |
|------|--------|------|------|
| 1 | fig1_difficulty_distribution.pdf | 难度分布（3合1） | PDF |
| 2 | fig2_feature_by_difficulty.pdf | 特征与难度关系（4合1） | PDF |
| 3 | fig3_model_comparison.pdf | 模型准确率对比 | PDF |
| 4 | fig4_confusion_matrix.pdf | 混淆矩阵 | PDF |
| 5 | fig5_feature_importance.pdf | 特征重要性 | PDF |
| 6 | fig6_eerie_comparison.pdf | EERIE与历史单词对比 | PDF |
| 7 | fig7_eerie_probability.pdf | EERIE预测概率 | PDF |

### 需要Person2绘制的图

| 序号 | 图名 | 内容 | 工具建议 |
|------|------|------|---------|
| 1 | 问题四建模流程图 | 按上述ASCII图绘制 | Draw.io / PPT |
| 2 | 难度定义标准图 | 三色难度区间图 | Draw.io / PPT |

**绘图规范**：
- 尺寸：宽度不超过论文单栏宽度
- 配色：Easy=绿色(#2ecc71)，Medium=黄色(#f39c12)，Hard=红色(#e74c3c)
- 字体：英文Arial，数字清晰可读
- 导出格式：PDF（矢量图）
