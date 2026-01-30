"""
问题一：图片导出脚本
与问题一建模分析.ipynb中的图片保持一致
图片命名：
  - fig1_consistency_analysis.pdf
  - fig2_uncertainty_analysis.pdf  
  - fig3_controversial_analysis.pdf
  - fig4_vote_score_relationship.pdf
  - fig5_certainty_distribution.pdf
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style='whitegrid')

# 设置保存路径
FIGURE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/figures'
os.makedirs(FIGURE_DIR, exist_ok=True)

# 标准配色
COLORS = {
    'primary': '#4682B4',
    'secondary': '#FF7F50',
    'accent': '#228B22',
    'neutral': '#708090'
}

def save_fig(fig, filename):
    """保存图片为PDF格式"""
    filepath = os.path.join(FIGURE_DIR, filename)
    fig.savefig(filepath, bbox_inches='tight', facecolor='white')
    print(f"✅ 已保存: {filepath}")
    plt.close(fig)

# ============================================================
# 读取数据
# ============================================================
vote_estimates = pd.read_csv('vote_estimates.csv')
verification_df = pd.read_csv('verification_results.csv')
certainty_df = pd.read_csv('certainty_metrics.csv')

# ============================================================
# 图1: 一致性分析 (fig1_consistency_analysis.pdf)
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

accuracy_by_season = verification_df.groupby('season')['is_correct'].mean()
accuracy = verification_df['is_correct'].mean()

ax1 = axes[0]
seasons = accuracy_by_season.index
accuracies = accuracy_by_season.values
colors = [COLORS['primary'] if acc >= 0.8 else COLORS['secondary'] if acc >= 0.6 else COLORS['neutral'] 
          for acc in accuracies]
ax1.bar(seasons, accuracies, color=colors)
ax1.axhline(y=accuracy, color='red', linestyle='--', linewidth=2, label=f'Overall: {accuracy:.1%}')
ax1.set_xlabel('Season')
ax1.set_ylabel('Consistency Rate')
ax1.set_ylim(0, 1.1)
ax1.legend()

ax2 = axes[1]
acc_by_n = verification_df.groupby('n_contestants')['is_correct'].agg(['mean', 'count'])
ax2.bar(acc_by_n.index, acc_by_n['mean'], color=COLORS['primary'])
ax2.set_xlabel('Number of Contestants')
ax2.set_ylabel('Consistency Rate')
ax2.set_ylim(0, 1.1)

plt.tight_layout()
save_fig(fig, 'fig1_consistency_analysis.pdf')

# ============================================================
# 图2: 不确定性分析 (fig2_uncertainty_analysis.pdf)
# 注：如果没有bootstrap数据，这里用准确率按方法对比代替
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 左图：按投票方式的准确率
ax1 = axes[0]
accuracy_by_method = verification_df.groupby('voting_method')['is_correct'].mean()
bars = ax1.bar(accuracy_by_method.index, accuracy_by_method.values, 
              color=[COLORS['primary'], COLORS['secondary']])
ax1.set_ylabel('Consistency Rate')
ax1.set_ylim(0, 1.1)
for bar, val in zip(bars, accuracy_by_method.values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
            f'{val:.1%}', ha='center', fontsize=12)

# 右图：确定性分布直方图
ax2 = axes[1]
ax2.hist(certainty_df['certainty'], bins=30, color=COLORS['primary'], edgecolor='white', alpha=0.7)
ax2.axvline(certainty_df['certainty'].mean(), color='red', linestyle='--', 
           label=f'Mean: {certainty_df["certainty"].mean():.3f}')
ax2.set_xlabel('Certainty Score')
ax2.set_ylabel('Frequency')
ax2.legend()

plt.tight_layout()
save_fig(fig, 'fig2_uncertainty_analysis.pdf')

# ============================================================
# 图3: 争议选手分析 (fig3_controversial_analysis.pdf)
# ============================================================
controversial = [
    ('Jerry Rice', 2),
    ('Billy Ray Cyrus', 4),
    ('Bristol Palin', 11),
    ('Bobby Bones', 27)
]

controversy_data = []
for name, season in controversial:
    player_data = vote_estimates[(vote_estimates['contestant'] == name) & 
                                  (vote_estimates['season'] == season)]
    if len(player_data) == 0:
        continue
    
    vote_ranks = []
    judge_ranks = []
    
    for week in player_data['week'].unique():
        week_all = vote_estimates[(vote_estimates['season'] == season) & 
                                   (vote_estimates['week'] == week)]
        if len(week_all) == 0:
            continue
        
        week_all_sorted = week_all.sort_values('estimated_vote_prop', ascending=False)
        if name in week_all_sorted['contestant'].tolist():
            vote_rank = week_all_sorted['contestant'].tolist().index(name) + 1
            vote_ranks.append(vote_rank)
        
        week_all_sorted = week_all.sort_values('total_score', ascending=False)
        if name in week_all_sorted['contestant'].tolist():
            judge_rank = week_all_sorted['contestant'].tolist().index(name) + 1
            judge_ranks.append(judge_rank)
    
    controversy_data.append({
        'contestant': name,
        'season': season,
        'avg_vote_rank': np.mean(vote_ranks) if vote_ranks else 0,
        'avg_judge_rank': np.mean(judge_ranks) if judge_ranks else 0
    })

controversy_df = pd.DataFrame(controversy_data)

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(controversy_df))
width = 0.35

bars1 = ax.bar(x - width/2, controversy_df['avg_judge_rank'], width, 
               label='Avg Judge Rank', color=COLORS['secondary'])
bars2 = ax.bar(x + width/2, controversy_df['avg_vote_rank'], width,
               label='Avg Fan Vote Rank', color=COLORS['primary'])

ax.set_xlabel('Controversial Contestants')
ax.set_ylabel('Average Weekly Rank (1=Best)')
ax.set_xticks(x)
ax.set_xticklabels([f"{row['contestant']}\n(S{row['season']})" for _, row in controversy_df.iterrows()])
ax.legend()
# 不反转Y轴，让柱状图从下往上延伸

plt.tight_layout()
save_fig(fig, 'fig3_controversial_analysis.pdf')

# ============================================================
# 图4: 投票vs得分关系 (fig4_vote_score_relationship.pdf)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
correlation = vote_estimates['total_score'].corr(vote_estimates['estimated_vote_prop'])
ax.scatter(vote_estimates['total_score'], vote_estimates['estimated_vote_prop'],
           alpha=0.3, color=COLORS['primary'], s=20)
z = np.polyfit(vote_estimates['total_score'], vote_estimates['estimated_vote_prop'], 1)
p = np.poly1d(z)
x_line = np.linspace(vote_estimates['total_score'].min(), vote_estimates['total_score'].max(), 100)
ax.plot(x_line, p(x_line), 'r--', linewidth=2, label=f'r = {correlation:.3f}')
ax.set_xlabel('Judge Total Score')
ax.set_ylabel('Estimated Fan Vote Proportion')
ax.legend()
plt.tight_layout()
save_fig(fig, 'fig4_vote_score_relationship.pdf')

# ============================================================
# 图5: 确定性分布 (fig5_certainty_distribution.pdf)
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ax1 = axes[0]
ax1.hist(certainty_df['certainty'], bins=30, color=COLORS['primary'], edgecolor='white', alpha=0.7)
ax1.axvline(certainty_df['certainty'].mean(), color='red', linestyle='--', 
           label=f'Mean: {certainty_df["certainty"].mean():.3f}')
ax1.set_xlabel('Certainty Score')
ax1.set_ylabel('Frequency')
ax1.legend()

ax2 = axes[1]
cert_by_n = certainty_df.groupby('n_contestants')['certainty'].mean()
ax2.bar(cert_by_n.index, cert_by_n.values, color=COLORS['primary'])
ax2.set_xlabel('Number of Contestants')
ax2.set_ylabel('Average Certainty')
ax2.set_ylim(0, 0.6)

plt.tight_layout()
save_fig(fig, 'fig5_certainty_distribution.pdf')

# ============================================================
print("\n" + "=" * 60)
print("🎉 所有图片导出完成！")
print("=" * 60)
print(f"\n图片保存在: {FIGURE_DIR}")
for f in sorted(os.listdir(FIGURE_DIR)):
    print(f"  - {f}")
