"""
2024 MCM C题 - 图片统一导出脚本

运行此脚本将重新生成所有问题的图片并保存到各自的figures目录
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve
from scipy import stats
import os
import warnings

warnings.filterwarnings('ignore')

# 设置
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style='whitegrid')

COLORS = {
    'p1': '#E74C3C',
    'p2': '#3498DB',
    'accent': '#27AE60',
    'neutral': '#95A5A6'
}

np.random.seed(42)

# 创建目录
for folder in ['问题一/figures', '问题二/figures', '问题三/figures', '问题四/figures']:
    os.makedirs(folder, exist_ok=True)

print("="*60)
print("开始导出所有图片...")
print("="*60)

# ========== 加载数据 ==========
df = pd.read_csv('processed_wimbledon_with_momentum.csv')
print(f"\n数据加载成功: {df.shape}")

# ========== 问题一图片 ==========
print("\n--- 问题一 ---")

final = df[df['match_id'] == '2023-wimbledon-1701'].copy()

# 图1: 决赛势头曲线
fig, ax = plt.subplots(figsize=(14, 6))
x = range(len(final))
momentum = final['momentum'].values
ax.fill_between(x, momentum, 0, where=(momentum >= 0), color=COLORS['p1'], alpha=0.3)
ax.fill_between(x, momentum, 0, where=(momentum < 0), color=COLORS['p2'], alpha=0.3)
ax.plot(x, momentum, color='black', linewidth=1.5, alpha=0.8)
set_changes = final[final['set_victor'] != 0].index.tolist()
for idx in set_changes[:-1]:
    point_idx = final.index.get_loc(idx)
    ax.axvline(x=point_idx, color='gray', linestyle='--', linewidth=1, alpha=0.7)
ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax.set_xlabel('Point Number', fontsize=12)
ax.set_ylabel('Momentum Score', fontsize=12)
ax.text(len(final)*0.02, ax.get_ylim()[1]*0.7, 'Alcaraz →', fontsize=10, color=COLORS['p1'])
ax.text(len(final)*0.02, ax.get_ylim()[0]*0.7, '← Djokovic', fontsize=10, color=COLORS['p2'])
plt.tight_layout()
plt.savefig('问题一/figures/fig1_final_momentum_curve.pdf', bbox_inches='tight')
plt.close()
print("✅ fig1_final_momentum_curve.pdf")

# 图2: 热力图
n_segments = 10
heatmap_data = []
for set_no in range(1, 6):
    set_data = final[final['set_no'] == set_no]['momentum'].values
    if len(set_data) > 0:
        segment_size = max(1, len(set_data) // n_segments)
        segments = [np.mean(set_data[i*segment_size:min((i+1)*segment_size, len(set_data))]) 
                   if i*segment_size < len(set_data) else np.nan for i in range(n_segments)]
        heatmap_data.append(segments)

heatmap_df = pd.DataFrame(heatmap_data, 
                          index=[f'Set {i}' for i in range(1, 6)],
                          columns=[f'{i*10}%' for i in range(1, 11)])

fig, ax = plt.subplots(figsize=(12, 5))
cmap = sns.diverging_palette(240, 10, as_cmap=True)
sns.heatmap(heatmap_df, cmap=cmap, center=0, annot=True, fmt='.1f',
            cbar_kws={'label': 'Momentum Score'}, ax=ax, linewidths=0.5)
ax.set_xlabel('Progress within Set', fontsize=12)
ax.set_ylabel('Set Number', fontsize=12)
plt.tight_layout()
plt.savefig('问题一/figures/fig2_momentum_heatmap.pdf', bbox_inches='tight')
plt.close()
print("✅ fig2_momentum_heatmap.pdf")

# 图5: 势头与结果
match_stats = []
for match_id in df['match_id'].unique():
    match_data = df[df['match_id'] == match_id]
    final_p1_sets = match_data['p1_sets'].iloc[-1]
    final_p2_sets = match_data['p2_sets'].iloc[-1]
    if match_data['set_victor'].iloc[-1] == 1:
        final_p1_sets += 1
    else:
        final_p2_sets += 1
    winner = 1 if final_p1_sets > final_p2_sets else 2
    match_stats.append({
        'match_id': match_id,
        'winner': winner,
        'avg_momentum': match_data['momentum'].mean(),
        'p1_time_ahead': (match_data['momentum'] > 0).mean(),
    })
stats_df = pd.DataFrame(match_stats)

fig, ax = plt.subplots(figsize=(10, 6))
p1_wins = stats_df[stats_df['winner'] == 1]
p2_wins = stats_df[stats_df['winner'] == 2]
ax.scatter(p1_wins['p1_time_ahead'], p1_wins['avg_momentum'], 
           color=COLORS['p1'], s=80, alpha=0.7, label='P1 Won')
ax.scatter(p2_wins['p1_time_ahead'], p2_wins['avg_momentum'], 
           color=COLORS['p2'], s=80, alpha=0.7, label='P2 Won')
ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax.axvline(x=0.5, color='gray', linestyle='--', alpha=0.5)
ax.set_xlabel('Proportion of Time P1 Ahead in Momentum', fontsize=12)
ax.set_ylabel('Average Momentum Score', fontsize=12)
ax.legend()
plt.tight_layout()
plt.savefig('问题一/figures/fig5_momentum_vs_result.pdf', bbox_inches='tight')
plt.close()
print("✅ fig5_momentum_vs_result.pdf")

# ========== 问题二图片 ==========
print("\n--- 问题二 ---")

def runs_test(sequence):
    n = len(sequence)
    n1 = sum(sequence == 1)
    n2 = sum(sequence == 2)
    if n1 == 0 or n2 == 0:
        return np.nan, np.nan, np.nan, np.nan
    runs = 1
    for i in range(1, n):
        if sequence.iloc[i] != sequence.iloc[i-1]:
            runs += 1
    expected_runs = (2 * n1 * n2) / n + 1
    var_runs = (2 * n1 * n2 * (2 * n1 * n2 - n)) / (n**2 * (n - 1))
    if var_runs <= 0:
        return runs, expected_runs, np.nan, np.nan
    z_stat = (runs - expected_runs) / np.sqrt(var_runs)
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    return runs, expected_runs, z_stat, p_value

runs_results = []
for match_id in df['match_id'].unique():
    match_df = df[df['match_id'] == match_id]
    n_runs, expected, z_stat, p_val = runs_test(match_df['point_victor'])
    if not np.isnan(z_stat):
        runs_results.append({
            'runs_ratio': n_runs / expected,
            'z_stat': z_stat,
            'significant': p_val < 0.05
        })
runs_df = pd.DataFrame(runs_results)

# 图1: 游程检验分布
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
ax1 = axes[0]
ax1.hist(runs_df['z_stat'], bins=15, color=COLORS['p1'], alpha=0.7, edgecolor='black')
ax1.axvline(x=0, color='black', linestyle='--', linewidth=1)
ax1.axvline(x=-1.96, color='red', linestyle='--', linewidth=1, label='p=0.05')
ax1.axvline(x=1.96, color='red', linestyle='--', linewidth=1)
ax1.set_xlabel('Z-statistic', fontsize=12)
ax1.set_ylabel('Number of Matches', fontsize=12)
ax1.legend()

ax2 = axes[1]
ax2.hist(runs_df['runs_ratio'], bins=15, color=COLORS['p1'], alpha=0.7, edgecolor='black')
ax2.axvline(x=1.0, color='black', linestyle='--', linewidth=2, label='Random Expectation')
ax2.axvline(x=runs_df['runs_ratio'].mean(), color='red', linestyle='-', linewidth=2, 
            label=f'Actual Mean = {runs_df["runs_ratio"].mean():.3f}')
ax2.set_xlabel('Runs Ratio (Actual / Expected)', fontsize=12)
ax2.set_ylabel('Number of Matches', fontsize=12)
ax2.legend()
plt.tight_layout()
plt.savefig('问题二/figures/fig1_runs_test_distribution.pdf', bbox_inches='tight')
plt.close()
print("✅ fig1_runs_test_distribution.pdf")

# 图2: 条件概率
all_after_p1, all_after_p2 = [], []
for match_id in df['match_id'].unique():
    victor = df[df['match_id'] == match_id]['point_victor'].values
    for i in range(1, len(victor)):
        if victor[i-1] == 1:
            all_after_p1.append(1 if victor[i] == 1 else 0)
        else:
            all_after_p2.append(1 if victor[i] == 1 else 0)

p1_overall = (df['point_victor'] == 1).mean()
p1_after_p1 = np.mean(all_after_p1)
p1_after_p2 = np.mean(all_after_p2)

fig, ax = plt.subplots(figsize=(10, 6))
categories = ['Overall Win Rate', 'After P1 Win', 'After P2 Win']
values = [p1_overall, p1_after_p1, p1_after_p2]
bars = ax.bar(categories, values, color=[COLORS['neutral'], COLORS['p1'], COLORS['p2']],
              edgecolor='black', alpha=0.8)
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f'{val:.3f}', ha='center', fontsize=11)
ax.set_ylabel('P(P1 Wins Next Point)', fontsize=12)
ax.set_ylim(0, 0.7)
plt.tight_layout()
plt.savefig('问题二/figures/fig2_conditional_probability.pdf', bbox_inches='tight')
plt.close()
print("✅ fig2_conditional_probability.pdf")

# ========== 问题三图片 ==========
print("\n--- 问题三 ---")

df['momentum_prev'] = df.groupby('match_id')['momentum'].shift(1)
df['momentum_shift'] = (
    (df['momentum'] * df['momentum_prev'] < 0) & 
    (abs(df['momentum_prev']) > 1)
).astype(int)

feature_cols = ['set_no', 'games_in_set', 'sets_played', 'point_diff', 'momentum_prev',
                'p1_streak_prev', 'p2_streak_prev', 'is_p1_serving', 'serve_no',
                'is_break_point', 'is_key_point', 'rally_count', 'point_duration',
                'p1_rolling_win_rate_5']
available_features = [col for col in feature_cols if col in df.columns]
model_df = df.dropna(subset=available_features + ['momentum_shift']).copy()

X = model_df[available_features]
y = model_df['momentum_shift']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_split=20,
                                   class_weight='balanced', random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)
y_pred_proba = rf_model.predict_proba(X_test)[:, 1]
auc_score = roc_auc_score(y_test, y_pred_proba)

# 图1: ROC曲线
fig, ax = plt.subplots(figsize=(10, 6))
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
ax.plot(fpr, tpr, color=COLORS['p1'], linewidth=2, label=f'Random Forest (AUC = {auc_score:.3f})')
ax.plot([0, 1], [0, 1], color='gray', linestyle='--', label='Random Baseline')
ax.set_xlabel('False Positive Rate', fontsize=12)
ax.set_ylabel('True Positive Rate', fontsize=12)
ax.legend(loc='lower right')
ax.set_xlim([0, 1])
ax.set_ylim([0, 1])
plt.tight_layout()
plt.savefig('问题三/figures/fig1_roc_curve.pdf', bbox_inches='tight')
plt.close()
print("✅ fig1_roc_curve.pdf")

# 图2: 特征重要性
feature_importance = pd.DataFrame({
    'feature': available_features,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

feature_names = {
    'momentum_prev': 'Previous Momentum', 'point_diff': 'Point Difference',
    'p1_streak_prev': 'P1 Previous Streak', 'p2_streak_prev': 'P2 Previous Streak',
    'p1_rolling_win_rate_5': 'P1 Rolling Win Rate', 'rally_count': 'Rally Count',
    'point_duration': 'Point Duration', 'is_break_point': 'Break Point',
    'is_key_point': 'Key Point', 'is_p1_serving': 'P1 Serving',
    'serve_no': 'Serve Number', 'set_no': 'Set Number',
    'games_in_set': 'Games in Set', 'sets_played': 'Sets Played'
}

fig, ax = plt.subplots(figsize=(10, 8))
plot_data = feature_importance.copy()
plot_data['feature_name'] = plot_data['feature'].map(feature_names).fillna(plot_data['feature'])
colors = [COLORS['p1'] if imp > 0.1 else COLORS['neutral'] for imp in plot_data['importance']]
ax.barh(plot_data['feature_name'], plot_data['importance'], color=colors, edgecolor='black', alpha=0.8)
ax.set_xlabel('Feature Importance', fontsize=12)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('问题三/figures/fig2_feature_importance.pdf', bbox_inches='tight')
plt.close()
print("✅ fig2_feature_importance.pdf")

# ========== 问题四图片 ==========
print("\n--- 问题四 ---")

model_df['round'] = model_df['match_id'].apply(lambda x: int(x.split('-')[2][0:2]))
round_names = {13: 'Round 3', 14: 'Round 4', 15: 'Quarter Final', 16: 'Semi Final', 17: 'Final'}

lomo_results = []
for test_match in model_df['match_id'].unique():
    train_df = model_df[model_df['match_id'] != test_match]
    test_df = model_df[model_df['match_id'] == test_match]
    if test_df['momentum_shift'].sum() < 1:
        continue
    
    X_train, y_train = train_df[available_features], train_df['momentum_shift']
    X_test, y_test = test_df[available_features], test_df['momentum_shift']
    
    rf = RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_split=20,
                                 class_weight='balanced', random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    y_pred_proba = rf.predict_proba(X_test)[:, 1]
    
    try:
        auc = roc_auc_score(y_test, y_pred_proba)
    except:
        auc = np.nan
    
    avg_momentum = test_df['momentum'].mean()
    final_row = test_df.iloc[-1]
    actual_p1_sets = final_row['p1_sets'] + (1 if final_row['set_victor'] == 1 else 0)
    actual_p2_sets = final_row['p2_sets'] + (1 if final_row['set_victor'] == 2 else 0)
    actual_winner = 1 if actual_p1_sets > actual_p2_sets else 2
    predicted_winner = 1 if avg_momentum > 0 else 2
    
    lomo_results.append({
        'match_id': test_match,
        'round': test_df['round'].iloc[0],
        'auc': auc,
        'correct': actual_winner == predicted_winner
    })

lomo_df = pd.DataFrame(lomo_results)

# 图1: 留一验证结果
fig, ax = plt.subplots(figsize=(12, 6))
plot_df = lomo_df.sort_values(['round', 'match_id']).reset_index(drop=True)
colors = [COLORS['accent'] if c else COLORS['p1'] for c in plot_df['correct']]
ax.bar(range(len(plot_df)), plot_df['auc'].fillna(0), color=colors, edgecolor='black', alpha=0.8)
ax.axhline(y=lomo_df['auc'].mean(), color='red', linestyle='--', label=f'Mean AUC = {lomo_df["auc"].mean():.3f}')
ax.axhline(y=0.5, color='gray', linestyle=':', label='Random Baseline')
ax.set_xlabel('Match Index', fontsize=12)
ax.set_ylabel('AUC Score', fontsize=12)
ax.legend(loc='lower right')
ax.set_ylim(0, 1)
plt.tight_layout()
plt.savefig('问题四/figures/fig1_lomo_results.pdf', bbox_inches='tight')
plt.close()
print("✅ fig1_lomo_results.pdf")

# 图3: 适用性
fig, ax = plt.subplots(figsize=(10, 6))
scenarios = ['Women\'s Tennis', 'Other Grand Slams', 'ATP Tour', 'Table Tennis', 'Team Sports']
applicability = [4, 4, 3, 3, 2]
colors = [COLORS['accent'] if a >= 4 else COLORS['p2'] if a >= 3 else COLORS['p1'] for a in applicability]
ax.barh(scenarios, applicability, color=colors, edgecolor='black', alpha=0.8)
ax.set_xlabel('Applicability Score (1-5)', fontsize=12)
ax.set_xlim(0, 5)
for i, (s, a) in enumerate(zip(scenarios, applicability)):
    ax.text(a + 0.1, i, f'{a}/5', va='center', fontsize=11)
plt.tight_layout()
plt.savefig('问题四/figures/fig3_applicability.pdf', bbox_inches='tight')
plt.close()
print("✅ fig3_applicability.pdf")

# ========== 完成 ==========
print("\n" + "="*60)
print("🎉 所有图片导出完成！")
print("="*60)

# 列出所有图片
for folder in ['问题一/figures', '问题二/figures', '问题三/figures', '问题四/figures']:
    print(f"\n{folder}/")
    for f in sorted(os.listdir(folder)):
        print(f"  - {f}")
