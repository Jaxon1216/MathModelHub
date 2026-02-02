#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problem 4 详细架构图
DWVS完整设计展示
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 8.5,
    'axes.linewidth': 0,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

# 配色
COLORS = {
    'title': ('#FCE4EC', '#C2185B'),
    'objective': ('#E8F5E9', '#388E3C'),
    'formula': ('#FFF9C4', '#F57C00'),
    'innovation': ('#E3F2FD', '#1976D2'),
    'optimization': ('#F3E5F5', '#7B1FA2'),
    'impact': ('#FFE0B2', '#E65100'),
    'comparison': ('#E1F5FE', '#0277BD'),
}

def box(ax, x, y, w, h, text, color, fs=8, fw='normal', align='left', lw=1.5):
    """创建框"""
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                           facecolor=color[0], edgecolor=color[1], linewidth=lw)
    ax.add_patch(patch)
    tx = x + 0.03 if align == 'left' else (x + w/2 if align == 'center' else x + w - 0.03)
    ax.text(tx, y + h - 0.05, text, ha=align, va='top', fontsize=fs, fontweight=fw)

def arrow(ax, x1, y1, x2, y2, color='#666', width=1.5):
    """创建箭头"""
    arr = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='->,head_width=0.15,head_length=0.15',
                         color=color, linewidth=width, mutation_scale=20)
    ax.add_patch(arr)

fig, ax = plt.subplots(figsize=(16, 11))
ax.set_xlim(0, 16)
ax.set_ylim(0, 11)
ax.axis('off')

# ===== 标题 =====
ax.text(8, 10.7, "Problem 4: Dynamic Weighted Voting System (DWVS)\nFrom Bobby Bones Controversy to Fair System",
        ha='center', va='top', fontsize=14, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', fc=COLORS['title'][0], ec=COLORS['title'][1], lw=2))

# ===== 设计目标 =====
box(ax, 0.3, 9.5, 15.4, 0.35, "Design Objectives (4 Pillars)", COLORS['objective'], 9, 'bold', 'center', 2)

objectives = [
    ("Entertainment", "High fan\nengagement\nin early weeks"),
    ("Expertise", "Technical\nskill matters\nin finals"),
    ("Fairness", "Prevent\nlow-skill wins\nvia fan mob"),
    ("Transparency", "Clear rules\nexplainable\nto audience")
]
for i, (title, desc) in enumerate(objectives):
    x = 0.5 + i * 3.8
    box(ax, x, 8.8, 3.6, 0.6, f"{title}\n\n{desc}", COLORS['objective'], 8, 'bold', 'center', 1.2)

# ===== 核心公式 =====
box(ax, 0.3, 7.8, 15.4, 0.35, "Core Formula", COLORS['formula'], 9, 'bold', 'center', 2)

formula_text = """Si(w) = α(w)·Ji + [1-α(w)]·Fi·Ti

where:  Si(w) = Comprehensive score  |  Ji = Judge score %  |  Fi = Fan vote %
        α(w) = Dynamic judge weight   |  Ti = Threshold penalty factor"""

box(ax, 0.3, 7.0, 15.4, 0.75, formula_text, COLORS['formula'], 8.5, 'bold', 'center', 1.5)

# ===== 创新1: 动态权重 =====
box(ax, 0.3, 5.8, 7.5, 0.35, "Innovation 1: Dynamic Weight Mechanism", COLORS['innovation'], 9, 'bold', 'center', 2)

innov1_text = """α(w) = min(0.30 + 0.04w, 0.80)

Evolution Table:
Week │ α(w) │Judge%│ Fan% │ Philosophy
─────┼──────┼──────┼──────┼─────────────
  1  │ 0.34 │ 34%  │ 66%  │ Entertainment
  2  │ 0.38 │ 38%  │ 62%  │ driven
  5  │ 0.50 │ 50%  │ 50%  │ (Audience
  9  │ 0.66 │ 66%  │ 34%  │  building)
 10+ │ 0.74 │ 74%  │ 26%  │ Merit-based

Early: High fan weight (engagement)
Finals: High judge weight (technical)"""

box(ax, 0.3, 4.1, 7.5, 1.65, innov1_text, COLORS['innovation'], 7.5, 'normal', 'left', 1.2)

# ===== 创新2: 门槛惩罚 =====
box(ax, 8.2, 5.8, 7.5, 0.35, "Innovation 2: Threshold Penalty", COLORS['innovation'], 9, 'bold', 'center', 2)

innov2_text = """      ⎧ 0.3  if Ji < 0.5 × J̄week
Ti = ⎨
      ⎩ 1.0  otherwise

Purpose:
• Prevent "low-skill high-popularity"
• If judge score < 50% average:
  → Fan votes count only 30%
• Maintains baseline quality standard

Bobby Bones Example (Week 9):
• Judge score = 45% < 50% threshold
• Fan votes: 35% → 10.5% (×0.3)
• Cannot accumulate enough to win

Result: Proportional correction,
        not arbitrary punishment"""

box(ax, 8.2, 4.1, 7.5, 1.65, innov2_text, COLORS['innovation'], 7.5, 'normal', 'left', 1.2)

# ===== 参数优化 =====
box(ax, 0.3, 3.1, 7.5, 0.35, "Parameter Optimization: Grid Search", COLORS['optimization'], 9, 'bold', 'center', 2)

opt_text = """Search Space:
• Base α₀ ∈ [0.25, 0.40] (step=0.01)
• Increment Δα ∈ [0.02, 0.06] (step=0.01)
• Total: 80 combinations

Optimal Result:
✓ α₀ = 0.30 (base judge weight)
✓ Δα = 0.04 (weekly increment)  
✓ Score = 0.98-0.99 (near-perfect)

Robustness:
Stable across ±0.05 parameter range
Diagonal pattern shows consistency"""

box(ax, 0.3, 1.6, 7.5, 1.45, opt_text, COLORS['optimization'], 7.5, 'normal', 'left', 1.2)

# ===== 影响评估 =====
box(ax, 8.2, 3.1, 7.5, 0.35, "Impact Assessment: 32 Controversial", COLORS['impact'], 9, 'bold', 'center', 2)

impact_text = """Overall Statistics:
• 78.1% rank LOWER under DWVS (25/32)
• Average adjustment: +0.45 positions
• Correlation (Score vs Change): r=0.42
  → Proportional, not arbitrary!

Top Cases:
Contestant       │Season│Original│DWVS│Change
─────────────────┼──────┼────────┼────┼──────
Bobby Bones      │  27  │  1st   │2nd │ +1
Bristol Palin    │  11  │  3rd   │4th │ +1
Jerry Rice       │   2  │  2nd   │3rd │ +1
Billy Ray Cyrus  │   4  │  5th   │6th │ +1

Key Insight: Bobby would place 2nd,
not 1st → Controversy prevented"""

box(ax, 8.2, 1.6, 7.5, 1.45, impact_text, COLORS['impact'], 7.5, 'normal', 'left', 1.2)

# ===== 系统对比 =====
box(ax, 0.3, 0.6, 15.4, 0.35, "System Comparison: Pareto Improvement", COLORS['comparison'], 9, 'bold', 'center', 2)

comp_text = """System    │ Fairness │ Expertise │ Balance │ Engagement │ Overall │ Rank
──────────┼──────────┼───────────┼─────────┼────────────┼─────────┼──────
DWVS      │   5/5    │    4/5    │   5/5   │    4/5     │   4.5   │  1st
Current   │   3/5    │    3/5    │   3/5   │    4/5     │   3.25  │  2nd
Judge-only│   3/5    │    5/5    │   3/5   │    2/5     │   3.25  │  3rd
Fan-only  │   2/5    │    1/5    │   2/5   │    5/5     │   2.50  │  4th

DWVS = Only system achieving 5/5 on both Fairness and Balance"""

box(ax, 0.3, 0.05, 15.4, 0.5, comp_text, COLORS['comparison'], 7.5, 'normal', 'left', 1.2)

# ===== 箭头连接 =====
arrow(ax, 8, 8.75, 8, 8.2)
arrow(ax, 8, 6.95, 4, 6.15)
arrow(ax, 8, 6.95, 12, 6.15)
arrow(ax, 4, 4.05, 4, 3.5)
arrow(ax, 12, 4.05, 12, 3.5)
arrow(ax, 4, 1.55, 8, 1.15)
arrow(ax, 12, 1.55, 8, 1.15)

plt.savefig('figures/p4_dwvs_detailed.pdf', bbox_inches='tight', pad_inches=0.1)
plt.savefig('figures/p4_dwvs_detailed.png', bbox_inches='tight', pad_inches=0.1, dpi=300)
print("✅ Problem 4 详细架构图已生成!")
print("   - figures/p4_dwvs_detailed.pdf")
print("   - figures/p4_dwvs_detailed.png")
plt.show()
