# 问题四建模分析 —— 写作指南

> 本文档面向写作手Person1，帮助理解新投票系统的设计思路和优势。

## 一、问题分析

### 1.1 问题核心

问题四要求设计一个**更公平**或**更有吸引力**的投票结合体系。

### 1.2 设计原则

1. **公平性**: 平衡评委与观众意见
2. **透明性**: 规则简单易懂
3. **激励性**: 鼓励进步
4. **稳定性**: 减少争议

---

## 二、新系统设计

### 2.1 动态加权投票系统 (DWVS)

**核心公式**：

$$S_{final,i} = \alpha \cdot P_{judge,i} + (1-\alpha) \cdot P_{fan,i} + \beta \cdot I_i$$

其中：
- $P_{judge,i} = \frac{J_i}{\sum_j J_j}$：评委得分百分比
- $P_{fan,i} = \frac{V_i}{\sum_j V_j}$：观众投票百分比
- $I_i$：进步指数
- $\alpha$：评委权重
- $\beta$：进步奖励系数

### 2.2 进步指数

$$I_i = \max\left(0, \frac{Score_{week} - \overline{Score}_{prev}}{Score_{max}}\right)$$

- 只奖励进步，不惩罚退步
- 鼓励选手持续提升

### 2.3 最优参数

经参数敏感性分析：
- **最佳 α = 0.3**
- **最佳 β = 0.0**

---

## 三、核心结果

### 3.1 系统比较（关键发现！）

| 系统 | 与实际一致率 |
|------|-------------|
| 排名制 | 64.4% |
| 百分比制 | 67.0% |
| **新系统 (α=0.3)** | **76.1%** |

**新系统提升约9-12个百分点！**

### 3.2 Alpha参数分析（重要发现！）

| Alpha范围 | 含义 | 平均一致率 |
|-----------|------|-----------|
| α ≤ 0.3 | 观众主导 | **73.0%** |
| 0.3 < α ≤ 0.7 | 平衡 | 61.9% |
| α > 0.7 | 评委主导 | 39.6% |

**关键发现**：
- α在0.05-0.45范围内，一致率稳定在76.1%（平台期）
- α > 0.5时一致率急剧下降至~40%
- 这说明**节目实际结果更偏向观众投票**

### 3.3 推荐权重

**从公平性角度推荐 α = 0.5**：
| 成分 | 权重 |
|------|------|
| 评委得分 | 50% |
| 观众投票 | 50% |

**理由**：虽然低α能更好拟合实际结果，但从公平性考虑，评委专业意见和观众民意应该各占一半。

### 3.3 争议选手影响

| 选手 | 排名制 | 百分比制 | 新系统 |
|------|--------|----------|--------|
| Jerry Rice (S2) | 3次 | 3次 | 3次 |
| Billy Ray Cyrus (S4) | 1次 | 1次 | 1次 |
| Bristol Palin (S11) | 0次 | 0次 | 0次 |
| Bobby Bones (S27) | 0次 | 0次 | 0次 |

**结论**：新系统不会改变争议选手的命运——他们的高观众支持在任何系统下都足以保护他们。

---

## 四、论文撰写建议

### 4.1 建议章节结构

```
6. Task 4: New Voting System Design
   6.1 Design Principles
   6.2 Proposed System: DWVS
       6.2.1 Mathematical Formulation
       6.2.2 Parameter Optimization
   6.3 Comparison with Existing Systems
   6.4 Analysis of Controversial Cases
   6.5 Recommendations
```

### 4.2 关键公式LaTeX

```latex
% 新系统公式
S_{final,i} = \alpha \cdot P_{judge,i} + (1-\alpha) \cdot P_{fan,i} + \beta \cdot I_i

% 评委百分比
P_{judge,i} = \frac{J_i}{\sum_{j=1}^{n} J_j}

% 进步指数
I_i = \max\left(0, \frac{S_{week} - \bar{S}_{prev}}{S_{max}}\right)
```

### 4.3 推荐理由要点

1. **更高一致性**：76.1% vs 64-67%
2. **数学透明**：公式简单，观众易懂
3. **保留专业性**：评委仍有30%权重
4. **反映现实**：优化参数显示节目实际更重观众

### 4.4 常用英文表达

| 中文 | 英文 |
|------|------|
| 动态加权 | dynamic weighting |
| 进步指数 | improvement index |
| 参数敏感性 | parameter sensitivity |
| 一致率 | consistency rate |

---

## 五、图片列表

| 编号 | 文件名 | 内容 | 建议章节 |
|------|--------|------|---------|
| 1 | fig1_parameter_sensitivity.pdf | 参数敏感性热力图 | 6.2.2 |
| 2 | fig2_system_comparison.pdf | 三种系统一致率对比 | 6.3 |
| 3 | fig3_controversial_impact.pdf | 争议选手三系统对比 | 6.4 |
| 4 | fig4_weight_composition.pdf | 权重构成饼图 | 6.2/6.5 |

---

## 六、数据引用速查

```
- 拟合最优alpha: 0.05-0.45 (平台期)
- 推荐alpha: 0.5 (公平性考虑)
- 排名制一致率: 64.4%
- 百分比制一致率: 67.0%
- 新系统一致率(α=0.3): 76.1%
- 新系统一致率(α=0.5): 74.6%
- 观众主导(α≤0.3)平均一致率: 73.0%
- 评委主导(α>0.7)平均一致率: 39.6%
```

## 七、关于"公平性"的讨论

**核心发现**：节目实际结果更偏向观众投票（低α一致率更高）。

**公平性vs拟合度的权衡**：
- 如果目标是"还原实际"，α=0.3最佳
- 如果目标是"重新设计公平系统"，α=0.5更合理

**建议论文写法**：
> Our analysis reveals that the actual show results favor fan votes over judge scores (optimal α ≈ 0.3). However, from a fairness perspective, we recommend a balanced system with α = 0.5, giving equal weight to professional judgment and audience preference.

---

## 七、备忘录要点

为报告最后的1-2页备忘录，建议包含：

1. **核心发现**：新系统一致率提升9-12%
2. **推荐方案**：采用DWVS，α=0.3
3. **关于争议**：争议源于观众-评委分歧本身，而非投票方式
4. **实施建议**：可在新赛季试点新系统
