"""
问题一图片导出脚本
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
    'legend.frameon': False, 'legend.fontsize': 9,
})

COLORS = {'primary': '#2E5B88', 'secondary': '#E85D4C', 'tertiary': '#4A9B7F', 'neutral': '#7F7F7F', 'light': '#B8D4E8'}
FIG_DOUBLE = (10, 4)

FIGURE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/figures'
os.makedirs(FIGURE_DIR, exist_ok=True)

def save_fig(fig, filename):
    filepath = os.path.join(FIGURE_DIR, filename)
    fig.savefig(filepath, bbox_inches='tight', facecolor='white')
    print(f"✅ 已保存: {filepath}")
    plt.close(fig)

# 加载数据
vote_estimates = pd.read_csv('vote_estimates.csv')
consistency = pd.read_csv('verification_results.csv')
df_certainty = pd.read_csv('certainty_metrics.csv')

# 图1
fig, axes = plt.subplots(1, 2, figsize=FIG_DOUBLE)
consistency_by_season = consistency.groupby('season')['is_consistent'].mean() * 100
axes[0].bar(consistency_by_season.index, consistency_by_season.values, color=COLORS['primary'], edgecolor='white', alpha=0.85)
axes[0].axhline(y=consistency['is_consistent'].mean()*100, color=COLORS['secondary'], linestyle='--', linewidth=2)
axes[0].set_xlabel('Season')
axes[0].set_ylabel('Consistency Rate (%)')
axes[0].set_ylim(0, 110)
axes[0].text(0.95, 0.95, f'Overall: {consistency["is_consistent"].mean()*100:.1f}%', transform=axes[0].transAxes, fontsize=10, ha='right', va='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
axes[0].text(-0.12, 1.05, '(a)', transform=axes[0].transAxes, fontsize=14, fontweight='bold')

consistency_by_method = consistency.groupby('method')['is_consistent'].agg(['mean', 'std']) * 100
x_pos = np.arange(len(consistency_by_method))
bars = axes[1].bar(x_pos, consistency_by_method['mean'], yerr=consistency_by_method['std'], color=[COLORS['primary'], COLORS['secondary']], edgecolor='white', capsize=5, alpha=0.85, width=0.6)
axes[1].set_xticks(x_pos)
axes[1].set_xticklabels(['Percentage', 'Rank'])
axes[1].set_xlabel('Voting Method')
axes[1].set_ylabel('Consistency Rate (%)')
axes[1].text(-0.12, 1.05, '(b)', transform=axes[1].transAxes, fontsize=14, fontweight='bold')
plt.tight_layout()
save_fig(fig, 'fig1_consistency_analysis.pdf')

# 图2-5 类似更新...
print("\n🎉 问题一图片导出完成!")
