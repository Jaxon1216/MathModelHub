# 问题二 —— 资料手工作指南

> 本文档面向资料手Person2，指导完成思路图绘制和参考文献查找工作。

## 一、需要绘制的思路图

### 思路图1：投票方式比较流程

```
┌─────────────────────────────────────────────────────────────┐
│              Voting Method Comparison                        │
└─────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┴─────────────────┐
            ▼                                   ▼
┌───────────────────────┐           ┌───────────────────────┐
│    Rank-Based Method  │           │  Percentage-Based     │
│    (S1-2, S28-34)     │           │  Method (S3-27)       │
│  Combined = R_judge   │           │  Combined = P_judge   │
│           + R_fan     │           │           + P_fan     │
└───────────────────────┘           └───────────────────────┘
            │                                   │
            └─────────────────┬─────────────────┘
                              ▼
              ┌───────────────────────────────┐
              │   Compare Elimination Results │
              │   + Analyze Controversial     │
              │     Contestants               │
              └───────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │   Tiebreaker Rule Simulation  │
              │   (Judge chooses from         │
              │    bottom 2)                  │
              └───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Output: Method Recommendation + Impact Analysis            │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、参考文献检索指南

### 2.1 检索关键词

| 领域 | 英文关键词 |
|------|------------|
| 投票系统 | voting systems, electoral methods, Borda count |
| 排名聚合 | rank aggregation, social choice theory |
| 反事实分析 | counterfactual analysis, what-if analysis |
| 真人秀研究 | reality TV, talent show voting |

### 2.2 推荐参考文献

1. Arrow, K. J. (1950). A difficulty in the concept of social welfare. *Journal of Political Economy*, 58(4), 328-346.
   - **相关性**：社会选择理论经典，投票悖论

2. Kemeny, J. G. (1959). Mathematics without numbers. *Daedalus*, 88(4), 577-591.
   - **相关性**：排名聚合方法

---

## 三、图片文件交付清单

### Coder已导出的图片

| 文件名 | 内容 | 状态 |
|--------|------|------|
| `fig1_method_comparison.pdf` | 方法比较 | ✅ |
| `fig2_controversial_methods.pdf` | 争议选手分析 | ✅ |
| `fig3_tiebreaker_analysis.pdf` | 评委打破平局 | ✅ |

### 数据文件

| 文件名 | 内容 |
|--------|------|
| `method_comparison.csv` | 方法差异详细数据 |
| `controversial_analysis.csv` | 争议选手分析 |
| `tiebreaker_analysis.csv` | 打破平局模拟结果 |
