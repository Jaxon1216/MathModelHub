"""
分析年龄和专业舞者对评委分数 vs 粉丝投票的差异影响
用于补充论文Problem 3的分析
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import pearsonr
import json

# 加载数据
data_long = pd.read_csv('../数据预处理/data_long_format.csv')
vote_estimates = pd.read_csv('../问题一/vote_estimates.csv')
raw_data = pd.read_csv('../2026_MCM_Problem_C_Data.csv')

# 合并数据
merged = data_long.merge(
    vote_estimates[['season', 'week', 'celebrity_name', 'estimated_vote_share']], 
    on=['season', 'week', 'celebrity_name'], 
    how='left'
)

# 筛选有效数据
analysis_df = merged[merged['total_score'].notna() & merged['estimated_vote_share'].notna()].copy()

print("="*80)
print("问题三：因素对评委分数 vs 粉丝投票的差异影响分析")
print("="*80)

# ============================================
# 1. 年龄影响分析
# ============================================
print("\n【1】年龄影响分析：Age → Judge Scores vs Fan Votes")
print("-"*80)

# 年龄 vs 评委分数的相关性
age_judge_corr, age_judge_p = pearsonr(
    analysis_df['celebrity_age_during_season'], 
    analysis_df['total_score']
)

# 年龄 vs 粉丝投票的相关性
age_fan_corr, age_fan_p = pearsonr(
    analysis_df['celebrity_age_during_season'], 
    analysis_df['estimated_vote_share']
)

print(f"年龄 vs 评委分数：")
print(f"  相关系数 r = {age_judge_corr:.3f}, p = {age_judge_p:.4f}")
print(f"  解释：{'年龄越大，评委分数越低' if age_judge_corr < 0 else '年龄越大，评委分数越高'}")

print(f"\n年龄 vs 粉丝投票份额：")
print(f"  相关系数 r = {age_fan_corr:.3f}, p = {age_fan_p:.4f}")
print(f"  解释：{'年龄越大，粉丝支持越低' if age_fan_corr < 0 else '年龄越大，粉丝支持越高'}")

print(f"\n关键发现：")
if abs(age_judge_corr) > abs(age_fan_corr):
    print(f"  年龄对评委分数的影响（|r|={abs(age_judge_corr):.3f}）强于对粉丝投票的影响（|r|={abs(age_fan_corr):.3f}）")
    print(f"  差异幅度：{abs(age_judge_corr) - abs(age_fan_corr):.3f}")
else:
    print(f"  年龄对粉丝投票的影响（|r|={abs(age_fan_corr):.3f}）强于对评委分数的影响（|r|={abs(age_judge_corr):.3f}）")
    print(f"  差异幅度：{abs(age_fan_corr) - abs(age_judge_corr):.3f}")

# 按年龄组分析
analysis_df['age_group'] = pd.cut(
    analysis_df['celebrity_age_during_season'], 
    bins=[0, 25, 35, 45, 100], 
    labels=['<25', '25-35', '35-45', '45+']
)

age_group_stats = analysis_df.groupby('age_group').agg({
    'total_score': ['mean', 'std'],
    'estimated_vote_share': ['mean', 'std']
}).round(3)

print(f"\n按年龄组统计：")
print(age_group_stats)

# ============================================
# 2. 专业舞者影响分析
# ============================================
print("\n" + "="*80)
print("【2】专业舞者影响分析：Pro Dancer → Judge Scores vs Fan Votes")
print("-"*80)

# 计算每个舞者的平均评委分数和粉丝投票份额
dancer_stats = analysis_df.groupby('ballroom_partner').agg({
    'total_score': ['mean', 'count'],
    'estimated_vote_share': 'mean',
    'placement': 'mean'
}).round(3)

dancer_stats.columns = ['avg_judge_score', 'n_partnerships', 'avg_fan_vote', 'avg_placement']
dancer_stats = dancer_stats[dancer_stats['n_partnerships'] >= 5].sort_values('avg_placement')

print(f"\n顶级舞者统计（至少5次合作）：")
print(dancer_stats.head(10).to_string())

# 计算舞者间的评委分数和粉丝投票变异
judge_cv = dancer_stats['avg_judge_score'].std() / dancer_stats['avg_judge_score'].mean()
fan_cv = dancer_stats['avg_fan_vote'].std() / dancer_stats['avg_fan_vote'].mean()

print(f"\n舞者间差异（变异系数 CV）：")
print(f"  评委分数 CV = {judge_cv:.3f}")
print(f"  粉丝投票 CV = {fan_cv:.3f}")
print(f"\n关键发现：")
if judge_cv > fan_cv:
    print(f"  专业舞者对评委分数的影响（CV={judge_cv:.3f}）强于对粉丝投票的影响（CV={fan_cv:.3f}）")
    print(f"  差异比例：{(judge_cv / fan_cv - 1) * 100:.1f}%")
else:
    print(f"  专业舞者对粉丝投票的影响（CV={fan_cv:.3f}）强于对评委分数的影响（CV={judge_cv:.3f}）")
    print(f"  差异比例：{(fan_cv / judge_cv - 1) * 100:.1f}%")

# 相关性分析：舞者的评委分数 vs 粉丝投票
dancer_corr, dancer_p = pearsonr(
    dancer_stats['avg_judge_score'], 
    dancer_stats['avg_fan_vote']
)
print(f"\n舞者层面：评委分数 vs 粉丝投票相关性")
print(f"  r = {dancer_corr:.3f}, p = {dancer_p:.4f}")

# ============================================
# 3. 保存结果用于论文
# ============================================
results = {
    'age_analysis': {
        'age_vs_judge_score': {
            'correlation': float(age_judge_corr),
            'p_value': float(age_judge_p),
            'strength': 'strong' if abs(age_judge_corr) > 0.3 else 'moderate' if abs(age_judge_corr) > 0.1 else 'weak'
        },
        'age_vs_fan_vote': {
            'correlation': float(age_fan_corr),
            'p_value': float(age_fan_p),
            'strength': 'strong' if abs(age_fan_corr) > 0.3 else 'moderate' if abs(age_fan_corr) > 0.1 else 'weak'
        },
        'impact_comparison': {
            'judge_stronger': bool(abs(age_judge_corr) > abs(age_fan_corr)),
            'difference': float(abs(age_judge_corr) - abs(age_fan_corr))
        }
    },
    'dancer_analysis': {
        'judge_score_cv': float(judge_cv),
        'fan_vote_cv': float(fan_cv),
        'dancer_correlation': float(dancer_corr),
        'impact_comparison': {
            'judge_stronger': bool(judge_cv > fan_cv),
            'difference_pct': float((max(judge_cv, fan_cv) / min(judge_cv, fan_cv) - 1) * 100)
        }
    }
}

# 保存为JSON
with open('judge_fan_impact_analysis.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n" + "="*80)
print("✅ 分析完成！结果已保存到 judge_fan_impact_analysis.json")
print("="*80)

# 生成LaTeX表格
print("\n" + "="*80)
print("【论文使用】LaTeX表格代码：")
print("="*80)

print("\n% 年龄影响对比表格")
print(r"\begin{table}[H]")
print(r"\centering")
print(r"\caption{Age Impact: Judge Scores vs. Fan Votes}")
print(r"\label{tab:age_impact}")
print(r"\begin{tabular}{lcc}")
print(r"\toprule")
print(r"\textbf{Dependent Variable} & \textbf{Correlation (r)} & \textbf{p-value} \\")
print(r"\midrule")
print(f"Judge Score & {age_judge_corr:.3f} & {'<0.001' if age_judge_p < 0.001 else f'{age_judge_p:.3f}'} \\\\")
print(f"Fan Vote Share & {age_fan_corr:.3f} & {'<0.001' if age_fan_p < 0.001 else f'{age_fan_p:.3f}'} \\\\")
print(r"\bottomrule")
print(r"\end{tabular}")
print(r"\end{table}")

print("\n% 专业舞者影响对比")
print(r"\textbf{Professional Dancer Impact (Coefficient of Variation):}")
print(f"Judge Scores: CV = {judge_cv:.3f}")
print(f"Fan Votes: CV = {fan_cv:.3f}")

print("\n" + "="*80)
