"""
问题三图片导出脚本
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

COLORS = {'primary': '#2E5B88', 'secondary': '#E85D4C', 'tertiary': '#4A9B7F', 'light': '#B8D4E8'}
FIG_DOUBLE = (10, 4)
FIG_SINGLE = (5, 4)

FIGURE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/figures'
os.makedirs(FIGURE_DIR, exist_ok=True)

def save_fig(fig, filename):
    filepath = os.path.join(FIGURE_DIR, filename)
    fig.savefig(filepath, bbox_inches='tight', facecolor='white')
    print(f"✅ 已保存: {filepath}")
    plt.close(fig)

# 加载数据
industry_stats = pd.read_csv('industry_analysis.csv', index_col=0)
pro_stats = pd.read_csv('pro_dancer_analysis.csv', index_col=0)
feature_importance = pd.read_csv('feature_importance.csv')

# 图1: 行业影响
fig, axes = plt.subplots(1, 2, figsize=FIG_DOUBLE)
y_pos = np.arange(len(industry_stats))
axes[0].barh(y_pos, industry_stats['avg_placement'], color=COLORS['primary'], edgecolor='white', alpha=0.85, height=0.6)
axes[0].set_yticks(y_pos)
axes[0].set_yticklabels(industry_stats.index)
axes[0].set_xlabel('Average Placement')
axes[0].invert_xaxis()
axes[0].text(-0.15, 1.05, '(a)', transform=axes[0].transAxes, fontsize=14, fontweight='bold')

axes[1].barh(y_pos, industry_stats['win_rate'], color=COLORS['secondary'], edgecolor='white', alpha=0.85, height=0.6)
axes[1].set_yticks(y_pos)
axes[1].set_yticklabels(industry_stats.index)
axes[1].set_xlabel('Win Rate (%)')
axes[1].text(-0.15, 1.05, '(b)', transform=axes[1].transAxes, fontsize=14, fontweight='bold')
plt.tight_layout()
save_fig(fig, 'fig1_industry_impact.pdf')

# 图3: 特征重要性
fig, ax = plt.subplots(figsize=FIG_SINGLE)
y_pos = np.arange(len(feature_importance))
colors = [COLORS['primary'] if i == 0 else COLORS['light'] for i in range(len(feature_importance))]
ax.barh(y_pos, feature_importance['importance'], color=colors, edgecolor='white', alpha=0.85, height=0.6)
ax.set_yticks(y_pos)
ax.set_yticklabels(feature_importance['feature'])
ax.set_xlabel('Feature Importance')
ax.invert_yaxis()
plt.tight_layout()
save_fig(fig, 'fig3_feature_importance.pdf')

# 图4: 专业舞者
top_pros = pro_stats.head(10)
fig, axes = plt.subplots(1, 2, figsize=FIG_DOUBLE)
y_pos = np.arange(len(top_pros))
axes[0].barh(y_pos, top_pros['wins'], color=COLORS['tertiary'], edgecolor='white', alpha=0.85, height=0.6)
axes[0].set_yticks(y_pos)
axes[0].set_yticklabels(top_pros.index, fontsize=9)
axes[0].set_xlabel('Number of Wins')
axes[0].text(-0.18, 1.05, '(a)', transform=axes[0].transAxes, fontsize=14, fontweight='bold')

axes[1].barh(y_pos, top_pros['avg_placement'], color=COLORS['primary'], edgecolor='white', alpha=0.85, height=0.6)
axes[1].set_yticks(y_pos)
axes[1].set_yticklabels(top_pros.index, fontsize=9)
axes[1].set_xlabel('Average Placement')
axes[1].text(-0.18, 1.05, '(b)', transform=axes[1].transAxes, fontsize=14, fontweight='bold')
plt.tight_layout()
save_fig(fig, 'fig4_pro_dancer_impact.pdf')

print("\n🎉 问题三图片导出完成!")
