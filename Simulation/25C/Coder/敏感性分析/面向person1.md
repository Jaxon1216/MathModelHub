# 敏感性分析 —— 写作指南

> 本文档面向写作手Person1，提供敏感性分析的写作要点、结果解读思路与图表引用建议。

## 一、分析目标与逻辑
敏感性分析用于验证模型对关键设定的稳健性，回答“变动什么、如何变、影响如何”。建议用三小节结构：正则化强度敏感性、模型类别敏感性、Bootstrap稳健性。

## 二、可直接写入的结果表述（可按需要改写）
敏感性分析结果显示，正则化强度在合理区间内变化时，RMSE与$R^2$仅有小幅波动，说明线性模型的预测性能对惩罚系数不敏感。对比模型类别后，线性/正则化模型与随机森林的性能保持一致量级，表明核心信号主要由工程特征所捕捉，建模设定变化不会改变总体结论。Bootstrap重采样的误差分布集中，预测区间稳定，支持预测结果在样本扰动下具有可靠性。

## 三、建议插入的图表
| 编号 | 文件名 | 内容 | 建议章节 |
|------|--------|------|---------|
| 1 | fig_sensitivity_alpha_rmse.pdf | Lasso/Ridge随alpha变化的RMSE曲线 | Sensitivity Analysis |
| 2 | fig_sensitivity_model_r2.pdf | 不同模型R2对比 | Sensitivity Analysis |
| 3 | fig_sensitivity_bootstrap_rmse.pdf | Bootstrap RMSE分布 | Sensitivity Analysis |

## 四、图表引用句式
- As illustrated in Fig. X, the RMSE remains stable across a wide range of regularization strengths, indicating limited sensitivity to penalty tuning.
- Fig. X compares model classes and shows consistent $R^2$, supporting the robustness of our predictive framework.
- The bootstrap RMSE distribution in Fig. X concentrates around a narrow interval, suggesting stable performance under resampling.
