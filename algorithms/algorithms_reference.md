# 🎯 数学建模算法参考手册

> **定位**：零基础也能读懂的美赛/国赛算法速查手册
> 
> **核心理念**：模型是"说服工具"，不是"答案机器"。评委看的是你的逻辑，不是你算得准不准。
可以查看一下**data_analysis/preprocessing/2025C示例**里面的模型分析文件夹
---

## 📋 目录

1. [模型选择决策树](#一模型选择决策树)
2. [评估指标大全](#二评估指标大全)
3. [预测类模型](#三预测类模型)
4. [评价决策类模型](#四评价决策类模型)
5. [分类与聚类模型](#五分类与聚类模型)
6. [优化类模型](#六优化类模型)
7. [统计分析类模型](#七统计分析类模型)
8. [图论与网络模型](#八图论与网络模型)
9. [仿真类模型](#九仿真类模型)

---

# 一、模型选择决策树

> 💡 **拿到题目第一步：判断问题类型**

## 1.1 总决策树

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
│   ├─ 指标模糊（好/中/差）？ → 模糊综合评价
│   └─ 评价效率？ → DEA
│
├─ 要分类/分群？ ────────────────→ 【分类聚类类】
│   ├─ 有标签（知道答案）？ → 随机森林 / SVM / 决策树 / Logistic回归
│   ├─ 无标签（自动分群）？ → K-means / 层次聚类 / DBSCAN
│   └─ 图像分类？ → CNN（卷积神经网络）
│
├─ 要优化（求最大/最小）？ ────────→ 【优化类】
│   ├─ 线性约束？ → 线性规划
│   ├─ 非线性/复杂？ → 遗传算法 / 模拟退火
│   ├─ 多目标冲突？ → NSGA-II / 加权和法
│   └─ 序贯决策？ → 动态规划
│
├─ 要分析变量关系？ ──────────────→ 【统计分析类】
│   ├─ 两变量相关？ → 相关分析（Pearson/Spearman）
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

## 1.2 美赛常见"王炸组合"

| 问题类型 | 推荐组合 | 说明 |
|----------|----------|------|
| 综合评价 | **AHP + TOPSIS** | AHP定权重，TOPSIS排序 |
| 预测+不确定性 | **XGBoost + Bootstrap/MCMC** | 预测+置信区间 |
| 方案优选 | **AHP + 熵权法 + TOPSIS** | 主客观结合更有说服力 |
| 风险评估 | **Logistic回归 + 蒙特卡洛** | 概率+模拟 |
| 文本分析 | **TF-IDF + LDA + 情感分析** | 特征提取+主题+情感 |
| 时空预测 | **ARIMA/LSTM + 空间聚类** | 时间+空间维度 |
| 投资优化 | **预测模型 + 动态规划/遗传算法** | 预测+优化 |
| 状态建模 | **HMM/马尔可夫 + 随机森林** | 状态+预测 |
| 效应分析 | **DID/回归 + SHAP值分析** | 因果+解释 |

---

## 1.3 美赛C题历年考察总结（2020-2025）

> 💡 **C题特点**：数据驱动型，强调数据分析、预测建模、不确定性量化

| 年份 | 题目主题 | 核心考察点 | 推荐算法模型 |
|------|----------|------------|-------------|
| **2020** | 亚马逊产品评论分析 | 情感分析、文本挖掘、产品声誉预测 | VADER/TextBlob（情感分析）、TF-IDF+LDA（文本特征）、有序Logistic回归、ARIMA/Prophet（时序）、随机森林 |
| **2021** | 亚洲巨蜂入侵预测 | 时空传播预测、图像分类、优先级评价 | ARIMA/LSTM（时空预测）、CNN（图像分类）、SVM/决策树（报告分类）、加权综合评价、K-means（空间聚类） |
| **2022** | 黄金比特币交易策略 | 价格预测、投资组合优化、风险度量 | ARIMA/XGBoost（价格预测）、动态规划/遗传算法（优化）、CVaR（风险度量）、NSGA-II（多目标优化）、敏感性分析 |
| **2023** | Wordle游戏结果预测 | 时序预测、分布预测、难度分类 | 二次指数平滑/灰色预测（时序）、随机森林/GBDT（分布预测）、K-means/层次聚类（难度分类）、皮尔逊相关分析 |
| **2024** | 网球比赛势头分析 | 状态建模、势头预测、可视化 | HMM/马尔可夫链（状态建模）、随机森林/XGBoost（预测）、Logistic回归（胜负）、PCA-TOPSIS（表现评估）、LSTM |
| **2025** | 奥运奖牌预测 | 奖牌预测、不确定性估计、教练效应 | 随机森林/XGBoost（预测）、MCMC/Bootstrap（不确定性）、Logistic回归（首奖概率）、SHAP值（效应分析）、关联规则 |

### C题高频考察能力统计

| 能力类型 | 出现频率 | 典型模型 | 应用场景 |
|----------|----------|----------|----------|
| **时序预测** | ⭐⭐⭐⭐⭐ | ARIMA、LSTM、指数平滑、Prophet | 价格、数量、趋势预测 |
| **分类/回归预测** | ⭐⭐⭐⭐⭐ | 随机森林、XGBoost、Logistic回归 | 结果预测、概率估计 |
| **不确定性量化** | ⭐⭐⭐⭐ | Bootstrap、MCMC、置信区间 | 预测区间、风险评估 |
| **特征重要性分析** | ⭐⭐⭐⭐ | SHAP、特征重要性、相关分析 | 影响因素识别 |
| **聚类/分群** | ⭐⭐⭐ | K-means、层次聚类、DBSCAN | 分类、分组、异常检测 |
| **文本/NLP分析** | ⭐⭐⭐ | TF-IDF、LDA、情感分析 | 评论分析、主题提取 |
| **优化决策** | ⭐⭐⭐ | 动态规划、遗传算法、线性规划 | 策略优化、资源配置 |
| **状态/序列建模** | ⭐⭐ | HMM、马尔可夫链、LSTM | 状态转移、序列预测 |
| **综合评价** | ⭐⭐ | AHP、TOPSIS、熵权法 | 方案排序、多指标评价 |

---

## 1.4 扩展模型速查

### 文本分析类（NLP）

| 模型 | 用途 | Python库 |
|------|------|----------|
| **VADER** | 英文情感分析（社交媒体） | `nltk.sentiment.vader` |
| **TextBlob** | 简单情感分析 | `textblob` |
| **TF-IDF** | 文本特征提取、关键词 | `sklearn.feature_extraction.text` |
| **LDA** | 主题建模 | `gensim` 或 `sklearn` |
| **Word2Vec** | 词向量表示 | `gensim` |

### 时序预测类

| 模型 | 适用场景 | Python库 |
|------|----------|----------|
| **ARIMA** | 平稳时序、短期预测 | `statsmodels` |
| **SARIMA** | 带季节性的时序 | `statsmodels` |
| **Prophet** | 带趋势+季节的时序 | `prophet` |
| **LSTM/GRU** | 复杂非线性时序 | `tensorflow/keras` |
| **指数平滑** | 简单趋势预测 | `statsmodels` |

### 优化类

| 模型 | 适用场景 | Python库 |
|------|----------|----------|
| **线性规划** | 线性目标+线性约束 | `scipy.optimize.linprog` |
| **整数规划** | 变量必须为整数 | `scipy.optimize.milp` |
| **遗传算法** | 复杂非线性优化 | `deap` 或 `scipy.optimize` |
| **动态规划** | 序贯决策问题 | 自行实现 |
| **NSGA-II** | 多目标优化 | `pymoo` |

### 风险度量类

| 指标 | 含义 | 应用 |
|------|------|------|
| **VaR** | 风险价值，最大可能损失 | 金融风险 |
| **CVaR** | 条件风险价值，尾部风险 | 极端情况评估 |
| **夏普比率** | 风险调整后收益 | 投资组合评价 |

---

# 二、评估指标大全

> 💡 **模型不是"算出来"的，是"用指标证明出来"的**

## 2.1 回归/预测模型指标

### R²（决定系数）⭐⭐⭐⭐⭐

**一句话**：模型解释了多少数据波动

```
范围：0 ≤ R² ≤ 1
```

| R² 值 | 含义 |
|-------|------|
| ≈ 0 | 几乎没学到规律 |
| 0.3~0.6 | 有一定解释能力 |
| 0.6~0.8 | 拟合较好 |
| > 0.8 | 非常好（警惕过拟合）|

**📝 论文句式**：
> The coefficient of determination (R²=0.85) indicates that the model explains 85% of the variance in medal counts.

**🎯 2025C题应用**：
> 在奖牌预测模型中，Lasso回归的R²=0.9484，说明模型能解释94.84%的奖牌数变化。

---

### MAE（平均绝对误差）⭐⭐⭐⭐⭐

**一句话**：预测值和真实值平均差多少

```python
MAE = mean(|y_true - y_pred|)
```

- 单位与原数据一致
- 不夸大极端误差
- **论文友好型指标**

**📝 论文句式**：
> The Mean Absolute Error (MAE=3.2) suggests that the average prediction deviation is approximately 3 medals.

---

### RMSE（均方根误差）⭐⭐⭐⭐⭐

**一句话**：对"大错"惩罚更重的误差指标

```python
RMSE = sqrt(mean((y_true - y_pred)²))
```

| MAE vs RMSE | 特点 |
|-------------|------|
| MAE | 人人平等 |
| RMSE | 错得离谱会被重点惩罚 |

**📝 论文句式**：
> RMSE is adopted to penalize large deviations, with a value of 5.8 indicating acceptable prediction accuracy.

---

### MAPE（平均相对误差）⭐⭐⭐⭐

**一句话**：平均误差占真实值的百分比

```python
MAPE = mean(|y_true - y_pred| / y_true) × 100%
```

⚠️ **注意**：真实值不能有0

**📝 论文句式**：
> The MAPE of 8.5% demonstrates that the model achieves satisfactory relative accuracy.

---

### 指标组合建议

| 模型类型 | 推荐指标组合 |
|----------|--------------|
| 线性回归 | R² + MAE + RMSE |
| 时间序列 | RMSE + MAPE + AIC |
| 灰色预测 | 平均相对误差 + 后验差比C |
| 神经网络 | R² + MAE + RMSE + Loss曲线 |

---

## 2.2 分类模型指标

### 混淆矩阵 ⭐⭐⭐⭐⭐

**必画！所有分类指标的基础**

|  | 预测=正 | 预测=负 |
|--|---------|---------|
| **实际=正** | TP（真正例）| FN（漏报）|
| **实际=负** | FP（误报）| TN（真负例）|

---

### Accuracy（准确率）

```python
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

⚠️ **陷阱**：类别不平衡时会骗人！

---

### Precision / Recall / F1 ⭐⭐⭐⭐⭐

| 指标 | 公式 | 含义 |
|------|------|------|
| Precision | TP/(TP+FP) | 预测为正的有多准 |
| Recall | TP/(TP+FN) | 实际为正的找回多少 |
| F1 | 2×P×R/(P+R) | 两者的调和平均 |

**📝 论文句式**：
> The model achieves a Precision of 0.89 and Recall of 0.92, with an F1-score of 0.90, indicating balanced classification performance.

---

### AUC-ROC ⭐⭐⭐⭐⭐

**一句话**：分类模型的"R²"

```
范围：0.5 ≤ AUC ≤ 1.0
```

| AUC值 | 含义 |
|-------|------|
| 0.5 | 随机猜测 |
| 0.7~0.8 | 一般 |
| 0.8~0.9 | 良好 |
| > 0.9 | 优秀 |

**📝 论文句式**：
> The AUC of 0.87 demonstrates strong discriminative ability of the classifier.

---

## 2.3 聚类模型指标

### 轮廓系数（Silhouette）⭐⭐⭐⭐⭐

**一句话**：聚类版的"R²"

```
范围：-1 ≤ s ≤ 1
```

| 值 | 含义 |
|----|------|
| 接近1 | 聚得很好 |
| ≈ 0 | 类别重叠 |
| < 0 | 分错了 |

---

### 肘部法则（Elbow Method）⭐⭐⭐⭐⭐

**用于确定K值**：看SSE随K变化的"拐点"

**📝 论文句式**：
> Based on the elbow method, K=4 is selected where the rate of SSE decrease significantly slows down.

---

## 2.4 时间序列模型指标

### AIC / BIC

**一句话**：在"拟合好"和"别太复杂"之间找平衡

```
AIC / BIC 越小，模型越好
```

**📝 论文句式**：
> The ARIMA(1,1,1) model is selected based on the minimum AIC value of 256.3.

---

## 2.5 指标速查表

| 模型类型 | 核心指标 | 对标 |
|----------|----------|------|
| 回归 | R², RMSE, MAE | R²越大越好 |
| 分类 | AUC, F1 | AUC≈分类版R² |
| 聚类 | 轮廓系数 | 轮廓≈聚类版R² |
| 时间序列 | AIC, MAPE | AIC越小越好 |

---

# 三、预测类模型

## 3.1 线性回归（基础必会）

**美赛出现率**：⭐⭐⭐⭐⭐

### 适用场景
- 多因素影响一个数值结果
- 需要分析各因素的影响方向和强度
- 需要高可解释性

### 核心思想
> 假设世界是"大致线性的"：原因变一点，结果也跟着变一点

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# 查看系数（重要！）
print("各特征影响权重:", model.coef_)
print("截距:", model.intercept_)
```

### 评价指标
```python
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
```

### 📝 论文句式

> A multiple linear regression model is established to quantify the influence of key factors on medal counts. The regression coefficients indicate that historical performance (β=0.85) has the most significant positive impact.

### 🎯 2025C题应用

> 在奥运奖牌预测中，我们建立多元线性回归模型，以`total_lag1`、`is_host`等为自变量预测`Total`。回归系数显示，`total_lag1`(β=0.82)影响最大，验证了"历史表现是最强预测因子"的假设。

---

## 3.2 正则化回归（Ridge / Lasso）

**美赛出现率**：⭐⭐⭐⭐

### 适用场景
- 特征较多，担心过拟合
- 特征间存在多重共线性
- 需要自动特征选择（Lasso）

### 核心区别

| 方法 | 正则化 | 特点 |
|------|--------|------|
| Ridge | L2 | 系数缩小但不为0 |
| Lasso | L1 | 系数可能变为0（自动选特征）|

```python
from sklearn.linear_model import Ridge, Lasso

# Ridge回归
ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)

# Lasso回归（会自动剔除不重要特征）
lasso = Lasso(alpha=0.1)
lasso.fit(X_train, y_train)
```

### 📝 论文句式

> Lasso regression is employed to address multicollinearity and perform automatic feature selection. The L1 regularization drives less important coefficients to zero, yielding a more parsimonious model.

### 🎯 2025C题应用

> 由于`total_lag1`、`gold_lag1`、`total_rolling3_mean`存在高度共线性（相关系数>0.8），我们采用Lasso回归进行特征筛选。结果显示Lasso(R²=0.9484)略优于普通线性回归(R²=0.9454)。

---

## 3.3 ARIMA时间序列

**美赛出现率**：⭐⭐⭐⭐⭐

### 适用场景
- 只有历史时间数据
- 数据按时间排列且有规律
- 需要预测未来趋势

### 核心思想
> 今天 ≈ 昨天 + 前天 + 随机波动

### ARIMA(p,d,q)参数
- **p**：自回归阶数（看PACF图）
- **d**：差分次数（让数据平稳）
- **q**：移动平均阶数（看ACF图）

```python
from statsmodels.tsa.arima.model import ARIMA

# 建立模型
model = ARIMA(data, order=(1, 1, 1))
fitted = model.fit()

# 预测未来10期
forecast = fitted.forecast(steps=10)

# 查看模型信息
print(fitted.summary())
print(f"AIC: {fitted.aic}")
```

### 📝 论文句式

> An ARIMA(1,1,1) model is constructed based on the Box-Jenkins methodology. The model selection is guided by the minimum AIC criterion, and the Ljung-Box test confirms that residuals exhibit no significant autocorrelation.

---

## 3.4 灰色预测 GM(1,1)

**美赛出现率**：⭐⭐⭐

### 适用场景
- 数据点很少（4~15个）
- 数据呈单调趋势
- 不满足统计学样本量要求

### 核心思想
> 把数据累加平滑，假设按指数发展

```python
def grey_model_gm11(x0, n_predict=3):
    """
    GM(1,1)灰色预测模型
    x0: 原始序列
    n_predict: 预测步数
    """
    n = len(x0)
    x1 = np.cumsum(x0)  # 一次累加生成
    
    # 构造数据矩阵
    B = np.zeros((n-1, 2))
    Y = x0[1:].reshape((n-1, 1))
    
    for i in range(n-1):
        B[i][0] = -(x1[i] + x1[i+1]) / 2
        B[i][1] = 1
    
    # 最小二乘估计参数
    params = np.linalg.inv(B.T @ B) @ B.T @ Y
    a, b = params[0][0], params[1][0]
    
    # 预测
    predictions = []
    for k in range(1, n + n_predict + 1):
        x1_pred = (x0[0] - b/a) * np.exp(-a * (k-1)) + b/a
        predictions.append(x1_pred)
    
    # 累减还原
    x0_pred = np.diff(predictions)
    x0_pred = np.insert(x0_pred, 0, predictions[0])
    
    return x0_pred[:n], x0_pred[n:]  # 拟合值, 预测值
```

### 评价指标
- **平均相对误差**：< 10% 为合格
- **后验差比C**：< 0.35 为优秀
- **小误差概率P**：> 0.95 为优秀

### 📝 论文句式

> Given the limited historical data (n=8), a GM(1,1) grey prediction model is applied. The posterior variance ratio C=0.28 and small error probability P=0.98 indicate excellent model fitting.

---

## 3.5 Logistic回归（预测概率）

**美赛出现率**：⭐⭐⭐⭐

### 适用场景
- 预测"是/否"、"成功/失败"
- 输出概率而非确定值
- 风险评估、事件发生可能性

### 核心思想
> 把各种因素的影响，转化为事件发生的概率(0~1)

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train, y_train)

# 预测概率
probabilities = model.predict_proba(X_test)[:, 1]

# 预测类别
predictions = model.predict(X_test)
```

### 📝 论文句式

> Logistic regression is employed to estimate the probability of a country winning more than 50 medals. The model yields an AUC of 0.89, demonstrating strong predictive power for identifying potential medal powerhouses.

---

## 3.6 随机森林回归

**美赛出现率**：⭐⭐⭐⭐

### 适用场景
- 特征多、关系复杂
- 不确定是否线性
- 需要特征重要性分析

### 核心思想
> 很多"不太聪明"的树，投票/平均决定结果

```python
from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

# 特征重要性（美赛加分项！）
importance = pd.DataFrame({
    'feature': feature_names,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)
```

### 📝 论文句式

> A Random Forest model with 100 trees is trained to capture non-linear relationships. Feature importance analysis reveals that historical medal count contributes 45% to the prediction, followed by host status (18%).

### 🎯 2025C题应用

> 尽管随机森林(R²=0.917)略低于线性模型(R²=0.948)，但其特征重要性分析直观展示了`total_lag1`(45%)和`is_host`(18%)是最重要的预测因子，与相关性分析结论一致。

---

# 四、评价决策类模型

## 4.1 AHP（层次分析法）

**美赛出现率**：⭐⭐⭐⭐⭐

### 适用场景
- 多准则决策问题
- 权重不明确，需要"专家判断"
- 定性+定量指标混合

### 核心思想
> 两两比较：哪个更重要？重要多少？

### 判断矩阵标度

| 标度 | 含义 |
|------|------|
| 1 | 同等重要 |
| 3 | 稍微重要 |
| 5 | 明显重要 |
| 7 | 强烈重要 |
| 9 | 极端重要 |

```python
import numpy as np

def ahp_weights(matrix):
    """计算AHP权重"""
    n = matrix.shape[0]
    
    # 方法1：几何平均法
    row_product = np.prod(matrix, axis=1)
    row_geo_mean = row_product ** (1/n)
    weights = row_geo_mean / row_geo_mean.sum()
    
    # 一致性检验
    lambda_max = np.sum(matrix @ weights / weights) / n
    CI = (lambda_max - n) / (n - 1)
    RI = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45]  # 随机一致性指标
    CR = CI / RI[n-1] if n > 2 else 0
    
    return weights, CR

# 示例：比较3个因素的重要性
matrix = np.array([
    [1,   3,   5],    # 因素1
    [1/3, 1,   2],    # 因素2  
    [1/5, 1/2, 1]     # 因素3
])

weights, cr = ahp_weights(matrix)
print(f"权重: {weights}")
print(f"一致性比率CR: {cr:.4f} {'(通过)' if cr < 0.1 else '(需调整)'}")
```

### 📝 论文句式

> The Analytic Hierarchy Process (AHP) is employed to determine indicator weights through pairwise comparison. The consistency ratio CR=0.05<0.1 confirms the reliability of the judgment matrix.

---

## 4.2 熵权法（客观赋权）

**美赛出现率**：⭐⭐⭐⭐⭐

### 适用场景
- 需要客观权重（不依赖主观判断）
- 有多个评价指标
- 常与AHP组合使用

### 核心思想
> 信息熵越小（数据差异越大），指标越重要

```python
def entropy_weight(data):
    """熵权法计算权重"""
    # 标准化
    data_norm = (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0) + 1e-10)
    
    # 计算比重
    p = data_norm / data_norm.sum(axis=0)
    p = np.where(p == 0, 1e-10, p)  # 避免log(0)
    
    # 计算熵值
    n = data.shape[0]
    e = -1/np.log(n) * np.sum(p * np.log(p), axis=0)
    
    # 计算权重
    d = 1 - e  # 差异系数
    weights = d / d.sum()
    
    return weights
```

### 📝 论文句式

> The Entropy Weight Method is applied to objectively determine indicator weights based on data variability. Higher weights are assigned to indicators with greater dispersion.

---

## 4.3 TOPSIS（排序神器）

**美赛出现率**：⭐⭐⭐⭐

### 适用场景
- 多对象综合排名
- 方案比较优选
- 数值型指标为主

### 核心思想
> 好方案 = 离"最好"近 + 离"最差"远

```python
def topsis(data, weights, is_benefit):
    """
    TOPSIS评价
    data: 决策矩阵 (m个方案 × n个指标)
    weights: 指标权重
    is_benefit: 是否为正向指标（True=越大越好）
    """
    # 标准化
    norm_data = data / np.sqrt((data**2).sum(axis=0))
    
    # 加权
    weighted = norm_data * weights
    
    # 确定正负理想解
    ideal_pos = np.where(is_benefit, weighted.max(axis=0), weighted.min(axis=0))
    ideal_neg = np.where(is_benefit, weighted.min(axis=0), weighted.max(axis=0))
    
    # 计算距离
    d_pos = np.sqrt(((weighted - ideal_pos)**2).sum(axis=1))
    d_neg = np.sqrt(((weighted - ideal_neg)**2).sum(axis=1))
    
    # 计算贴近度
    scores = d_neg / (d_pos + d_neg)
    ranks = scores.argsort()[::-1] + 1
    
    return scores, ranks
```

### 📝 论文句式

> The TOPSIS method is employed to rank alternatives based on their relative closeness to the ideal solution. The results indicate that Alternative A achieves the highest score (0.78), followed by B (0.65) and C (0.52).

---

## 4.4 模糊综合评价

**美赛出现率**：⭐⭐⭐⭐

### 适用场景
- 主观/模糊指标（满意度、舒适度）
- 只能说"好/中/差"
- 问卷调查分析

### 核心思想
> 把"模糊判断"量化为隶属度

```python
def fuzzy_evaluation(weights, membership_matrix, levels):
    """
    模糊综合评价
    weights: 指标权重
    membership_matrix: 隶属度矩阵 (指标数 × 等级数)
    levels: 评价等级分值
    """
    # 模糊综合运算
    B = weights @ membership_matrix
    B = B / B.sum()  # 归一化
    
    # 计算综合得分
    score = B @ np.array(levels)
    
    # 确定等级
    max_level_idx = B.argmax()
    
    return B, score, max_level_idx
```

### 📝 论文句式

> A Fuzzy Comprehensive Evaluation model is constructed with evaluation grades {Excellent, Good, Medium, Poor}. The final membership vector B=(0.35, 0.42, 0.18, 0.05) indicates that the overall evaluation tends toward "Good".

---

## 4.5 DEA（数据包络分析）

**美赛出现率**：⭐⭐⭐

### 适用场景
- 评价"效率"而非"好坏"
- 多投入多产出系统
- 不需要预设权重

### 核心思想
> 别人用更少资源，干更多事，那就更有效率

### 📝 论文句式

> Data Envelopment Analysis (DEA) is applied to evaluate the relative efficiency of decision-making units. The CCR model identifies 5 units as technically efficient (θ=1), while the remaining units exhibit varying degrees of inefficiency.

---

## 4.6 主客观组合权重

**美赛强烈推荐**：⭐⭐⭐⭐⭐

```python
def combined_weight(subjective, objective, alpha=0.5):
    """
    组合权重
    alpha: 主观权重的比例
    """
    return alpha * subjective + (1 - alpha) * objective
```

### 📝 论文句式

> To balance subjectivity and objectivity, the final weights are obtained by combining AHP weights (subjective) and entropy weights (objective) with equal proportion (α=0.5).

---

# 五、分类与聚类模型

## 5.1 K-means聚类

**美赛出现率**：⭐⭐⭐⭐

### 适用场景
- 无标签，想"分堆"
- 发现数据内部结构
- 客户分群、区域划分

### 核心思想
> 把点分成K堆，让每堆内部尽量紧凑

```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# 用肘部法则确定K
inertias = []
silhouettes = []
K_range = range(2, 10)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(data)
    inertias.append(kmeans.inertia_)
    silhouettes.append(silhouette_score(data, kmeans.labels_))

# 最终聚类
best_k = 4  # 根据肘部法则确定
kmeans = KMeans(n_clusters=best_k, random_state=42)
labels = kmeans.fit_predict(data)
```

### 📝 论文句式

> K-means clustering is performed to segment countries into distinct groups. The optimal number of clusters (K=4) is determined by the elbow method, with a silhouette coefficient of 0.65 confirming good cluster separation.

### 🎯 2025C题应用

> 我们对各国历史奖牌表现进行K-means聚类，识别出4类国家：超级强国(美中俄)、传统强国(英德法日)、中等水平国家、以及偶尔获奖国家。这一分类为分层预测模型提供了依据。

---

## 5.2 随机森林分类

**美赛出现率**：⭐⭐⭐⭐

### 适用场景
- 有标签的分类问题
- 特征多、关系复杂
- 需要特征重要性

### 核心思想
> 很多不太聪明的树，投票决定类别

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# 预测
y_pred = rf.predict(X_test)
y_prob = rf.predict_proba(X_test)[:, 1]

# 评价
print(classification_report(y_test, y_pred))
print(f"AUC: {roc_auc_score(y_test, y_prob):.4f}")

# 特征重要性
importance = pd.Series(rf.feature_importances_, index=feature_names)
print(importance.sort_values(ascending=False))
```

### 📝 论文句式

> A Random Forest classifier with 100 trees is trained to predict medal categories. The model achieves an accuracy of 0.87 and AUC of 0.92. Feature importance analysis highlights historical performance as the dominant predictor.

---

## 5.3 SVM（支持向量机）

**美赛出现率**：⭐⭐⭐

### 适用场景
- 样本少、维度高
- 边界清晰的分类问题
- 文本、图像分类

### 核心思想
> 找一条分界线，让两边离得尽量远

```python
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

# SVM对尺度敏感，必须标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 训练
svm = SVC(kernel='rbf', probability=True)
svm.fit(X_train_scaled, y_train)
```

### 📝 论文句式

> Support Vector Machine with RBF kernel is employed given the high-dimensional feature space. The model achieves an F1-score of 0.85, demonstrating effective classification with limited samples.

---

## 5.4 决策树

**美赛出现率**：⭐⭐⭐⭐

### 适用场景
- 需要"规则"，不是黑盒
- 可解释性要求高
- 生成决策流程图

### 核心思想
> 一步一步问问题，把样本分开

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree

dt = DecisionTreeClassifier(max_depth=4, random_state=42)
dt.fit(X_train, y_train)

# 可视化决策树
plt.figure(figsize=(20, 10))
plot_tree(dt, feature_names=feature_names, class_names=class_names, filled=True)
plt.show()
```

### 📝 论文句式

> A Decision Tree classifier is constructed for its interpretability. The tree structure reveals that if historical medals > 50 and is_host = 1, the country is predicted to achieve high performance with 92% confidence.

---

# 六、优化类模型

## 6.1 线性规划

**美赛出现率**：⭐⭐⭐⭐

### 适用场景
- 资源分配、生产计划
- 目标和约束都是线性的
- 追求最大/最小化

```python
from scipy.optimize import linprog

# 目标：最小化 c'x
c = [1, 2]  # 目标函数系数

# 不等式约束：Ax <= b
A_ub = [[-1, 1], [1, 2]]
b_ub = [1, 4]

# 等式约束：A_eq x = b_eq
A_eq = [[1, 1]]
b_eq = [3]

# 变量边界
bounds = [(0, None), (0, None)]

# 求解
result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
print(f"最优解: {result.x}")
print(f"最优值: {result.fun}")
```

### 📝 论文句式

> A linear programming model is formulated to minimize total cost subject to resource constraints. The optimal solution allocates x₁=2 and x₂=1 with a minimum cost of 4 units.

---

## 6.2 整数规划

**美赛出现率**：⭐⭐⭐⭐

### 适用场景
- 变量必须是整数
- 选址、调度、分配问题

```python
from scipy.optimize import milp, LinearConstraint, Bounds

# 目标函数系数
c = np.array([1, 2, 3])

# 约束
constraints = LinearConstraint(A=[[1, 1, 1], [2, 1, 0]], lb=[3, 2], ub=[np.inf, np.inf])

# 整数约束
integrality = np.ones(3)  # 1表示整数，0表示连续

# 求解
result = milp(c, constraints=constraints, integrality=integrality, bounds=Bounds(0, np.inf))
```

### 📝 论文句式

> An integer programming model is developed to determine the optimal facility locations. The binary decision variables represent whether to open a facility at each candidate site.

---

## 6.3 遗传算法

**美赛出现率**：⭐⭐⭐⭐

### 适用场景
- 问题复杂，无法用传统方法
- 组合优化、参数调优
- 全局搜索

### 核心思想
> 模拟自然选择：选择、交叉、变异

```python
# 使用 DEAP 库
from deap import base, creator, tools, algorithms

# 或使用 scipy
from scipy.optimize import differential_evolution

def objective(x):
    return x[0]**2 + x[1]**2

bounds = [(-5, 5), (-5, 5)]
result = differential_evolution(objective, bounds)
print(f"最优解: {result.x}")
print(f"最优值: {result.fun}")
```

### 📝 论文句式

> A Genetic Algorithm is employed to solve the complex optimization problem. After 100 generations with a population size of 50, the algorithm converges to a near-optimal solution with fitness value of 0.02.

---

## 6.4 多目标规划

**美赛出现率**：⭐⭐⭐

### 适用场景
- 多个目标相互冲突
- 无法同时最优化所有目标
- 需要权衡折中

### 核心概念
- **帕累托前沿**：改善一个目标必然牺牲另一个
- **加权法**：给目标分配权重

```python
from scipy.optimize import minimize

def multi_objective(x, w1=0.5, w2=0.5):
    f1 = x[0]**2 + x[1]**2  # 目标1
    f2 = (x[0]-1)**2 + (x[1]-1)**2  # 目标2
    return w1 * f1 + w2 * f2  # 加权和

result = minimize(multi_objective, x0=[0, 0])
```

### 📝 论文句式

> A multi-objective optimization model is formulated to balance cost minimization and quality maximization. The Pareto front is generated using the ε-constraint method, providing decision-makers with a set of trade-off solutions.

---

# 七、统计分析类模型

## 7.1 相关分析

**美赛出现率**：⭐⭐⭐⭐⭐

### Pearson vs Spearman

| 方法 | 适用场景 | 关系类型 |
|------|----------|----------|
| Pearson | 连续、正态、线性 | 线性关系 |
| Spearman | 有序、非正态 | 单调关系 |

```python
from scipy.stats import pearsonr, spearmanr

# Pearson相关
r, p_value = pearsonr(x, y)
print(f"Pearson r = {r:.4f}, p = {p_value:.4f}")

# Spearman相关
rho, p_value = spearmanr(x, y)
print(f"Spearman ρ = {rho:.4f}, p = {p_value:.4f}")
```

### 相关系数解读

| r值 | 强度 |
|-----|------|
| 0.8~1.0 | 极强 |
| 0.6~0.8 | 强 |
| 0.4~0.6 | 中等 |
| 0.2~0.4 | 弱 |
| 0~0.2 | 极弱 |

### 📝 论文句式

> Pearson correlation analysis reveals a strong positive relationship between historical performance and current medals (r=0.80, p<0.001), indicating that past success is a reliable predictor of future performance.

### 🎯 2025C题应用

> 相关性分析显示，`total_lag1`与`Total`的Pearson相关系数为0.80(p<0.001)，说明上届奖牌数是预测本届成绩的最强指标。`is_host`与`Total`的相关系数为0.37，虽然中等，但考虑到它是二元变量，在t检验中显示出显著的东道主效应。

---

## 7.2 方差分析（ANOVA）

**美赛出现率**：⭐⭐⭐⭐

### 适用场景
- 比较多组均值是否有差异
- 实验设计、处理效果比较

```python
from scipy.stats import f_oneway

# 单因素方差分析
group1 = [23, 25, 27, 22, 24]
group2 = [31, 33, 35, 30, 32]
group3 = [18, 20, 22, 17, 19]

f_stat, p_value = f_oneway(group1, group2, group3)
print(f"F = {f_stat:.4f}, p = {p_value:.4f}")
```

### 📝 论文句式

> One-way ANOVA is conducted to compare medal counts across different continental groups. The significant F-value (F=15.32, p<0.001) indicates that geographic region has a significant effect on Olympic performance.

### 🎯 2025C题应用

> 方差分析显示东道主与非东道主的奖牌数存在显著差异(F=45.6, p<0.001)。事后检验进一步确认东道主平均获得68.2枚奖牌，显著高于非东道主的11.3枚。

---

## 7.3 灰色关联分析

**美赛出现率**：⭐⭐⭐

### 适用场景
- 小样本（<15个数据点）
- 因素排序
- 不要求数据分布

### 核心思想
> 哪个因素的曲线形状和结果曲线最像

```python
def grey_relational_analysis(reference, comparisons, rho=0.5):
    """
    灰色关联分析
    reference: 参考序列（因变量）
    comparisons: 比较序列（各因素）
    rho: 分辨系数，通常取0.5
    """
    # 初值化处理
    ref_norm = reference / reference[0]
    comp_norm = comparisons / comparisons[:, 0:1]
    
    # 计算差序列
    diff = np.abs(comp_norm - ref_norm)
    
    # 最大差和最小差
    diff_min = diff.min()
    diff_max = diff.max()
    
    # 关联系数
    xi = (diff_min + rho * diff_max) / (diff + rho * diff_max)
    
    # 关联度
    gamma = xi.mean(axis=1)
    
    return gamma
```

### 📝 论文句式

> Grey Relational Analysis is applied given the limited data points (n=10). The results indicate that Factor A exhibits the highest grey relational grade (γ=0.82), suggesting it has the strongest influence on the target variable.

---

# 八、图论与网络模型

## 8.1 最短路径（Dijkstra）

**美赛出现率**：⭐⭐⭐⭐

```python
import networkx as nx

# 创建图
G = nx.Graph()
G.add_weighted_edges_from([
    (1, 2, 4), (1, 3, 2), (2, 3, 1), 
    (2, 4, 5), (3, 4, 8)
])

# 最短路径
path = nx.shortest_path(G, source=1, target=4, weight='weight')
length = nx.shortest_path_length(G, source=1, target=4, weight='weight')

print(f"最短路径: {path}")
print(f"最短距离: {length}")
```

### 📝 论文句式

> Dijkstra's algorithm is applied to find the shortest path in the transportation network. The optimal route from node A to node E has a total distance of 15 km, passing through nodes B and D.

---

## 8.2 最大流

**美赛出现率**：⭐⭐⭐

```python
# 最大流问题
G = nx.DiGraph()
G.add_edge('s', 'a', capacity=10)
G.add_edge('s', 'b', capacity=5)
G.add_edge('a', 't', capacity=7)
G.add_edge('b', 't', capacity=8)
G.add_edge('a', 'b', capacity=3)

flow_value, flow_dict = nx.maximum_flow(G, 's', 't')
print(f"最大流: {flow_value}")
```

### 📝 论文句式

> The maximum flow algorithm is applied to determine the network capacity. The maximum flow from source to sink is 12 units, with the bottleneck identified at edge (A, B).

---

# 九、仿真类模型

## 9.1 蒙特卡洛模拟

**美赛出现率**：⭐⭐⭐⭐

### 适用场景
- 不确定性分析
- 风险评估
- 复杂系统模拟

### 核心思想
> 用大量随机试验，模拟所有可能结果

```python
import numpy as np

def monte_carlo_simulation(n_simulations=10000):
    """蒙特卡洛模拟示例：估算项目风险"""
    
    results = []
    for _ in range(n_simulations):
        # 随机生成各因素
        cost = np.random.normal(100, 10)      # 成本：均值100，标准差10
        time = np.random.uniform(5, 15)       # 时间：5-15天均匀分布
        quality = np.random.triangular(0.7, 0.9, 1.0)  # 质量：三角分布
        
        # 计算结果
        outcome = cost * time / quality
        results.append(outcome)
    
    results = np.array(results)
    
    # 统计分析
    print(f"均值: {results.mean():.2f}")
    print(f"标准差: {results.std():.2f}")
    print(f"95%置信区间: [{np.percentile(results, 2.5):.2f}, {np.percentile(results, 97.5):.2f}]")
    print(f"超过1500的概率: {(results > 1500).mean()*100:.2f}%")
    
    return results

results = monte_carlo_simulation()
```

### 📝 论文句式

> Monte Carlo simulation with 10,000 iterations is conducted to quantify uncertainty. The results show a mean outcome of 1,250 with a 95% confidence interval of [980, 1,580]. The probability of exceeding the threshold is estimated at 12.5%.

---

## 9.2 元胞自动机

**美赛出现率**：⭐⭐⭐

### 适用场景
- 空间扩散模拟
- 传染病、森林火灾、城市扩张
- 局部规则产生全局模式

### 核心思想
> 每个格子只看"邻居"状态来决定下一时刻

```python
def cellular_automaton(grid, steps=10):
    """
    简单元胞自动机示例（类似生命游戏）
    """
    rows, cols = grid.shape
    
    for _ in range(steps):
        new_grid = grid.copy()
        for i in range(1, rows-1):
            for j in range(1, cols-1):
                # 统计邻居
                neighbors = (grid[i-1:i+2, j-1:j+2].sum() - grid[i,j])
                
                # 规则：邻居太少或太多则"死亡"
                if grid[i,j] == 1:
                    if neighbors < 2 or neighbors > 3:
                        new_grid[i,j] = 0
                else:
                    if neighbors == 3:
                        new_grid[i,j] = 1
        
        grid = new_grid
    
    return grid
```

### 📝 论文句式

> A Cellular Automaton model is developed to simulate the spatial spread of the phenomenon. The local rules are defined based on neighborhood states, and the simulation reveals emergent patterns consistent with observed data.

---

## ✅ 美赛建模技巧

1. **模型不要太复杂**：复杂模型容易止步M奖
2. **多做检验**：灵敏度分析、稳定性分析越多越好
3. **可视化重要**：图表要精美、清晰、专业
4. **假设要充分**：说明合理性和必要性
5. **创新可容错**：有创新即使有小错误也可能获奖

---


> 📝 **最后提醒**：
> 
> 这份手册是"速查工具"，不是"万能答案"。
> 
> 真正的建模能力来自于：**多做题 + 多思考 + 多总结**。
> 
> 祝你比赛顺利！🎉
