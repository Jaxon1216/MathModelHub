# 问题一 —— 资料手工作指南

> 本文档面向资料手Person2，指导完成思路图绘制和参考文献查找工作。建模思路在面向person1的文件里自行查阅。

## 一、需要绘制的思路图

### 1.1 投票估算流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Fan Vote Estimation Framework                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────────┐       │
│  │  Input   │ ──→│  Processing  │ ──→│     Output       │       │
│  └──────────┘    └──────────────┘    └──────────────────┘       │
│       │                │                      │                  │
│       ▼                ▼                      ▼                  │
│  ┌─────────┐    ┌─────────────────┐   ┌─────────────────┐       │
│  │ Judge   │    │ Check Voting    │   │ Estimated Vote  │       │
│  │ Scores  │    │ Method          │   │ Proportions     │       │
│  │   +     │    │    ↓            │   │      +          │       │
│  │Elimination│  │ ┌────────────┐  │   │ Uncertainty     │       │
│  │ Results │    │ │ Rank-based │  │   │ Metrics         │       │
│  └─────────┘    │ │(S1-2,28-34)│  │   └─────────────────┘       │
│                 │ └────────────┘  │                              │
│                 │    ↓            │                              │
│                 │ ┌────────────┐  │                              │
│                 │ │ Percentage │  │                              │
│                 │ │  (S3-27)   │  │                              │
│                 │ └────────────┘  │                              │
│                 │    ↓            │                              │
│                 │ ┌────────────┐  │                              │
│                 │ │Constrained │  │                              │
│                 │ │Optimization│  │                              │
│                 │ └────────────┘  │                              │
│                 └─────────────────┘                              │
└─────────────────────────────────────────────────────────────────┘
```

**绘图要点**：
- 清晰展示输入（评委得分+淘汰结果）→ 处理（两种投票方式的约束优化）→ 输出（投票比例+确定性）
- 突出两种投票方式的分支
- 使用浅蓝色块标注「Constrained Optimization」核心方法

---

## 二、参考文献检索指南

### 2.1 检索关键词

| 主题 | 推荐关键词 |
|------|------------|
| 反向推断 | inverse problem, backward inference, parameter estimation |
| 约束优化 | constrained optimization, quadratic programming |
| 投票系统 | voting system, scoring rule, Borda count |
| 不确定性量化 | uncertainty quantification, Bootstrap, confidence interval |
| 选秀节目研究 | talent show, reality TV voting, audience engagement |

### 2.2 推荐数据库

1. **Google Scholar**: 综合搜索
2. **IEEE Xplore**: 优化算法
3. **JSTOR**: 社会科学/投票理论
4. **arXiv**: 预印本/最新研究

### 2.3 推荐文献方向

1. **投票理论**
   - Borda count / plurality voting 相关论文
   - Social choice theory

2. **约束优化**
   - Sequential Quadratic Programming (SQP)
   - Interior point methods

3. **选秀节目研究**（可选）
   - Reality TV audience behavior
   - Fan voting patterns in competitions

### 2.4 引用格式示例（APA）

```
Author, A. A., & Author, B. B. (Year). Title of the article. 
Journal Name, Volume(Issue), Page numbers. https://doi.org/xxxxx
```

---

## 三、图片文件交付清单

### 3.1 Coder已导出的图片

| 文件名 | 内容 | 状态 |
|--------|------|------|
| fig1_consistency_analysis.pdf | 一致性分析（按赛季+按选手数） | ✅ 已完成 |
| fig2_accuracy_by_method.pdf | 两种方式准确率对比 | ✅ 已完成 |
| fig3_certainty_distribution.pdf | 确定性指标分布 | ✅ 已完成 |
| fig4_vote_score_relationship.pdf | 投票-得分散点图 | ✅ 已完成 |
| fig5_controversial_analysis.pdf | 争议选手分析 | ✅ 已完成 |

### 3.2 需要Person2绘制的图

| 图名 | 说明 | 优先级 |
|------|------|--------|
| 投票估算流程图 | 展示整体建模流程 | 高 |

**流程图绘图工具推荐**：Draw.io, Visio, Lucidchart

---

## 四、关键数据速查（供校对）

| 指标 | 数值 |
|------|------|
| 总体一致性准确率 | 93.9% |
| 百分比制准确率 | 98.5% |
| 排名制准确率 | 80.3% |
| 平均确定性 | 0.273 |
| 投票-得分相关系数 | 0.371 |
| Bobby Bones排名差距 | +0.7 |

---

## 五、工作优先级

1. **高优先级**
   - 检查已导出图片是否清晰、标签正确
   - 绘制投票估算流程图

2. **中优先级**
   - 检索1-2篇关于voting system的参考文献
   - 检索1篇关于constrained optimization的参考文献

3. **低优先级**
   - 检索reality TV相关研究（如有时间）
