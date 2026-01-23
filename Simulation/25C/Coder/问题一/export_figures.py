"""
图片导出脚本
用于从问题一建模分析中导出所有可视化图片为PDF格式
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import poisson
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
import os

warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 设置保存路径
FIGURE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/figures'
os.makedirs(FIGURE_DIR, exist_ok=True)

def save_fig(fig, filename):
    """保存图片为PDF格式"""
    filepath = os.path.join(FIGURE_DIR, filename)
    fig.savefig(filepath, bbox_inches='tight', facecolor='white')
    print(f"✅ 已保存: {filepath}")
    plt.close(fig)

# 加载数据
print("=" * 60)
print("📊 加载数据...")
print("=" * 60)

# 获取脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 数据文件在25C根目录下
data_dir = os.path.join(script_dir, '..', '..')  # 25C目录
data_path = os.path.join(data_dir, 'processed_medal_data.csv')
df = pd.read_csv(data_path)
print(f"数据形状: {df.shape}")

# ============================================================
# 图1：目标变量分布
# ============================================================
print("\n生成图1：目标变量分布...")

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# 1. 直方图
axes[0].hist(df['Total'], bins=50, edgecolor='black', alpha=0.7, color='steelblue')
axes[0].set_xlabel('Total Medals')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Distribution of Total Medals')
axes[0].axvline(df['Total'].mean(), color='red', linestyle='--', label=f"Mean: {df['Total'].mean():.1f}")
axes[0].axvline(df['Total'].median(), color='green', linestyle='--', label=f"Median: {df['Total'].median():.1f}")
axes[0].legend()

# 2. 箱线图
axes[1].boxplot(df['Total'], vert=True)
axes[1].set_ylabel('Total Medals')
axes[1].set_title('Box Plot of Total Medals')

# 3. 按年份的趋势
yearly_stats = df.groupby('Year')['Total'].agg(['mean', 'sum', 'count'])
axes[2].plot(yearly_stats.index, yearly_stats['mean'], marker='o', color='steelblue')
axes[2].set_xlabel('Year')
axes[2].set_ylabel('Average Medals per Country')
axes[2].set_title('Average Medals Trend Over Time')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
save_fig(fig, 'fig1_target_distribution.pdf')

# ============================================================
# 图2：相关性热力图
# ============================================================
print("生成图2：相关性热力图...")

numeric_features = ['Total', 'Gold', 'Silver', 'Bronze', 'is_host', 'total_events',
                    'total_lag1', 'gold_lag1', 'total_lag2', 'total_rolling3_mean',
                    'total_change', 'participation_count', 'gold_ratio']

corr_matrix = df[numeric_features].corr()

fig = plt.figure(figsize=(12, 10))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',
            center=0, square=True, linewidths=0.5)
plt.title('Feature Correlation Matrix', fontsize=14)
plt.tight_layout()
save_fig(fig, 'fig2_correlation_heatmap.pdf')

# ============================================================
# 图3：东道主效应对比
# ============================================================
print("生成图3：东道主效应对比...")

host_medals = df[df['is_host'] == 1]['Total']
non_host_medals = df[df['is_host'] == 0]['Total']

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 1. 箱线图比较
bp = axes[0].boxplot([non_host_medals, host_medals], labels=['Non-Host', 'Host'], 
                      patch_artist=True)
bp['boxes'][0].set_facecolor('lightblue')
bp['boxes'][1].set_facecolor('coral')
axes[0].set_ylabel('Total Medals')
axes[0].set_title('Medal Distribution: Host vs Non-Host')
axes[0].grid(True, alpha=0.3)
axes[0].scatter([1, 2], [non_host_medals.mean(), host_medals.mean()], 
                color='red', s=100, zorder=5, label='Mean')
axes[0].legend()

# 2. 东道主历史表现
host_records = df[df['is_host'] == 1][['Year', 'NOC', 'Total']].sort_values('Year')
axes[1].barh(range(len(host_records)), host_records['Total'], color='coral', alpha=0.8)
axes[1].set_yticks(range(len(host_records)))
axes[1].set_yticklabels([f"{row['Year']} {row['NOC']}" for _, row in host_records.iterrows()], fontsize=8)
axes[1].set_xlabel('Total Medals')
axes[1].set_title('Host Country Performance History')
axes[1].axvline(non_host_medals.mean(), color='blue', linestyle='--', 
                label=f'Non-Host Avg: {non_host_medals.mean():.1f}')
axes[1].legend()

plt.tight_layout()
save_fig(fig, 'fig3_host_effect.pdf')

# ============================================================
# 训练模型准备
# ============================================================
print("\n准备模型训练...")

feature_columns = [
    'total_lag1', 'total_lag2', 'gold_lag1', 'total_rolling3_mean',
    'is_host', 'total_events', 'participation_count',
]

X = df[feature_columns].copy()
y = df['Total'].copy()

train_mask = df['Year'] <= 2020
test_mask = df['Year'] == 2024

X_train = X[train_mask]
X_test = X[test_mask]
y_train = y[train_mask]
y_test = y[test_mask]

# 标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 训练随机森林
rf_model = RandomForestRegressor(n_estimators=100, max_depth=10, 
                                   min_samples_split=5, min_samples_leaf=2, random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

# 训练其他模型
lr_model = LinearRegression()
lr_model.fit(X_train_scaled, y_train)
y_pred_lr = lr_model.predict(X_test_scaled)

ridge_model = Ridge(alpha=1.0)
ridge_model.fit(X_train_scaled, y_train)
y_pred_ridge = ridge_model.predict(X_test_scaled)

lasso_model = Lasso(alpha=0.1)
lasso_model.fit(X_train_scaled, y_train)
y_pred_lasso = lasso_model.predict(X_test_scaled)

gb_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5,
                                       min_samples_split=5, min_samples_leaf=2, random_state=42)
gb_model.fit(X_train, y_train)
y_pred_gb = gb_model.predict(X_test)

# ============================================================
# 图4：特征重要性
# ============================================================
print("生成图4：特征重要性...")

importance_df = pd.DataFrame({
    'Feature': feature_columns,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)

fig = plt.figure(figsize=(10, 5))
plt.barh(importance_df['Feature'], importance_df['Importance'], color='forestgreen')
plt.xlabel('Importance')
plt.title('Random Forest Feature Importance')
plt.gca().invert_yaxis()
plt.tight_layout()
save_fig(fig, 'fig4_feature_importance.pdf')

# ============================================================
# 图5：模型性能对比
# ============================================================
print("生成图5：模型性能对比...")

def calc_metrics(y_true, y_pred):
    return {
        'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
        'mae': mean_absolute_error(y_true, y_pred),
        'r2': r2_score(y_true, y_pred)
    }

lr_metrics = calc_metrics(y_test, y_pred_lr)
ridge_metrics = calc_metrics(y_test, y_pred_ridge)
lasso_metrics = calc_metrics(y_test, y_pred_lasso)
rf_metrics = calc_metrics(y_test, y_pred_rf)
gb_metrics = calc_metrics(y_test, y_pred_gb)

results = pd.DataFrame({
    'Model': ['Linear Regression', 'Ridge', 'Lasso', 'Random Forest', 'Gradient Boosting'],
    'R²': [lr_metrics['r2'], ridge_metrics['r2'], lasso_metrics['r2'], rf_metrics['r2'], gb_metrics['r2']]
})

best_model_idx = results['R²'].idxmax()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 1. R²对比
colors = ['steelblue', 'steelblue', 'steelblue', 'forestgreen', 'coral']
axes[0].barh(results['Model'], results['R²'], color=colors)
axes[0].set_xlabel('R² Score')
axes[0].set_title('Model Comparison: R² Score')
for i, v in enumerate(results['R²']):
    axes[0].text(v + 0.01, i, f'{v:.3f}', va='center')

# 2. 预测vs实际（使用Lasso）
axes[1].scatter(y_test, y_pred_lasso, alpha=0.6, color='coral')
axes[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 
             'k--', lw=2, label='Perfect Prediction')
axes[1].set_xlabel('Actual Total Medals')
axes[1].set_ylabel('Predicted Total Medals')
axes[1].set_title('Actual vs Predicted (Lasso)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
save_fig(fig, 'fig5_model_comparison.pdf')

# ============================================================
# 准备2028预测数据
# ============================================================
print("\n准备2028年预测...")

df_2024 = df[df['Year'] == 2024].copy()
df_2028 = df_2024[['NOC']].copy()

df_2028['total_lag1'] = df_2024['Total'].values
df_2028['gold_lag1'] = df_2024['Gold'].values

df_2020 = df[df['Year'] == 2020].set_index('NOC')['Total']
df_2028['total_lag2'] = df_2028['NOC'].map(df_2020).fillna(0)

def get_rolling_mean(noc):
    country_data = df[df['NOC'] == noc].sort_values('Year')
    recent_3 = country_data.tail(3)['Total'].mean()
    return recent_3

df_2028['total_rolling3_mean'] = df_2028['NOC'].apply(get_rolling_mean)
df_2028['is_host'] = (df_2028['NOC'] == 'United States').astype(int)
df_2028['total_events'] = df_2024['total_events'].values[0]
df_2028['participation_count'] = df_2024['participation_count'].values + 1

X_2028 = df_2028[feature_columns]

# 使用全量数据重新训练
gb_model_full = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5,
                                           min_samples_split=5, min_samples_leaf=2, random_state=42)
gb_model_full.fit(X, y)
df_2028['Predicted_Total'] = gb_model_full.predict(X_2028).round().astype(int)

# Bootstrap置信区间
print("计算Bootstrap置信区间...")

def bootstrap_predict_interval(X_train, y_train, X_pred, n_bootstrap=50):
    n_samples = X_pred.shape[0]
    predictions = np.zeros((n_bootstrap, n_samples))
    
    for i in range(n_bootstrap):
        idx = np.random.choice(len(X_train), size=len(X_train), replace=True)
        X_boot = X_train.iloc[idx] if hasattr(X_train, 'iloc') else X_train[idx]
        y_boot = y_train.iloc[idx] if hasattr(y_train, 'iloc') else y_train[idx]
        
        model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, 
                                           max_depth=5, random_state=42)
        model.fit(X_boot, y_boot)
        predictions[i, :] = model.predict(X_pred)
    
    mean_pred = predictions.mean(axis=0)
    lower = np.percentile(predictions, 2.5, axis=0)
    upper = np.percentile(predictions, 97.5, axis=0)
    
    return mean_pred, lower, upper

mean_pred, lower, upper = bootstrap_predict_interval(X, y, X_2028, n_bootstrap=50)

df_2028['CI_Lower'] = np.maximum(0, lower.round()).astype(int)
df_2028['CI_Upper'] = upper.round().astype(int)
df_2028['2024_Actual'] = df_2028['total_lag1']
df_2028['Change'] = df_2028['Predicted_Total'] - df_2028['2024_Actual']

predictions_2028 = df_2028.sort_values('Predicted_Total', ascending=False)

# ============================================================
# 图6：2028预测奖牌榜
# ============================================================
print("生成图6：2028预测奖牌榜...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# 1. TOP 10 预测
top10 = predictions_2028.head(10)
colors = ['gold' if h == 1 else 'steelblue' for h in top10['is_host']]
bars = axes[0].barh(range(len(top10)), top10['Predicted_Total'], color=colors)
axes[0].set_yticks(range(len(top10)))
axes[0].set_yticklabels(top10['NOC'])
axes[0].set_xlabel('Predicted Total Medals')
axes[0].set_title('2028 Los Angeles Olympics - Predicted Medal Ranking')
axes[0].invert_yaxis()

for i, (_, row) in enumerate(top10.iterrows()):
    axes[0].text(row['Predicted_Total'] + 1, i, str(row['Predicted_Total']), va='center')

from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='gold', label='Host Country'),
                   Patch(facecolor='steelblue', label='Other Countries')]
axes[0].legend(handles=legend_elements, loc='lower right')

# 2. 2024实际 vs 2028预测
x = range(len(top10))
width = 0.35

axes[1].bar([i - width/2 for i in x], top10['2024_Actual'], width, 
            label='2024 Actual', color='lightblue', edgecolor='black')
axes[1].bar([i + width/2 for i in x], top10['Predicted_Total'], width, 
            label='2028 Predicted', color='coral', edgecolor='black')
axes[1].set_xticks(x)
axes[1].set_xticklabels(top10['NOC'], rotation=45, ha='right')
axes[1].set_ylabel('Total Medals')
axes[1].set_title('2024 Actual vs 2028 Predicted (Top 10)')
axes[1].legend()
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
save_fig(fig, 'fig6_2028_prediction.pdf')

# ============================================================
# 图7：置信区间图
# ============================================================
print("生成图7：置信区间图...")

fig, ax = plt.subplots(figsize=(12, 8))

top15 = predictions_2028.head(15).copy()
top15 = top15.iloc[::-1]

y_pos = range(len(top15))
colors = ['gold' if h == 1 else 'steelblue' for h in top15['is_host']]

err_left = (top15['Predicted_Total'] - top15['CI_Lower']).clip(lower=0)
err_right = (top15['CI_Upper'] - top15['Predicted_Total']).clip(lower=0)

ax.barh(y_pos, top15['Predicted_Total'], xerr=[err_left, err_right],
        color=colors, alpha=0.8, capsize=5)

ax.scatter(top15['2024_Actual'], y_pos, color='red', marker='o', s=50, 
           zorder=5, label='2024 Actual')

ax.set_yticks(y_pos)
ax.set_yticklabels(top15['NOC'])
ax.set_xlabel('Total Medals')
ax.set_title('2028 Olympic Medal Predictions with 95% Confidence Intervals (Top 15)')

legend_elements = [
    Patch(facecolor='gold', label='Host (USA)'),
    Patch(facecolor='steelblue', label='Other Countries'),
]
ax.legend(handles=legend_elements + [plt.scatter([], [], c='red', marker='o', label='2024 Actual')], 
          loc='lower right')
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
save_fig(fig, 'fig7_confidence_interval.pdf')

# ============================================================
# 图8：泊松分布预测
# ============================================================
print("生成图8：泊松分布预测...")

# 读取原始奖牌数据
medal_counts_raw = pd.read_csv(os.path.join(data_dir, 'summerOly_medal_counts.csv'))
medal_counts_raw['NOC'] = medal_counts_raw['NOC'].str.replace('\xa0', '', regex=False).str.strip()

first_medal_year = medal_counts_raw.groupby('NOC')['Year'].min().reset_index()
first_medal_year.columns = ['NOC', 'First_Medal_Year']

first_medals_by_year = medal_counts_raw.merge(first_medal_year, on='NOC')
first_medals_by_year = first_medals_by_year[first_medals_by_year['Year'] == first_medals_by_year['First_Medal_Year']]
first_medals_count = first_medals_by_year.groupby('Year').size().reset_index(name='New_Countries')

recent_data = first_medals_count[first_medals_count['Year'] >= 2008]
lambda_param = recent_data['New_Countries'].mean()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 历史趋势
axes[0].bar(first_medals_count['Year'], first_medals_count['New_Countries'], 
            color='steelblue', alpha=0.7)
axes[0].axhline(y=lambda_param, color='red', linestyle='--', label=f'Recent Average: {lambda_param:.1f}')
axes[0].set_xlabel('Year')
axes[0].set_ylabel('Number of New Countries Winning Medals')
axes[0].set_title('Historical: New Medal-Winning Countries per Olympics')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# 概率分布
k_values = np.arange(0, 12)
pmf_values = poisson.pmf(k_values, lambda_param)
ci_90_lower = poisson.ppf(0.05, lambda_param)
ci_90_upper = poisson.ppf(0.95, lambda_param)

axes[1].bar(k_values, pmf_values, color='coral', alpha=0.8)
axes[1].axvline(x=lambda_param, color='red', linestyle='--', label=f'Expected: {lambda_param:.1f}')
axes[1].fill_between([ci_90_lower-0.5, ci_90_upper+0.5], 0, 0.3, alpha=0.2, color='green', label='90% CI')
axes[1].set_xlabel('Number of New Countries')
axes[1].set_ylabel('Probability')
axes[1].set_title('2028 Prediction: Poisson Distribution of New Medal Countries')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
save_fig(fig, 'fig8_poisson_distribution.pdf')

print("\n" + "=" * 60)
print("🎉 所有图片导出完成！")
print("=" * 60)
print(f"\n图片保存在: {FIGURE_DIR}")
print("\n导出的图片列表:")
for f in sorted(os.listdir(FIGURE_DIR)):
    print(f"  - {f}")

