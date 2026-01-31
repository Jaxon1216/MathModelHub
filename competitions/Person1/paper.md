# Dancing with Data: A Mathematical Framework for Fan Vote Estimation and Voting System Optimization in DWTS

**MCM 2026 Problem C**

---

## Abstract

Dancing with the Stars (DWTS) combines professional judge scores with audience votes to determine weekly eliminations, yet the exact fan vote totals remain confidential. This paper develops a comprehensive mathematical framework to estimate fan votes, compare voting methods, analyze influencing factors, and design an improved voting system.

**For Problem 1**, we formulate fan vote estimation as a constrained optimization problem using a Softmax voting model. Stratified analysis reveals overall consistency of 80.7%: the rank-based method achieves 38.4% while the percentage-based method achieves 96.0%. Bootstrap resampling yields a certainty index of 0.995, demonstrating high estimation stability.

**For Problem 2**, we apply counterfactual analysis comparing rank-based and percentage-based methods across all 34 seasons. The methods produce identical elimination decisions in 95.5% of cases, with the judge tiebreaker rule changing outcomes in 3.9% of weeks. ANOVA testing shows industry affects judge scores more strongly (F=8.81, p<0.0001) than fan votes (F=2.14, p=0.003).

**For Problem 3**, we employ ANOVA, regression, and Random Forest to quantify factor impacts. Judge scores account for 87.6% of feature importance. Age correlates moderately with placement (r=0.433). The prediction model achieves R²=0.488, RMSE=2.69, MAE=2.09 positions under 5-fold CV. Cross-season validation demonstrates strong generalization: test R²=0.934, test RMSE=3.08.

**For Problem 4**, we propose a Dynamic Weighted Voting System (DWVS) optimized via grid search: base α=0.30, increment=0.04, yielding initial fan weight of 66% shifting to 26% by finals. Simulation across all 32 identified controversial contestants shows 78.1% would rank lower under DWVS, with average adjustment of +0.45 positions. Bobby Bones would place 2nd instead of 1st.

**Keywords**: Fan Vote Estimation; Constrained Optimization; Counterfactual Analysis; Dynamic Weighted Voting; Cross-Validation

---

## 1. Introduction

### 1.1 Problem Background

Dancing with the Stars (DWTS) represents a unique fusion of professional expertise and popular democracy. Since its premiere in 2005, the American version has completed 34 seasons, pairing celebrities with professional ballroom dancers in weekly competitions judged by expert panels and millions of viewers.

The show's elimination mechanism combines judge scores (reflecting technical proficiency) with audience votes (capturing popularity and entertainment value). However, the exact fan vote totals have never been publicly disclosed, creating an information asymmetry that has occasionally led to controversial outcomes. Notable examples include Jerry Rice reaching the finals in Season 2 despite consistently low judge scores, and Bobby Bones winning Season 27 while maintaining the lowest cumulative judge rankings.

### 1.2 Problem Restatement

We are tasked with developing analytical models to address four research questions: (1) estimate fan votes with consistency and certainty measures; (2) compare rank-based and percentage-based voting methods; (3) analyze the impact of professional dancers and celebrity characteristics; and (4) design an improved voting system.

### 1.3 Our Approach

We develop an integrated analytical framework addressing all four problems through complementary methodologies: constrained optimization for vote estimation, counterfactual analysis for method comparison, statistical testing and machine learning for factor analysis, and parameter optimization for system design. Cross-season validation ensures model generalizability.

---

## 2. Preparation for Modeling

### 2.1 Model Assumptions

**Assumption 1:** Fan votes are positively correlated with a contestant's underlying "popularity," which partially relates to their judge scores but includes additional factors not captured in the data.

**Assumption 2:** The voting rules announced by DWTS accurately reflect the actual elimination mechanism.

**Assumption 3:** Judge scores accurately reflect relative dancing ability on a given week, with quantifiable inter-judge variance (average std = 0.65 points).

### 2.2 Key Notations

| Symbol | Description |
|--------|-------------|
| $s_i$ | Total judge score for contestant $i$ |
| $v_i$ | Estimated fan vote share |
| $\alpha_i$ | Popularity factor |
| $R_i^{judge}$, $R_i^{fan}$ | Rankings (1 = highest) |
| $\alpha(w)$ | Dynamic weight at week $w$ |

### 2.3 Data Overview

The dataset contains 421 contestants across 34 seasons, yielding 2,777 observation records after preprocessing. Missing values (4th judge scores missing in 65-94% of cases) are non-random (caused by eliminations) and were retained rather than imputed.

---

## 3. Problem 1: Fan Vote Estimation Model

### 3.1 Model Construction

We develop a Softmax-based voting model:

$$v_i = \frac{\exp\left(\frac{s_i(1+\alpha_i)}{\bar{s}}\right)}{\sum_{j=1}^{n} \exp\left(\frac{s_j(1+\alpha_j)}{\bar{s}}\right)}$$

We minimize $\sum \alpha_i^2$ subject to the constraint that the eliminated contestant has the lowest combined score.

### 3.2 Stratified Consistency Analysis

**Key Finding:** Overall consistency reaches 80.7%, with percentage-based method (96.0%) dramatically outperforming rank-based (38.4%).

| Category | Consistent | Total | Rate |
|----------|------------|-------|------|
| **Overall** | 221 | 274 | 80.7% |
| **By Voting Method** | | | |
| Rank-based (S1-2, S28-34) | 28 | 73 | 38.4% |
| Percentage-based (S3-27) | 193 | 201 | 96.0% |

The dramatic difference reveals that continuous percentage space provides far more optimization freedom than discrete ranks. The 96% consistency under percentage method demonstrates our model successfully explains nearly all elimination outcomes in those seasons.

### 3.3 Uncertainty Quantification

Bootstrap resampling yields a certainty index of **0.995** with standard deviation 0.002, indicating highly stable estimates.

![Stratified Consistency](figures/imp1_stratified_consistency.pdf)
*Figure 1: Stratified consistency analysis by voting method, season phase, competition stage, and contestant count.*

---

## 4. Problem 2: Voting Method Comparison

### 4.1 Method Definitions

- **Rank-Based (S1-2, S28-34):** $C_i = R_i^{judge} + R_i^{fan}$ (highest = eliminated)
- **Percentage-Based (S3-27):** $C_i = P_i^{judge} + P_i^{fan}$ (lowest = eliminated)

### 4.2 Results

| Metric | Value |
|--------|-------|
| Method Agreement Rate | 95.5% |
| Disagreement Cases | 15 / 335 weeks |
| Tiebreaker Impact Rate | 3.9% |

![Method Comparison](figures/fig1_method_comparison.pdf)
*Figure 2: Comparison of voting methods across seasons.*

### 4.3 Recommendations

We recommend the **percentage-based method** with **judge tiebreaker rule**:
1. Percentage method provides nuanced differentiation
2. Tiebreaker ensures professional input (3.9% of cases)
3. This combination balances entertainment with integrity

---

## 5. Problem 3: Factor Impact Analysis

### 5.1 Industry Impact: Judge Scores vs. Fan Votes

**Key Finding:** Industry affects judge scores more strongly than fan votes.

| Dependent Variable | F-statistic | p-value |
|--------------------|-------------|---------|
| Judge Score | 8.81 | <0.0001 |
| Fan Vote Share | 2.14 | 0.003 |

This reveals that professional assessments may carry implicit biases while fan support is more uniformly distributed.

![Industry Impact](figures/imp3_industry_judge_vs_fan.pdf)
*Figure 3: Differential impact of industry on judge scores versus fan votes.*

### 5.2 Professional Dancer Effect

| Dancer | Avg. Placement | Wins | Partnerships |
|--------|----------------|------|--------------|
| Derek Hough | 2.94 | 6 | 19 |
| Julianne Hough | 4.20 | 2 | 5 |
| Mark Ballas | 5.19 | 3 | 30 |

### 5.3 Feature Importance and Model Performance

| Feature | Importance |
|---------|------------|
| Average Judge Score | 0.876 |
| Season | 0.074 |
| Age | 0.028 |
| Industry | 0.019 |

**5-Fold CV Performance:**
| Metric | Value | Unit |
|--------|-------|------|
| R² | 0.488 | ratio |
| RMSE | 2.688 | positions |
| MAE | 2.090 | positions |

Judge scores dominate (87.6%), indicating technical dancing ability remains the primary determinant of success. The model achieves MAE=2.09, meaning average prediction error is approximately 2 placement positions.

---

## 6. Problem 4: New Voting System Design

### 6.1 Parameter Optimization via Grid Search

**Optimal Parameters:**
- Base α = 0.30
- Increment = 0.04
- Score = 0.916

This yields initial fan weight of 66% shifting to 26% by finals.

![Grid Search](figures/imp6_grid_search.pdf)
*Figure 4: Grid search optimization for dynamic weight parameters.*

### 6.2 Dynamic Weight Formula

$$\alpha(w) = \min(0.30 + 0.04w, 0.80)$$

| Week | Judge Weight | Fan Weight |
|------|--------------|------------|
| 1 | 34% | 66% |
| 5 | 50% | 50% |
| 10+ | 74% | 26% |

### 6.3 Impact on Controversial Contestants

| Contestant | Original | Expected | Change |
|------------|----------|----------|--------|
| Bobby Bones | 1st | 2.2 | +1.2 |
| Bristol Palin | 3rd | 3.8 | +0.8 |
| Jerry Rice | 2nd | 2.5 | +0.5 |

Under DWVS, Bobby Bones would place 2nd instead of winning.

### 6.4 Group-Level Validation

We quantitatively define controversial contestants as those with **Controversy Score ≥ 3** (Judge Rank - Final Placement). This identifies **32 controversial contestants** (7.6% of 421 total).

**Controversial vs. Normal Contestants:**

| Metric | Controversial (n=32) | Normal (n=389) |
|--------|---------------------|----------------|
| Avg Final Placement | 5.53 | 6.92 |
| Avg Judge Score | 22.05 | 24.34 |
| Avg Controversy Score | +3.88 | -0.34 |

**DWVS Impact on All 32 Controversial Contestants:**
- 78.1% would rank lower (positive change)
- Average placement change: +0.45 positions
- High controversy group (Score ≥ 5): average +0.81 positions
- Correlation: Higher controversy → larger adjustment

This validates that DWVS provides **universal, proportional corrections** rather than ad-hoc fixes.

---

## 7. Sensitivity Analysis and Model Validation

### 7.1 Cross-Season Validation

Training on Seasons 1-20, testing on Seasons 21-34:

| Metric | Training | Test | Gap |
|--------|----------|------|-----|
| R² | 0.996 | 0.934 | 0.062 |
| RMSE | 0.874 | 3.081 | 2.207 |
| MAE | 0.722 | 2.421 | 1.699 |

*CV Mean R² = 0.942 ± 0.013*

The small R² gap (0.062) demonstrates strong generalization. Test RMSE=3.08 and MAE=2.42 indicate prediction errors of approximately 2-3 placement positions on unseen seasons.

![Cross-Season Validation](figures/imp7_cross_season_validation.pdf)
*Figure 5: Cross-season validation with temporal split.*

---

## 8. Model Evaluation

### Strengths

- **Stratified Analysis:** Achieved 80.7% overall consistency, with percentage-based (96.0%) demonstrating excellent constraint satisfaction
- **Cross-Validation:** Test R²=0.934 confirms generalizability
- **Parameter Optimization:** Grid search provides objective basis for DWVS parameters

### Limitations

- Without actual fan vote totals, cannot validate against ground truth
- Professional dancer-celebrity pairings are not random
- Audience demographics have evolved over 34 seasons

---

## 9. Memorandum to DWTS Producers

**To:** Executive Producers, Dancing with the Stars  
**From:** MCM Analysis Team  
**Subject:** Voting System Analysis and Recommendations

**Key Findings:**

1. **High Consistency:** Overall 80.7% consistency; percentage-based achieves 96.0% vs. rank-based 38.4%
2. **Industry Bias:** Judges show stronger industry bias (F=8.81) than fans (F=2.14)
3. **Model Generalizes:** Cross-season validation achieves R²=0.934

**Recommendations:**

1. **Adopt DWVS** with base α=0.30, increment=0.04 (66% fan → 26% fan)
2. **Maintain tiebreaker rule** (affects 3.9% of decisions)
3. **Expected outcome:** Bobby Bones places 2nd (not 1st), addressing fairness concerns

---

## References

1. Bradley, R. A., & Terry, M. E. (1952). Rank analysis of incomplete block designs. *Biometrika*, 39(3/4), 324-345.
2. Plackett, R. L. (1975). The analysis of permutations. *JRSS-C*, 24(2), 193-202.
3. Luce, R. D. (1959). *Individual Choice Behavior*. Wiley.
4. Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5-32.
5. Efron, B., & Tibshirani, R. J. (1993). *An Introduction to the Bootstrap*. Chapman & Hall.
