"""
问题四：图片导出脚本
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

COLORS = {'primary': '#4682B4', 'secondary': '#FF7F50', 'accent': '#228B22'}

def save_fig(fig, filename):
    filepath = os.path.join(FIGURE_DIR, filename)
    fig.savefig(filepath, bbox_inches='tight', facecolor='white')
    print(f"✅ 已保存: {filepath}")
    plt.close(fig)

# 读取数据
sensitivity = pd.read_csv('parameter_sensitivity.csv')
controversy = pd.read_csv('controversial_impact.csv')
results = pd.read_csv('results_summary.csv')

# ============================================================
# 图1：参数敏感性热力图
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))

sensitivity_pivot = sensitivity.pivot(index='alpha', columns='beta', values='match_rate')
sns.heatmap(sensitivity_pivot, annot=True, fmt='.3f', cmap='YlOrRd', ax=ax)
ax.set_xlabel('Beta (Improvement Bonus)')
ax.set_ylabel('Alpha (Judge Weight)')

plt.tight_layout()
save_fig(fig, 'fig1_parameter_sensitivity.pdf')

# ============================================================
# 图2：系统比较
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))

systems = ['Rank-based', 'Percentage-based', 'DWVS (New)']
consistencies = [results['rank_consistency'].values[0], 
                 results['pct_consistency'].values[0], 
                 results['new_system_consistency'].values[0]]
colors_list = [COLORS['primary'], COLORS['secondary'], COLORS['accent']]

bars = ax.bar(systems, consistencies, color=colors_list)

for bar, val in zip(bars, consistencies):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
            f'{val:.1%}', ha='center', va='bottom', fontsize=12)

ax.set_ylabel('Consistency with Actual Elimination')
ax.set_ylim(0, 1.0)

plt.tight_layout()
save_fig(fig, 'fig2_system_comparison.pdf')

# ============================================================
# 图3：争议选手影响
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(len(controversy))
width = 0.25

bars1 = ax.bar(x - width, controversy['rank_elim'], width,
               label='Rank-based', color=COLORS['primary'])
bars2 = ax.bar(x, controversy['pct_elim'], width,
               label='Percentage-based', color=COLORS['secondary'])
bars3 = ax.bar(x + width, controversy['new_elim'], width,
               label='DWVS (New)', color=COLORS['accent'])

ax.set_xlabel('Controversial Contestants')
ax.set_ylabel('Weeks Would Be Eliminated')
ax.set_xticks(x)
ax.set_xticklabels([f"{row['contestant']}\n(S{row['season']})" 
                    for _, row in controversy.iterrows()])
ax.legend()

plt.tight_layout()
save_fig(fig, 'fig3_controversial_impact.pdf')

# ============================================================
# 图4：权重构成
# ============================================================
fig, ax = plt.subplots(figsize=(8, 8))

judge_pct = results['judge_weight_pct'].values[0]
fan_pct = results['fan_weight_pct'].values[0]
improvement_pct = results['improvement_weight_pct'].values[0]

sizes = [judge_pct, fan_pct, improvement_pct]
labels = [f'Judge Score\n({judge_pct:.1f}%)', 
          f'Fan Vote\n({fan_pct:.1f}%)', 
          f'Improvement\n({improvement_pct:.1f}%)']
colors_list = [COLORS['primary'], COLORS['secondary'], COLORS['accent']]
explode = (0.05, 0.05, 0.1)

ax.pie(sizes, labels=labels, colors=colors_list, explode=explode,
       autopct='', startangle=90, pctdistance=0.85)

plt.tight_layout()
save_fig(fig, 'fig4_weight_composition.pdf')

# ============================================================
print("\n" + "=" * 60)
print("🎉 所有图片导出完成！")
print("=" * 60)
