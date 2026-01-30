"""
灵敏度分析：图片导出脚本
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
noise_df = pd.read_csv('q1_noise_sensitivity.csv')
sample_df = pd.read_csv('q1_sample_sensitivity.csv')
ridge_df = pd.read_csv('q3_ridge_sensitivity.csv')
alpha_df = pd.read_csv('q4_alpha_sensitivity.csv')
q4_sensitivity = pd.read_csv('../问题四/parameter_sensitivity.csv')

# Bootstrap数据
comparison_df = pd.read_csv('../问题二/method_comparison.csv')
np.random.seed(42)
bootstrap_agreements = [comparison_df.sample(n=len(comparison_df), replace=True)['methods_agree'].mean() 
                        for _ in range(1000)]
boot_mean = np.mean(bootstrap_agreements)
boot_ci_low = np.percentile(bootstrap_agreements, 2.5)
boot_ci_high = np.percentile(bootstrap_agreements, 97.5)

# ============================================================
# 图1：问题一敏感性
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ax1 = axes[0]
ax1.errorbar(noise_df['noise_level'], noise_df['correlation_mean'], 
             yerr=noise_df['correlation_std'], fmt='o-', color=COLORS['primary'],
             capsize=5, markersize=8)
ax1.set_xlabel('Noise Level (proportion of std)')
ax1.set_ylabel('Correlation with Original Score')
ax1.set_ylim(0.3, 0.4)

ax2 = axes[1]
ax2.errorbar(sample_df['sample_ratio'], sample_df['vote_mean'], 
             yerr=sample_df['vote_mean_std'], fmt='s-', color=COLORS['secondary'],
             capsize=5, markersize=8)
ax2.axhline(sample_df[sample_df['sample_ratio']==1.0]['vote_mean'].values[0], 
            color='red', linestyle='--', label='Full sample mean')
ax2.set_xlabel('Sample Ratio')
ax2.set_ylabel('Mean Estimated Vote Proportion')
ax2.legend()

plt.tight_layout()
save_fig(fig, 'fig1_q1_sensitivity.pdf')

# ============================================================
# 图2：问题二敏感性
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

seasons = comparison_df['season'].unique()
cumulative_results = []
for n_seasons in range(5, len(seasons)+1, 5):
    selected_seasons = seasons[:n_seasons]
    subset = comparison_df[comparison_df['season'].isin(selected_seasons)]
    cumulative_results.append({
        'n_seasons': n_seasons,
        'agreement_rate': subset['methods_agree'].mean()
    })
cumulative_df = pd.DataFrame(cumulative_results)

ax1 = axes[0]
ax1.plot(cumulative_df['n_seasons'], cumulative_df['agreement_rate'], 
         'o-', color=COLORS['primary'], markersize=8)
ax1.axhline(boot_mean, color='red', linestyle='--', label=f'Final: {boot_mean:.3f}')
ax1.fill_between(cumulative_df['n_seasons'], boot_ci_low, boot_ci_high, 
                 alpha=0.2, color='red')
ax1.set_xlabel('Number of Seasons')
ax1.set_ylabel('Agreement Rate')
ax1.legend()

ax2 = axes[1]
ax2.hist(bootstrap_agreements, bins=30, color=COLORS['secondary'], alpha=0.7, edgecolor='black')
ax2.axvline(boot_mean, color='red', linewidth=2, label=f'Mean: {boot_mean:.3f}')
ax2.axvline(boot_ci_low, color='red', linestyle='--', linewidth=1)
ax2.axvline(boot_ci_high, color='red', linestyle='--', linewidth=1)
ax2.set_xlabel('Agreement Rate')
ax2.set_ylabel('Frequency')
ax2.legend()

plt.tight_layout()
save_fig(fig, 'fig2_q2_sensitivity.pdf')

# ============================================================
# 图3：问题三敏感性
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))

ax.errorbar(range(len(ridge_df)), ridge_df['score_r2_mean'], 
            yerr=ridge_df['score_r2_std'], fmt='o-', color=COLORS['primary'],
            capsize=5, markersize=10, linewidth=2)
ax.set_xticks(range(len(ridge_df)))
ax.set_xticklabels([str(a) for a in ridge_df['alpha']])
ax.set_xlabel('Ridge Alpha')
ax.set_ylabel('R² (Cross-validation)')
ax.axhline(ridge_df['score_r2_mean'].max(), color='red', linestyle='--', alpha=0.5)

plt.tight_layout()
save_fig(fig, 'fig3_q3_sensitivity.pdf')

# ============================================================
# 图4：问题四敏感性
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ax1 = axes[0]
ax1.plot(alpha_df['alpha'], alpha_df['consistency'], 'o-', 
         color=COLORS['primary'], markersize=6, linewidth=2)
best_alpha = alpha_df.loc[alpha_df['consistency'].idxmax(), 'alpha']
best_consistency = alpha_df['consistency'].max()
ax1.axvline(best_alpha, color='red', linestyle='--', 
            label=f'Best alpha: {best_alpha:.2f}')
ax1.axhline(best_consistency, color='red', linestyle=':', alpha=0.5)
ax1.set_xlabel('Alpha (Judge Weight)')
ax1.set_ylabel('Consistency Rate')
ax1.legend()

ax2 = axes[1]
pivot = q4_sensitivity.pivot(index='alpha', columns='beta', values='match_rate')
sns.heatmap(pivot, annot=True, fmt='.3f', cmap='RdYlGn', ax=ax2,
            cbar_kws={'label': 'Consistency Rate'})
ax2.set_xlabel('Beta (Improvement Bonus)')
ax2.set_ylabel('Alpha (Judge Weight)')

plt.tight_layout()
save_fig(fig, 'fig4_q4_sensitivity.pdf')

# ============================================================
print("\n" + "=" * 60)
print("🎉 所有图片导出完成！")
print("=" * 60)
