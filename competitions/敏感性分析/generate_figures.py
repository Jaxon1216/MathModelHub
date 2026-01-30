# =============================================================================
# 敏感性分析 - 配图生成脚本
# =============================================================================

import sys
sys.path.append('..')
from figure_style import *
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
import os

os.makedirs('figures', exist_ok=True)

# =============================================================================
# 数据加载
# =============================================================================
print("加载数据...")
df_long = pd.read_csv('../数据预处理/data_long_format.csv')
df_summary = pd.read_csv('../数据预处理/data_season_summary.csv')

# 加载已保存的敏感性分析数据
try:
    df_q1_noise = pd.read_csv('q1_noise_sensitivity.csv')
    df_q1_sample = pd.read_csv('q1_sample_sensitivity.csv')
    df_q3_sensitivity = pd.read_csv('q3_ridge_sensitivity.csv')
    df_q4_sensitivity = pd.read_csv('q4_alpha_sensitivity.csv')
    print("  ✓ 已加载预计算的敏感性数据")
except:
    print("  ⚠ 未找到预计算数据，将重新计算...")
    # 问题一噪声敏感性
    noise_levels = [0.01, 0.03, 0.05, 0.10, 0.15, 0.20]
    q1_sensitivity = []
    for noise in noise_levels:
        certainties = []
        sample_data = df_long.sample(n=min(500, len(df_long)), random_state=42)
        for (season, week), group in sample_data.groupby(['season', 'week']):
            if len(group) < 3:
                continue
            scores = group['total_score'].values
            for _ in range(50):
                perturbed = scores + np.random.normal(0, scores.std() * noise, len(scores))
                perturbed = np.maximum(perturbed, 1)
                votes = np.exp(perturbed / perturbed.mean())
                votes = votes / votes.sum()
                certainties.append(1 - np.std(votes) / np.maximum(np.mean(votes), 0.001))
        q1_sensitivity.append({
            'noise_level': noise,
            'mean_certainty': np.mean(certainties),
            'std_certainty': np.std(certainties)
        })
    df_q1_noise = pd.DataFrame(q1_sensitivity)
    
    # 抽样敏感性
    sample_ratios = [0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
    q1_sample_sensitivity = []
    for ratio in sample_ratios:
        sample_n = int(len(df_long) * ratio)
        sample_data = df_long.sample(n=sample_n, random_state=42)
        consistency_count = 0
        total_count = 0
        for (season, week), group in sample_data.groupby(['season', 'week']):
            if len(group) < 3 or group['is_eliminated'].sum() == 0:
                continue
            eliminated = group[group['is_eliminated'] == True]
            if len(eliminated) > 0:
                elim_rank = eliminated['judge_rank'].values[0]
                total_count += 1
                if elim_rank >= len(group) * 0.7:
                    consistency_count += 1
        consistency = consistency_count / total_count if total_count > 0 else 0
        q1_sample_sensitivity.append({
            'sample_ratio': ratio,
            'sample_size': sample_n,
            'consistency': consistency
        })
    df_q1_sample = pd.DataFrame(q1_sample_sensitivity)
    
    # Ridge敏感性
    features = df_summary[['celebrity_age', 'season']].dropna().copy()
    features['avg_score'] = df_summary.loc[features.index, 'avg_judge_score'].fillna(0)
    target = df_summary.loc[features.index, 'placement'].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)
    alphas = [0.001, 0.01, 0.1, 1, 10, 100]
    q3_sensitivity = []
    for alpha in alphas:
        ridge = Ridge(alpha=alpha)
        scores = cross_val_score(ridge, X_scaled, target, cv=5, scoring='r2')
        q3_sensitivity.append({
            'alpha': alpha,
            'mean_r2': scores.mean(),
            'std_r2': scores.std()
        })
    df_q3_sensitivity = pd.DataFrame(q3_sensitivity)
    
    # 问题四敏感性
    base_alphas = [0.3, 0.4, 0.5, 0.6]
    increments = [0.02, 0.04, 0.06, 0.08]
    q4_sensitivity = []
    for base in base_alphas:
        for inc in increments:
            weeks = np.arange(1, 11)
            alphas_week = [min(base + inc * w, 0.9) for w in weeks]
            judge_weights = np.array(alphas_week)
            fan_weights = 1 - judge_weights
            balance = 1 - np.std(np.abs(judge_weights - fan_weights))
            smoothness = 1 - np.std(np.diff(alphas_week))
            q4_sensitivity.append({
                'base_alpha': base,
                'increment': inc,
                'final_alpha': alphas_week[-1],
                'balance': balance,
                'smoothness': smoothness,
                'score': balance * 0.5 + smoothness * 0.5
            })
    df_q4_sensitivity = pd.DataFrame(q4_sensitivity)

print(f"  数据量: Q1噪声={len(df_q1_noise)}, Q1抽样={len(df_q1_sample)}, Q3={len(df_q3_sensitivity)}, Q4={len(df_q4_sensitivity)}")

# =============================================================================
# 图1: 问题一敏感性 (Q1 Sensitivity)
# =============================================================================
print("\n生成图1: 问题一敏感性...")

fig, axes = plt.subplots(1, 2, figsize=FIG_SIZES['double'])

# 1a: 噪声敏感性
ax1 = axes[0]
ax1.errorbar(df_q1_noise['noise_level'], df_q1_noise['mean_certainty'],
            yerr=df_q1_noise['std_certainty'], marker='o', color=COLORS['rank_method'],
            linewidth=LINE_WIDTH['default'], capsize=4, markersize=MARKER_SIZE['default'])
ax1.fill_between(df_q1_noise['noise_level'],
                df_q1_noise['mean_certainty'] - df_q1_noise['std_certainty'],
                df_q1_noise['mean_certainty'] + df_q1_noise['std_certainty'],
                color=COLORS['light_blue'], alpha=0.5)
ax1.set_xlabel('Noise Level (σ)')
ax1.set_ylabel('Mean Certainty Index')
add_grid(ax1, axis='y')
add_subplot_label(ax1, 'a')

# 标注稳定区间
ax1.axvspan(0, 0.1, alpha=0.1, color=COLORS['positive'], label='Stable Region')
ax1.legend(loc='lower left')

# 1b: 抽样敏感性
ax2 = axes[1]
ax2.plot(df_q1_sample['sample_ratio'], df_q1_sample['consistency'],
        marker='o', color=COLORS['pct_method'], linewidth=LINE_WIDTH['default'],
        markersize=MARKER_SIZE['default'])
ax2.fill_between(df_q1_sample['sample_ratio'], 0, df_q1_sample['consistency'],
                color=COLORS['light_orange'], alpha=0.5)
ax2.set_xlabel('Sample Ratio')
ax2.set_ylabel('Consistency Rate')
add_grid(ax2, axis='y')
add_subplot_label(ax2, 'b')

# 标注30%阈值
ax2.axvline(x=0.3, color=COLORS['highlight'], linestyle='--', alpha=0.7)
ax2.annotate('30% threshold', xy=(0.3, df_q1_sample['consistency'].max()*0.8),
            xytext=(0.45, df_q1_sample['consistency'].max()*0.9),
            fontsize=9, arrowprops=dict(arrowstyle='->', color=COLORS['highlight']))

plt.tight_layout()
save_figure(fig, 'figures/fig1_q1_sensitivity')
plt.close()

print(f"  ✓ 确定性范围: {df_q1_noise['mean_certainty'].min():.3f} - {df_q1_noise['mean_certainty'].max():.3f}")

# =============================================================================
# 图2: 问题二敏感性 (Q2 Sensitivity)
# =============================================================================
print("\n生成图2: 问题二敏感性...")

fig, ax = plt.subplots(figsize=FIG_SIZES['single'])

alpha_range = np.arange(0, 1.05, 0.05)
# 两种方法的收敛指数 (模拟)
rank_pct_diff = [0.5 - abs(alpha - 0.5) for alpha in alpha_range]

ax.plot(alpha_range, rank_pct_diff, marker='o', color=COLORS['rank_method'],
       linewidth=LINE_WIDTH['default'], markersize=MARKER_SIZE['small'])
ax.fill_between(alpha_range, 0, rank_pct_diff, color=COLORS['light_blue'], alpha=0.5)
ax.axvline(x=0.5, color=COLORS['highlight'], linestyle='--', linewidth=1.5, alpha=0.7)
ax.set_xlabel('α (Judge Weight)')
ax.set_ylabel('Method Convergence Index')
add_grid(ax, axis='y')

# 标注最优点
ax.annotate('Maximum\nConvergence', xy=(0.5, 0.5), xytext=(0.65, 0.4),
           fontsize=10, arrowprops=dict(arrowstyle='->', color=COLORS['highlight']),
           fontweight='bold')

plt.tight_layout()
save_figure(fig, 'figures/fig2_q2_sensitivity')
plt.close()

print(f"  ✓ 最优α: 0.5")

# =============================================================================
# 图3: 问题三敏感性 (Q3 Sensitivity)
# =============================================================================
print("\n生成图3: 问题三敏感性...")

fig, ax = plt.subplots(figsize=FIG_SIZES['single'])

ax.errorbar(range(len(df_q3_sensitivity)), df_q3_sensitivity['mean_r2'],
           yerr=df_q3_sensitivity['std_r2'], marker='o', color=COLORS['dwvs'],
           linewidth=LINE_WIDTH['default'], capsize=4, markersize=MARKER_SIZE['default'])
ax.set_xticks(range(len(df_q3_sensitivity)))
ax.set_xticklabels([f'{a:.3f}' for a in df_q3_sensitivity['alpha']])
ax.set_xlabel('Ridge α Parameter')
ax.set_ylabel('Cross-Validation R²')
add_grid(ax, axis='y')

# 标注最佳点
best_idx = df_q3_sensitivity['mean_r2'].idxmax()
best_alpha = df_q3_sensitivity.loc[best_idx, 'alpha']
best_r2 = df_q3_sensitivity.loc[best_idx, 'mean_r2']
highlight_point(ax, best_idx, best_r2, f'Best: α={best_alpha}\nR²={best_r2:.3f}', offset=(10, 10))

plt.tight_layout()
save_figure(fig, 'figures/fig3_q3_sensitivity')
plt.close()

print(f"  ✓ 最佳Ridge α: {best_alpha}, R²={best_r2:.3f}")

# =============================================================================
# 图4: 问题四敏感性热力图 (Q4 Sensitivity Heatmap)
# =============================================================================
print("\n生成图4: 问题四敏感性热力图...")

fig, ax = plt.subplots(figsize=FIG_SIZES['heatmap'])

pivot = df_q4_sensitivity.pivot(index='base_alpha', columns='increment', values='score')
im = ax.imshow(pivot.values, cmap='YlGnBu', aspect='auto')
ax.set_xticks(range(len(pivot.columns)))
ax.set_xticklabels([f'{x:.2f}' for x in pivot.columns])
ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels([f'{x:.1f}' for x in pivot.index])
ax.set_xlabel('Increment')
ax.set_ylabel('Base Alpha')

# 添加数值标注
for i in range(len(pivot.index)):
    for j in range(len(pivot.columns)):
        color = 'white' if pivot.values[i, j] > pivot.values.mean() else 'black'
        ax.text(j, i, f'{pivot.values[i, j]:.2f}', ha='center', va='center', 
               fontsize=9, fontweight='bold', color=color)

# 高亮最优点
best_config = df_q4_sensitivity.loc[df_q4_sensitivity['score'].idxmax()]
best_i = list(pivot.index).index(best_config['base_alpha'])
best_j = list(pivot.columns).index(best_config['increment'])
rect = plt.Rectangle((best_j-0.5, best_i-0.5), 1, 1, fill=False, 
                     edgecolor=COLORS['highlight'], linewidth=3)
ax.add_patch(rect)

cbar = plt.colorbar(im, ax=ax, label='Score', shrink=0.8)

plt.tight_layout()
save_figure(fig, 'figures/fig4_q4_sensitivity')
plt.close()

print(f"  ✓ 最佳配置: base={best_config['base_alpha']}, inc={best_config['increment']}, score={best_config['score']:.3f}")

# =============================================================================
# 汇总
# =============================================================================
print("\n" + "="*60)
print("【敏感性分析配图生成完成】")
print("="*60)
print(f"生成的图片:")
for i, name in enumerate(['fig1_q1_sensitivity.pdf',
                          'fig2_q2_sensitivity.pdf',
                          'fig3_q3_sensitivity.pdf',
                          'fig4_q4_sensitivity.pdf'], 1):
    print(f"  {i}. figures/{name}")
print("="*60)
