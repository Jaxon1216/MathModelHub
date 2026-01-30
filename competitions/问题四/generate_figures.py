# =============================================================================
# 问题四：新投票系统设计 - 配图生成脚本
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
param_sensitivity = pd.read_csv('parameter_sensitivity.csv')
controversial_impact = pd.read_csv('controversial_impact.csv')

print(f"  参数敏感性数据: {len(param_sensitivity)} 条")

# 动态权重函数
def get_dynamic_alpha(week, base=0.30, increment=0.04):
    """计算动态评委权重"""
    return min(base + increment * week, 0.80)

# =============================================================================
# 图1: 参数敏感性 (Parameter Sensitivity)
# =============================================================================
print("\n生成图1: 参数敏感性...")

fig, axes = plt.subplots(1, 2, figsize=FIG_SIZES['double'])

# 准备数据 - 数据已经是汇总格式
alpha_summary = param_sensitivity.copy()
# 确保列名正确
if 'mean_consistency' not in alpha_summary.columns and 'consistency' in alpha_summary.columns:
    alpha_summary = param_sensitivity.groupby('alpha').agg({
        'consistency': ['mean', 'std']
    }).reset_index()
    alpha_summary.columns = ['alpha', 'mean_consistency', 'std_consistency']

# 1a: α vs 一致性
ax1 = axes[0]
ax1.errorbar(alpha_summary['alpha'], alpha_summary['mean_consistency'],
            yerr=alpha_summary['std_consistency'], marker='o',
            color=COLORS['rank_method'], linewidth=LINE_WIDTH['default'], capsize=4,
            markersize=MARKER_SIZE['default'])
ax1.fill_between(alpha_summary['alpha'],
                alpha_summary['mean_consistency'] - alpha_summary['std_consistency'],
                alpha_summary['mean_consistency'] + alpha_summary['std_consistency'],
                color=COLORS['light_blue'], alpha=0.5)
ax1.set_xlabel('α (Judge Weight)')
ax1.set_ylabel('Consistency Index')
add_grid(ax1, axis='y')
add_subplot_label(ax1, 'a')

# 标注最优点
if len(alpha_summary) > 0:
    best_idx = alpha_summary['mean_consistency'].idxmax()
    best_alpha = alpha_summary.loc[best_idx, 'alpha']
    best_val = alpha_summary.loc[best_idx, 'mean_consistency']
    highlight_point(ax1, best_alpha, best_val, f'α={best_alpha:.2f}', offset=(8, 8))

# 1b: 不同参数组合
ax2 = axes[1]
# 模拟不同base和increment组合
bases = [0.3, 0.4, 0.5]
increments = [0.02, 0.04, 0.06]
weeks = np.arange(1, 11)

for i, base in enumerate(bases):
    alphas = [get_dynamic_alpha(w, base, 0.04) for w in weeks]
    linestyle = ['-', '--', '-.'][i]
    ax2.plot(weeks, alphas, label=f'base={base}', color=CATEGORY_COLORS[i],
            linewidth=LINE_WIDTH['default'], linestyle=linestyle, marker='o',
            markersize=MARKER_SIZE['small'])

ax2.set_xlabel('Week')
ax2.set_ylabel('α (Judge Weight)')
ax2.legend(loc='lower right')
add_grid(ax2, axis='y')
add_subplot_label(ax2, 'b')

plt.tight_layout()
save_figure(fig, 'figures/fig1_parameter_sensitivity')
plt.close()

print(f"  ✓ 生成完毕")

# =============================================================================
# 图2: 动态权重可视化 (Dynamic Alpha)
# =============================================================================
print("\n生成图2: 动态权重...")

fig, ax = plt.subplots(figsize=FIG_SIZES['single'])

weeks = np.arange(1, 12)
dynamic_alphas = [get_dynamic_alpha(w) for w in weeks]
fan_weights = [1 - a for a in dynamic_alphas]

# 堆叠面积图
ax.fill_between(weeks, 0, fan_weights, color=COLORS['pct_method'], alpha=0.7, label='Fan Vote Weight')
ax.fill_between(weeks, fan_weights, 1, color=COLORS['rank_method'], alpha=0.7, label='Judge Weight')

# 添加数值标注
for i in [0, 4, 9]:  # Week 1, 5, 10
    ax.annotate(f'J:{dynamic_alphas[i]*100:.0f}%\nF:{fan_weights[i]*100:.0f}%',
               xy=(weeks[i], 0.5), fontsize=9, ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax.set_xlabel('Week')
ax.set_ylabel('Weight Distribution')
ax.set_ylim(0, 1)
ax.set_xticks(weeks)
ax.legend(loc='center right')
add_subplot_label(ax, '')

plt.tight_layout()
save_figure(fig, 'figures/fig2_dynamic_alpha')
plt.close()

print(f"  ✓ Week 1: 评委{dynamic_alphas[0]*100:.0f}%, 粉丝{fan_weights[0]*100:.0f}%")
print(f"  ✓ Week 10: 评委{dynamic_alphas[9]*100:.0f}%, 粉丝{fan_weights[9]*100:.0f}%")

# =============================================================================
# 图3: 系统对比 (System Comparison)
# =============================================================================
print("\n生成图3: 系统对比...")

fig, ax = plt.subplots(figsize=FIG_SIZES['heatmap'])

systems = ['Current\n(Fixed α=0.5)', 'DWVS\n(Dynamic)', 'Judge Only\n(α=1.0)', 'Fan Only\n(α=0)']
features = ['Balance', 'Expertise', 'Engagement', 'Fairness']

# 评分矩阵 (1-5分)
scores = np.array([
    [3, 3, 4, 3],  # Current
    [5, 4, 4, 5],  # DWVS
    [2, 5, 2, 4],  # Judge Only
    [2, 1, 5, 1],  # Fan Only
])

im = ax.imshow(scores.T, cmap='YlGnBu', aspect='auto', vmin=1, vmax=5)
ax.set_xticks(np.arange(len(systems)))
ax.set_xticklabels(systems, fontsize=10)
ax.set_yticks(np.arange(len(features)))
ax.set_yticklabels(features)

# 添加数值标注
for i in range(len(features)):
    for j in range(len(systems)):
        color = 'white' if scores[j, i] > 3 else 'black'
        ax.text(j, i, f'{scores[j, i]}', ha='center', va='center', 
               fontsize=11, fontweight='bold', color=color)

# 高亮最佳系统列
ax.axvline(x=0.5, color=COLORS['highlight'], linewidth=2, linestyle='-')
ax.axvline(x=1.5, color=COLORS['highlight'], linewidth=2, linestyle='-')

cbar = plt.colorbar(im, ax=ax, label='Score (1-5)', shrink=0.8)

plt.tight_layout()
save_figure(fig, 'figures/fig2_system_comparison')
plt.close()

print(f"  ✓ DWVS平均得分: {scores[1].mean():.1f}")

# =============================================================================
# 图4: 争议选手影响 (Controversial Impact)
# =============================================================================
print("\n生成图4: 争议选手影响...")

fig, ax = plt.subplots(figsize=FIG_SIZES['single'])

# 准备数据
contestants = controversial_impact['celebrity'].values
original = controversial_impact['final_placement'].values
expected = controversial_impact['expected_new_placement'].values
changes = expected - original

y_pos = np.arange(len(contestants))
colors_bar = [COLORS['highlight'] if c > 0 else COLORS['positive'] for c in changes]

bars = ax.barh(y_pos, changes, color=colors_bar, edgecolor='black', linewidth=0.5)
ax.set_yticks(y_pos)
ax.set_yticklabels(contestants)
ax.set_xlabel('Expected Placement Change (+ = Lower Ranking)')
ax.axvline(x=0, color='black', linewidth=1)
add_grid(ax, axis='x')

# 标注变化值
for bar, change, orig, exp in zip(bars, changes, original, expected):
    sign = '+' if change > 0 else ''
    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
           f'{sign}{change:.1f}\n({int(orig)}→{exp:.1f})',
           va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
save_figure(fig, 'figures/fig3_controversial_impact')
plt.close()

print(f"  ✓ Bobby Bones变化: +{changes[list(contestants).index('Bobby Bones')]:.1f}")

# =============================================================================
# 图5: 权重组成时间线 (Weight Composition)
# =============================================================================
print("\n生成图5: 权重组成时间线...")

fig, ax = plt.subplots(figsize=FIG_SIZES['wide'])

weeks = np.arange(1, 12)
judge_w = [get_dynamic_alpha(w) for w in weeks]
fan_w = [1 - a for a in judge_w]

# 双线对比
ax.plot(weeks, judge_w, color=COLORS['rank_method'], marker='o',
       linewidth=LINE_WIDTH['thick'], markersize=MARKER_SIZE['default'],
       label='Judge Weight', linestyle=LINE_STYLES['rank_method'])
ax.plot(weeks, fan_w, color=COLORS['pct_method'], marker='s',
       linewidth=LINE_WIDTH['thick'], markersize=MARKER_SIZE['default'],
       label='Fan Weight', linestyle=LINE_STYLES['pct_method'])

# 标注交叉点
cross_week = 5  # approximately where weights are equal
ax.axvline(x=cross_week, color=COLORS['neutral'], linestyle=':', alpha=0.7)
ax.annotate('Equal\nWeights', xy=(cross_week, 0.5), xytext=(cross_week+1, 0.6),
           fontsize=9, arrowprops=dict(arrowstyle='->', color=COLORS['neutral']))

ax.set_xlabel('Week')
ax.set_ylabel('Weight')
ax.set_ylim(0, 1)
ax.set_xticks(weeks)
ax.legend(loc='center right')
add_grid(ax, axis='y')

plt.tight_layout()
save_figure(fig, 'figures/fig4_weight_composition')
plt.close()

print(f"  ✓ 生成完毕")

# =============================================================================
# 汇总
# =============================================================================
print("\n" + "="*60)
print("【问题四配图生成完成】")
print("="*60)
print(f"生成的图片:")
for i, name in enumerate(['fig1_parameter_sensitivity.pdf',
                          'fig2_dynamic_alpha.pdf',
                          'fig2_system_comparison.pdf',
                          'fig3_controversial_impact.pdf',
                          'fig4_weight_composition.pdf'], 1):
    print(f"  {i}. figures/{name}")
print("="*60)
