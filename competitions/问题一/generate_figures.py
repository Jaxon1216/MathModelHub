# =============================================================================
# 问题一：粉丝投票估算模型 - 配图生成脚本
# =============================================================================
# 使用统一样式配置生成所有图表
# =============================================================================

import sys
sys.path.append('..')
from figure_style import *
import pandas as pd
import numpy as np
from scipy import stats
import os

os.makedirs('figures', exist_ok=True)

# =============================================================================
# 数据加载
# =============================================================================
print("加载数据...")
df_long = pd.read_csv('../数据预处理/data_long_format.csv')
vote_estimates = pd.read_csv('vote_estimates.csv')
consistency = pd.read_csv('verification_results.csv')
certainty = pd.read_csv('certainty_metrics.csv')

print(f"  投票估算数据: {len(vote_estimates)} 条")
print(f"  一致性验证数据: {len(consistency)} 条")
print(f"  确定性指标数据: {len(certainty)} 条")

# =============================================================================
# 图1: 一致性分析 (Consistency Analysis)
# =============================================================================
print("\n生成图1: 一致性分析...")

fig, axes = plt.subplots(1, 2, figsize=FIG_SIZES['double'])

# 1a: 按季一致性 (Season-wise Consistency)
consistency_by_season = consistency.groupby('season')['is_consistent'].mean() * 100
ax1 = axes[0]
bars1 = ax1.bar(consistency_by_season.index, consistency_by_season.values, 
                color=COLORS['rank_method'], edgecolor='black', linewidth=0.5, alpha=0.85)
ax1.set_xlabel('Season')
ax1.set_ylabel('Consistency Rate (%)')
add_grid(ax1, axis='y')
add_subplot_label(ax1, 'a')

# 标注关键数据点 - 最高一致性
max_idx = consistency_by_season.idxmax()
max_val = consistency_by_season.max()
if max_val > 0:
    highlight_point(ax1, max_idx, max_val, f'{max_val:.1f}%', offset=(5, 8))

# 设置x轴刻度间隔
format_axis_ticks(ax1, axis='x', interval=5)

# 1b: 按投票方法对比 (Method Comparison)
ax2 = axes[1]
method_consistency = consistency.groupby('method')['is_consistent'].mean() * 100

# 确保顺序一致
methods = ['rank', 'percentage']
method_labels = ['Rank-Based', 'Percentage-Based']
values = [method_consistency.get('rank', 0), method_consistency.get('percentage', 0)]
colors = [COLORS['rank_method'], COLORS['pct_method']]

bars2 = ax2.bar(method_labels, values, color=colors, edgecolor='black', linewidth=0.5)

# 在柱状图上标注数值
for bar, val in zip(bars2, values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
             f'{val:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax2.set_xlabel('Voting Method')
ax2.set_ylabel('Consistency Rate (%)')
ax2.set_ylim(0, max(values) * 1.2 + 5)
add_grid(ax2, axis='y')
add_subplot_label(ax2, 'b')

plt.tight_layout()
save_figure(fig, 'figures/fig1_consistency_analysis')
plt.close()

print(f"  ✓ Rank方法一致性: {values[0]:.1f}%")
print(f"  ✓ Percentage方法一致性: {values[1]:.1f}%")

# =============================================================================
# 图2: 不确定性分析 (Uncertainty Analysis)
# =============================================================================
print("\n生成图2: 不确定性分析...")

fig, axes = plt.subplots(1, 2, figsize=FIG_SIZES['double'])

# 2a: 确定性分布直方图
ax1 = axes[0]
ax1.hist(certainty['certainty'], bins=30, color=COLORS['positive'], 
         edgecolor='black', linewidth=0.5, alpha=0.85)
ax1.set_xlabel('Certainty Index')
ax1.set_ylabel('Frequency')
add_grid(ax1, axis='y')
add_subplot_label(ax1, 'a')

# 标注均值
mean_cert = certainty['certainty'].mean()
add_reference_line(ax1, mean_cert, axis='x', color=COLORS['highlight'], 
                   linestyle='--', label=f'Mean={mean_cert:.3f}')
ax1.legend(loc='upper left')

# 2b: 确定性 vs 评委总分
ax2 = axes[1]
# certainty数据已包含total_score
ax2.scatter(certainty['total_score'], certainty['certainty'],
           c=COLORS['rank_method'], alpha=0.4, s=25, edgecolors='none')

# 添加趋势线
valid_data = certainty.dropna(subset=['total_score', 'certainty'])
if len(valid_data) > 2:
    z = np.polyfit(valid_data['total_score'], valid_data['certainty'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(valid_data['total_score'].min(), valid_data['total_score'].max(), 100)
    ax2.plot(x_line, p(x_line), color=COLORS['highlight'], linewidth=2, linestyle='--',
             label=f'Trend')

ax2.set_xlabel('Judge Total Score')
ax2.set_ylabel('Certainty Index')
add_grid(ax2, axis='both')
add_subplot_label(ax2, 'b')

# 计算相关性并标注
corr = valid_data['total_score'].corr(valid_data['certainty'])
ax2.text(0.95, 0.05, f'r = {corr:.3f}', transform=ax2.transAxes, 
         fontsize=10, ha='right', va='bottom',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
save_figure(fig, 'figures/fig2_uncertainty_analysis')
plt.close()

print(f"  ✓ 平均确定性指数: {mean_cert:.3f}")
print(f"  ✓ 确定性与评分相关性: r={corr:.3f}")

# =============================================================================
# 图3: 争议选手分析 (Controversial Contestant Analysis)
# =============================================================================
print("\n生成图3: 争议选手分析...")

controversial = ['Jerry Rice', 'Billy Ray Cyrus', 'Bristol Palin', 'Bobby Bones']
controversial_data = vote_estimates[vote_estimates['celebrity_name'].isin(controversial)]

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes = axes.flatten()

panel_labels = ['a', 'b', 'c', 'd']
highlight_colors = [COLORS['cat1'], COLORS['cat2'], COLORS['cat3'], COLORS['cat6']]

for i, name in enumerate(controversial):
    ax = axes[i]
    data = controversial_data[controversial_data['celebrity_name'] == name].sort_values('week')
    
    if len(data) > 0:
        # 投票份额 (左Y轴)
        color1 = highlight_colors[i]
        ax.plot(data['week'], data['estimated_vote_share'] * 100, 
               color=color1, marker='o', linewidth=LINE_WIDTH['default'],
               markersize=MARKER_SIZE['default'], label='Vote Share')
        ax.set_xlabel('Week')
        ax.set_ylabel('Vote Share (%)', color=color1)
        ax.tick_params(axis='y', labelcolor=color1)
        
        # 评委排名 (右Y轴)
        ax2 = ax.twinx()
        ax2.plot(data['week'], data['judge_rank'], 
                color=COLORS['neutral'], marker='s', linestyle='--',
                linewidth=LINE_WIDTH['thin'], markersize=MARKER_SIZE['small'],
                label='Judge Rank')
        ax2.set_ylabel('Judge Rank', color=COLORS['neutral'])
        ax2.tick_params(axis='y', labelcolor=COLORS['neutral'])
        ax2.invert_yaxis()  # 排名越小越好
        
        # 标题和子图标签
        ax.set_title(name, fontsize=11, fontweight='bold', pad=10)
        add_subplot_label(ax, panel_labels[i])
        
        # 添加网格
        add_grid(ax, axis='y', alpha=0.3)

plt.tight_layout()
save_figure(fig, 'figures/fig3_controversial_analysis')
plt.close()

print(f"  ✓ 分析了 {len(controversial)} 位争议选手")

# =============================================================================
# 图4: 投票与评委得分关系 (Vote-Score Relationship)
# =============================================================================
print("\n生成图4: 投票与评委得分关系...")

fig, axes = plt.subplots(1, 2, figsize=FIG_SIZES['double'])

# 4a: 散点图 + 趋势线
ax1 = axes[0]
ax1.scatter(vote_estimates['total_score'], vote_estimates['estimated_vote_share'],
           c=COLORS['rank_method'], alpha=0.3, s=20, edgecolors='none')

# 趋势线
valid = vote_estimates.dropna(subset=['total_score', 'estimated_vote_share'])
z = np.polyfit(valid['total_score'], valid['estimated_vote_share'], 1)
p = np.poly1d(z)
x_line = np.linspace(valid['total_score'].min(), valid['total_score'].max(), 100)
ax1.plot(x_line, p(x_line), color=COLORS['highlight'], linewidth=2.5, linestyle='--')

# 相关性标注
corr = valid['total_score'].corr(valid['estimated_vote_share'])
ax1.text(0.05, 0.95, f'r = {corr:.3f}', transform=ax1.transAxes,
         fontsize=11, va='top',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax1.set_xlabel('Judge Total Score')
ax1.set_ylabel('Estimated Vote Share')
add_grid(ax1, axis='both')
add_subplot_label(ax1, 'a')

# 4b: popularity factor 分布
ax2 = axes[1]
# 普通选手 vs 争议选手
normal_alpha = vote_estimates[~vote_estimates['celebrity_name'].isin(controversial)]['popularity_factor']
controversial_alpha = vote_estimates[vote_estimates['celebrity_name'].isin(controversial)]['popularity_factor']

ax2.hist(normal_alpha, bins=30, color=COLORS['rank_method'], alpha=0.7, 
         edgecolor='black', linewidth=0.5, label='Normal Contestants')
ax2.hist(controversial_alpha, bins=15, color=COLORS['highlight'], alpha=0.7,
         edgecolor='black', linewidth=0.5, label='Controversial')

ax2.set_xlabel('Popularity Factor (α)')
ax2.set_ylabel('Frequency')
ax2.legend(loc='upper right')
add_grid(ax2, axis='y')
add_subplot_label(ax2, 'b')

plt.tight_layout()
save_figure(fig, 'figures/fig4_vote_score_relationship')
plt.close()

print(f"  ✓ 投票-评分相关性: r={corr:.3f}")

# =============================================================================
# 图5: 确定性分布 (Certainty Distribution)
# =============================================================================
print("\n生成图5: 确定性分布...")

fig, axes = plt.subplots(1, 2, figsize=FIG_SIZES['double'])

# 5a: 按季确定性
ax1 = axes[0]
certainty_by_season = certainty.groupby('season')['certainty'].mean()
ax1.plot(certainty_by_season.index, certainty_by_season.values,
        color=COLORS['positive'], marker='o', linewidth=LINE_WIDTH['default'],
        markersize=MARKER_SIZE['default'])
ax1.fill_between(certainty_by_season.index, certainty_by_season.values,
                alpha=0.3, color=COLORS['positive'])
ax1.set_xlabel('Season')
ax1.set_ylabel('Average Certainty Index')
add_grid(ax1, axis='y')
add_subplot_label(ax1, 'a')
format_axis_ticks(ax1, axis='x', interval=5)

# 5b: 按周确定性
ax2 = axes[1]
certainty_by_week = certainty.groupby('week')['certainty'].agg(['mean', 'std'])
ax2.errorbar(certainty_by_week.index, certainty_by_week['mean'],
            yerr=certainty_by_week['std'], color=COLORS['rank_method'],
            marker='o', linewidth=LINE_WIDTH['default'], capsize=3,
            markersize=MARKER_SIZE['default'])
ax2.set_xlabel('Week')
ax2.set_ylabel('Average Certainty Index')
add_grid(ax2, axis='y')
add_subplot_label(ax2, 'b')

plt.tight_layout()
save_figure(fig, 'figures/fig5_certainty_distribution')
plt.close()

print(f"  ✓ 生成完毕")

# =============================================================================
# 汇总
# =============================================================================
print("\n" + "="*60)
print("【问题一配图生成完成】")
print("="*60)
print(f"生成的图片:")
for i, name in enumerate(['fig1_consistency_analysis.pdf',
                          'fig2_uncertainty_analysis.pdf',
                          'fig3_controversial_analysis.pdf',
                          'fig4_vote_score_relationship.pdf',
                          'fig5_certainty_distribution.pdf'], 1):
    print(f"  {i}. figures/{name}")
print("="*60)
