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

### 1.1 问题本质

设计一个新的投票系统，需要平衡多个目标：
1. **专业性**：尊重评委的专业判断
2. **参与性**：鼓励观众积极投票
3. **公平性**：避免纯靠粉丝晋级的争议
4. **观赏性**：保持比赛悬念和娱乐性

### 1.2 设计理念

**Dynamic Weighted Voting System (DWVS)**

核心思想：
- **初期**：粉丝权重高，增加节目热度和观众参与
- **后期**：评委权重高，确保冠军具有真正的舞蹈实力
- **门槛**：防止技术太差的选手纯靠粉丝投票晋级

---

## 二、模型介绍与公式

### 2.1 动态权重公式

$$\alpha(w) = \min(0.4 + 0.04w, 0.8)$$

其中：
- $w$：当前周数
- $\alpha$：评委权重
- $1-\alpha$：粉丝权重

**权重变化**：
| 周次 | 评委权重 | 粉丝权重 |
|------|---------|---------|
| Week 1 | 44% | 56% |
| Week 5 | 60% | 40% |
| Week 10+ | 80% | 20% |

### 2.2 综合得分计算

$$C_i = \alpha(w) \cdot P_i^{judge} + (1-\alpha(w)) \cdot P_i^{fan} \cdot T_i$$

其中 $T_i$ 是门槛调整因子：

$$T_i = \begin{cases} 0.3 & \text{if } P_i^{judge} < 0.5 \cdot \bar{P}^{judge} \\ 1.0 & \text{otherwise} \end{cases}$$

### 2.3 平局处理规则

当两位选手综合得分差距小于5%时：
$$|C_i - C_j| < 0.05 \cdot \max(C_i, C_j) \Rightarrow \text{Judge Tiebreaker}$$

---

## 三、结果解读

### 3.1 新系统设计特点

| 特点 | 描述 | 作用 |
|------|------|------|
| 动态权重 | 评委权重从44%增至80% | 初期吸引观众，后期保证专业性 |
| 门槛约束 | 评委得分过低时粉丝投票打折 | 防止争议选手过度晋级 |
| 平局处理 | 综合得分接近时评委决定 | 确保专业性最终决定权 |
| 透明度 | 实时公布评委得分和排名 | 增加公信力 |

### 3.2 争议选手影响分析

| 选手 | 原名次 | 预期新名次 | 变化 | 影响 |
|------|--------|-----------|------|------|
| Jerry Rice | 2 | 2.5 | +0.5 | 名次下降 |
| Billy Ray Cyrus | 5 | 5.3 | +0.3 | 名次下降 |
| Bristol Palin | 3 | 3.8 | +0.8 | 名次下降 |
| Bobby Bones | 1 | 2.2 | +1.2 | 名次下降 |

**分析**：
- 新系统会使争议选手的名次下降（正值表示名次数字变大=排名变差）
- Bobby Bones受影响最大（评委排名7，但夺冠）→ 新系统下预计第2名
- 体现了新系统对「评委-粉丝不一致」情况的调整
- 所有争议选手均会因门槛机制和动态权重而名次下滑

### 3.3 系统对比评分

| 系统 | 平衡性 | 专业性 | 参与性 | 公平性 |
|------|--------|--------|--------|--------|
| 当前系统 | 4 | 3 | 4 | 3 |
| **新动态系统** | **5** | **4** | **4** | **4** |
| 纯评委 | 2 | 5 | 1 | 4 |
| 纯粉丝 | 2 | 1 | 5 | 2 |

---

## 四、论文撰写建议

### 4.1 建议章节结构

```
6. New Voting System Design
   6.1 Design Objectives and Constraints
   6.2 Dynamic Weighted Voting System (DWVS)
   6.3 Threshold Mechanism
   6.4 Tiebreaker Rules
   6.5 Impact Analysis on Controversial Cases
   6.6 Recommendations for Implementation
```

### 4.2 关键公式LaTeX

```latex
% 动态权重
\alpha(w) = \min(0.4 + 0.04w, 0.8)

% 综合得分
C_i = \alpha(w) \cdot P_i^{judge} + (1-\alpha(w)) \cdot P_i^{fan} \cdot T_i

% 门槛因子
T_i = \begin{cases} 
0.3 & \text{if } P_i^{judge} < 0.5 \cdot \bar{P}^{judge} \\ 
1.0 & \text{otherwise} 
\end{cases}
```

### 4.3 常用英文表达

- "We propose a Dynamic Weighted Voting System (DWVS) that balances professional judgment with audience engagement."
- "The dynamic weight function gradually shifts emphasis from fan participation to judge expertise as the competition progresses."
- "The threshold mechanism prevents contestants with significantly below-average dance skills from advancing purely on fan support."
- "Under the new system, controversial contestants such as Bobby Bones would see an expected placement drop of 1.2 positions."

---

## 五、图片列表与插入位置

| 编号 | 文件名 | 内容 | 建议插入章节 |
|------|--------|------|-------------|
| 1 | fig1_parameter_sensitivity.pdf | α参数敏感性分析 | 6.2 |
| 2 | fig2_dynamic_alpha.pdf | 动态权重随周变化 | 6.2 |
| 3 | fig2_system_comparison.pdf | 系统对比热力图 | 6.1 |
| 4 | fig3_controversial_impact.pdf | 争议选手影响 | 6.5 |
| 5 | fig4_weight_composition.pdf | 权重组成堆叠图 | 6.2 |

### 图片引用示例

```latex
As shown in Fig. 5, the proposed Dynamic Weighted Voting System (DWVS) 
gradually shifts the weight distribution from 44% judge / 56% fan in 
Week 1 to 80% judge / 20% fan by Week 10, ensuring that the final 
winner possesses genuine dancing ability while maintaining audience 
engagement throughout the competition.
```

### 系统推荐总结

> **Recommendation**: We recommend ABC to adopt the Dynamic Weighted Voting 
> System (DWVS) for future seasons of DWTS. This system:
> 1. Maintains high audience engagement in early rounds (56% fan weight)
> 2. Ensures professional winners in finals (80% judge weight)
> 3. Prevents skill-deficient contestants from unfair advancement
> 4. Provides transparent and explainable scoring rules
