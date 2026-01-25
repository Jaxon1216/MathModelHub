# 2024 MCM C题 —— 资料手工作指南

> 本文档面向资料手Person2，指导完成思路图绘制和参考文献查找工作。

---

## 一、需要绘制的思路图

### 1. 整体建模流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Tennis Momentum Analysis                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │   Q1     │    │   Q2     │    │   Q3     │    │   Q4     │  │
│  │ Momentum │    │ Momentum │    │ Momentum │    │ Model    │  │
│  │  Model   │    │Validation│    │Prediction│    │Generalize│  │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘  │
│       │               │               │               │         │
│       ▼               ▼               ▼               ▼         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  DMS     │    │Statistical│    │ Random   │    │  LOMO    │  │
│  │ Algorithm│    │  Tests   │    │ Forest   │    │Cross-Val │  │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘  │
│       │               │               │               │         │
│       ▼               ▼               ▼               ▼         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │Momentum  │    │ Momentum │    │Key Factor│    │ 90% Win  │  │
│  │  Curves  │    │ is Real  │    │Analysis  │    │ Accuracy │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2. 势头模型核心框架图

建议用AI画图工具绘制，提示词如下：

```
Create a professional academic flowchart for "Dynamic Momentum Score Model" with these elements:

INPUT (left box):
- Match point data
- Player statistics
- Serve information

PROCESSING (center, 4 sequential boxes with arrows):
1. "Base Weight Calculation" (gray box)
2. "Serve Advantage Adjustment" (blue highlighted box)
   - Server wins: ×0.65
   - Receiver wins: ×1.54
3. "Key Point Multiplier" (blue highlighted box)
   - Break point: ×1.5
   - Other key points: ×1.2
4. "Streak Bonus + Decay" (blue highlighted box)

OUTPUT (right box):
- Momentum Score Mt
- Momentum State (P1_Strong/Neutral/P2_Strong)

Style: Clean academic diagram, black text, light blue accent boxes, no background texture, arrows connecting elements
```

---

## 二、参考文献检索指南

### 推荐检索关键词

| 主题 | 英文关键词 | 推荐数据库 |
|------|-----------|-----------|
| 运动势头 | "momentum in sports" "hot hand effect" | Google Scholar, JSTOR |
| 网球分析 | "tennis analytics" "tennis match prediction" | Web of Science |
| 时序体育数据 | "sports time series" "sequential sports data" | IEEE Xplore |
| 统计检验 | "runs test" "permutation test" | 统计学教材 |
| 机器学习预测 | "random forest classification" "sports prediction" | arXiv, ACM |

### 核心参考文献建议

1. **Hot Hand Effect**
   - Gilovich, T., Vallone, R., & Tversky, A. (1985). The hot hand in basketball: On the misperception of random sequences.

2. **Tennis Analytics**
   - Kovalchik, S. A. (2016). Searching for the GOAT of tennis win prediction.
   
3. **Momentum in Sports**
   - Iso-Ahola, S. E., & Mobily, K. (1980). "Psychological momentum": A phenomenon and an empirical (unobtrusive) validation.

4. **Machine Learning in Sports**
   - Bunker, R. P., & Thabtah, F. (2019). A machine learning framework for sport result prediction.

### 引用格式 (IEEE)
```
[1] T. Gilovich, R. Vallone, and A. Tversky, "The hot hand in basketball: 
    On the misperception of random sequences," Cognitive Psychology, 
    vol. 17, no. 3, pp. 295-314, 1985.
```

---

## 三、图片文件交付清单

### Coder已导出的图片

| 问题 | 文件名 | 内容描述 |
|------|--------|----------|
| Q1 | fig1_final_momentum_curve.pdf | 决赛势头曲线（时序图） |
| Q1 | fig2_momentum_heatmap.pdf | 分盘势头热力图 |
| Q1 | fig5_momentum_vs_result.pdf | 势头与比赛结果散点图 |
| Q2 | fig1_runs_test_distribution.pdf | 游程检验Z统计量分布 |
| Q2 | fig2_conditional_probability.pdf | 条件概率柱状图 |
| Q3 | fig1_roc_curve.pdf | ROC曲线 |
| Q3 | fig2_feature_importance.pdf | 特征重要性排名 |
| Q4 | fig1_lomo_results.pdf | 留一验证各比赛AUC |
| Q4 | fig3_applicability.pdf | 模型适用性评分 |

### 需要Person2绘制的图

1. **研究框架图** (建议使用draw.io或AI画图)
   - 整体研究流程
   - 四个问题的逻辑关系

2. **势头模型示意图**
   - 势头计算公式的可视化表示
   - 参数作用示意

---

## 四、研究架构图AI绘图提示词

基于项目研究框架，生成用于AI画图工具的提示词：

```
Create a professional academic research framework diagram for "Tennis Momentum Analysis" with 4 columns representing 4 tasks:

TASK 1 - Momentum Modeling:
- Input: Point-by-point match data (with table icon)
- Steps: Data preprocessing → Feature extraction → Dynamic Momentum Score (DMS) calculation (highlight in blue)
- Output: Momentum curves, momentum states

TASK 2 - Statistical Validation:
- Input: Momentum sequences
- Steps: Runs test → Conditional probability test → Permutation test (all highlighted in blue)
- Output: Statistical evidence (p-values, effect sizes)

TASK 3 - Prediction Model:
- Input: Momentum features
- Steps: Feature engineering → Random Forest classifier → Feature importance analysis (highlight in blue)
- Output: Shift prediction, key factors

TASK 4 - Generalization:
- Input: All match data
- Steps: Leave-one-match-out cross-validation → Multi-round testing (highlight in blue)
- Output: AUC scores, applicability assessment

Style requirements:
- Use vertical flow within each column (top to bottom)
- Separate columns with thin dashed lines
- Highlight method boxes in light blue
- Input/output boxes in plain black border
- Include small icons where applicable (charts, tables)
- Clean academic style, no decorative elements
- Black text on white background
```

---

## 五、数据可视化注意事项

1. **配色方案**
   - P1 (红色): #E74C3C
   - P2 (蓝色): #3498DB
   - 中性/强调: #27AE60, #F39C12

2. **图表格式**
   - 所有图片为PDF矢量格式
   - 图内不含标题，标题在正文中给出
   - 坐标轴标签清晰，字号不小于12pt

3. **论文图片要求**
   - 单栏宽度约3.5英寸
   - 双栏宽度约7英寸
   - 分辨率至少300dpi
