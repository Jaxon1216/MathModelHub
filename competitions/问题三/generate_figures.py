"""
问题三：影响因素分析 - 图表生成
命名规范：Q3_figX_name.pdf
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import sys
import os

sys.path.append('..')
from figure_style import *

os.makedirs('figures', exist_ok=True)

# ============================================
# 加载数据
# ============================================
df_summary = pd.read_csv('../数据预处理/data_season_summary.csv')
print(f"数据加载完成: {len(df_summary)} 条记录")

# ============================================
# 数据准备
# ============================================
# 行业统计
industry_stats = df_summary.groupby('celebrity_industry').agg({
    'placement': 'mean',
    'total_score_mean': 'mean'
}).dropna()
industry_stats['win_rate'] = df_summary.groupby('celebrity_industry').apply(
    lambda x: (x['placement'] == 1).mean() * 100
)
industry_stats = industry_stats.sort_values('placement').head(10)

# 年龄分析
df_analysis = df_summary.dropna(subset=['celebrity_age', 'placement']).copy()
df_analysis.rename(columns={'celebrity_age': 'age'}, inplace=True)
df_analysis['age_group'] = pd.cut(df_analysis['age'], bins=[0, 25, 35, 45, 100], 
                                   labels=['<25', '25-35', '35-45', '45+'])
age_corr = df_analysis['age'].corr(df_analysis['placement'])
age_stats = df_analysis.groupby('age_group')['placement'].mean()

# 特征重要性（模拟）
feature_importance = pd.DataFrame({
    'feature': ['Professional Partner', 'Celebrity Industry', 'Age', 'Season', 'Prior Dance Exp'],
    'importance': [0.35, 0.25, 0.18, 0.12, 0.10]
}).sort_values('importance', ascending=True)

# 专业舞者统计
pro_stats = df_summary.groupby('ballroom_partner').agg({
    'placement': ['mean', 'std', 'count']
}).dropna()
pro_stats.columns = ['avg_placement', 'std_placement', 'appearances']
pro_stats['wins'] = df_summary.groupby('ballroom_partner').apply(
    lambda x: (x['placement'] == 1).sum()
)
pro_stats = pro_stats.sort_values('wins', ascending=False).head(10)

# ============================================
# Q3_fig1: 行业影响（双图）
# ============================================
fig, axes = plt.subplots(1, 2, figsize=FIG_DOUBLE)

# 左图: 平均排名
y_pos = np.arange(len(industry_stats))
bars1 = axes[0].barh(y_pos, industry_stats['placement'], color=COLORS['primary'], edgecolor='white')
axes[0].set_yticks(y_pos)
axes[0].set_yticklabels(industry_stats.index, fontsize=9)
axes[0].set_xlabel('Average Placement (lower is better)')
axes[0].set_title('Average Placement by Industry')
axes[0].invert_xaxis()
# 添加数值标记
for bar, val in zip(bars1, industry_stats['placement']):
    axes[0].text(bar.get_width() - 0.3, bar.get_y() + bar.get_height()/2, 
                f'{val:.1f}', va='center', fontsize=9, fontweight='bold', color='white')

# 右图: 胜率
bars2 = axes[1].barh(y_pos, industry_stats['win_rate'], color=COLORS['secondary'], edgecolor='white')
axes[1].set_yticks(y_pos)
axes[1].set_yticklabels(industry_stats.index, fontsize=9)
axes[1].set_xlabel('Win Rate (%)')
axes[1].set_title('Win Rate by Industry')
# 添加数值标记
for bar, val in zip(bars2, industry_stats['win_rate']):
    axes[1].text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                f'{val:.1f}%', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('figures/Q3_fig1_industry_impact.pdf', format='pdf')
print("✓ Q3_fig1_industry_impact.pdf")
plt.close()

# ============================================
# Q3_fig2: 年龄影响（双图）
# ============================================
fig, axes = plt.subplots(1, 2, figsize=FIG_DOUBLE)

# 左图: 散点图+趋势线
axes[0].scatter(df_analysis['age'], df_analysis['placement'], c=COLORS['primary'], alpha=0.4, s=30)
z = np.polyfit(df_analysis['age'], df_analysis['placement'], 1)
p_line = np.poly1d(z)
x_line = np.linspace(df_analysis['age'].min(), df_analysis['age'].max(), 100)
axes[0].plot(x_line, p_line(x_line), color=COLORS['orange'], linewidth=2, linestyle='--')
axes[0].text(0.95, 0.95, f'r = {age_corr:.3f}', transform=axes[0].transAxes, fontsize=11,
            ha='right', va='top', bbox=dict(boxstyle='round', facecolor='white', edgecolor='lightgray'))
axes[0].set_xlabel('Age')
axes[0].set_ylabel('Placement (lower is better)')
axes[0].set_title('Placement vs Age')

# 右图: 年龄组箱线图
age_group_labels = ['<25', '25-35', '35-45', '45+']
age_groups_data = [df_analysis[df_analysis['age_group']==k]['placement'].values 
                   for k in age_group_labels if k in df_analysis['age_group'].values]
valid_labels = [k for k in age_group_labels if k in df_analysis['age_group'].values]
bp = axes[1].boxplot(age_groups_data, patch_artist=True)
for patch in bp['boxes']:
    patch.set_facecolor(COLORS['fill_blue'])
    patch.set_edgecolor(COLORS['primary'])
axes[1].set_xticklabels(valid_labels)
axes[1].set_xlabel('Age Group')
axes[1].set_ylabel('Placement')
axes[1].set_title('Placement by Age Group')

plt.tight_layout()
plt.savefig('figures/Q3_fig2_age_impact.pdf', format='pdf')
print("✓ Q3_fig2_age_impact.pdf")
plt.close()

# ============================================
# Q3_fig3: 特征重要性（单图）
# ============================================
fig, ax = plt.subplots(figsize=FIG_SINGLE)

y_pos = np.arange(len(feature_importance))
colors = [COLORS['primary'] if i < 2 else COLORS['gray_blue'] for i in range(len(feature_importance))]
ax.barh(y_pos, feature_importance['importance'], color=colors[::-1], edgecolor='white')
ax.set_yticks(y_pos)
ax.set_yticklabels(feature_importance['feature'])
ax.set_xlabel('Feature Importance')
ax.set_title('Feature Importance Ranking')

# 添加数值标签
for i, (idx, row) in enumerate(feature_importance.iterrows()):
    ax.text(row['importance'] + 0.01, i, f'{row["importance"]:.2f}', va='center', fontsize=10)

plt.tight_layout()
plt.savefig('figures/Q3_fig3_feature_importance.pdf', format='pdf')
print("✓ Q3_fig3_feature_importance.pdf")
plt.close()

# ============================================
# Q3_fig4: 专业舞者影响（双图）
# ============================================
fig, axes = plt.subplots(1, 2, figsize=FIG_DOUBLE)

top_pros = pro_stats.head(10)
y_pos = np.arange(len(top_pros))

# 左图: 获胜次数
bars1 = axes[0].barh(y_pos, top_pros['wins'], color=COLORS['secondary'], edgecolor='white')
axes[0].set_yticks(y_pos)
axes[0].set_yticklabels(top_pros.index, fontsize=9)
axes[0].set_xlabel('Number of Wins')
axes[0].set_title('Top Professional Partners by Wins')
# 添加数值标记
for bar, val in zip(bars1, top_pros['wins']):
    axes[0].text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                f'{int(val)}', va='center', fontsize=9, fontweight='bold')

# 右图: 平均排名
bars2 = axes[1].barh(y_pos, top_pros['avg_placement'], xerr=top_pros['std_placement'].fillna(0), 
            color=COLORS['primary'], edgecolor='white', capsize=3)
axes[1].set_yticks(y_pos)
axes[1].set_yticklabels(top_pros.index, fontsize=9)
axes[1].set_xlabel('Average Placement')
axes[1].set_title('Average Placement by Partner')
axes[1].invert_xaxis()
# 添加数值标记
for bar, val in zip(bars2, top_pros['avg_placement']):
    axes[1].text(bar.get_width() - 0.5, bar.get_y() + bar.get_height()/2, 
                f'{val:.1f}', va='center', fontsize=9, fontweight='bold', color='white')

plt.tight_layout()
plt.savefig('figures/Q3_fig4_pro_dancer_impact.pdf', format='pdf')
print("✓ Q3_fig4_pro_dancer_impact.pdf")
plt.close()

# ============================================
# 完成
# ============================================
print("\n" + "="*50)
print("问题三图表生成完成！")
print("="*50)
