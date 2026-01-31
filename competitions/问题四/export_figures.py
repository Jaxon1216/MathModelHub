"""
问题四图片导出脚本
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

def get_dynamic_alpha(week, base=0.4, increment=0.04, max_alpha=0.8):
    return min(base + increment * week, max_alpha)

# 图2: 动态alpha
fig, ax = plt.subplots(figsize=FIG_SINGLE)
weeks = np.arange(1, 12)
dynamic_alphas = [get_dynamic_alpha(w) for w in weeks]

ax.fill_between(weeks, 0, [1-a for a in dynamic_alphas], color=COLORS['secondary'], alpha=0.7, label='Fan Vote Weight')
ax.fill_between(weeks, [1-a for a in dynamic_alphas], 1, color=COLORS['primary'], alpha=0.7, label='Judge Score Weight')
ax.axhline(y=0.5, color='black', linestyle='--', linewidth=1, label='Equal Weights')
ax.set_xlabel('Week')
ax.set_ylabel('Weight Proportion')
ax.set_ylim(0, 1)
ax.legend(loc='center right')
ax.set_xticks(weeks)
plt.tight_layout()
save_fig(fig, 'fig2_dynamic_alpha.pdf')

# 图4: 权重组成
fig, ax = plt.subplots(figsize=FIG_SINGLE)
weeks_ext = np.arange(1, 12)
judge_w = [get_dynamic_alpha(w) for w in weeks_ext]
fan_w = [1 - a for a in judge_w]

ax.stackplot(weeks_ext, fan_w, judge_w, labels=['Fan Vote', 'Judge Score'],
            colors=[COLORS['secondary'], COLORS['primary']], alpha=0.8)
ax.set_xlabel('Week')
ax.set_ylabel('Weight')
ax.set_ylim(0, 1)
ax.legend(loc='upper right')
ax.set_xticks(weeks_ext)
plt.tight_layout()
save_fig(fig, 'fig4_weight_composition.pdf')

print("\n🎉 图片导出完成!")
