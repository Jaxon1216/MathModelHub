"""
问题二图片导出脚本
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams.update({
    'font.family': 'Arial', 'font.size': 11,
    'axes.spines.top': False, 'axes.spines.right': False,
    'figure.dpi': 300, 'savefig.dpi': 300,
})

COLORS = {'primary': '#2E5B88', 'secondary': '#E85D4C', 'tertiary': '#4A9B7F', 'light': '#B8D4E8'}
FIG_DOUBLE = (10, 4)

FIGURE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/figures'
os.makedirs(FIGURE_DIR, exist_ok=True)

def save_fig(fig, filename):
    filepath = os.path.join(FIGURE_DIR, filename)
    fig.savefig(filepath, bbox_inches='tight', facecolor='white')
    print(f"✅ 已保存: {filepath}")
    plt.close(fig)

# 加载数据
method_diff = pd.read_csv('method_comparison.csv')
bias_analysis = pd.read_csv('bias_analysis.csv')
tiebreaker_analysis = pd.read_csv('tiebreaker_analysis.csv')

# 图1
fig, axes = plt.subplots(1, 2, figsize=FIG_DOUBLE)
consistency_by_season = method_diff.groupby('season')['same_method_result'].mean() * 100
axes[0].bar(consistency_by_season.index, consistency_by_season.values, color=COLORS['primary'], edgecolor='black')
axes[0].set_xlabel('Season')
axes[0].set_ylabel('Methods Agreement Rate (%)')
axes[0].text(0.02, 0.98, '(a)', transform=axes[0].transAxes, fontsize=12, fontweight='bold', va='top')

fan_influence = bias_analysis.groupby('season')[['rank_fan_influence', 'pct_fan_influence']].mean()
x = np.arange(len(fan_influence))
width = 0.35
axes[1].bar(x - width/2, fan_influence['rank_fan_influence'], width, label='Rank', color=COLORS['primary'])
axes[1].bar(x + width/2, fan_influence['pct_fan_influence'], width, label='Percentage', color=COLORS['secondary'])
axes[1].set_xlabel('Season')
axes[1].set_ylabel('Fan Vote Influence')
axes[1].legend()
axes[1].text(0.02, 0.98, '(b)', transform=axes[1].transAxes, fontsize=12, fontweight='bold', va='top')
plt.tight_layout()
save_fig(fig, 'fig1_method_comparison.pdf')

# 图3
fig, axes = plt.subplots(1, 2, figsize=FIG_DOUBLE)
tb_by_season = tiebreaker_analysis.groupby('season')['tiebreaker_changes_result'].mean() * 100
axes[0].bar(tb_by_season.index, tb_by_season.values, color=COLORS['tertiary'], edgecolor='black')
axes[0].set_xlabel('Season')
axes[0].set_ylabel('Tiebreaker Impact Rate (%)')
axes[0].text(0.02, 0.98, '(a)', transform=axes[0].transAxes, fontsize=12, fontweight='bold', va='top')

tb_diff = tiebreaker_analysis.groupby('season').apply(
    lambda x: (x['judge_tiebreaker_choice'] != x['pure_fan_choice']).mean() * 100
)
axes[1].plot(tb_diff.index, tb_diff.values, marker='o', color=COLORS['primary'], linewidth=2)
axes[1].set_xlabel('Season')
axes[1].set_ylabel('Judge-Fan Disagreement Rate (%)')
axes[1].text(0.02, 0.98, '(b)', transform=axes[1].transAxes, fontsize=12, fontweight='bold', va='top')
plt.tight_layout()
save_fig(fig, 'fig3_tiebreaker_analysis.pdf')

print("\n🎉 图片导出完成!")
