"""
计算Industry对Judge Score和Fan Vote的ANOVA F统计量
用于验证论文中的数据
"""

import pandas as pd
import numpy as np
from scipy import stats

print("="*80)
print("计算Industry ANOVA: Judge Score vs Fan Vote")
print("="*80)

# 加载数据
df_long = pd.read_csv('../数据预处理/data_long_format.csv')
vote_est = pd.read_csv('../问题一/vote_estimates.csv')

# 合并数据
merged = df_long.merge(
    vote_est[['season', 'week', 'celebrity_name', 'estimated_vote_share']], 
    on=['season', 'week', 'celebrity_name'], 
    how='left'
)

# 筛选有效数据
valid = merged[merged['total_score'].notna() & merged['estimated_vote_share'].notna()].copy()

print(f"\n有效数据行数: {len(valid)}")

# 行业分组（与论文一致）
industry_map = {
    'Actor/Actress': 'Actor/Actress',
    'Singer/Rapper': 'Singer/Rapper', 
    'Athlete': 'Athlete',
    'TV Personality': 'TV Personality',
    'Comedian': 'Comedian',
    'Model': 'Model'
}

valid['industry_grouped'] = valid['celebrity_industry'].map(industry_map)
valid['industry_grouped'] = valid['industry_grouped'].fillna('Other')

# 筛选主要行业
industry_df = valid[valid['industry_grouped'].isin([
    'Actor/Actress', 'Singer/Rapper', 'Athlete', 
    'TV Personality', 'Comedian', 'Model', 'Other'
])].copy()

print(f"用于ANOVA的数据行数: {len(industry_df)}")
print(f"行业分类: {industry_df['industry_grouped'].value_counts().to_dict()}")

# ==========================================
# ANOVA分析
# ==========================================

# ANOVA - Judge Score by Industry
print("\n" + "="*80)
print("【1】ANOVA: Judge Score ~ Industry")
print("="*80)

groups_judge = [group['total_score'].values for name, group in industry_df.groupby('industry_grouped')]
f_judge, p_judge = stats.f_oneway(*groups_judge)

print(f"F统计量: {f_judge:.4f}")
print(f"p值: {p_judge:.6f}")
print(f"显著性: {'高度显著 (p<0.001)' if p_judge < 0.001 else '显著 (p<0.05)' if p_judge < 0.05 else '不显著'}")

# ANOVA - Fan Vote by Industry  
print("\n" + "="*80)
print("【2】ANOVA: Fan Vote ~ Industry")
print("="*80)

groups_fan = [group['estimated_vote_share'].values for name, group in industry_df.groupby('industry_grouped')]
f_fan, p_fan = stats.f_oneway(*groups_fan)

print(f"F统计量: {f_fan:.4f}")
print(f"p值: {p_fan:.6f}")
print(f"显著性: {'高度显著 (p<0.001)' if p_fan < 0.001 else '显著 (p<0.05)' if p_fan < 0.05 else '不显著'}")

# ==========================================
# 对比分析
# ==========================================
print("\n" + "="*80)
print("【3】对比分析: Judge vs Fan")
print("="*80)

f_ratio = f_judge / f_fan
print(f"F值比率 (Judge/Fan): {f_ratio:.4f}")

if f_judge > f_fan:
    diff_pct = ((f_judge - f_fan) / f_fan) * 100
    print(f"结论: Industry对Judge Score的影响更强 (大{diff_pct:.1f}%)")
else:
    diff_pct = ((f_fan - f_judge) / f_judge) * 100
    print(f"结论: Industry对Fan Vote的影响更强 (大{diff_pct:.1f}%)")

# ==========================================
# 各行业均值对比
# ==========================================
print("\n" + "="*80)
print("【4】各行业Judge Score和Fan Vote均值")
print("="*80)

industry_stats = industry_df.groupby('industry_grouped').agg({
    'total_score': ['mean', 'std', 'count'],
    'estimated_vote_share': ['mean', 'std']
}).round(4)

print(industry_stats)

# ==========================================
# 保存结果
# ==========================================
results_df = pd.DataFrame({
    'Metric': ['Judge Score F-statistic', 'Judge Score p-value', 
               'Fan Vote F-statistic', 'Fan Vote p-value',
               'F-ratio (Judge/Fan)', 'Stronger on'],
    'Value': [f_judge, p_judge, f_fan, p_fan, f_ratio, 
              'Judge' if f_judge > f_fan else 'Fan']
})

output_file = 'industry_anova_judge_vs_fan.csv'
results_df.to_csv(output_file, index=False)

print(f"\n结果已保存至: {output_file}")

# 保存详细的行业统计
industry_stats_flat = industry_df.groupby('industry_grouped').agg({
    'total_score': 'mean',
    'estimated_vote_share': 'mean'
}).reset_index()
industry_stats_flat.columns = ['Industry', 'Avg_Judge_Score', 'Avg_Fan_Vote']
industry_stats_flat.to_csv('industry_judge_fan_means.csv', index=False)

print("\n" + "="*80)
print("验证完成！")
print("="*80)
print(f"\n论文声称: Judge F=8.08, Fan F=2.81")
print(f"实际计算: Judge F={f_judge:.2f}, Fan F={f_fan:.2f}")

if abs(f_judge - 8.08) > 0.5 or abs(f_fan - 2.81) > 0.5:
    print("\n⚠️  警告: 论文数据与实际计算结果存在显著差异！")
else:
    print("\n✓ 论文数据与实际计算结果一致")
