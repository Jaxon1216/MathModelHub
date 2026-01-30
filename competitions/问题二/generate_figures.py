# =============================================================================
# 问题二：投票方法比较 - 配图生成脚本
# =============================================================================

import sys
sys.path.append('..')
from figure_style import *
import pandas as pd
import numpy as np
import os

os.makedirs('figures', exist_ok=True)

# =============================================================================
# 数据加载
# =============================================================================
print("加载数据...")
df_long = pd.read_csv('../数据预处理/data_long_format.csv')
method_diff = pd.read_csv('method_comparison.csv')
tiebreaker_analysis = pd.read_csv('tiebreaker_analysis.csv')
controversial_data = pd.read_csv('controversial_analysis.csv')

print(f"  方法比较数据: {len(method_diff)} 条")

# =============================================================================
# 图1: 方法比较 (Method Comparison)
# =============================================================================
print("\n生成图1: 方法比较...")

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

# 1a: 按季一致性 - 使用折线图替代密集柱状图
ax1 = axes[0]
consistency_by_season = method_diff.groupby('season')['same_method_result'].mean() * 100

# 使用折线图+散点，更清晰
ax1.plot(consistency_by_season.index, consistency_by_season.values,
         color='#3498DB', linewidth=2, marker='o', markersize=5,
         markerfacecolor='white', markeredgecolor='#3498DB', markeredgewidth=1.5)
ax1.fill_between(consistency_by_season.index, consistency_by_season.values, 
                 alpha=0.15, color='#3498DB')
ax1.axhline(y=consistency_by_season.mean(), color='#E74C3C', 
            linestyle='--', linewidth=2, label=f'Mean = {consistency_by_season.mean():.1f}%')
ax1.set_xlabel('Season')
ax1.set_ylabel('Method Agreement Rate (%)')
ax1.set_ylim(75, 105)
ax1.legend(loc='lower right', fontsize=10)
add_grid(ax1, axis='both')
add_subplot_label(ax1, 'a')
ax1.set_xticks([1, 5, 10, 15, 20, 25, 30, 34])

# 1b: 方法差异分布
ax2 = axes[1]
# 计算两种方法的结果差异情况
agree_count = method_diff['same_method_result'].sum()
disagree_count = len(method_diff) - agree_count
total = len(method_diff)

categories = ['Agree\n(Same Elimination)', 'Disagree\n(Different Elimination)']
values = [agree_count/total*100, disagree_count/total*100]
colors_bar = [COLORS['positive'], COLORS['negative']]

bars2 = ax2.bar(categories, values, color=colors_bar, edgecolor='black', linewidth=0.5)

# 标注数值
for bar, val, count in zip(bars2, values, [agree_count, disagree_count]):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             f'{val:.1f}%\n(n={count})', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax2.set_ylabel('Percentage of Weeks (%)')
ax2.set_ylim(0, 110)
add_grid(ax2, axis='y')
add_subplot_label(ax2, 'b')

plt.tight_layout()
save_figure(fig, 'figures/fig1_method_comparison')
plt.close()

print(f"  ✓ 总体一致率: {agree_count/total*100:.1f}%")

# =============================================================================
# 图2: 争议选手两种方法对比 (Controversial Contestants)
# =============================================================================
print("\n生成图2: 争议选手方法对比...")

controversial = ['Jerry Rice', 'Billy Ray Cyrus', 'Bristol Palin', 'Bobby Bones']

# 获取详细周数据
df_long_cont = df_long[df_long['celebrity_name'].isin(controversial)].copy()

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes = axes.flatten()

panel_labels = ['a', 'b', 'c', 'd']

for i, name in enumerate(controversial):
    ax = axes[i]
    data = df_long_cont[df_long_cont['celebrity_name'] == name].sort_values('week')
    
    if len(data) > 0:
        weeks = data['week'].values
        
        # 计算两种方法下的位置百分位
        # 使用judge_rank作为代理
        judge_ranks = data['judge_rank'].values
        n_contestants = data['contestants_this_week'].values
        
        # Rank方法百分位 (排名/总人数)
        rank_pct = judge_ranks / n_contestants * 100
        
        # 画两条线对比
        ax.plot(weeks, rank_pct, color=COLORS['rank_method'], marker='o',
               linewidth=LINE_WIDTH['default'], markersize=MARKER_SIZE['default'],
               label='Rank Position %', linestyle=LINE_STYLES['rank_method'])
        
        # 添加淘汰线
        ax.axhline(y=100, color=COLORS['highlight'], linestyle=':', alpha=0.7)
        ax.fill_between(weeks, rank_pct, 100, where=(rank_pct > 80), 
                       alpha=0.2, color=COLORS['highlight'])
        
        ax.set_xlabel('Week')
        ax.set_ylabel('Position Percentile (%)')
        ax.set_title(name, fontsize=11, fontweight='bold', pad=8)
        ax.set_ylim(0, 105)
        add_grid(ax, axis='y', alpha=0.3)
        add_subplot_label(ax, panel_labels[i])

plt.tight_layout()
save_figure(fig, 'figures/fig2_controversial_methods')
plt.close()

print(f"  ✓ 分析了 {len(controversial)} 位争议选手")

# =============================================================================
# 图3: 评委打破平局分析 (Tiebreaker Analysis)
# =============================================================================
print("\n生成图3: 评委打破平局分析...")

fig, axes = plt.subplots(1, 2, figsize=FIG_SIZES['double'])

# 3a: 按季tiebreaker影响
ax1 = axes[0]
tb_by_season = tiebreaker_analysis.groupby('season')['tiebreaker_changes_result'].mean() * 100
bars = ax1.bar(tb_by_season.index, tb_by_season.values,
               color=COLORS['dwvs'], edgecolor='black', linewidth=0.5, alpha=0.85)
ax1.axhline(y=tb_by_season.mean(), color=COLORS['highlight'], linestyle='--',
            linewidth=1.5, label=f'Mean={tb_by_season.mean():.1f}%')
ax1.set_xlabel('Season')
ax1.set_ylabel('Tiebreaker Impact Rate (%)')
ax1.legend(loc='upper right')
add_grid(ax1, axis='y')
add_subplot_label(ax1, 'a')
format_axis_ticks(ax1, axis='x', interval=5)

# 3b: 总体影响分布
ax2 = axes[1]
impact_count = tiebreaker_analysis['tiebreaker_changes_result'].sum()
no_impact_count = len(tiebreaker_analysis) - impact_count
total = len(tiebreaker_analysis)

categories = ['No Change', 'Changed Result']
values = [no_impact_count/total*100, impact_count/total*100]
colors_bar = [COLORS['neutral'], COLORS['dwvs']]

bars2 = ax2.bar(categories, values, color=colors_bar, edgecolor='black', linewidth=0.5)

for bar, val, count in zip(bars2, values, [no_impact_count, impact_count]):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             f'{val:.1f}%\n(n={count})', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax2.set_ylabel('Percentage of Weeks (%)')
ax2.set_ylim(0, 110)
add_grid(ax2, axis='y')
add_subplot_label(ax2, 'b')

plt.tight_layout()
save_figure(fig, 'figures/fig3_tiebreaker_analysis')
plt.close()

print(f"  ✓ Tiebreaker改变结果比例: {impact_count/total*100:.1f}%")

# =============================================================================
# 汇总
# =============================================================================
print("\n" + "="*60)
print("【问题二配图生成完成】")
print("="*60)
print(f"生成的图片:")
for i, name in enumerate(['fig1_method_comparison.pdf',
                          'fig2_controversial_methods.pdf',
                          'fig3_tiebreaker_analysis.pdf'], 1):
    print(f"  {i}. figures/{name}")
print("="*60)
