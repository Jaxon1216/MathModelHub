# 问题四建模分析 —— 写作指南

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

问题四要求：
1. 建立模型对目标单词进行**难度分类**（简单/中等/困难）
2. 识别与难度相关的**单词属性**
3. 用模型判断「EERIE」的难度
4. 讨论**模型准确性**

### 1.2 难度定义

基于平均猜测次数定义难度等级：

| 难度等级 | 平均猜测次数 | 占比 |
|----------|-------------|------|
| Easy | < 4.0 | 8.9% |
| Medium | 4.0 ~ 4.5 | 45.1% |
| Hard | >= 4.5 | 46.0% |

### 1.3 建模思路

采用**多分类模型**方法：

```
特征提取 → 分类模型训练 → 交叉验证 → EERIE预测
```

**核心思想**：
- **输入**：单词属性特征（10维）
- **输出**：难度类别（Easy/Medium/Hard）
- **评估**：准确率、F1分数、混淆矩阵

---

## 二、模型介绍与公式

### 2.1 随机森林分类器

随机森林通过集成多棵决策树进行投票分类：

$$\hat{y} = \text{mode}\{h_1(\mathbf{x}), h_2(\mathbf{x}), ..., h_B(\mathbf{x})\}$$

其中：
- $B = 200$：决策树数量
- $h_b(\mathbf{x})$：第 $b$ 棵决策树的预测
- mode：众数（投票最多的类别）

### 2.2 评估指标

**准确率（Accuracy）**：
$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$

**精确率（Precision）**：
$$\text{Precision} = \frac{TP}{TP + FP}$$

**召回率（Recall）**：
$$\text{Recall} = \frac{TP}{TP + FN}$$

**F1分数**：
$$F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$

### 2.3 特征重要性

随机森林通过基尼不纯度（Gini Impurity）计算特征重要性：

$$\text{Importance}(X_j) = \sum_{t \in T_j} \frac{n_t}{N} \Delta G(t)$$

---

## 三、结果解读

### 3.1 模型性能

| 模型 | 交叉验证准确率 | 测试准确率 |
|------|---------------|-----------|
| Logistic Regression | 63.4% | 69.4% |
| Random Forest | 67.9% | **66.7%** |
| Gradient Boosting | 65.5% | 70.8% |
| SVM | 63.0% | 65.3% |

**选择Random Forest**：虽然测试准确率略低，但交叉验证表现更稳定。

### 3.2 与难度相关的单词属性

| 排名 | 特征 | 重要性 | 解读 |
|------|------|--------|------|
| 1 | avg_letter_freq | 0.229 | 平均字母频率越低，难度越高 |
| 2 | min_letter_freq | 0.204 | 最稀有字母频率越低，难度越高 |
| 3 | first_letter_freq | 0.141 | 首字母频率影响首次猜测 |

### 3.3 EERIE难度判断

| 预测结果 | 概率 |
|----------|------|
| Easy | 18.4% |
| **Medium** | **53.2%** |
| Hard | 28.4% |

**结论**：EERIE被分类为「Medium」难度，置信度53.2%。

### 3.4 EERIE特征分析

| 特征 | EERIE值 | 解读 |
|------|---------|------|
| 元音数量 | 4 | 极高（正常1-2） |
| 重复字母 | 2 | 较高（3个E） |
| 元音占比 | 80% | 极高 |
| 平均字母频率 | 10.21 | 较高（E高频） |

**为什么EERIE是Medium而非Hard？**
- E是最高频字母，玩家容易猜到
- 虽然有重复，但重复的是高频字母
- 整体平均字母频率较高

---

## 四、论文撰写建议

### 4.1 建议章节结构

```
4.4 Problem 4: Word Difficulty Classification
    4.4.1 Difficulty Definition
    4.4.2 Feature Analysis
    4.4.3 Classification Model
    4.4.4 Feature Importance
    4.4.5 EERIE Difficulty Prediction
    4.4.6 Model Accuracy Discussion
```

### 4.2 关键公式LaTeX格式

```latex
% 随机森林投票
\hat{y} = \text{mode}\{h_1(\mathbf{x}), h_2(\mathbf{x}), ..., h_B(\mathbf{x})\}

% 准确率
\text{Accuracy} = \frac{\text{TP} + \text{TN}}{\text{TP} + \text{TN} + \text{FP} + \text{FN}}

% F1分数
F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}
```

### 4.3 常用英文表达

**描述分类模型**：
- "We employ a Random Forest classifier with 200 decision trees to categorize words into three difficulty levels: Easy, Medium, and Hard."
- "The model achieves an overall accuracy of 66.7% on the test set, with a weighted F1 score of 0.66."

**描述特征重要性**：
- "Feature importance analysis reveals that average letter frequency (0.229) is the most predictive attribute for word difficulty."
- "Words containing rare letters tend to be more difficult, as players have fewer common starting guesses."

**描述EERIE预测**：
- "The model classifies EERIE as Medium difficulty with 53.2% confidence."
- "Despite having 3 repeated E's, EERIE is not classified as Hard because E is the most common letter in English."

### 4.4 模型准确性讨论模板

```latex
\textbf{Model Accuracy Discussion}

The classification model achieves an overall accuracy of 66.7\%, which is 
reasonably good given the inherent subjectivity of word difficulty. Several 
factors limit the model's accuracy:

\begin{enumerate}
    \item \textbf{Sample size}: Only 359 words in the training data
    \item \textbf{Class imbalance}: Easy class significantly underrepresented
    \item \textbf{Feature coverage}: Semantic features not included
    \item \textbf{Difficulty definition}: Based solely on average tries
\end{enumerate}

Potential improvements include incorporating word frequency data and 
semantic complexity measures.
```

---

## 五、图片列表与插入位置

| 编号 | 文件名 | 内容 | 建议插入章节 |
|------|--------|------|-------------|
| 图1 | fig1_difficulty_distribution.pdf | 难度分布（3合1） | 4.4.1 数据描述 |
| 图2 | fig2_feature_by_difficulty.pdf | 特征与难度关系（4合1箱线图） | 4.4.2 特征分析 |
| 图3 | fig3_model_comparison.pdf | 模型准确率对比 | 4.4.3 模型选择 |
| 图4 | fig4_confusion_matrix.pdf | 混淆矩阵 | 4.4.3 模型评估 |
| 图5 | fig5_feature_importance.pdf | 特征重要性 | 4.4.4 特征重要性 |
| 图6 | fig6_eerie_comparison.pdf | EERIE与历史单词对比 | 4.4.5 EERIE分析 |
| 图7 | fig7_eerie_probability.pdf | EERIE预测概率 | 4.4.5 EERIE分析 |

### 图片引用示例

```latex
Figure \ref{fig:confusion} shows the confusion matrix for our Random Forest 
classifier. The model performs best on the Medium class (highest true positive 
rate), while the Easy class has lower recall due to its small sample size.

The feature importance analysis (Fig. \ref{fig:importance}) identifies 
average letter frequency as the most predictive attribute, followed by 
minimum letter frequency and first letter frequency.
```
