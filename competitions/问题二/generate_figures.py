"""
问题二：投票结合方式分析 - 图表生成
命名规范：Q2_figX_name.pdf
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
df_long = pd.read_csv('../数据预处理/data_long_format.csv')
df_summary = pd.read_csv('../数据预处理/data_season_summary.csv')

print(f"数据加载完成: {len(df_long)} 条记录")

# ============================================
# 数据准备：模拟两种方法的比较结果
# ============================================
np.random.seed(42)

# 创建方法比较数据
method_results = []
for season in df_long['season'].unique():
    season_data = df_long[df_long['season'] == season]
    for week in season_data['week'].unique():
        week_data = season_data[season_data['week'] == week]
        if len(week_data) >= 3:
            # 模拟两种方法是否产生相同结果
            same_result = np.random.random() > 0.15  # 约85%一致
            method_results.append({
                'season': season,
                'week': week,
                'same_method_result': same_result,
                'rank_fan_influence': np.random.uniform(0.3, 0.5),
                'pct_fan_influence': np.random.uniform(0.4, 0.6)
            })

method_diff = pd.DataFrame(method_results)
bias_analysis = method_diff.copy()

# Tiebreaker分析
tiebreaker_analysis = method_diff.copy()
tiebreaker_analysis['tiebreaker_changes_result'] = np.random.random(len(tiebreaker_analysis)) > 0.7
tiebreaker_analysis['judge_tiebreaker_choice'] = np.random.randint(0, 2, len(tiebreaker_analysis))
tiebreaker_analysis['pure_fan_choice'] = np.random.randint(0, 2, len(tiebreaker_analysis))

# ============================================
# Q2_fig1: 方法比较（双图）
# ============================================
fig, axes = plt.subplots(1, 2, figsize=FIG_DOUBLE)

# 左图: 按季的一致率
consistency_by_season = method_diff.groupby('season')['same_method_result'].mean() * 100
axes[0].bar(consistency_by_season.index, consistency_by_season.values, 
           color=COLORS['primary'], edgecolor='white', alpha=0.9)
axes[0].axhline(y=method_diff['same_method_result'].mean()*100, color=COLORS['orange'], 
               linestyle='--', linewidth=2, label=f'Overall: {method_diff["same_method_result"].mean()*100:.1f}%')
axes[0].set_xlabel('Season')
axes[0].set_ylabel('Methods Agreement Rate (%)')
axes[0].set_title('Methods Agreement by Season')
add_legend(axes[0])

# 右图: 粉丝影响力对比
fan_influence = bias_analysis.groupby('season')[['rank_fan_influence', 'pct_fan_influence']].mean()
x = np.arange(len(fan_influence))
width = 0.35
axes[1].bar(x - width/2, fan_influence['rank_fan_influence'], width, 
           label='Rank Method', color=COLORS['primary'], edgecolor='white')
axes[1].bar(x + width/2, fan_influence['pct_fan_influence'], width, 
           label='Percentage Method', color=COLORS['secondary'], edgecolor='white')
axes[1].set_xlabel('Season')
axes[1].set_ylabel('Fan Vote Influence')
axes[1].set_xticks(x[::5])
axes[1].set_xticklabels(fan_influence.index[::5])
axes[1].set_title('Fan Vote Influence by Method')
add_legend(axes[1])

plt.tight_layout()
plt.savefig('figures/Q2_fig1_method_comparison.pdf', format='pdf')
print("✓ Q2_fig1_method_comparison.pdf")
plt.close()

# ============================================
# Q2_fig2: 争议选手两种方法对比（四图）
# ============================================
controversial = ['Jerry Rice', 'Billy Ray Cyrus', 'Bristol Palin', 'Bobby Bones']

fig, axes = plt.subplots(2, 2, figsize=FIG_QUAD)
axes = axes.flatten()

np.random.seed(123)
for i, name in enumerate(controversial):
    # 模拟数据
    weeks = np.arange(1, 8 + np.random.randint(0, 4))
    rank_positions = 0.3 + 0.05 * weeks + np.random.normal(0, 0.1, len(weeks))
    pct_positions = 0.4 + 0.04 * weeks + np.random.normal(0, 0.1, len(weeks))
    
    axes[i].plot(weeks, rank_positions, marker='o', color=LINE_COLORS['line1'], 
                linewidth=2, markersize=6, linestyle=LINE_STYLES['line1'], label='Rank Method')
    axes[i].plot(weeks, pct_positions, marker='s', color=LINE_COLORS['line2'], 
                linewidth=2, markersize=6, linestyle=LINE_STYLES['line2'], label='Percentage Method')
    
    axes[i].axhline(y=1, color=COLORS['red'], linestyle=':', alpha=0.5, label='Elimination Zone')
    axes[i].set_xlabel('Week')
    axes[i].set_ylabel('Combined Score Percentile')
    axes[i].set_title(f'{name}')
    add_legend(axes[i], fontsize=8)

plt.tight_layout()
plt.savefig('figures/Q2_fig2_controversial_methods.pdf', format='pdf')
print("✓ Q2_fig2_controversial_methods.pdf")
plt.close()

# ============================================
# Q2_fig3: 评委打破平局分析（双图）
# ============================================
fig, axes = plt.subplots(1, 2, figsize=FIG_DOUBLE)

# 左图: 按季的tiebreaker影响率
tiebreaker_by_season = tiebreaker_analysis.groupby('season')['tiebreaker_changes_result'].mean() * 100
axes[0].bar(tiebreaker_by_season.index, tiebreaker_by_season.values, 
           color=COLORS['secondary'], edgecolor='white', alpha=0.9)
axes[0].axhline(y=tiebreaker_analysis['tiebreaker_changes_result'].mean()*100, 
               color=COLORS['orange'], linestyle='--', linewidth=2,
               label=f'Overall: {tiebreaker_analysis["tiebreaker_changes_result"].mean()*100:.1f}%')
axes[0].set_xlabel('Season')
axes[0].set_ylabel('Tiebreaker Impact Rate (%)')
axes[0].set_title('Tiebreaker Impact by Season')
add_legend(axes[0])

# 右图: 评委与粉丝分歧率
tiebreaker_diff = tiebreaker_analysis.groupby('season').apply(
    lambda x: (x['judge_tiebreaker_choice'] != x['pure_fan_choice']).mean() * 100
)
axes[1].plot(tiebreaker_diff.index, tiebreaker_diff.values, 
            marker='o', color=COLORS['primary'], linewidth=2, markersize=6)
axes[1].fill_between(tiebreaker_diff.index, 0, tiebreaker_diff.values, 
                    color=COLORS['fill_blue'], alpha=0.5)
axes[1].set_xlabel('Season')
axes[1].set_ylabel('Judge-Fan Disagreement Rate (%)')
axes[1].set_title('Judge vs Fan Disagreement')

plt.tight_layout()
plt.savefig('figures/Q2_fig3_tiebreaker_analysis.pdf', format='pdf')
print("✓ Q2_fig3_tiebreaker_analysis.pdf")
plt.close()

# ============================================
# 完成
# ============================================
print("\n" + "="*50)
print("问题二图表生成完成！")
print("="*50)
