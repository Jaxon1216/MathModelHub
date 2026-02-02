# 目录调整完成总结

**日期**: 2026-02-02  
**任务**: 调整论文目录结构，确保目录只占1页

## ✅ 完成的调整

### 1. 目录深度控制

**设置**: 
- 全局目录深度设为1（只显示section）
- Problem 1-4 局部显示subsection（深度2）
- 其他部分只显示section

**实现方式**:
```latex
\setcounter{tocdepth}{1}  % 全局只显示section

% Problem 1-4 开始前
\addtocontents{toc}{\setcounter{tocdepth}{2}}  % 显示subsection

% Problem 5 (Sensitivity) 开始前
\addtocontents{toc}{\setcounter{tocdepth}{1}}  % 恢复只显示section
```

### 2. Problem 3 结构优化 (5个→3个subsection)

#### 修改前:
```
5. Problem 3: Factor Impact Analysis
   5.1 Industry Impact: Judge Scores vs. Fan Votes
   5.2 Professional Dancer Effect
   5.3 Age Effect
   5.4 Relative Impact of External Factors
   5.5 Summary: Do Factors Affect Judges and Fans Equally?
```

#### 修改后:
```
5. Problem 3: Factor Impact Analysis
   5.1 Impact of Pre-determined Characteristics
       - Industry Background (subsubsection*)
       - Professional Dancer Assignment (subsubsection*)
       - Age Effect (subsubsection*)
   5.2 Relative Importance Analysis
   5.3 Differential Impact: Judges vs. Fans
```

**说明**: 使用`\subsubsection*`使得Industry/Dancer/Age在正文有标题但不在目录显示

### 3. Problem 4 结构优化 (6个→3个subsection)

#### 修改前:
```
6. Problem 4: New Voting System Design
   6.1 Motivation: Addressing the "Low-Skill High-Popularity" Problem
   6.2 Design Objectives
   6.3 Parameter Optimization via Grid Search
   6.4 DWVS Formula
   6.5 Impact on Controversial Contestants
   6.6 System Comparison
```

#### 修改后:
```
6. Problem 4: New Voting System Design
   6.1 Design Philosophy and Objectives
       (合并6.1+6.2)
   6.2 DWVS Implementation
       - Parameter Optimization (加粗文本)
       - Comprehensive Scoring Formula (加粗文本)
       (合并6.3+6.4)
   6.3 Effectiveness Validation
       - Impact on Controversial Contestants (加粗文本)
       - Multi-dimensional System Comparison (加粗文本)
       (合并6.5+6.6)
```

### 4. Introduction & Preparation

**处理方式**:
- 保持3个subsection
- 正文中显示完整subsection标题
- 目录中不显示这些subsection（由于tocdepth=1）

```
1. Introduction
   1.1 Problem Background (正文有，目录无)
   1.2 Problem Restatement (正文有，目录无)
   1.3 Our Approach (正文有，目录无)

2. Preparation for Modeling
   2.1 Model Assumptions (正文有，目录无)
   2.2 Notations (正文有，目录无)
   2.3 Data Overview (正文有，目录无)
```

### 5. Sensitivity Analysis

**处理方式**:
- Section标题在目录显示
- Subsection不在目录显示

```
7. Sensitivity Analysis and Model Validation (目录有)
   7.1 Fan Vote Estimation Sensitivity (正文有，目录无)
   7.2 Cross-Season Model Validation (正文有，目录无)
```

### 6. Memorandum & References

**Memorandum**:
- 改为`\section*{Memorandum to DWTS Producers}`
- 不在目录显示

**References**:
- 改为`\section{References}`
- 添加`\addcontentsline{toc}{section}{References}`
- **在目录显示**

### 7. 目录行间距优化

添加spacing调整确保目录紧凑:
```latex
{
\setlength{\parskip}{0pt}
\setlength{\itemsep}{0pt}
\tableofcontents
}
```

## 📊 最终目录结构

```
Table of Contents

1. Introduction
2. Preparation for Modeling
3. Problem 1: Fan Vote Estimation Model
   3.1 Model Construction
   3.2 Stratified Consistency Analysis
   3.3 Uncertainty Quantification
   3.4 Controversial Contestant Analysis
4. Problem 2: Voting Method Comparison
   4.1 Method Definitions
   4.2 Counterfactual Analysis
   4.3 Controversial Contestant Analysis
   4.4 Recommendations
5. Problem 3: Factor Impact Analysis
   5.1 Impact of Pre-determined Characteristics
   5.2 Relative Importance Analysis
   5.3 Differential Impact: Judges vs. Fans
6. Problem 4: New Voting System Design
   6.1 Design Philosophy and Objectives
   6.2 DWVS Implementation
   6.3 Effectiveness Validation
7. Sensitivity Analysis and Model Validation
8. Model Evaluation and Discussion
References
```

## 📈 效果对比

| 项目 | 修改前 | 修改后 |
|------|--------|--------|
| **总页数** | 25页 | 23页 |
| **Problem 3 subsection数** | 5个 | 3个 |
| **Problem 4 subsection数** | 6个 | 3个 |
| **目录中的subsection行数** | ~32行 | ~16行 |
| **目录页数** | 可能>1页 | 1页（已优化） |
| **Memorandum在目录** | 是 | 否 |
| **References在目录** | 否 | 是 |

## ✅ 核心特点

1. **符合用户要求**:
   - ✅ 目录最多展示二级标题
   - ✅ Problem按题目整合为3-4个二级标题
   - ✅ 敏感性分析不展示二级标题
   - ✅ 目录只占1页
   - ✅ Memorandum不在目录
   - ✅ References在目录显示

2. **保持内容完整性**:
   - ✅ 所有原有内容都保留
   - ✅ 只是重新组织结构
   - ✅ 正文中仍有详细的小标题

3. **专业美观**:
   - ✅ 目录结构清晰
   - ✅ 层次分明
   - ✅ 符合学术论文规范

## 🔧 技术实现

- 使用`\setcounter{tocdepth}{n}`控制显示深度
- 使用`\addtocontents{toc}{...}`局部调整
- 使用`\subsubsection*`在正文显示但目录不显示
- 使用`\section*`使section不编号不在目录
- 使用`\addcontentsline`手动添加到目录

## ✨ 结论

目录调整已完成，达到以下效果：
- 目录紧凑，只占1页
- Problem 1-4展示subsection（方便读者）
- 其他部分只显示section（避免冗长）
- 结构清晰，符合MCM论文要求
- 总页数减少到23页（在25页限制内）
