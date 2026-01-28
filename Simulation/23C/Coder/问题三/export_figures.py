"""
问题三：图片导出脚本
用于从建模分析中导出所有可视化图片为PDF格式

运行方式：
    python export_figures.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
import os
import warnings

warnings.filterwarnings('ignore')

# ============================================================
# 配置
# ============================================================

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style='whitegrid')

FIGSIZE_WIDE = (12, 6)
FIGSIZE_NORMAL = (10, 6)
COLORS = {
    'primary': '#4682B4',
    'secondary': '#FF7F50',
    'accent': '#228B22',
    'neutral': '#708090'
}

FIGURE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/figures'
os.makedirs(FIGURE_DIR, exist_ok=True)

def save_fig(fig, filename):
    """保存图片为PDF格式"""
    filepath = os.path.join(FIGURE_DIR, filename)
    fig.savefig(filepath, bbox_inches='tight', facecolor='white')
    print(f"✅ 已保存: {filepath}")
    plt.close(fig)

# ============================================================
# 数据加载
# ============================================================

print("="*60)
print("问题三：图片导出脚本")
print("="*60)

df = pd.read_csv('../数据预处理/data_processed.csv')
df['date'] = pd.to_datetime(df['date'])

print(f"📊 数据加载完成: {len(df)} 条记录")

target_cols = ['try_1', 'try_2', 'try_3', 'try_4', 'try_5', 'try_6', 'try_x']
feature_cols = [
    'num_vowels', 'vowel_ratio', 'num_unique_letters', 'num_repeated_letters',
    'has_repeated', 'avg_letter_freq', 'min_letter_freq', 'max_letter_freq',
    'first_letter_freq', 'last_letter_freq'
]

colors_box = ['#2ecc71', '#3498db', '#9b59b6', '#f39c12', '#e74c3c', '#c0392b', '#7f8c8d']

# ============================================================
# 图1: 结果分布箱线图
# ============================================================

fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)

bp = ax.boxplot([df[col] for col in target_cols], 
                labels=['1 try', '2 tries', '3 tries', '4 tries', '5 tries', '6 tries', 'X'],
                patch_artist=True)

for patch, color in zip(bp['boxes'], colors_box):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_xlabel('Number of Tries', fontsize=12)
ax.set_ylabel('Percentage (%)', fontsize=12)

means = [df[col].mean() for col in target_cols]
ax.scatter(range(1, 8), means, color='red', s=80, zorder=5, label='Mean', marker='D')
ax.legend()

plt.tight_layout()
save_fig(fig, 'fig1_distribution_boxplot.pdf')

# ============================================================
# 图2: 平均结果分布柱状图
# ============================================================

fig, ax = plt.subplots(figsize=FIGSIZE_NORMAL)

mean_dist = df[target_cols].mean()
bars = ax.bar(['1', '2', '3', '4', '5', '6', 'X'], mean_dist, 
              color=colors_box, edgecolor='black', alpha=0.8)

ax.set_xlabel('Number of Tries', fontsize=12)
ax.set_ylabel('Average Percentage (%)', fontsize=12)

for bar, val in zip(bars, mean_dist):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{val:.1f}%', ha='center', fontsize=10)

plt.tight_layout()
save_fig(fig, 'fig2_average_distribution.pdf')

# ============================================================
# 图3: 特征-目标相关性热力图
# ============================================================

corr_matrix = df[feature_cols + target_cols].corr()
feature_target_corr = corr_matrix.loc[feature_cols, target_cols]

fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(feature_target_corr, annot=True, cmap='RdBu_r', center=0, 
            fmt='.2f', linewidths=0.5, ax=ax, cbar_kws={'shrink': 0.8})
ax.set_xticklabels(['1 try', '2 tries', '3 tries', '4 tries', '5 tries', '6 tries', 'X'])
plt.tight_layout()
save_fig(fig, 'fig3_feature_target_correlation.pdf')

# ============================================================
# 模型训练
# ============================================================

X = df[feature_cols].values
y = df[target_cols].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

models = {
    'Ridge Regression': MultiOutputRegressor(Ridge(alpha=1.0)),
    'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
    'Gradient Boosting': MultiOutputRegressor(GradientBoostingRegressor(n_estimators=100, 
                                              max_depth=5, random_state=42))
}

model_mae_detail = {}
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    mae_per_target = [mean_absolute_error(y_test[:, i], y_pred[:, i]) for i in range(7)]
    model_mae_detail[name] = mae_per_target

# ============================================================
# 图4: 模型MAE对比
# ============================================================

fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)

x = np.arange(7)
width = 0.25

for i, (name, maes) in enumerate(model_mae_detail.items()):
    ax.bar(x + i*width, maes, width, label=name, alpha=0.8)

ax.set_xlabel('Target Variable', fontsize=12)
ax.set_ylabel('Mean Absolute Error (%)', fontsize=12)
ax.set_xticks(x + width)
ax.set_xticklabels(['1 try', '2 tries', '3 tries', '4 tries', '5 tries', '6 tries', 'X'])
ax.legend()

plt.tight_layout()
save_fig(fig, 'fig4_model_comparison.pdf')

# ============================================================
# 最佳模型 & 图5: 特征重要性
# ============================================================

best_model = RandomForestRegressor(n_estimators=200, max_depth=10, 
                                   min_samples_split=5, random_state=42)
best_model.fit(X_train_scaled, y_train)

feature_importance = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': best_model.feature_importances_
}).sort_values('Importance', ascending=False)

fig, ax = plt.subplots(figsize=FIGSIZE_NORMAL)

fi_sorted = feature_importance.sort_values('Importance', ascending=True)
bars = ax.barh(fi_sorted['Feature'], fi_sorted['Importance'], 
               color=COLORS['primary'], edgecolor='black', alpha=0.8)

ax.set_xlabel('Feature Importance', fontsize=12)
ax.set_ylabel('Feature', fontsize=12)

for bar, val in zip(bars, fi_sorted['Importance']):
    ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2,
            f'{val:.3f}', va='center', fontsize=9)

plt.tight_layout()
save_fig(fig, 'fig5_feature_importance.pdf')

# ============================================================
# EERIE预测
# ============================================================

letter_freq = {
    'E': 12.70, 'A': 8.17, 'R': 5.99, 'I': 6.97, 'O': 7.51, 'T': 9.06, 'N': 6.75,
    'S': 6.33, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'D': 4.25, 'P': 1.93, 'M': 2.41,
    'H': 6.09, 'G': 2.02, 'B': 1.49, 'F': 2.23, 'Y': 1.97, 'W': 2.36, 'K': 0.77,
    'V': 0.98, 'X': 0.15, 'Z': 0.07, 'J': 0.15, 'Q': 0.10
}

def extract_word_features(word):
    word = word.upper()
    letters = list(word)
    unique_letters = set(letters)
    
    vowels = set('AEIOU')
    num_vowels = sum(1 for l in letters if l in vowels)
    vowel_ratio = num_vowels / len(letters)
    
    num_unique = len(unique_letters)
    num_repeated = len(letters) - num_unique
    has_repeated = 1 if num_repeated > 0 else 0
    
    freqs = [letter_freq.get(l, 0) for l in letters]
    avg_freq = np.mean(freqs)
    min_freq = np.min(freqs)
    max_freq = np.max(freqs)
    first_freq = letter_freq.get(letters[0], 0)
    last_freq = letter_freq.get(letters[-1], 0)
    
    return {
        'num_vowels': num_vowels, 'vowel_ratio': vowel_ratio,
        'num_unique_letters': num_unique, 'num_repeated_letters': num_repeated,
        'has_repeated': has_repeated, 'avg_letter_freq': avg_freq,
        'min_letter_freq': min_freq, 'max_letter_freq': max_freq,
        'first_letter_freq': first_freq, 'last_letter_freq': last_freq
    }

eerie_features = extract_word_features('EERIE')
eerie_X = np.array([[eerie_features[col] for col in feature_cols]])
eerie_X_scaled = scaler.transform(eerie_X)
eerie_pred = best_model.predict(eerie_X_scaled)[0]

# Bootstrap
n_bootstrap = 200
bootstrap_preds = []

np.random.seed(42)
X_full_scaled = scaler.fit_transform(X)

for i in range(n_bootstrap):
    idx = np.random.choice(len(X), size=len(X), replace=True)
    X_boot = X_full_scaled[idx]
    y_boot = y[idx]
    
    model_boot = RandomForestRegressor(n_estimators=100, max_depth=10, 
                                       random_state=i, n_jobs=-1)
    model_boot.fit(X_boot, y_boot)
    
    eerie_X_boot = scaler.transform(eerie_X)
    pred = model_boot.predict(eerie_X_boot)[0]
    bootstrap_preds.append(pred)

bootstrap_preds = np.array(bootstrap_preds)

ci_lower = np.percentile(bootstrap_preds, 2.5, axis=0)
ci_upper = np.percentile(bootstrap_preds, 97.5, axis=0)
pred_mean = np.mean(bootstrap_preds, axis=0)

# ============================================================
# 图6: EERIE预测vs历史平均
# ============================================================

fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)

x = np.arange(7)
width = 0.35

hist_mean = df[target_cols].mean().values
bars1 = ax.bar(x - width/2, hist_mean, width, label='Historical Average', 
               color=COLORS['neutral'], edgecolor='black', alpha=0.7)

bars2 = ax.bar(x + width/2, pred_mean, width, label='EERIE Prediction', 
               color=COLORS['primary'], edgecolor='black', alpha=0.8,
               yerr=[pred_mean - ci_lower, ci_upper - pred_mean], capsize=4)

ax.set_xlabel('Number of Tries', fontsize=12)
ax.set_ylabel('Percentage (%)', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(['1', '2', '3', '4', '5', '6', 'X'])
ax.legend()

for bar, val in zip(bars2, pred_mean):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
            f'{val:.1f}%', ha='center', fontsize=9)

plt.tight_layout()
save_fig(fig, 'fig6_eerie_prediction.pdf')

# ============================================================
# 图7: Bootstrap分布
# ============================================================

fig, axes = plt.subplots(2, 4, figsize=(16, 8))
axes = axes.flatten()

for i, col in enumerate(target_cols):
    ax = axes[i]
    ax.hist(bootstrap_preds[:, i], bins=25, color=COLORS['primary'], 
            edgecolor='black', alpha=0.7)
    ax.axvline(x=pred_mean[i], color='red', linestyle='--', linewidth=2, label='Mean')
    ax.axvline(x=ci_lower[i], color='green', linestyle=':', linewidth=2, label='95% CI')
    ax.axvline(x=ci_upper[i], color='green', linestyle=':', linewidth=2)
    ax.set_xlabel(f'{col} (%)', fontsize=10)
    ax.set_ylabel('Frequency', fontsize=10)
    ax.legend(fontsize=8)

axes[7].axis('off')

plt.tight_layout()
save_fig(fig, 'fig7_bootstrap_distribution.pdf')

# ============================================================
# 完成
# ============================================================

print("\n" + "="*60)
print("🎉 所有图片导出完成！")
print("="*60)
print(f"\n图片保存在: {FIGURE_DIR}")
for f in sorted(os.listdir(FIGURE_DIR)):
    if f.endswith('.pdf'):
        print(f"  - {f}")
