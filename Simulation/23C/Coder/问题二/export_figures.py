"""
问题二：图片导出脚本
用于从建模分析中导出所有可视化图片为PDF格式

运行方式：
    python export_figures.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from matplotlib.patches import Patch
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
print("问题二：图片导出脚本")
print("="*60)

df = pd.read_csv('../数据预处理/data_processed.csv')
df['date'] = pd.to_datetime(df['date'])

print(f"📊 数据加载完成: {len(df)} 条记录")

target = 'hard_mode_ratio'
word_features = [
    'num_vowels', 'vowel_ratio', 'num_unique_letters', 'num_repeated_letters',
    'has_repeated', 'avg_letter_freq', 'min_letter_freq', 'max_letter_freq',
    'first_letter_freq', 'last_letter_freq'
]

# ============================================================
# 图1: 困难模式占比分布
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df['hard_mode_ratio'] * 100, bins=30, color=COLORS['primary'], 
             edgecolor='black', alpha=0.7)
axes[0].axvline(x=df['hard_mode_ratio'].mean() * 100, color='red', 
                linestyle='--', linewidth=2, label=f'Mean: {df["hard_mode_ratio"].mean()*100:.2f}%')
axes[0].set_xlabel('Hard Mode Ratio (%)', fontsize=12)
axes[0].set_ylabel('Frequency', fontsize=12)
axes[0].legend()

df_sorted = df.sort_values('date')
axes[1].plot(df_sorted['date'], df_sorted['hard_mode_ratio'] * 100, 
             color=COLORS['primary'], alpha=0.6, linewidth=1)
ma7 = df_sorted['hard_mode_ratio'].rolling(7).mean() * 100
axes[1].plot(df_sorted['date'], ma7, color=COLORS['secondary'], linewidth=2, label='7-day MA')
axes[1].set_xlabel('Date', fontsize=12)
axes[1].set_ylabel('Hard Mode Ratio (%)', fontsize=12)
axes[1].legend()

plt.tight_layout()
save_fig(fig, 'fig1_hard_mode_distribution.pdf')

# ============================================================
# 图2: 单词属性分布
# ============================================================

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()
plot_features = ['num_vowels', 'num_repeated_letters', 'avg_letter_freq', 
                 'min_letter_freq', 'num_unique_letters', 'vowel_ratio']

for i, feat in enumerate(plot_features):
    axes[i].hist(df[feat], bins=20, color=COLORS['primary'], edgecolor='black', alpha=0.7)
    axes[i].axvline(x=df[feat].mean(), color='red', linestyle='--', linewidth=2)
    axes[i].set_xlabel(feat, fontsize=11)
    axes[i].set_ylabel('Frequency', fontsize=11)

plt.tight_layout()
save_fig(fig, 'fig2_word_features_distribution.pdf')

# ============================================================
# 相关性分析
# ============================================================

correlations = []
for feat in word_features:
    r, p = stats.pearsonr(df[feat], df[target])
    correlations.append({
        'Feature': feat, 'Pearson_r': r, 'p_value': p,
        'Significant': 'Yes' if p < 0.05 else 'No'
    })
corr_df = pd.DataFrame(correlations).sort_values('p_value')

# ============================================================
# 图3: 相关性热力图
# ============================================================

corr_features = word_features + [target]
corr_matrix = df[corr_features].corr()

fig, ax = plt.subplots(figsize=(12, 10))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='RdBu_r', center=0, 
            fmt='.3f', square=True, linewidths=0.5, ax=ax, cbar_kws={'shrink': 0.8})
plt.tight_layout()
save_fig(fig, 'fig3_correlation_heatmap.pdf')

# ============================================================
# 图4: 相关系数柱状图
# ============================================================

fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
corr_df_sorted = corr_df.sort_values('Pearson_r', key=abs, ascending=True)

colors = [COLORS['accent'] if sig == 'Yes' else COLORS['neutral'] 
          for sig in corr_df_sorted['Significant']]

bars = ax.barh(corr_df_sorted['Feature'], corr_df_sorted['Pearson_r'], 
               color=colors, edgecolor='black', alpha=0.8)

ax.axvline(x=0, color='black', linewidth=1)
ax.set_xlabel('Pearson Correlation Coefficient', fontsize=12)
ax.set_ylabel('Word Feature', fontsize=12)

legend_elements = [Patch(facecolor=COLORS['accent'], edgecolor='black', label='Significant (p<0.05)'),
                   Patch(facecolor=COLORS['neutral'], edgecolor='black', label='Not Significant')]
ax.legend(handles=legend_elements, loc='lower right')

plt.tight_layout()
save_fig(fig, 'fig4_correlation_barplot.pdf')

# ============================================================
# 多元线性回归
# ============================================================

X = df[word_features].copy()
y = df[target].copy()

scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
X_scaled_const = sm.add_constant(X_scaled)

model = sm.OLS(y, X_scaled_const).fit()

# ============================================================
# 图5: 回归系数
# ============================================================

regression_results = pd.DataFrame({
    'Feature': model.params.index[1:],
    'Coefficient': model.params.values[1:],
    'p_value': model.pvalues.values[1:],
    'Significant': ['Yes' if p < 0.05 else 'No' for p in model.pvalues.values[1:]]
}).sort_values('p_value')

fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)

conf_int = model.conf_int().iloc[1:]
sorted_features = regression_results.sort_values('Coefficient', key=abs, ascending=True)['Feature']

y_pos = range(len(sorted_features))
coefs = [model.params[feat] for feat in sorted_features]
errors = [(model.params[feat] - conf_int.loc[feat, 0], 
           conf_int.loc[feat, 1] - model.params[feat]) for feat in sorted_features]
errors = np.array(errors).T

colors = [COLORS['accent'] if model.pvalues[feat] < 0.05 else COLORS['neutral'] 
          for feat in sorted_features]

ax.barh(y_pos, coefs, xerr=errors, color=colors, edgecolor='black', alpha=0.8, capsize=3)
ax.axvline(x=0, color='black', linewidth=1)
ax.set_yticks(y_pos)
ax.set_yticklabels(sorted_features)
ax.set_xlabel('Standardized Coefficient (with 95% CI)', fontsize=12)
ax.set_ylabel('Feature', fontsize=12)

legend_elements = [Patch(facecolor=COLORS['accent'], edgecolor='black', label='Significant (p<0.05)'),
                   Patch(facecolor=COLORS['neutral'], edgecolor='black', label='Not Significant')]
ax.legend(handles=legend_elements, loc='lower right')

plt.tight_layout()
save_fig(fig, 'fig5_regression_coefficients.pdf')

# ============================================================
# 随机森林
# ============================================================

rf_model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=5)
rf_model.fit(X, y)

feature_importance = pd.DataFrame({
    'Feature': word_features,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)

# ============================================================
# 图6: 特征重要性
# ============================================================

fig, ax = plt.subplots(figsize=FIGSIZE_NORMAL)
feature_importance_sorted = feature_importance.sort_values('Importance', ascending=True)

bars = ax.barh(feature_importance_sorted['Feature'], 
               feature_importance_sorted['Importance'],
               color=COLORS['primary'], edgecolor='black', alpha=0.8)

ax.set_xlabel('Feature Importance', fontsize=12)
ax.set_ylabel('Feature', fontsize=12)

for bar, val in zip(bars, feature_importance_sorted['Importance']):
    ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2,
            f'{val:.3f}', va='center', fontsize=9)

plt.tight_layout()
save_fig(fig, 'fig6_feature_importance.pdf')

# ============================================================
# 图7: 散点图
# ============================================================

key_features = ['num_vowels', 'num_repeated_letters', 'avg_letter_freq', 'min_letter_freq']

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()

for i, feat in enumerate(key_features):
    ax = axes[i]
    ax.scatter(df[feat], df['hard_mode_ratio'] * 100, 
               alpha=0.5, color=COLORS['primary'], edgecolor='white', s=50)
    
    z = np.polyfit(df[feat], df['hard_mode_ratio'] * 100, 1)
    p = np.poly1d(z)
    x_line = np.linspace(df[feat].min(), df[feat].max(), 100)
    ax.plot(x_line, p(x_line), color=COLORS['secondary'], linewidth=2, linestyle='--')
    
    r, pval = stats.pearsonr(df[feat], df['hard_mode_ratio'])
    ax.text(0.05, 0.95, f'r = {r:.3f}\np = {pval:.3f}', 
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    ax.set_xlabel(feat, fontsize=11)
    ax.set_ylabel('Hard Mode Ratio (%)', fontsize=11)

plt.tight_layout()
save_fig(fig, 'fig7_scatter_plots.pdf')

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
