---
name: math-modeling
description: 数学建模算法选择与可视化指南。用于模型选择、算法实现、评估指标、可视化绑图、论文图表生成等场景。当用户提到建模、预测、分类、聚类、优化、回归、可视化、绑图、matplotlib、model selection时触发。
---

# 第一部分：建模与可视化

此部分生成对应的ipynb文件解决建模问题。

## 产出物清单

每个建模问题完成后，必须产出以下文件：

| 文件 | 格式 | 说明 |
|------|------|------|
| `问题X建模分析.ipynb` | Jupyter Notebook | 完整建模代码，含markdown说明 |
| `面向person1.md` | Markdown | 写作指南，面向写作手 |
| `面向person2.md` | Markdown | 资料/绘图指南，面向资料手 |
| `export_figures.py` | Python脚本 | 图片导出脚本 |
| `figures/` | 目录 | 导出的PDF图片 |

**目录结构参考**：
```
问题X/
├── 问题X建模分析.ipynb   # 主建模文件
├── export_figures.py      # 图片导出脚本
├── 面向person1.md         # 写作指南
├── 面向person2.md         # 资料/绘图指南
└── figures/               # PDF图片目录
    ├── fig1_xxx.pdf
    ├── fig2_xxx.pdf
    └── ...
```

---

## 必须执行的验证步骤

**完成ipynb后，必须执行以下验证**：

1. **运行全部单元格**：确保代码能完整跑通，无报错
2. **检查输出**：验证模型结果合理性
3. **执行图片导出**：运行 `export_figures.py` 确保图片正确生成
4. **检查文件产出**：确认所有必需文件都已生成

---

## 图片规范

### 图片内容要求
- **图片本身不要带标题/标注**
- **标注放在ipynb的markdown单元格中**
- 使用ipynb的markdown单元格描述图片内容和解读
- 不要将图片拼在一起，**一个PDF一个图片**，如果适合放在一块展示，在markdown单元格做出提醒！（但不要真的合并）
### 图片导出格式
- **仅导出PDF格式**（矢量图，可无损缩放）
- 不要保存别的格式

### 绑图标准配置

```python
import matplotlib.pyplot as plt
import seaborn as sns

# 中文显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Seaborn主题
sns.set_theme(style='whitegrid')

# 标准尺寸
FIGSIZE_NORMAL = (10, 6)   # 常规图表
FIGSIZE_WIDE = (12, 6)     # 时序图
FIGSIZE_SQUARE = (8, 8)    # 散点图/热力图

# 项目标准配色
COLORS = {
    'primary': '#4682B4',    # steelblue
    'secondary': '#FF7F50',  # coral
    'accent': '#228B22',     # forestgreen
    'neutral': '#708090'     # slategray
}
```

### 绑图时不加标题

```python
# 正确：不加title，标注在ipynb markdown中说明
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(data, bins=30, color='steelblue', edgecolor='black', alpha=0.7)
ax.set_xlabel('Value')
ax.set_ylabel('Frequency')
# 不要加 ax.set_title()

# 保存为PDF
plt.savefig('figures/fig1_distribution.pdf', bbox_inches='tight')
```

### 图片导出脚本模板

将以下脚本保存为 `export_figures.py`：

```python
"""
图片导出脚本
用于从建模分析中导出所有可视化图片为PDF格式
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 设置保存路径
FIGURE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/figures'
os.makedirs(FIGURE_DIR, exist_ok=True)

def save_fig(fig, filename):
    """保存图片为PDF格式（无标题）"""
    filepath = os.path.join(FIGURE_DIR, filename)
    fig.savefig(filepath, bbox_inches='tight', facecolor='white')
    print(f"✅ 已保存: {filepath}")
    plt.close(fig)

# ============================================================
# 在此处添加各图片的生成代码
# 注意：图片不要加title，标注在ipynb的markdown单元格中
# ============================================================

# 示例：图1
# fig, ax = plt.subplots(figsize=(10, 6))
# ax.hist(data, bins=30, color='steelblue')
# ax.set_xlabel('Value')
# ax.set_ylabel('Frequency')
# save_fig(fig, 'fig1_distribution.pdf')

print("\n" + "=" * 60)
print("🎉 所有图片导出完成！")
print("=" * 60)
print(f"\n图片保存在: {FIGURE_DIR}")
for f in sorted(os.listdir(FIGURE_DIR)):
    print(f"  - {f}")
```

---

## 面向person1.md 模板

写作指南文件结构：

```markdown
# 问题X建模分析 —— 写作指南

> 本文档面向写作手Person1，帮助理解建模方法、公式符号，并指导论文撰写。

## 目录
1. [问题分析与建模思路](#一问题分析与建模思路)
2. [模型介绍与公式](#二模型介绍与公式)
3. [结果解读](#三结果解读)
4. [论文撰写建议](#四论文撰写建议)
5. [图片列表与插入位置](#五图片列表与插入位置)

---

## 一、问题分析与建模思路
（解释为什么选择这种方法，通俗易懂）

## 二、模型介绍与公式
（公式、符号说明、参数解释）

## 三、结果解读
（关键发现、数据表格、结论）

## 四、论文撰写建议
（建议的章节结构、关键公式LaTeX格式、常用英文表达）

## 五、图片列表与插入位置
| 编号 | 文件名 | 内容 | 建议插入章节 |
|------|--------|------|-------------|
| 1 | fig1_xxx.pdf | 描述 | X.X章节 |
```

---

## 面向person2.md 模板

资料/绘图指南文件结构：

```markdown
# 问题X —— 资料手工作指南

> 本文档面向资料手Person2，指导完成思路图绘制和参考文献查找工作。

## 一、需要绘制的思路图
（流程图ASCII示意、建议的绘图工具，这里选择意义大的思路图不超过2个，如果没有有价值的可画的就不用画）

## 二、参考文献检索指南
（检索关键词、推荐数据库、引用格式）

## 三、图片文件交付清单
（Coder已导出的图片列表、需要Person2绘制的图，有就写没有就不用，）

## 四、工作优先级
（高/中/低优先级任务）

## 五、与Person1协作说明
```

---

## 1. 模型选择决策树

```
拿到问题后，问自己：
│
├─ 要预测未来数值？ ──────────────→ 【预测类】
│   ├─ 有多个影响因素？ → 回归模型（线性/Ridge/Lasso/XGBoost）
│   ├─ 只有时间序列？ → ARIMA / Prophet / 指数平滑 / LSTM
│   ├─ 数据很少(<15个)？ → 灰色预测 GM(1,1)
│   ├─ 非线性很强？ → 随机森林 / XGBoost / GBDT
│   └─ 需要不确定性估计？ → MCMC / Bootstrap
│
├─ 要评价/排序/选方案？ ──────────→ 【评价决策类】
│   ├─ 需要定权重？ → AHP（主观）/ 熵权法（客观）
│   ├─ 方案排序？ → TOPSIS / PCA-TOPSIS
│   ├─ 指标模糊？ → 模糊综合评价
│   └─ 评价效率？ → DEA
│
├─ 要分类/分群？ ────────────────→ 【分类聚类类】
│   ├─ 有标签？ → 随机森林 / SVM / 决策树 / Logistic回归
│   ├─ 无标签？ → K-means / 层次聚类 / DBSCAN
│   └─ 图像分类？ → CNN（卷积神经网络）
│
├─ 要优化（求最大/最小）？ ────────→ 【优化类】
│   ├─ 线性约束？ → 线性规划
│   ├─ 非线性/复杂？ → 遗传算法 / 模拟退火
│   ├─ 多目标冲突？ → NSGA-II / 加权和法
│   └─ 序贯决策？ → 动态规划
│
├─ 要分析变量关系？ ──────────────→ 【统计分析类】
│   ├─ 两变量相关？ → Pearson/Spearman相关分析
│   ├─ 多组比较？ → 方差分析 ANOVA / t检验
│   ├─ 特征重要性？ → SHAP值分析 / 特征重要性排序
│   └─ 关联规则？ → Apriori / FP-Growth
│
├─ 要处理文本数据？ ──────────────→ 【NLP类】
│   ├─ 情感分析？ → VADER / TextBlob / BERT
│   ├─ 主题提取？ → LDA / TF-IDF
│   └─ 关键词提取？ → TF-IDF / TextRank
│
├─ 要建模状态转移？ ──────────────→ 【序列/状态类】
│   ├─ 状态转移概率？ → 马尔可夫链
│   ├─ 隐藏状态？ → 隐马尔可夫模型（HMM）
│   └─ 时序依赖？ → LSTM / GRU
│
└─ 要模拟系统演化？ ──────────────→ 【仿真类】
    ├─ 不确定性/风险？ → 蒙特卡洛模拟
    ├─ 空间扩散/演化？ → 元胞自动机
    └─ 风险度量？ → CVaR / VaR
```

### 美赛C题常见"王炸组合"

| 问题类型 | 推荐组合 | 说明 |
|----------|----------|------|
| 综合评价 | AHP + TOPSIS | AHP定权重，TOPSIS排序 |
| 预测+不确定性 | XGBoost + Bootstrap/MCMC | 预测+置信区间 |
| 方案优选 | AHP + 熵权法 + TOPSIS | 主客观结合更有说服力 |
| 风险评估 | Logistic回归 + 蒙特卡洛 | 概率+模拟 |
| 文本分析 | TF-IDF + LDA + 情感分析 | 特征提取+主题+情感 |
| 时空预测 | ARIMA/LSTM + 空间聚类 | 时间+空间维度 |
| 投资优化 | 预测模型 + 动态规划/遗传算法 | 预测+优化 |
| 状态建模 | HMM/马尔可夫 + 随机森林 | 状态+预测 |
| 效应分析 | DID/回归 + SHAP值分析 | 因果+解释 |

---

## 1.1 美赛C题历年考察总结（2020-2025）

| 年份 | 题目要点 | 核心算法模型 |
|------|----------|-------------|
| **2020** | 星级评论分析、情感分析、产品声誉预测 | VADER/TextBlob（情感）、TF-IDF+LDA（文本）、有序Logistic回归、ARIMA、随机森林 |
| **2021** | 亚洲巨蜂传播预测、图像分类、优先级评价 | ARIMA/LSTM（时空预测）、CNN（图像）、SVM/决策树、K-means（聚类） |
| **2022** | 黄金比特币交易策略、投资组合优化 | ARIMA/XGBoost（价格预测）、动态规划/遗传算法、CVaR（风险）、NSGA-II |
| **2023** | 时序预测、分布预测、难度分类、特征挖掘 | 指数平滑/灰色预测、随机森林/GBDT、K-means/层次聚类、相关分析 |
| **2024** | 网球势头建模、随机性验证、势头预测 | HMM/马尔可夫链、随机森林/XGBoost、Logistic回归、PCA-TOPSIS、LSTM |
| **2025** | 奖牌预测、不确定性估计、教练效应量化 | 随机森林/XGBoost、MCMC/Bootstrap、Logistic回归、SHAP值分析、关联规则 |

### C题高频考察能力

| 能力类型 | 出现频率 | 典型模型 |
|----------|----------|----------|
| **时序预测** | 每年必考 | ARIMA、LSTM、指数平滑、Prophet |
| **分类预测** | 高频 | 随机森林、XGBoost、Logistic回归 |
| **不确定性量化** | 高频 | Bootstrap、MCMC、置信区间 |
| **特征重要性** | 高频 | SHAP、特征重要性、相关分析 |
| **聚类分群** | 中频 | K-means、层次聚类、DBSCAN |
| **文本分析** | 中频 | TF-IDF、LDA、情感分析 |
| **优化决策** | 中频 | 动态规划、遗传算法、线性规划 |
| **状态建模** | 低频 | HMM、马尔可夫链 |

---

## 2. 评估指标速查

### 回归/预测模型

| 指标 | 公式 | 解读 | 论文句式 |
|------|------|------|----------|
| R² | 决定系数 | 0.8+ 非常好 | The R²=0.85 indicates that the model explains 85% of the variance. |
| MAE | 平均绝对误差 | 单位与原数据一致 | The MAE=3.2 suggests an average prediction deviation of 3 medals. |
| RMSE | 均方根误差 | 对大误差惩罚更重 | RMSE=5.8 indicates acceptable prediction accuracy. |
| MAPE | 平均相对误差 | <10%合格 | The MAPE of 8.5% demonstrates satisfactory relative accuracy. |

```python
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np

r2 = r2_score(y_true, y_pred)
mae = mean_absolute_error(y_true, y_pred)
rmse = np.sqrt(mean_squared_error(y_true, y_pred))
mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
```

### 分类模型

| 指标 | 解读 | 论文句式 |
|------|------|----------|
| Accuracy | 总体正确率（类别不平衡时会骗人） | The model achieves an accuracy of 0.87. |
| Precision | 预测为正的有多准 | Precision of 0.89 indicates high positive prediction accuracy. |
| Recall | 实际为正的找回多少 | Recall of 0.92 demonstrates comprehensive detection. |
| F1 | 精确率与召回率的调和平均 | F1-score of 0.90 indicates balanced performance. |
| AUC | 分类模型的"R²"，0.8+良好 | The AUC of 0.87 demonstrates strong discriminative ability. |

### 聚类模型

| 指标 | 范围 | 解读 |
|------|------|------|
| 轮廓系数 | -1~1 | 接近1聚得好，≈0重叠，<0分错了 |
| 肘部法则 | SSE拐点 | 确定最优K值 |

---

## 3. 论文句式模板

### 模型构建
```
We develop/establish/construct a [模型名称] to [模型功能].

Example: We develop a multidimensional predictive model to analyze Olympic 
medal patterns, utilizing PCA for dimensionality reduction.
```

### 技术融合
```
By combining/integrating [技术1] and [技术2], the model achieves [性能优势].

Example: By combining LSTM networks and XGBoost, the model achieves high 
accuracy in capturing temporal trends and nonlinear relationships.
```

### 结果描述
```
The results indicate/reveal/show [结论].
[指标] is statistically significant (p < 0.05), suggesting that [结论].

Example: The results indicate an upward trend for the United States. 
The correlation coefficient (r=0.80, p<0.001) suggests a strong positive 
relationship between historical and current performance.
```

### 图表引用
```
As illustrated in Fig. X, [图表核心内容].
Fig. X shows/depicts/demonstrates that [趋势/关系].

Example: As illustrated in Figs. 6(a)-(b), the United States is projected 
to see a significant increase in both gold and total medal counts.
```

---

## 4. 可视化禁止事项

- **不用3D图表**（除非绝对必要）
- **不用饼图**（改用柱状图）
- **同一图表不超过7种颜色**
- **避免过多装饰**（保持简洁）
- **图片不加标题**（标注放在ipynb markdown中）

---

## 5. 深度参考

- 完整算法手册：[algorithms/algorithms_reference.md](algorithms/algorithms_reference.md)
- 可视化指南：[data_analysis/visualization/可视化指南.ipynb](data_analysis/visualization/可视化指南.ipynb)
- 图表示例：[data_analysis/visualization/](data_analysis/visualization/) 目录下的各类图表示例
- 实战参考：[Simulation/25C/Coder/问题一/](Simulation/25C/Coder/问题一/) 完整案例
