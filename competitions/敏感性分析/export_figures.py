"""
敏感性分析图片导出脚本
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
df_q1_noise = pd.read_csv('q1_noise_sensitivity.csv')
df_q1_sample = pd.read_csv('q1_sample_sensitivity.csv')
df_q3 = pd.read_csv('q3_ridge_sensitivity.csv')
df_q4 = pd.read_csv('q4_alpha_sensitivity.csv')

# 图1: 问题一敏感性
fig, axes = plt.subplots(1, 2, figsize=FIG_DOUBLE)
axes[0].errorbar(df_q1_noise['noise_level'], df_q1_noise['mean_certainty'], yerr=df_q1_noise['std_certainty'], marker='o', color=COLORS['primary'], linewidth=2, capsize=4, markersize=6)
axes[0].set_xlabel('Noise Level (σ)')
axes[0].set_ylabel('Mean Certainty Index')
axes[0].text(-0.12, 1.05, '(a)', transform=axes[0].transAxes, fontsize=14, fontweight='bold')

axes[1].plot(df_q1_sample['sample_ratio'], df_q1_sample['consistency'], marker='o', color=COLORS['secondary'], linewidth=2, markersize=6)
axes[1].set_xlabel('Sample Ratio')
axes[1].set_ylabel('Consistency Rate')
axes[1].text(-0.12, 1.05, '(b)', transform=axes[1].transAxes, fontsize=14, fontweight='bold')
plt.tight_layout()
save_fig(fig, 'fig1_q1_sensitivity.pdf')

# 图4: 热力图（使用Blues配色）
fig, ax = plt.subplots(figsize=(6, 5))
pivot = df_q4.pivot(index='base_alpha', columns='increment', values='score')
im = ax.imshow(pivot.values, cmap=plt.cm.Blues, aspect='auto')
ax.set_xticks(range(len(pivot.columns)))
ax.set_xticklabels(pivot.columns)
ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels(pivot.index)
ax.set_xlabel('Increment')
ax.set_ylabel('Base Alpha')
for i in range(len(pivot.index)):
    for j in range(len(pivot.columns)):
        ax.text(j, i, f'{pivot.values[i,j]:.2f}', ha='center', va='center', fontsize=9)
plt.colorbar(im, ax=ax, shrink=0.8, label='Score')
plt.tight_layout()
save_fig(fig, 'fig4_q4_sensitivity.pdf')

print("\n🎉 敏感性分析图片导出完成!")
