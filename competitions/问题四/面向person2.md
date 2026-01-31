# 问题四 —— 资料手工作指南

> 本文档面向资料手Person2，指导完成思路图绘制和参考文献查找工作。

## 一、需要绘制的思路图

### 思路图1：新投票系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│         Dynamic Weighted Voting System (DWVS)               │
└─────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┴─────────────────┐
            ▼                                   ▼
┌───────────────────────┐           ┌───────────────────────┐
│    Judge Score        │           │    Fan Vote           │
│    (Professional)     │           │    (Popularity)       │
└───────────────────────┘           └───────────────────────┘
            │                                   │
            │         ┌─────────────┐           │
            └────────►│  Dynamic    │◄──────────┘
                      │  Weight α(w)│
                      │  = 0.4+0.04w│
                      └─────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │   Threshold Check             │
              │   If judge_pct < 50% mean:    │
              │   → fan_weight = 0.3          │
              └───────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │   Combined Score              │
              │   C = α×Judge + (1-α)×Fan×T   │
              └───────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │   Tiebreaker (if diff < 5%)   │
              │   → Judge Decision            │
              └───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│         Final Ranking + Elimination Decision                 │
└─────────────────────────────────────────────────────────────┘
```

**绘制要点**：
- 强调动态权重和门槛机制的核心作用
- 使用不同颜色区分评委（蓝色）和粉丝（红色）路径
- 在关键节点标注公式

---

## 二、参考文献检索指南

### 2.1 检索关键词

| 领域 | 英文关键词 |
|------|------------|
| 投票系统设计 | voting system design, electoral mechanism |
| 多目标优化 | multi-objective optimization, Pareto efficiency |
| 博弈论 | game theory, mechanism design |
| 公平性 | fairness, equity in competitions |

### 2.2 推荐参考文献

1. Myerson, R. B. (1981). Optimal auction design. *Mathematics of Operations Research*, 6(1), 58-73.
   - **相关性**：机制设计经典论文

2. Balinski, M., & Laraki, R. (2010). *Majority judgment: measuring, ranking, and electing*. MIT Press.
   - **相关性**：投票系统设计

---

## 三、图片文件交付清单

| 文件名 | 内容 | 状态 |
|--------|------|------|
| `fig1_parameter_sensitivity.pdf` | 参数敏感性 | ✅ |
| `fig2_dynamic_alpha.pdf` | 动态权重 | ✅ |
| `fig2_system_comparison.pdf` | 系统对比 | ✅ |
| `fig3_controversial_impact.pdf` | 争议选手 | ✅ |
| `fig4_weight_composition.pdf` | 权重组成 | ✅ |

### 需要Person2绘制的图

| 图名 | 类型 | 说明 |
|------|------|------|
| DWVS系统架构图 | 流程图 | 见上方ASCII示意 |
