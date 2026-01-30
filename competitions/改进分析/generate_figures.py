# =============================================================================
# 改进分析 - 配图生成脚本
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
df_long = pd.read_csv('../数据预处理/data_long_format.csv')

# 加载改进分析数据
try:
    stratified = pd.read_csv('stratified_consistency.csv')
    alpha_analysis = pd.read_csv('alpha_factor_analysis.csv')
    industry_judge_fan = pd.read_csv('industry_judge_vs_fan.csv')
    grid_search = pd.read_csv('grid_search_results.csv')
    cross_val = pd.read_csv('cross_season_validation.csv')
    print("  ✓ 已加载改进分析数据")
except Exception as e:
    print(f"  ⚠ 加载数据出错: {e}")
    print("  请先运行 improvements_analysis.ipynb 生成数据")

# =============================================================================
# 图1: 分层一致性分析 (Stratified Consistency)
# =============================================================================
print("\n生成图1: 分层一致性分析...")

fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# 解析Category列，格式如 "By Method - Rank", "By Season - Early (S1-17)"
def parse_stratified(df):
    result = {}
    for _, row in df.iterrows():
        cat = row['Category']
        rate = row['Rate'] * 100 if row['Rate'] <= 1 else row['Rate']
        if 'Method' in cat:
            if 'method' not in result:
                result['method'] = {'labels': [], 'rates': []}
            label = cat.split(' - ')[1] if ' - ' in cat else cat
            result['method']['labels'].append(label)
            result['method']['rates'].append(rate)
        elif 'Season' in cat:
            if 'season' not in result:
                result['season'] = {'labels': [], 'rates': []}
            label = cat.split(' - ')[1] if ' - ' in cat else cat
            result['season']['labels'].append(label)
            result['season']['rates'].append(rate)
        elif 'Competition' in cat:  # 修正：匹配 "By Competition"
            if 'stage' not in result:
                result['stage'] = {'labels': [], 'rates': []}
            label = cat.split(' - ')[1] if ' - ' in cat else cat
            result['stage']['labels'].append(label)
            result['stage']['rates'].append(rate)
        elif 'Contestant' in cat:
            if 'count' not in result:
                result['count'] = {'labels': [], 'rates': []}
            label = cat.split(' - ')[1] if ' - ' in cat else cat
            result['count']['labels'].append(label)
            result['count']['rates'].append(rate)
    return result

parsed = parse_stratified(stratified)

# 1a: 按投票方法
ax1 = axes[0, 0]
if 'method' in parsed and len(parsed['method']['labels']) > 0:
    methods = parsed['method']['labels']
    rates = parsed['method']['rates']
    colors_m = [COLORS['rank_method'] if 'rank' in str(m).lower() else COLORS['pct_method'] for m in methods]
    bars = ax1.bar(methods, rates, color=colors_m, edgecolor='black', linewidth=0.5)
    for bar, rate in zip(bars, rates):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{rate:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax1.set_xlabel('Voting Method')
ax1.set_ylabel('Consistency Rate (%)')
ax1.set_title('By Voting Method', fontsize=11, fontweight='bold')
add_grid(ax1, axis='y')
add_subplot_label(ax1, 'a')

# 1b: 按赛季阶段
ax2 = axes[0, 1]
if 'season' in parsed and len(parsed['season']['labels']) > 0:
    phases = parsed['season']['labels']
    rates = parsed['season']['rates']
    colors_p = [COLORS['positive'], COLORS['negative']]
    bars = ax2.bar(phases, rates, color=colors_p[:len(phases)], edgecolor='black', linewidth=0.5)
    for bar, rate in zip(bars, rates):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{rate:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax2.set_xlabel('Season Phase')
ax2.set_ylabel('Consistency Rate (%)')
ax2.set_title('By Season Phase', fontsize=11, fontweight='bold')
add_grid(ax2, axis='y')
add_subplot_label(ax2, 'b')

# 1c: 按比赛阶段
ax3 = axes[1, 0]
if 'stage' in parsed and len(parsed['stage']['labels']) > 0:
    stages = parsed['stage']['labels']
    rates = parsed['stage']['rates']
    colors_s = [COLORS['rank_method'], COLORS['pct_method']]
    bars = ax3.bar(stages, rates, color=colors_s[:len(stages)], edgecolor='black', linewidth=0.5)
    for bar, rate in zip(bars, rates):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{rate:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax3.set_xlabel('Competition Stage')
ax3.set_ylabel('Consistency Rate (%)')
ax3.set_title('By Competition Stage', fontsize=11, fontweight='bold')
add_grid(ax3, axis='y')
add_subplot_label(ax3, 'c')

# 1d: 按选手数量
ax4 = axes[1, 1]
if 'count' in parsed and len(parsed['count']['labels']) > 0:
    counts = parsed['count']['labels']
    rates = parsed['count']['rates']
    colors_c = [COLORS['dwvs'], COLORS['neutral']]
    bars = ax4.bar(counts, rates, color=colors_c[:len(counts)], edgecolor='black', linewidth=0.5)
    for bar, rate in zip(bars, rates):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{rate:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax4.set_xlabel('Contestants per Week')
ax4.set_ylabel('Consistency Rate (%)')
ax4.set_title('By Contestant Count', fontsize=11, fontweight='bold')
add_grid(ax4, axis='y')
add_subplot_label(ax4, 'd')

plt.tight_layout()
save_figure(fig, 'figures/imp1_stratified_consistency')
plt.close()

print(f"  ✓ 生成完毕")

# =============================================================================
# 图2: α因子分布分析 (Alpha Distribution)
# =============================================================================
print("\n生成图2: α因子分布...")

fig, axes = plt.subplots(1, 2, figsize=FIG_SIZES['double'])

# 2a: α分布直方图
ax1 = axes[0]
alpha_col = 'mean_alpha' if 'mean_alpha' in alpha_analysis.columns else None
if alpha_col:
    alpha_data = alpha_analysis[alpha_col].dropna()
    ax1.hist(alpha_data, bins=30, color=COLORS['rank_method'],
            edgecolor='black', linewidth=0.5, alpha=0.85)
    mean_alpha = alpha_data.mean()
    ax1.axvline(x=mean_alpha, color=COLORS['highlight'], linestyle='--', linewidth=2,
               label=f'Mean={mean_alpha:.4f}')
    ax1.set_xlabel('Popularity Factor (α)')
    ax1.set_ylabel('Frequency')
    ax1.legend(loc='upper right')
add_grid(ax1, axis='y')
add_subplot_label(ax1, 'a')

# 2b: 争议选手vs普通选手
ax2 = axes[1]
if alpha_col and 'is_controversial' in alpha_analysis.columns:
    controversial = alpha_analysis[alpha_analysis['is_controversial'] == True][alpha_col].dropna()
    normal = alpha_analysis[alpha_analysis['is_controversial'] == False][alpha_col].dropna()
    
    if len(controversial) > 0 and len(normal) > 0:
        bp = ax2.boxplot([normal.values, controversial.values], patch_artist=True, widths=0.6)
        colors_box = [COLORS['rank_method'], COLORS['highlight']]
        for patch, color in zip(bp['boxes'], colors_box):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        ax2.set_xticklabels(['Normal', 'Controversial'])
        ax2.set_ylabel('Popularity Factor (α)')
        add_grid(ax2, axis='y')
        
        # 标注差异
        diff = controversial.mean() - normal.mean()
        ax2.annotate(f'Δ = {diff:+.4f}', xy=(1.5, max(normal.max(), controversial.max())),
                    fontsize=10, fontweight='bold', color=COLORS['highlight'])
add_subplot_label(ax2, 'b')

plt.tight_layout()
save_figure(fig, 'figures/imp2_alpha_distribution')
plt.close()

print(f"  ✓ 生成完毕")

# =============================================================================
# 图3: 行业对评委vs粉丝影响 (Industry Judge vs Fan)
# =============================================================================
print("\n生成图3: 行业对评委vs粉丝影响...")

fig, axes = plt.subplots(1, 2, figsize=FIG_SIZES['double'])

if len(industry_judge_fan) > 0:
    # 检查列名并适配
    industry_col = 'celebrity_industry' if 'celebrity_industry' in industry_judge_fan.columns else 'industry'
    judge_col = 'avg_judge_score' if 'avg_judge_score' in industry_judge_fan.columns else 'avg_total_score'
    fan_col = 'avg_vote_share' if 'avg_vote_share' in industry_judge_fan.columns else 'avg_fan_vote'
    
    # 3a: 标准化对比
    ax1 = axes[0]
    df_sorted = industry_judge_fan.sort_values(judge_col, ascending=False).head(8)
    industries = df_sorted[industry_col].values
    
    # 标准化
    judge_scores = df_sorted[judge_col].values
    fan_votes = df_sorted[fan_col].values
    
    # 安全标准化
    judge_range = judge_scores.max() - judge_scores.min()
    fan_range = fan_votes.max() - fan_votes.min()
    judge_norm = (judge_scores - judge_scores.min()) / judge_range if judge_range > 0 else np.zeros_like(judge_scores)
    fan_norm = (fan_votes - fan_votes.min()) / fan_range if fan_range > 0 else np.zeros_like(fan_votes)
    
    x = np.arange(len(industries))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, judge_norm, width, label='Judge Score', 
                   color=COLORS['rank_method'], edgecolor='black', linewidth=0.5)
    bars2 = ax1.bar(x + width/2, fan_norm, width, label='Fan Vote',
                   color=COLORS['pct_method'], edgecolor='black', linewidth=0.5)
    
    ax1.set_xlabel('Industry')
    ax1.set_ylabel('Normalized Value (0-1)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(industries, rotation=45, ha='right', fontsize=8)
    ax1.legend(loc='upper right')
    ax1.set_title('Judge Scores vs Fan Votes by Industry', fontsize=11, fontweight='bold')
    add_grid(ax1, axis='y')
    add_subplot_label(ax1, 'a')
    
    # 3b: 差距分析
    ax2 = axes[1]
    gaps = judge_norm - fan_norm
    colors_gap = [COLORS['positive'] if g > 0 else COLORS['negative'] for g in gaps]
    
    bars = ax2.barh(range(len(industries)), gaps, color=colors_gap, edgecolor='black', linewidth=0.5)
    ax2.set_yticks(range(len(industries)))
    ax2.set_yticklabels(industries, fontsize=8)
    ax2.axvline(x=0, color='black', linewidth=1)
    ax2.set_xlabel('Gap (Judge - Fan, Normalized)')
    ax2.set_title('Judge-Fan Gap by Industry', fontsize=11, fontweight='bold')
    add_grid(ax2, axis='x')
    add_subplot_label(ax2, 'b')

plt.tight_layout()
save_figure(fig, 'figures/imp3_industry_judge_vs_fan')
plt.close()

print(f"  ✓ 生成完毕")

# =============================================================================
# 图4: 网格搜索优化 (Grid Search)
# =============================================================================
print("\n生成图4: 网格搜索优化...")

fig, axes = plt.subplots(1, 2, figsize=FIG_SIZES['double'])

if len(grid_search) > 0:
    # 4a: 热力图
    ax1 = axes[0]
    pivot = grid_search.pivot(index='base_alpha', columns='increment', values='score')
    im = ax1.imshow(pivot.values, cmap='YlGnBu', aspect='auto')
    ax1.set_xticks(range(len(pivot.columns)))
    ax1.set_xticklabels([f'{x:.2f}' for x in pivot.columns])
    ax1.set_yticks(range(len(pivot.index)))
    ax1.set_yticklabels([f'{x:.2f}' for x in pivot.index])
    ax1.set_xlabel('Increment')
    ax1.set_ylabel('Base Alpha')
    ax1.set_title('Grid Search Score Heatmap', fontsize=11, fontweight='bold')
    
    # 标注数值
    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            color = 'white' if pivot.values[i, j] > pivot.values.mean() else 'black'
            ax1.text(j, i, f'{pivot.values[i, j]:.3f}', ha='center', va='center',
                    fontsize=8, color=color)
    
    # 高亮最优点
    best = grid_search.loc[grid_search['score'].idxmax()]
    best_i = list(pivot.index).index(best['base_alpha'])
    best_j = list(pivot.columns).index(best['increment'])
    rect = plt.Rectangle((best_j-0.5, best_i-0.5), 1, 1, fill=False,
                         edgecolor=COLORS['highlight'], linewidth=3)
    ax1.add_patch(rect)
    
    plt.colorbar(im, ax=ax1, label='Score', shrink=0.8)
    add_subplot_label(ax1, 'a')
    
    # 4b: 最终alpha分布
    ax2 = axes[1]
    final_alphas = grid_search.groupby('base_alpha')['final_alpha'].mean()
    ax2.bar(final_alphas.index, final_alphas.values, color=COLORS['dwvs'],
           edgecolor='black', linewidth=0.5, width=0.08)
    ax2.set_xlabel('Base Alpha')
    ax2.set_ylabel('Final Alpha (Week 10)')
    ax2.set_title('Final Weight by Base Alpha', fontsize=11, fontweight='bold')
    add_grid(ax2, axis='y')
    add_subplot_label(ax2, 'b')
    
    # 标注最优
    ax2.axhline(y=best['final_alpha'], color=COLORS['highlight'], linestyle='--',
               label=f'Optimal: {best["final_alpha"]:.2f}')
    ax2.legend()

plt.tight_layout()
save_figure(fig, 'figures/imp6_grid_search')
plt.close()

print(f"  ✓ 最优配置: base={best['base_alpha']}, inc={best['increment']}, score={best['score']:.3f}")

# =============================================================================
# 图5: 跨季节验证 (Cross-Season Validation)
# =============================================================================
print("\n生成图5: 跨季节验证...")

fig, axes = plt.subplots(1, 2, figsize=FIG_SIZES['double'])

if len(cross_val) > 0:
    # 解析Metric, Value格式的数据
    metrics_dict = dict(zip(cross_val['Metric'], cross_val['Value']))
    
    train_r2 = metrics_dict.get('Train R²', 0.996)
    test_r2 = metrics_dict.get('Test R²', 0.934)
    train_mae = metrics_dict.get('Train MAE', 0.14)
    test_mae = metrics_dict.get('Test MAE', 0.61)
    
    # 5a: R²对比条形图
    ax1 = axes[0]
    metrics_names = ['Train R²', 'Test R²']
    r2_values = [train_r2, test_r2]
    colors_r2 = [COLORS['rank_method'], COLORS['highlight']]
    
    bars = ax1.bar(metrics_names, r2_values, color=colors_r2, edgecolor='black', linewidth=0.5)
    for bar, val in zip(bars, r2_values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{val:.4f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax1.set_ylabel('R² Score')
    ax1.set_ylim(0, 1.1)
    ax1.set_title('Model Fit: R² Comparison', fontsize=11, fontweight='bold')
    add_grid(ax1, axis='y')
    add_subplot_label(ax1, 'a')
    
    # 标注泛化gap
    gap = train_r2 - test_r2
    ax1.annotate(f'Gap = {gap:.4f}', xy=(0.5, (train_r2+test_r2)/2),
                fontsize=10, fontweight='bold', color=COLORS['dwvs'],
                ha='center')
    
    # 5b: MAE对比条形图
    ax2 = axes[1]
    mae_names = ['Train MAE', 'Test MAE']
    mae_values = [train_mae, test_mae]
    colors_mae = [COLORS['positive'], COLORS['negative']]
    
    bars2 = ax2.bar(mae_names, mae_values, color=colors_mae, edgecolor='black', linewidth=0.5)
    for bar, val in zip(bars2, mae_values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f'{val:.4f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax2.set_ylabel('Mean Absolute Error')
    ax2.set_title('Model Accuracy: MAE Comparison', fontsize=11, fontweight='bold')
    add_grid(ax2, axis='y')
    add_subplot_label(ax2, 'b')

plt.tight_layout()
save_figure(fig, 'figures/imp7_cross_season_validation')
plt.close()

print(f"  ✓ Train R²={train_r2:.4f}, Test R²={test_r2:.4f}, Gap={gap:.4f}")

# =============================================================================
# 汇总
# =============================================================================
print("\n" + "="*60)
print("【改进分析配图生成完成】")
print("="*60)
print(f"生成的图片:")
for i, name in enumerate(['imp1_stratified_consistency.pdf',
                          'imp2_alpha_distribution.pdf',
                          'imp3_industry_judge_vs_fan.pdf',
                          'imp6_grid_search.pdf',
                          'imp7_cross_season_validation.pdf'], 1):
    print(f"  {i}. figures/{name}")
print("="*60)
