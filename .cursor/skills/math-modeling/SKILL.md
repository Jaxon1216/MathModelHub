---
name: math-modeling
description: 数学建模算法选择与可视化指南。用于模型选择、算法实现、评估指标、可视化绑图、论文图表生成等场景。当用户提到建模、预测、分类、聚类、优化、回归、可视化、绑图、matplotlib、model selection时触发。
---

# 数学建模与可视化指南

## 1. 模型选择决策树

```
拿到问题后，问自己：
│
├─ 要预测未来数值？ ──────────────→ 【预测类】
│   ├─ 有多个影响因素？ → 回归模型（线性/Ridge/Lasso）
│   ├─ 只有时间序列？ → ARIMA / 指数平滑
│   ├─ 数据很少(<15个)？ → 灰色预测 GM(1,1)
│   └─ 非线性很强？ → 随机森林 / XGBoost
│
├─ 要评价/排序/选方案？ ──────────→ 【评价决策类】
│   ├─ 需要定权重？ → AHP（主观）/ 熵权法（客观）
│   ├─ 方案排序？ → TOPSIS
│   ├─ 指标模糊？ → 模糊综合评价
│   └─ 评价效率？ → DEA
│
├─ 要分类/分群？ ────────────────→ 【分类聚类类】
│   ├─ 有标签？ → 随机森林 / SVM / 决策树
│   └─ 无标签？ → K-means / 层次聚类
│
├─ 要优化（求最大/最小）？ ────────→ 【优化类】
│   ├─ 线性约束？ → 线性规划
│   ├─ 非线性/复杂？ → 遗传算法 / 模拟退火
│   └─ 多目标冲突？ → 多目标规划
│
├─ 要分析变量关系？ ──────────────→ 【统计分析类】
│   ├─ 两变量相关？ → Pearson/Spearman相关分析
│   ├─ 多组比较？ → 方差分析 ANOVA
│   └─ 小样本因素排序？ → 灰色关联分析
│
└─ 要模拟系统演化？ ──────────────→ 【仿真类】
    ├─ 不确定性/风险？ → 蒙特卡洛模拟
    └─ 空间扩散/演化？ → 元胞自动机
```

### 美赛常见"王炸组合"

| 问题类型 | 推荐组合 | 说明 |
|----------|----------|------|
| 综合评价 | AHP + TOPSIS | AHP定权重，TOPSIS排序 |
| 预测问题 | 回归 + 时间序列 | 多角度验证预测结果 |
| 方案优选 | AHP + 熵权法 + TOPSIS | 主客观结合更有说服力 |
| 风险评估 | Logistic回归 + 蒙特卡洛 | 概率+模拟 |

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

## 3. 可视化风格规范

### 配色方案

| 场景 | 推荐配色 | 示例 |
|------|----------|------|
| 单系列数据 | `steelblue` | 专业、稳重 |
| 强调对比 | `steelblue` + `coral` | 冷暖对比 |
| 正负值 | `RdBu_r` (colormap) | 红正蓝负 |
| 多系列 | `tab10` (palette) | 默认调色板 |
| 热力图 | `coolwarm`, `RdYlGn` | 渐变色 |

### 标准配置

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

### 保存图片

```python
# SVG
plt.savefig('figure.svg', bbox_inches='tight')
```

### 可视化禁止事项

- **不用3D图表**（除非绝对必要）
- **不用饼图**（改用柱状图）
- **同一图表不超过7种颜色**
- **避免过多装饰**（保持简洁）

---

## 4. 快速绑图模板

### 直方图
```python
def quick_histogram(data, title="Distribution", xlabel="Value", bins=30):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(data, bins=bins, edgecolor='black', alpha=0.7, color='steelblue')
    ax.axvline(data.mean(), color='red', linestyle='--', label=f'Mean: {data.mean():.2f}')
    ax.axvline(data.median(), color='green', linestyle='--', label=f'Median: {data.median():.2f}')
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Frequency')
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    return fig, ax
```

### 热力图
```python
def quick_heatmap(df, title="Correlation Matrix"):
    fig, ax = plt.subplots(figsize=(10, 8))
    corr = df.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r', 
                center=0, square=True, ax=ax)
    ax.set_title(title)
    plt.tight_layout()
    return fig, ax
```

### 预测评估散点图
```python
def quick_scatter_pred(y_true, y_pred, title="Actual vs Predicted"):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(y_true, y_pred, alpha=0.5, color='steelblue', edgecolor='white')
    min_val, max_val = min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())
    ax.plot([min_val, max_val], [min_val, max_val], 'k--', linewidth=2, label='Perfect')
    ax.set_xlabel('Actual')
    ax.set_ylabel('Predicted')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig, ax
```

---

## 5. 论文句式模板

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

### 模型假设
```
Assumption X: [假设内容]. → Justification: [合理性说明].

Example: Assumption 2: A country's past Olympic performance is a reliable 
indicator of future medal counts. → Justification: Historical performance 
reflects long-term trends in national sports development.
```

### 结果描述
```
The results indicate/reveal/show [结论].
[指标] is statistically significant (p < 0.05), suggesting that [结论].
There is a strong/weak positive/negative correlation between [变量1] and [变量2].

Example: The results indicate an upward trend for the United States and 
the United Kingdom. The correlation coefficient (r=0.80, p<0.001) suggests 
a strong positive relationship between historical and current performance.
```

### 图表引用
```
As illustrated in Fig. X, [图表核心内容].
Fig. X shows/depicts/demonstrates that [趋势/关系].
The [图表类型] in Fig. X further confirms that [结论].

Example: As illustrated in Figs. 6(a)-(b), the United States is projected 
to see a significant increase in both gold and total medal counts.
```

---

## 6. 深度参考

- 完整算法手册：[algorithms/algorithms_reference.md](algorithms/algorithms_reference.md)
- 可视化指南：[data_analysis/visualization/可视化指南.ipynb](data_analysis/visualization/可视化指南.ipynb)
- 图表示例：[data_analysis/visualization/](data_analysis/visualization/) 目录下的各类图表示例
