"""
问题一：粉丝投票估算模型 - 图表生成
命名规范：Q1_figX_name.pdf
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.special import softmax
import sys
import os

# 导入统一配色
sys.path.append('..')
from figure_style import *

# 确保figures文件夹存在
os.makedirs('figures', exist_ok=True)

# ============================================
# 加载数据
# ============================================
df_long = pd.read_csv('../数据预处理/data_long_format.csv')
df_summary = pd.read_csv('../数据预处理/data_season_summary.csv')
vote_estimates = pd.read_csv('vote_estimates.csv')
consistency = pd.read_csv('verification_results.csv')
df_certainty = pd.read_csv('certainty_metrics.csv')

print(f"数据加载完成: {len(vote_estimates)} 条投票估算记录")

# ============================================
# Q1_fig1: 一致性分析（双图）
# ============================================
fig, axes = plt.subplots(1, 2, figsize=FIG_DOUBLE)

# 左图: 按季的一致性
consistency_by_season = consistency.groupby('season')['is_consistent'].mean() * 100
axes[0].bar(consistency_by_season.index, consistency_by_season.values, 
           color=COLORS['primary'], edgecolor='white', alpha=0.9)
axes[0].axhline(y=consistency['is_consistent'].mean()*100, color=COLORS['orange'], 
               linestyle='--', linewidth=2, label=f'Overall: {consistency["is_consistent"].mean()*100:.1f}%')
axes[0].set_xlabel('Season')
axes[0].set_ylabel('Consistency Rate (%)')
axes[0].set_title('Consistency Rate by Season')
add_legend(axes[0])

# 右图: 按投票方式的一致性
consistency_by_method = consistency.groupby('method')['is_consistent'].agg(['mean', 'std'])
consistency_by_method['mean'] *= 100
consistency_by_method['std'] *= 100
x_pos = np.arange(len(consistency_by_method))
colors = [COLORS['primary'], COLORS['secondary']]
bars = axes[1].bar(x_pos, consistency_by_method['mean'], yerr=consistency_by_method['std'],
                   color=colors, edgecolor='white', capsize=5, alpha=0.9)
axes[1].set_xticks(x_pos)
axes[1].set_xticklabels(['Rank', 'Percentage'])
axes[1].set_xlabel('Voting Method')
axes[1].set_ylabel('Consistency Rate (%)')
axes[1].set_title('Consistency Rate by Method')

# 添加数值标签
for bar, val in zip(bars, consistency_by_method['mean']):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3, 
                f'{val:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('figures/Q1_fig1_consistency_analysis.pdf', format='pdf')
print("✓ Q1_fig1_consistency_analysis.pdf")
plt.close()

# ============================================
# Q1_fig2: 不确定性分析（双图）
# ============================================
fig, axes = plt.subplots(1, 2, figsize=FIG_DOUBLE)

# 左图: 确定性分布
axes[0].hist(df_certainty['certainty'], bins=30, color=COLORS['primary'], 
            edgecolor='white', alpha=0.8)
axes[0].axvline(x=df_certainty['certainty'].mean(), color=COLORS['orange'], 
               linestyle='--', linewidth=2, label=f'Mean: {df_certainty["certainty"].mean():.3f}')
axes[0].set_xlabel('Certainty Index')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Distribution of Certainty Index')
add_legend(axes[0])

# 右图: 确定性与评委得分的关系
axes[1].scatter(df_certainty['total_score'], df_certainty['certainty'], 
               c=COLORS['primary'], alpha=0.3, s=20, edgecolors='none')
# 趋势线
z = np.polyfit(df_certainty['total_score'], df_certainty['certainty'], 1)
p = np.poly1d(z)
x_line = np.linspace(df_certainty['total_score'].min(), df_certainty['total_score'].max(), 100)
axes[1].plot(x_line, p(x_line), color=COLORS['orange'], linewidth=2, linestyle='--')

corr = df_certainty['total_score'].corr(df_certainty['certainty'])
axes[1].text(0.95, 0.95, f'r = {corr:.3f}', transform=axes[1].transAxes, 
            fontsize=11, ha='right', va='top',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='lightgray', alpha=0.9))
axes[1].set_xlabel('Judge Total Score')
axes[1].set_ylabel('Certainty Index')
axes[1].set_title('Certainty vs Judge Score')

plt.tight_layout()
plt.savefig('figures/Q1_fig2_uncertainty_analysis.pdf', format='pdf')
print("✓ Q1_fig2_uncertainty_analysis.pdf")
plt.close()

# ============================================
# Q1_fig3: 争议选手分析（四图）
# ============================================
controversial = ['Jerry Rice', 'Billy Ray Cyrus', 'Bristol Palin', 'Bobby Bones']
controversial_data = vote_estimates[vote_estimates['celebrity_name'].isin(controversial)]

fig, axes = plt.subplots(2, 2, figsize=FIG_QUAD)
axes = axes.flatten()

for i, name in enumerate(controversial):
    data = controversial_data[controversial_data['celebrity_name'] == name].sort_values('week')
    if len(data) > 0:
        # 投票份额折线
        axes[i].plot(data['week'], data['estimated_vote_share'], 
                    marker='o', color=COLORS['primary'], linewidth=2, markersize=6,
                    label='Vote Share')
        axes[i].fill_between(data['week'], 0, data['estimated_vote_share'], 
                            color=COLORS['fill_blue'], alpha=0.5)
        
        # 评委排名（右轴）
        ax2 = axes[i].twinx()
        ax2.plot(data['week'], data['judge_rank'], 
                marker='s', color=COLORS['orange'], linewidth=2, 
                markersize=6, linestyle='--', label='Judge Rank')
        ax2.set_ylabel('Judge Rank', color=COLORS['orange'])
        ax2.tick_params(axis='y', labelcolor=COLORS['orange'])
        ax2.invert_yaxis()
        
        axes[i].set_xlabel('Week')
        axes[i].set_ylabel('Vote Share', color=COLORS['primary'])
        axes[i].tick_params(axis='y', labelcolor=COLORS['primary'])
        season = data['season'].iloc[0]
        axes[i].set_title(f'{name} (S{int(season)})')
        
        # 合并图例
        lines1, labels1 = axes[i].get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        axes[i].legend(lines1 + lines2, labels1 + labels2, loc='upper right',
                      frameon=True, fancybox=True, edgecolor='lightgray', fontsize=8)

plt.tight_layout()
plt.savefig('figures/Q1_fig3_controversial_analysis.pdf', format='pdf')
print("✓ Q1_fig3_controversial_analysis.pdf")
plt.close()

# ============================================
# Q1_fig4: 投票与评委得分关系（双图）
# ============================================
fig, axes = plt.subplots(1, 2, figsize=FIG_DOUBLE)

# 左图: 散点图
axes[0].scatter(vote_estimates['total_score'], vote_estimates['estimated_vote_share'], 
               c=COLORS['primary'], alpha=0.3, s=20, edgecolors='none')
# 趋势线
z = np.polyfit(vote_estimates['total_score'], vote_estimates['estimated_vote_share'], 1)
p = np.poly1d(z)
x_line = np.linspace(vote_estimates['total_score'].min(), vote_estimates['total_score'].max(), 100)
axes[0].plot(x_line, p(x_line), color=COLORS['orange'], linewidth=2)

corr_score_vote = vote_estimates['total_score'].corr(vote_estimates['estimated_vote_share'])
axes[0].text(0.95, 0.95, f'r = {corr_score_vote:.3f}\np < 0.001', 
            transform=axes[0].transAxes, fontsize=11, ha='right', va='top',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='lightgray', alpha=0.9))
axes[0].set_xlabel('Judge Total Score')
axes[0].set_ylabel('Estimated Vote Share')
axes[0].set_title('Vote Share vs Judge Score')

# 右图: 人气因子分布
axes[1].hist(vote_estimates['popularity_factor'], bins=30, color=COLORS['secondary'], 
            edgecolor='white', alpha=0.8)
axes[1].axvline(x=0, color=COLORS['neutral'], linestyle='-', linewidth=1)
axes[1].axvline(x=vote_estimates['popularity_factor'].mean(), color=COLORS['orange'], 
               linestyle='--', linewidth=2, label=f'Mean: {vote_estimates["popularity_factor"].mean():.3f}')
axes[1].set_xlabel('Popularity Factor (α)')
axes[1].set_ylabel('Frequency')
axes[1].set_title('Distribution of Popularity Factor')
add_legend(axes[1])

plt.tight_layout()
plt.savefig('figures/Q1_fig4_vote_score_relationship.pdf', format='pdf')
print("✓ Q1_fig4_vote_score_relationship.pdf")
plt.close()

# ============================================
# Q1_fig5: 确定性分布（双图）
# ============================================
fig, axes = plt.subplots(1, 2, figsize=FIG_DOUBLE)

# 左图: 按季的平均确定性
certainty_by_season = df_certainty.groupby('season')['certainty'].mean()
axes[0].plot(certainty_by_season.index, certainty_by_season.values, 
            marker='o', color=COLORS['primary'], linewidth=2, markersize=6)
axes[0].fill_between(certainty_by_season.index, 
                    certainty_by_season.min() - 0.001, certainty_by_season.values, 
                    color=COLORS['fill_blue'], alpha=0.5)
axes[0].axhline(y=df_certainty['certainty'].mean(), color=COLORS['orange'], 
               linestyle='--', linewidth=2, label=f'Mean: {df_certainty["certainty"].mean():.3f}')
axes[0].set_xlabel('Season')
axes[0].set_ylabel('Average Certainty Index')
axes[0].set_title('Certainty by Season')
add_legend(axes[0])

# 右图: 按周的平均确定性
certainty_by_week = df_certainty.groupby('week')['certainty'].agg(['mean', 'std'])
axes[1].errorbar(certainty_by_week.index, certainty_by_week['mean'], 
                yerr=certainty_by_week['std'], marker='o', color=COLORS['secondary'], 
                linewidth=2, markersize=6, capsize=3)
axes[1].set_xlabel('Week')
axes[1].set_ylabel('Average Certainty Index')
axes[1].set_title('Certainty by Week')

plt.tight_layout()
plt.savefig('figures/Q1_fig5_certainty_distribution.pdf', format='pdf')
print("✓ Q1_fig5_certainty_distribution.pdf")
plt.close()

# ============================================
# Q1_fig6: 争议选手整体分析（三图）
# ============================================
# 计算争议度
df_summary_copy = df_summary.copy()
df_summary_copy['judge_rank'] = df_summary_copy.groupby('season')['total_score_mean'].rank(ascending=False, method='min')
df_summary_copy['controversy_score'] = df_summary_copy['judge_rank'] - df_summary_copy['placement']
controversial_all = df_summary_copy[df_summary_copy['controversy_score'] >= 3].copy()
normal_all = df_summary_copy[df_summary_copy['controversy_score'] < 3].copy()

fig, axes = plt.subplots(1, 3, figsize=FIG_TRIPLE)

# 左图: 最终排名分布
ax = axes[0]
bins = np.arange(0.5, 14.5, 1)
ax.hist(controversial_all['placement'], bins=bins, alpha=0.7, 
        label=f'Controversial (n={len(controversial_all)})', 
        color=COLORS['orange'], edgecolor='white')
ax.hist(normal_all['placement'], bins=bins, alpha=0.5, 
        label=f'Normal (n={len(normal_all)})', 
        color=COLORS['primary'], edgecolor='white')
ax.axvline(controversial_all['placement'].mean(), color=COLORS['orange'], linestyle='--', linewidth=2)
ax.axvline(normal_all['placement'].mean(), color=COLORS['primary'], linestyle='--', linewidth=2)
ax.set_xlabel('Final Placement')
ax.set_ylabel('Count')
ax.set_title('Placement Distribution')
add_legend(ax, fontsize=8)

# 中图: 裁判分数对比箱线图
ax = axes[1]
bp = ax.boxplot([controversial_all['total_score_mean'].dropna(), normal_all['total_score_mean'].dropna()], 
                tick_labels=['Controversial', 'Normal'], patch_artist=True)
bp['boxes'][0].set_facecolor(COLORS['fill_orange'])
bp['boxes'][1].set_facecolor(COLORS['fill_blue'])
bp['boxes'][0].set_edgecolor(COLORS['orange'])
bp['boxes'][1].set_edgecolor(COLORS['primary'])
ax.set_ylabel('Average Judge Score')
ax.set_title('Judge Score Comparison')
# 添加均值点
for i, data in enumerate([controversial_all['total_score_mean'], normal_all['total_score_mean']]):
    ax.scatter(i+1, data.mean(), color=COLORS['red'], s=80, zorder=5, marker='D')
    ax.annotate(f'{data.mean():.1f}', (i+1, data.mean()), xytext=(10, 5), 
               textcoords='offset points', fontsize=9)

# 右图: 争议度分布
ax = axes[2]
controversy_counts = controversial_all['controversy_score'].value_counts().sort_index()
bars = ax.bar(controversy_counts.index, controversy_counts.values, 
              color=COLORS['secondary'], edgecolor='white')
ax.set_xlabel('Controversy Score')
ax.set_ylabel('Number of Contestants')
ax.set_title('Controversy Score Distribution')
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width()/2, height),
                xytext=(0, 3), textcoords='offset points', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('figures/Q1_fig6_controversial_group.pdf', format='pdf')
print("✓ Q1_fig6_controversial_group.pdf")
plt.close()

# ============================================
# 完成
# ============================================
print("\n" + "="*50)
print("问题一图表生成完成！")
print("="*50)
print("生成的文件：")
print("  - Q1_fig1_consistency_analysis.pdf")
print("  - Q1_fig2_uncertainty_analysis.pdf")
print("  - Q1_fig3_controversial_analysis.pdf")
print("  - Q1_fig4_vote_score_relationship.pdf")
print("  - Q1_fig5_certainty_distribution.pdf")
print("  - Q1_fig6_controversial_group.pdf")
