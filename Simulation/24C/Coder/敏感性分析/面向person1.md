# 敏感性分析 —— 写作指南

> 本文档面向写作手Person1，帮助理解敏感性分析的方法和结论。

## 一、敏感性分析概述

敏感性分析用于评估模型参数变化对结果的影响程度，验证模型的鲁棒性（Robustness）。

### 分析内容

| 模型类型 | 参数 | 默认值 | 敏感性 |
|----------|------|--------|--------|
| 势头模型 | Serve Advantage | 0.65 | **高** |
| 势头模型 | Break Point Mult | 1.5 | 低 |
| 势头模型 | Streak Bonus | 0.1 | 低 |
| 势头模型 | Decay Rate | 0.02 | 低 |
| 随机森林 | n_estimators | 100 | 中 |
| 随机森林 | max_depth | 10 | 中 |
| 随机森林 | min_samples_split | 20 | 低 |

## 二、主要结论

### 2.1 势头模型参数

1. **发球优势因子 (Serve Advantage)** 是最敏感的参数
   - 测试范围: 0.50 - 0.80
   - 准确率变化: 0.806 - 0.903
   - 建议: 根据实际数据中发球方胜率进行校准

2. **其他参数敏感性较低**
   - 破发点权重、连胜加成、衰减率变化对结果影响较小
   - 默认参数配置有效

### 2.2 随机森林参数

1. **树数量**: 50棵以上趋于稳定，100棵足够
2. **最大深度**: 10左右效果最佳，过深可能过拟合
3. **最小样本分割**: 对结果影响最小

### 2.3 鲁棒性结论

模型整体表现**稳定**，在参数合理变化范围内，预测准确率保持在80%以上。这表明：
- 模型不依赖于特定参数的精确调整
- 结论具有较强的可信度
- 模型可应用于不同场景

## 三、论文撰写建议

### 建议章节位置
敏感性分析通常放在 **Results** 章节的最后部分或 **Discussion** 章节开头。

### 关键句式

**介绍敏感性分析**:
```
To assess the robustness of our model, we conduct sensitivity analysis 
on key parameters.
```

**描述结果**:
```
The model demonstrates strong robustness across parameter variations. 
Serve advantage factor shows the highest sensitivity (index = 0.110), 
while other parameters remain relatively insensitive.
```

**结论性陈述**:
```
The sensitivity analysis confirms that our model produces stable results 
under reasonable parameter perturbations, supporting the reliability 
of our conclusions.
```

## 四、图片列表与插入位置

| 编号 | 文件名 | 内容 | 建议位置 |
|------|--------|------|----------|
| 1 | fig1_momentum_params_sensitivity.pdf | 势头模型4参数敏感性 | Sensitivity Analysis |
| 2 | fig2_rf_params_sensitivity.pdf | 随机森林3参数敏感性 | Sensitivity Analysis |
| 4 | fig4_dual_param_heatmap.pdf | 双参数热力图 | Sensitivity Analysis |
| 5 | fig5_sensitivity_summary.pdf | 敏感性指标汇总 | Sensitivity Analysis |

### 图片使用建议

**fig1_momentum_params_sensitivity.pdf** 最重要，展示了核心势头模型的参数敏感性。

**fig4_dual_param_heatmap.pdf** 直观展示了两个关键参数的交互作用。
