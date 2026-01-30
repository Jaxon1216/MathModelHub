"""
问题三：图片导出脚本
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
industry_analysis = pd.read_csv('industry_analysis.csv', index_col=0)
pro_analysis = pd.read_csv('pro_dancer_analysis.csv', index_col=0)
importance = pd.read_csv('feature_importance.csv')
results = pd.read_csv('results_summary.csv')

# 读取原始数据用于scatter plot
df = pd.read_csv('../数据预处理/data_processed.csv')
vote_estimates = pd.read_csv('../问题一/vote_estimates.csv')

contestant_info = df[['celebrity_name', 'season', 'celebrity_age_during_season', 'celebrity_industry']].copy()
contestant_info = contestant_info.rename(columns={
    'celebrity_name': 'contestant',
    'celebrity_age_during_season': 'celebrity_age'
})
contestant_votes = vote_estimates.groupby(['contestant', 'season']).agg({
    'estimated_vote_prop': 'mean',
    'total_score': 'mean'
}).reset_index()
contestant_votes.columns = ['contestant', 'season', 'avg_vote_prop', 'avg_score']
analysis_df = contestant_info.merge(contestant_votes, on=['contestant', 'season'], how='left')
analysis_df = analysis_df.dropna(subset=['avg_vote_prop', 'avg_score'])

# ============================================================
# 图1：行业影响
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 8))

top_industries = industry_analysis[industry_analysis['count'] >= 3].head(10)

ax1 = axes[0]
ax1.barh(range(len(top_industries)), top_industries['avg_score_mean'], 
         xerr=top_industries['avg_score_std'].fillna(0), color=COLORS['primary'], alpha=0.7)
ax1.set_yticks(range(len(top_industries)))
ax1.set_yticklabels(top_industries.index)
ax1.set_xlabel('Average Judge Score')
ax1.invert_yaxis()

ax2 = axes[1]
ax2.barh(range(len(top_industries)), top_industries['avg_vote_mean'], 
         xerr=top_industries['avg_vote_std'].fillna(0), color=COLORS['secondary'], alpha=0.7)
ax2.set_yticks(range(len(top_industries)))
ax2.set_yticklabels(top_industries.index)
ax2.set_xlabel('Average Vote Proportion')
ax2.invert_yaxis()

plt.tight_layout()
save_fig(fig, 'fig1_industry_impact.pdf')

# ============================================================
# 图2：年龄影响
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

age_score_corr = results['age_score_corr'].values[0]
age_vote_corr = results['age_vote_corr'].values[0]

ax1 = axes[0]
ax1.scatter(analysis_df['celebrity_age'], analysis_df['avg_score'], 
            alpha=0.5, color=COLORS['primary'])
z = np.polyfit(analysis_df['celebrity_age'].dropna(), 
               analysis_df.loc[analysis_df['celebrity_age'].notna(), 'avg_score'], 1)
p = np.poly1d(z)
age_range = np.linspace(analysis_df['celebrity_age'].min(), analysis_df['celebrity_age'].max(), 100)
ax1.plot(age_range, p(age_range), 'r--', linewidth=2, label=f'r={age_score_corr:.3f}')
ax1.set_xlabel('Celebrity Age')
ax1.set_ylabel('Average Judge Score')
ax1.legend()

ax2 = axes[1]
ax2.scatter(analysis_df['celebrity_age'], analysis_df['avg_vote_prop'], 
            alpha=0.5, color=COLORS['secondary'])
z2 = np.polyfit(analysis_df['celebrity_age'].dropna(), 
                analysis_df.loc[analysis_df['celebrity_age'].notna(), 'avg_vote_prop'], 1)
p2 = np.poly1d(z2)
ax2.plot(age_range, p2(age_range), 'r--', linewidth=2, label=f'r={age_vote_corr:.3f}')
ax2.set_xlabel('Celebrity Age')
ax2.set_ylabel('Average Vote Proportion')
ax2.legend()

plt.tight_layout()
save_fig(fig, 'fig2_age_impact.pdf')

# ============================================================
# 图3：特征重要性
# ============================================================
fig, ax = plt.subplots(figsize=(12, 8))

top_features = importance.head(10)
x = np.arange(len(top_features))
width = 0.35

bars1 = ax.barh(x - width/2, top_features['score_importance'], width,
                label='Judge Score', color=COLORS['primary'])
bars2 = ax.barh(x + width/2, top_features['vote_importance'], width,
                label='Fan Vote', color=COLORS['secondary'])

ax.set_xlabel('Feature Importance')
ax.set_ylabel('Features')
ax.set_yticks(x)
ax.set_yticklabels(top_features['feature'])
ax.legend()
ax.invert_yaxis()

plt.tight_layout()
save_fig(fig, 'fig3_feature_importance.pdf')

# ============================================================
# 图4：专业舞者影响
# ============================================================
top_pros = pro_analysis[pro_analysis['count'] >= 5].head(10)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

ax1 = axes[0]
ax1.barh(range(len(top_pros)), top_pros['avg_score_mean'], 
         xerr=top_pros['avg_score_std'], color=COLORS['primary'], alpha=0.7)
ax1.set_yticks(range(len(top_pros)))
ax1.set_yticklabels(top_pros.index)
ax1.set_xlabel('Average Judge Score')
ax1.invert_yaxis()

ax2 = axes[1]
ax2.barh(range(len(top_pros)), top_pros['finalist_rate'], 
         color=COLORS['secondary'], alpha=0.7)
ax2.set_yticks(range(len(top_pros)))
ax2.set_yticklabels(top_pros.index)
ax2.set_xlabel('Finalist Rate')
ax2.invert_yaxis()

plt.tight_layout()
save_fig(fig, 'fig4_pro_dancer_impact.pdf')

# ============================================================
print("\n" + "=" * 60)
print("🎉 所有图片导出完成！")
print("=" * 60)
