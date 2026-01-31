# =============================================================================
# 问题三：影响因素分析 - 配图生成脚本
# =============================================================================

import sys
sys.path.append('..')
from figure_style import *
import pandas as pd
import numpy as np
from scipy import stats
import os

os.makedirs('figures', exist_ok=True)

# =============================================================================
# 数据加载
# =============================================================================
print("加载数据...")
df_summary = pd.read_csv('../数据预处理/data_season_summary.csv')
df_long = pd.read_csv('../数据预处理/data_long_format.csv')
industry_stats = pd.read_csv('industry_analysis.csv', index_col=0)
pro_stats = pd.read_csv('pro_dancer_analysis.csv', index_col=0)
feature_importance = pd.read_csv('feature_importance.csv')

print(f"  季汇总数据: {len(df_summary)} 条")

# 数据准备
df_analysis = df_summary.copy()
df_analysis['age'] = pd.to_numeric(df_analysis['celebrity_age'], errors='coerce')
df_analysis = df_analysis[df_analysis['age'].notna()]

# =============================================================================
# 图1: 行业影响 (Industry Impact)
# =============================================================================
print("\n生成图1: 行业影响...")

fig, axes = plt.subplots(1, 2, figsize=FIG_SIZES['double'])

# 1a: 平均名次
ax1 = axes[0]
y_pos = np.arange(len(industry_stats))
colors_industry = CATEGORY_COLORS[:len(industry_stats)]

bars1 = ax1.barh(y_pos, industry_stats['avg_placement'], 
                color=colors_industry, edgecolor='black', linewidth=0.5)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(industry_stats.index)
ax1.set_xlabel('Average Placement (lower is better)')
ax1.invert_xaxis()  # 名次越低越好
add_grid(ax1, axis='x')
add_subplot_label(ax1, 'a')

# 标注最佳和最差
best_idx = industry_stats['avg_placement'].idxmin()
worst_idx = industry_stats['avg_placement'].idxmax()
ax1.annotate(f'Best: {industry_stats.loc[best_idx, "avg_placement"]:.1f}',
            xy=(industry_stats.loc[best_idx, 'avg_placement'], 
                list(industry_stats.index).index(best_idx)),
            xytext=(10, 5), textcoords='offset points',
            fontsize=9, color=COLORS['positive'], fontweight='bold')

# 1b: 胜率
ax2 = axes[1]
win_rate = industry_stats['win_rate'] if 'win_rate' in industry_stats.columns else \
           (industry_stats['wins'] / industry_stats['count'] * 100)

bars2 = ax2.barh(y_pos, win_rate, color=colors_industry, edgecolor='black', linewidth=0.5)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(industry_stats.index)
ax2.set_xlabel('Win Rate (%)')
add_grid(ax2, axis='x')
add_subplot_label(ax2, 'b')

plt.tight_layout()
save_figure(fig, 'figures/fig1_industry_impact')
plt.close()

print(f"  ✓ 最佳行业: {best_idx}")

# =============================================================================
# 图2: 年龄影响 (Age Impact)
# =============================================================================
print("\n生成图2: 年龄影响...")

fig, axes = plt.subplots(1, 2, figsize=FIG_SIZES['double'])

# 2a: 散点图 + 趋势线
ax1 = axes[0]
ax1.scatter(df_analysis['age'], df_analysis['placement'],
           c=COLORS['rank_method'], alpha=0.4, s=30, edgecolors='none')

# 趋势线
z = np.polyfit(df_analysis['age'], df_analysis['placement'], 1)
p = np.poly1d(z)
x_line = np.linspace(df_analysis['age'].min(), df_analysis['age'].max(), 100)
ax1.plot(x_line, p(x_line), color=COLORS['highlight'], linewidth=2.5, linestyle='--')

# 相关性
age_corr = df_analysis['age'].corr(df_analysis['placement'])
ax1.text(0.05, 0.95, f'r = {age_corr:.3f}', transform=ax1.transAxes,
         fontsize=11, va='top', fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax1.set_xlabel('Age')
ax1.set_ylabel('Placement (lower is better)')
add_grid(ax1, axis='both')
add_subplot_label(ax1, 'a')

# 2b: 年龄组箱线图
ax2 = axes[1]
age_groups = ['<25', '25-35', '35-45', '45+']
df_analysis['age_group'] = pd.cut(df_analysis['age'], bins=[0, 25, 35, 45, 100], 
                                  labels=age_groups)
age_data = [df_analysis[df_analysis['age_group']==g]['placement'].dropna().values 
            for g in age_groups]
age_data = [d for d in age_data if len(d) > 0]

bp = ax2.boxplot(age_data, patch_artist=True, widths=0.6)
colors_box = [COLORS['positive'], COLORS['rank_method'], COLORS['pct_method'], COLORS['negative']]
for patch, color in zip(bp['boxes'], colors_box[:len(bp['boxes'])]):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax2.set_xticklabels([g for g in age_groups if g in df_analysis['age_group'].values])
ax2.set_xlabel('Age Group')
ax2.set_ylabel('Placement')
add_grid(ax2, axis='y')
add_subplot_label(ax2, 'b')

plt.tight_layout()
save_figure(fig, 'figures/fig2_age_impact')
plt.close()

print(f"  ✓ 年龄-名次相关性: r={age_corr:.3f}")

# =============================================================================
# 图3: 特征重要性 (Feature Importance)
# =============================================================================
print("\n生成图3: 特征重要性...")

fig, ax = plt.subplots(figsize=FIG_SIZES['single'])

y_pos = np.arange(len(feature_importance))
colors_feat = [COLORS['highlight'] if i == 0 else COLORS['rank_method'] 
               for i in range(len(feature_importance))]

bars = ax.barh(y_pos, feature_importance['importance'], 
               color=colors_feat, edgecolor='black', linewidth=0.5)
ax.set_yticks(y_pos)
ax.set_yticklabels(feature_importance['feature'])
ax.set_xlabel('Feature Importance')
ax.invert_yaxis()
add_grid(ax, axis='x')

# 标注最重要特征
top_feat = feature_importance.iloc[0]
ax.annotate(f'{top_feat["importance"]*100:.1f}%', 
           xy=(top_feat['importance'], 0),
           xytext=(5, 0), textcoords='offset points',
           fontsize=10, fontweight='bold', color=COLORS['highlight'], va='center')

plt.tight_layout()
save_figure(fig, 'figures/fig3_feature_importance')
plt.close()

print(f"  ✓ 最重要特征: {top_feat['feature']} ({top_feat['importance']:.3f})")

# =============================================================================
# 图4: 专业舞者影响 (Professional Dancer Impact)
# =============================================================================
print("\n生成图4: 专业舞者影响...")

fig, axes = plt.subplots(1, 2, figsize=FIG_SIZES['double'])

top_pros = pro_stats.head(10)
y_pos = np.arange(len(top_pros))

# 4a: 冠军数
ax1 = axes[0]
bars1 = ax1.barh(y_pos, top_pros['wins'], color=COLORS['dwvs'], 
                edgecolor='black', linewidth=0.5)
ax1.set_yticks(y_pos)
ax1.set_yticklabels(top_pros.index)
ax1.set_xlabel('Number of Wins')
add_grid(ax1, axis='x')
add_subplot_label(ax1, 'a')

# 标注最佳舞者
if top_pros['wins'].max() > 0:
    best_dancer = top_pros['wins'].idxmax()
    best_wins = top_pros.loc[best_dancer, 'wins']
    highlight_point(ax1, best_wins, list(top_pros.index).index(best_dancer),
                   f'{int(best_wins)} wins', offset=(8, 0))

# 4b: 平均名次
ax2 = axes[1]
bars2 = ax2.barh(y_pos, top_pros['avg_placement'], 
                xerr=top_pros['std_placement'].fillna(0),
                color=COLORS['rank_method'], edgecolor='black', linewidth=0.5, capsize=3)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(top_pros.index)
ax2.set_xlabel('Average Placement')
add_grid(ax2, axis='x')
add_subplot_label(ax2, 'b')

plt.tight_layout()
save_figure(fig, 'figures/fig4_pro_dancer_impact')
plt.close()

print(f"  ✓ 最佳舞伴: {top_pros.index[0]}")

# =============================================================================
# 汇总
# =============================================================================
print("\n" + "="*60)
print("【问题三配图生成完成】")
print("="*60)
print(f"生成的图片:")
for i, name in enumerate(['fig1_industry_impact.pdf',
                          'fig2_age_impact.pdf',
                          'fig3_feature_importance.pdf',
                          'fig4_pro_dancer_impact.pdf'], 1):
    print(f"  {i}. figures/{name}")
print("="*60)
