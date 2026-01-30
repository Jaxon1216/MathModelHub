# 问题一 —— 资料手工作指南

> 本文档面向资料手Person2，指导完成思路图绘制和参考文献查找工作。建模思路在面向person1的文件里自行查阅。

## 一、需要绘制的思路图

### 思路图1：粉丝投票估算流程图

```
┌─────────────────────────────────────────────────────────────┐
│                    Fan Vote Estimation                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Input: Judge Scores (known) + Elimination Results (known)  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │   Softmax Voting Model        │
              │   v_i = softmax(s_i × (1+α))  │
              └───────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │   Constrained Optimization    │
              │   min Σα²                     │
              │   s.t. eliminated = lowest    │
              └───────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │   Bootstrap Uncertainty       │
              │   B = 100 iterations          │
              └───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Output: Estimated Vote Shares + Consistency + Certainty    │
└─────────────────────────────────────────────────────────────┘
```

**绘制要点**：
- 使用draw.io或类似工具
- 颜色方案：输入框用浅灰，核心方法用浅蓝高亮
- 保持简洁学术风格

---

## 二、参考文献检索指南

### 2.1 检索关键词

| 领域 | 英文关键词 | 中文关键词 |
|------|------------|------------|
| 投票估算 | vote estimation, polling prediction, Bradley-Terry model | 投票预测，民意估算 |
| 约束优化 | constrained optimization, inverse problem | 约束优化，逆问题 |
| 选秀节目 | reality TV voting, talent competition | 选秀节目投票 |
| Softmax模型 | softmax regression, multinomial logit | 多项Logit模型 |

### 2.2 推荐数据库

1. **Google Scholar** - 学术文献综合搜索
2. **SSRN** - 社会科学预印本
3. **arXiv** - 统计学/机器学习预印本

### 2.3 推荐参考文献

1. Bradley, R. A., & Terry, M. E. (1952). Rank analysis of incomplete block designs: I. The method of paired comparisons. *Biometrika*, 39(3/4), 324-345.
   - **相关性**：配对比较模型，投票排名的经典方法

2. Plackett, R. L. (1975). The analysis of permutations. *Journal of the Royal Statistical Society: Series C*, 24(2), 193-202.
   - **相关性**：排名数据分析

3. Luce, R. D. (1959). Individual choice behavior: A theoretical analysis. *Wiley*.
   - **相关性**：选择行为理论，Softmax模型理论基础

### 2.4 引用格式（APA）

```
Author, A. A., & Author, B. B. (Year). Title of article. Journal Name, Volume(Issue), Pages. https://doi.org/xxx
```

---

## 三、图片文件交付清单

### Coder已导出的图片

| 文件名 | 内容描述 | 状态 |
|--------|----------|------|
| `fig1_consistency_analysis.pdf` | 一致性分析（按季、按投票方式） | ✅ 已完成 |
| `fig2_uncertainty_analysis.pdf` | 不确定性分析（分布图、相关性） | ✅ 已完成 |
| `fig3_controversial_analysis.pdf` | 争议选手分析（4个子图） | ✅ 已完成 |
| `fig4_vote_score_relationship.pdf` | 投票与得分关系、人气因子分布 | ✅ 已完成 |
| `fig5_certainty_distribution.pdf` | 确定性按季/周分布 | ✅ 已完成 |

### 需要Person2绘制的图

| 图名 | 类型 | 说明 |
|------|------|------|
| 投票估算流程图 | 流程图 | 见上方ASCII示意，用draw.io绘制 |

---

## 四、数据文件说明

| 文件名 | 内容 | 用途 |
|--------|------|------|
| `vote_estimates.csv` | 所有选手-周的投票估算 | 后续问题分析 |
| `verification_results.csv` | 一致性验证结果 | 论文数据支撑 |
| `certainty_metrics.csv` | 确定性指标 | 不确定性分析 |
| `results_summary.csv` | 关键结果汇总 | 快速引用 |
