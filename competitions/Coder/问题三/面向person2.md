# 问题三 —— 资料手工作指南

> 本文档面向资料手Person2，指导完成思路图绘制和参考文献查找工作。

## 一、需要绘制的思路图

### 1.1 影响因素分析流程图

```
┌─────────────────────────────────────────────────────────────────┐
│              Factor Analysis Framework                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    INPUT FEATURES                        │    │
│  │    • Celebrity Age                                       │    │
│  │    • Celebrity Industry                                  │    │
│  │    • Professional Dancer                                 │    │
│  │    • Home State (US/Non-US)                             │    │
│  └─────────────────────────────────────────────────────────┘    │
│                          │                                       │
│            ┌─────────────┴─────────────┐                        │
│            ▼                           ▼                        │
│  ┌──────────────────┐       ┌──────────────────┐               │
│  │  JUDGE SCORE     │       │  FAN VOTE        │               │
│  │  Analysis        │       │  Analysis        │               │
│  ├──────────────────┤       ├──────────────────┤               │
│  │ • Correlation    │       │ • Correlation    │               │
│  │ • Ridge Regress. │       │ • Ridge Regress. │               │
│  │ • Random Forest  │       │ • Random Forest  │               │
│  │ • ANOVA          │       │ • ANOVA          │               │
│  │ R² = 0.128       │       │ R² = 0.047       │               │
│  └──────────────────┘       └──────────────────┘               │
│            │                           │                        │
│            └─────────────┬─────────────┘                        │
│                          ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    KEY FINDINGS                          │    │
│  │    • Age: r = -0.424 (Judge) vs -0.338 (Fan)            │    │
│  │    • Pro Dancer: F = 3.62*** (Judge) vs 1.60* (Fan)     │    │
│  │    • Features explain more Judge variance than Fan      │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、参考文献检索指南

### 2.1 检索关键词

| 主题 | 推荐关键词 |
|------|------------|
| 影响因素分析 | factor analysis, regression analysis |
| 选秀节目 | talent show, reality competition |
| 年龄效应 | age effect, aging, performance |
| 舞蹈表演 | dance performance, ballroom dance |
| 观众投票 | audience voting, viewer preference |

### 2.2 推荐数据库

1. **Google Scholar**: 综合搜索
2. **JSTOR**: 社会科学
3. **PubMed**: 年龄与运动表现

---

## 三、图片文件交付清单

| 文件名 | 内容 | 状态 |
|--------|------|------|
| fig1_industry_impact.pdf | 行业影响分析 | ✅ 已完成 |
| fig2_age_impact.pdf | 年龄影响散点图 | ✅ 已完成 |
| fig3_feature_importance.pdf | 特征重要性对比 | ✅ 已完成 |
| fig4_pro_dancer_impact.pdf | 专业舞者效应 | ✅ 已完成 |

---

## 四、关键数据速查

| 指标 | 数值 |
|------|------|
| 分析选手数 | 421 |
| 年龄vs评委 | r = -0.424 |
| 年龄vs观众 | r = -0.338 |
| 评委模型R² | 0.128 |
| 观众模型R² | 0.047 |
| 专业舞者F值(评委) | 3.62 |
| 专业舞者F值(观众) | 1.60 |
