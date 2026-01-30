"""
问题二：图片导出脚本
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style='whitegrid')

FIGURE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/figures'
os.makedirs(FIGURE_DIR, exist_ok=True)

COLORS = {
    'primary': '#4682B4',
    'secondary': '#FF7F50',
    'accent': '#228B22',
    'neutral': '#708090'
}

def save_fig(fig, filename):
    filepath = os.path.join(FIGURE_DIR, filename)
    fig.savefig(filepath, bbox_inches='tight', facecolor='white')
    print(f"✅ 已保存: {filepath}")
    plt.close(fig)

# 读取数据
comparison_df = pd.read_csv('method_comparison.csv')
controversy_df = pd.read_csv('controversial_analysis.csv')
tiebreaker_df = pd.read_csv('tiebreaker_analysis.csv')
bias_df = pd.read_csv('bias_analysis.csv')

agreement_rate = comparison_df['methods_agree'].mean()

# ============================================================
# 图1: 两种方式比较
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ax1 = axes[0]
ax1.hist(bias_df['rank_bias'], bins=20, alpha=0.6, label='Rank-based', color=COLORS['primary'])
ax1.hist(bias_df['pct_bias'], bins=20, alpha=0.6, label='Percentage-based', color=COLORS['secondary'])
ax1.axvline(0, color='black', linestyle='--', linewidth=1)
ax1.axvline(bias_df['rank_bias'].mean(), color=COLORS['primary'], linestyle='-', linewidth=2)
ax1.axvline(bias_df['pct_bias'].mean(), color=COLORS['secondary'], linestyle='-', linewidth=2)
ax1.set_xlabel('Bias Score (positive = favors judges)')
ax1.set_ylabel('Frequency')
ax1.legend()

ax2 = axes[1]
agreement_by_season = comparison_df.groupby('season')['methods_agree'].mean()
ax2.bar(agreement_by_season.index, agreement_by_season.values, color=COLORS['primary'])
ax2.axhline(agreement_rate, color='red', linestyle='--', label=f'Overall: {agreement_rate:.1%}')
ax2.set_xlabel('Season')
ax2.set_ylabel('Agreement Rate')
ax2.set_ylim(0, 1.1)
ax2.legend()

plt.tight_layout()
save_fig(fig, 'fig1_method_comparison.pdf')

# ============================================================
# 图2: 争议选手分析
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))

x = np.arange(len(controversy_df))
width = 0.35

bars1 = ax.bar(x - width/2, controversy_df['rank_would_eliminate'], width,
               label='Rank-based', color=COLORS['primary'])
bars2 = ax.bar(x + width/2, controversy_df['pct_would_eliminate'], width,
               label='Percentage-based', color=COLORS['secondary'])

ax.set_xlabel('Controversial Contestants')
ax.set_ylabel('Weeks Would Be Eliminated')
ax.set_xticks(x)
ax.set_xticklabels([f"{row['contestant']}\n(S{row['season']})" 
                    for _, row in controversy_df.iterrows()])
ax.legend()

plt.tight_layout()
save_fig(fig, 'fig2_controversial_methods.pdf')

# ============================================================
# 图3: 评委决胜规则分析
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ax1 = axes[0]
change_by_season_rank = tiebreaker_df.groupby('season')['rank_changed'].mean()
change_by_season_pct = tiebreaker_df.groupby('season')['pct_changed'].mean()

x = np.arange(len(change_by_season_rank))
width = 0.35
ax1.bar(x - width/2, change_by_season_rank.values, width, label='Rank-based', color=COLORS['primary'], alpha=0.7)
ax1.bar(x + width/2, change_by_season_pct.values, width, label='Percentage-based', color=COLORS['secondary'], alpha=0.7)
ax1.set_xlabel('Season')
ax1.set_ylabel('Change Rate with Judge Tiebreaker')
ax1.set_xticks(x[::5])
ax1.set_xticklabels(change_by_season_rank.index[::5])
ax1.legend()

ax2 = axes[1]
methods = ['Rank\nOriginal', 'Rank +\nTiebreaker', 'Pct\nOriginal', 'Pct +\nTiebreaker']
rank_orig_correct = (tiebreaker_df['rank_original'] == tiebreaker_df['actual_eliminated']).mean()
rank_tb_correct = (tiebreaker_df['rank_with_tiebreaker'] == tiebreaker_df['actual_eliminated']).mean()
pct_orig_correct = (tiebreaker_df['pct_original'] == tiebreaker_df['actual_eliminated']).mean()
pct_tb_correct = (tiebreaker_df['pct_with_tiebreaker'] == tiebreaker_df['actual_eliminated']).mean()

values = [rank_orig_correct, rank_tb_correct, pct_orig_correct, pct_tb_correct]
colors_list = [COLORS['primary'], COLORS['primary'], COLORS['secondary'], COLORS['secondary']]
alphas = [0.6, 1.0, 0.6, 1.0]

bars = ax2.bar(methods, values, color=colors_list)
for bar, alpha in zip(bars, alphas):
    bar.set_alpha(alpha)
ax2.set_ylabel('Consistency with Actual Elimination')
ax2.set_ylim(0, 1.0)

plt.tight_layout()
save_fig(fig, 'fig3_tiebreaker_analysis.pdf')

# ============================================================
print("\n" + "=" * 60)
print("🎉 所有图片导出完成！")
print("=" * 60)
print(f"\n图片保存在: {FIGURE_DIR}")
for f in sorted(os.listdir(FIGURE_DIR)):
    print(f"  - {f}")
