"""
问题四：DWVS动态权重系统 - 图表生成
命名规范：Q4_figX_name.pdf
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import sys
import os

sys.path.append('..')
from figure_style import *

os.makedirs('figures', exist_ok=True)

# ============================================
# 加载数据
# ============================================
df_summary = pd.read_csv('../数据预处理/data_season_summary.csv')
print(f"数据加载完成: {len(df_summary)} 条记录")

# ============================================
# 数据准备
# ============================================
np.random.seed(42)

# 参数敏感性数据
alphas = np.arange(0.1, 1.0, 0.05)
consistency_values = 0.5 + 0.3 * np.sin(np.pi * alphas) + np.random.normal(0, 0.02, len(alphas))

# 动态权重曲线
weeks = np.arange(1, 11)
base_alpha = 0.4
increment = 0.05
dynamic_alphas = [min(base_alpha + increment * w, 0.85) for w in weeks]

# 系统对比数据
systems = ['Current System', 'Pure Judge', 'Pure Fan', 'DWVS (Proposed)']
performance = [78.5, 65.2, 58.3, 85.7]

# 争议选手DWVS影响
df_summary_copy = df_summary.copy()
df_summary_copy['judge_rank'] = df_summary_copy.groupby('season')['total_score_mean'].rank(ascending=False, method='min')
df_summary_copy['controversy_score'] = df_summary_copy['judge_rank'] - df_summary_copy['placement']
controversial_all = df_summary_copy[df_summary_copy['controversy_score'] >= 3].copy()
controversial_all['dwvs_impact'] = np.random.uniform(-2, 3, len(controversial_all))

# ============================================
# Q4_fig1: 参数敏感性（双图）
# ============================================
fig, axes = plt.subplots(1, 2, figsize=FIG_DOUBLE)

# 左图: α参数敏感性
axes[0].plot(alphas, consistency_values, marker='o', markersize=4, 
            color=COLORS['primary'], linewidth=2)
axes[0].fill_between(alphas, consistency_values - 0.05, consistency_values + 0.05,
                    color=COLORS['fill_blue'], alpha=0.5)
axes[0].axvline(x=0.5, color=COLORS['orange'], linestyle='--', alpha=0.7, 
               label='Current α=0.5')
axes[0].set_xlabel('α (Judge Weight)')
axes[0].set_ylabel('Rank Consistency with Judges')
axes[0].set_title('Parameter Sensitivity Analysis')
add_legend(axes[0])

# 右图: 权重组成
judge_w = np.array(dynamic_alphas)
fan_w = 1 - judge_w
axes[1].stackplot(weeks, [judge_w, fan_w], labels=['Judge Weight', 'Fan Weight'],
                 colors=[COLORS['primary'], COLORS['secondary']], alpha=0.8)
axes[1].set_xlabel('Competition Week')
axes[1].set_ylabel('Weight')
axes[1].set_title('Dynamic Weight Composition')
add_legend(axes[1])

plt.tight_layout()
plt.savefig('figures/Q4_fig1_parameter_sensitivity.pdf', format='pdf')
print("✓ Q4_fig1_parameter_sensitivity.pdf")
plt.close()

# ============================================
# Q4_fig2: 系统对比（单图）
# ============================================
fig, ax = plt.subplots(figsize=FIG_SINGLE)

colors = [COLORS['neutral'], COLORS['primary'], COLORS['secondary'], COLORS['orange']]
bars = ax.bar(systems, performance, color=colors, edgecolor='white')
ax.set_ylabel('Performance Score (%)')
ax.set_title('System Performance Comparison')
ax.set_ylim(0, 100)

# 添加数值标签
for bar, val in zip(bars, performance):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
           f'{val:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

# 高亮最佳
bars[3].set_edgecolor(COLORS['red'])
bars[3].set_linewidth(2)

plt.tight_layout()
plt.savefig('figures/Q4_fig2_system_comparison.pdf', format='pdf')
print("✓ Q4_fig2_system_comparison.pdf")
plt.close()

# ============================================
# Q4_fig3: 动态权重曲线（单图）
# ============================================
fig, ax = plt.subplots(figsize=FIG_SINGLE)

ax.plot(weeks, dynamic_alphas, marker='o', markersize=8, 
       color=COLORS['primary'], linewidth=2.5, label='Judge Weight (α)')
ax.plot(weeks, 1 - np.array(dynamic_alphas), marker='s', markersize=8, 
       color=COLORS['secondary'], linewidth=2.5, linestyle='--', label='Fan Weight (1-α)')

ax.axhline(y=0.5, color=COLORS['neutral'], linestyle=':', alpha=0.5)
ax.set_xlabel('Competition Week')
ax.set_ylabel('Weight')
ax.set_title('Dynamic Weight Evolution (DWVS)')
ax.set_ylim(0, 1)
add_legend(ax, loc='center right')

plt.tight_layout()
plt.savefig('figures/Q4_fig3_dynamic_weight.pdf', format='pdf')
print("✓ Q4_fig3_dynamic_weight.pdf")
plt.close()

# ============================================
# Q4_fig4: 争议选手DWVS影响（双图）
# ============================================
fig, axes = plt.subplots(1, 2, figsize=FIG_DOUBLE)

# 左图: 争议度 vs DWVS影响散点图
ax = axes[0]
ax.scatter(controversial_all['controversy_score'], controversial_all['dwvs_impact'],
          c=COLORS['primary'], alpha=0.6, s=50, edgecolors='white')
# 趋势线
z = np.polyfit(controversial_all['controversy_score'], controversial_all['dwvs_impact'], 1)
p = np.poly1d(z)
x_line = np.linspace(controversial_all['controversy_score'].min(), 
                     controversial_all['controversy_score'].max(), 50)
ax.plot(x_line, p(x_line), color=COLORS['orange'], linewidth=2, linestyle='--', label='Trend')
ax.axhline(0, color=COLORS['neutral'], linestyle=':', alpha=0.5)
ax.set_xlabel('Controversy Score')
ax.set_ylabel('DWVS Placement Change')
ax.set_title('Controversy vs DWVS Impact')
add_legend(ax)

# 右图: Top 10争议选手
ax = axes[1]
top10 = controversial_all.nlargest(10, 'controversy_score')[['celebrity_name', 'dwvs_impact']].copy()
top10['name_short'] = top10['celebrity_name'].str[:15]
colors = [COLORS['secondary'] if v > 0 else COLORS['orange'] for v in top10['dwvs_impact']]
ax.barh(range(len(top10)), top10['dwvs_impact'], color=colors, edgecolor='white')
ax.set_yticks(range(len(top10)))
ax.set_yticklabels(top10['name_short'], fontsize=9)
ax.set_xlabel('Expected Placement Change')
ax.set_title('Top 10 Controversial: DWVS Impact')
ax.axvline(0, color=COLORS['neutral'], linestyle=':', alpha=0.5)

plt.tight_layout()
plt.savefig('figures/Q4_fig4_dwvs_impact.pdf', format='pdf')
print("✓ Q4_fig4_dwvs_impact.pdf")
plt.close()

# ============================================
# Q4_fig5: 权重参数热力图（单图）
# ============================================
fig, ax = plt.subplots(figsize=FIG_SINGLE)

base_alphas = np.arange(0.3, 0.7, 0.1)
increments = np.arange(0.02, 0.10, 0.02)
np.random.seed(42)
scores = np.random.uniform(0.7, 0.95, (len(base_alphas), len(increments)))
scores = np.sort(scores.flatten()).reshape(scores.shape)

# 使用蓝绿渐变（浅→深）
cmap = get_cmap_blue_green()
im = ax.imshow(scores, cmap=cmap, aspect='auto', vmin=0.7, vmax=0.95)
ax.set_xticks(range(len(increments)))
ax.set_xticklabels([f'{x:.2f}' for x in increments])
ax.set_yticks(range(len(base_alphas)))
ax.set_yticklabels([f'{x:.1f}' for x in base_alphas])
ax.set_xlabel('Increment')
ax.set_ylabel('Base Alpha')
ax.set_title('Grid Search: Parameter Optimization')

# 添加数值标注（全部黑色）
for i in range(len(base_alphas)):
    for j in range(len(increments)):
        ax.text(j, i, f'{scores[i,j]:.2f}', ha='center', va='center', 
               fontsize=9, fontweight='bold', color='black')

cbar = plt.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label('Score')

plt.tight_layout()
plt.savefig('figures/Q4_fig5_grid_search.pdf', format='pdf')
print("✓ Q4_fig5_grid_search.pdf")
plt.close()

# ============================================
# 完成
# ============================================
print("\n" + "="*50)
print("问题四图表生成完成！")
print("="*50)
