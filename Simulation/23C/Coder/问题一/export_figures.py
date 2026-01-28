"""
问题一：图片导出脚本
用于从建模分析中导出所有可视化图片为PDF格式

运行方式：
    python export_figures.py

注意：
    - 图片不含标题（标注在论文正文中）
    - 所有图片为PDF矢量格式
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os
import warnings

warnings.filterwarnings('ignore')

# ============================================================
# 配置
# ============================================================

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Seaborn主题
sns.set_theme(style='whitegrid')

# 标准尺寸
FIGSIZE_NORMAL = (10, 6)
FIGSIZE_WIDE = (12, 6)
FIGSIZE_TALL = (12, 10)

# 项目标准配色
COLORS = {
    'primary': '#4682B4',    # steelblue
    'secondary': '#FF7F50',  # coral
    'accent': '#228B22',     # forestgreen
    'neutral': '#708090'     # slategray
}

# 设置保存路径
FIGURE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/figures'
os.makedirs(FIGURE_DIR, exist_ok=True)

def save_fig(fig, filename):
    """保存图片为PDF格式（无标题）"""
    filepath = os.path.join(FIGURE_DIR, filename)
    fig.savefig(filepath, bbox_inches='tight', facecolor='white')
    print(f"✅ 已保存: {filepath}")
    plt.close(fig)

# ============================================================
# 数据加载
# ============================================================

print("="*60)
print("问题一：图片导出脚本")
print("="*60)

# 加载预处理数据
df = pd.read_csv('../数据预处理/data_processed.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

print(f"📊 数据加载完成: {len(df)} 条记录")

# ============================================================
# 图1: 时间序列趋势
# ============================================================

df['ma_7'] = df['num_results'].rolling(window=7, center=True).mean()
df['ma_30'] = df['num_results'].rolling(window=30, center=True).mean()

fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
ax.plot(df['date'], df['num_results'], color=COLORS['primary'], alpha=0.6, linewidth=1, label='Daily')
ax.plot(df['date'], df['ma_7'], color=COLORS['secondary'], linewidth=2, label='7-day MA')
ax.plot(df['date'], df['ma_30'], color=COLORS['accent'], linewidth=2.5, label='30-day MA')
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Number of Reported Results', fontsize=12)
ax.legend(loc='upper right')
ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
save_fig(fig, 'fig1_time_series_trend.pdf')

# ============================================================
# 图2: 周末效应分析
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['dayofweek_name'] = pd.Categorical(df['dayofweek_name'], categories=day_order, ordered=True)

sns.boxplot(data=df, x='dayofweek_name', y='num_results', ax=axes[0], palette='Blues')
axes[0].set_xlabel('Day of Week', fontsize=11)
axes[0].set_ylabel('Number of Reported Results', fontsize=11)
axes[0].tick_params(axis='x', rotation=45)
axes[0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))

weekend_stats = df.groupby('is_weekend')['num_results'].agg(['mean', 'std', 'count'])
weekend_stats.index = ['Weekday', 'Weekend']

bars = axes[1].bar(['Weekday', 'Weekend'], weekend_stats['mean'], 
                   yerr=weekend_stats['std']/np.sqrt(weekend_stats['count']),
                   color=[COLORS['primary'], COLORS['secondary']], 
                   capsize=5, edgecolor='black')
axes[1].set_xlabel('Day Type', fontsize=11)
axes[1].set_ylabel('Mean Number of Results', fontsize=11)
axes[1].ticklabel_format(style='sci', axis='y', scilimits=(0,0))

for bar, val in zip(bars, weekend_stats['mean']):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3000, 
                 f'{val:,.0f}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
save_fig(fig, 'fig2_weekly_pattern.pdf')

# ============================================================
# 图3: 月度趋势
# ============================================================

monthly_stats = df.groupby('month')['num_results'].agg(['mean', 'std', 'count'])

fig, ax = plt.subplots(figsize=FIGSIZE_NORMAL)
bars = ax.bar(monthly_stats.index, monthly_stats['mean'], 
              yerr=monthly_stats['std']/np.sqrt(monthly_stats['count']),
              color=COLORS['primary'], capsize=3, edgecolor='black', alpha=0.8)
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Mean Number of Reported Results', fontsize=12)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
save_fig(fig, 'fig3_monthly_trend.pdf')

# ============================================================
# 图4: STL分解
# ============================================================

from statsmodels.tsa.seasonal import STL

ts = df.set_index('date')['num_results']
stl = STL(ts, period=7, robust=True)
result = stl.fit()

fig, axes = plt.subplots(4, 1, figsize=FIGSIZE_TALL, sharex=True)

axes[0].plot(ts.index, ts.values, color=COLORS['primary'], linewidth=0.8)
axes[0].set_ylabel('Original', fontsize=11)
axes[0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))

axes[1].plot(ts.index, result.trend, color=COLORS['secondary'], linewidth=1.5)
axes[1].set_ylabel('Trend', fontsize=11)
axes[1].ticklabel_format(style='sci', axis='y', scilimits=(0,0))

axes[2].plot(ts.index, result.seasonal, color=COLORS['accent'], linewidth=0.8)
axes[2].set_ylabel('Seasonal', fontsize=11)

axes[3].plot(ts.index, result.resid, color=COLORS['neutral'], linewidth=0.8)
axes[3].set_ylabel('Residual', fontsize=11)
axes[3].set_xlabel('Date', fontsize=11)

save_fig(fig, 'fig4_stl_decomposition.pdf')

# ============================================================
# 图5: ACF/PACF
# ============================================================

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

ts_log = np.log(ts)
ts_diff = ts_log.diff().dropna()

fig, axes = plt.subplots(2, 2, figsize=(14, 8))

plot_acf(ts_log.dropna(), ax=axes[0, 0], lags=40, alpha=0.05)
axes[0, 0].set_xlabel('Lag')
axes[0, 0].set_ylabel('ACF (Log Series)')

plot_pacf(ts_log.dropna(), ax=axes[0, 1], lags=40, alpha=0.05, method='ywm')
axes[0, 1].set_xlabel('Lag')
axes[0, 1].set_ylabel('PACF (Log Series)')

plot_acf(ts_diff, ax=axes[1, 0], lags=40, alpha=0.05)
axes[1, 0].set_xlabel('Lag')
axes[1, 0].set_ylabel('ACF (Differenced)')

plot_pacf(ts_diff, ax=axes[1, 1], lags=40, alpha=0.05, method='ywm')
axes[1, 1].set_xlabel('Lag')
axes[1, 1].set_ylabel('PACF (Differenced)')

save_fig(fig, 'fig5_acf_pacf.pdf')

# ============================================================
# 模型训练（用于后续图）
# ============================================================

from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy.stats import norm
from scipy import stats as scipy_stats

print("\n🔄 训练SARIMA模型...")

model = SARIMAX(ts_log, order=(1, 1, 1), seasonal_order=(1, 1, 1, 7),
                enforce_stationarity=False, enforce_invertibility=False)
model_fit = model.fit(disp=False, maxiter=200)

residuals = model_fit.resid[1:]

# ============================================================
# 图6: 残差诊断
# ============================================================

fig, axes = plt.subplots(2, 2, figsize=(12, 8))

axes[0, 0].plot(residuals, color=COLORS['primary'], linewidth=0.8)
axes[0, 0].axhline(y=0, color='red', linestyle='--', linewidth=1)
axes[0, 0].set_xlabel('Time')
axes[0, 0].set_ylabel('Residuals')

axes[0, 1].hist(residuals, bins=30, color=COLORS['primary'], edgecolor='black', alpha=0.7, density=True)
x = np.linspace(residuals.min(), residuals.max(), 100)
axes[0, 1].plot(x, norm.pdf(x, residuals.mean(), residuals.std()), 'r-', linewidth=2)
axes[0, 1].set_xlabel('Residuals')
axes[0, 1].set_ylabel('Density')

scipy_stats.probplot(residuals, dist="norm", plot=axes[1, 0])
axes[1, 0].get_lines()[0].set_color(COLORS['primary'])
axes[1, 0].get_lines()[1].set_color('red')

plot_acf(residuals, ax=axes[1, 1], lags=30, alpha=0.05)
axes[1, 1].set_xlabel('Lag')
axes[1, 1].set_ylabel('ACF')

save_fig(fig, 'fig6_residual_diagnostics.pdf')

# ============================================================
# 图7: 模型拟合效果
# ============================================================

fitted_log = model_fit.predict(start=0, end=len(ts_log)-1)
fitted_values = np.exp(fitted_log)
actual_values = ts.values

start_idx = 14
y_true = actual_values[start_idx:]
y_pred = fitted_values.values[start_idx:]
r2 = r2_score(y_true, y_pred)
mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)
ax.plot(ts.index, actual_values, color=COLORS['primary'], alpha=0.7, linewidth=1, label='Actual')
ax.plot(ts.index, fitted_values, color=COLORS['secondary'], linewidth=1.5, label='Fitted')
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Number of Reported Results', fontsize=12)
ax.legend(loc='upper right')
ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
textstr = f'R² = {r2:.3f}\nMAPE = {mape:.1f}%'
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
save_fig(fig, 'fig7_model_fit.pdf')

# ============================================================
# 图8: 预测可视化
# ============================================================

last_date = df['date'].max()
target_date = pd.Timestamp('2023-03-01')
forecast_steps = (target_date - last_date).days

forecast = model_fit.get_forecast(steps=forecast_steps)
forecast_mean = forecast.predicted_mean
forecast_ci = forecast.conf_int(alpha=0.05)

forecast_mean_original = np.exp(forecast_mean)
forecast_ci_original = np.exp(forecast_ci)

march1_pred = forecast_mean_original.iloc[-1]
march1_lower = forecast_ci_original.iloc[-1, 0]
march1_upper = forecast_ci_original.iloc[-1, 1]

forecast_dates = pd.date_range(start=last_date + timedelta(days=1), periods=forecast_steps, freq='D')

fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(df['date'], df['num_results'], color=COLORS['primary'], linewidth=1, label='Historical Data')
ax.plot(forecast_dates, forecast_mean_original, color=COLORS['secondary'], linewidth=2, label='Forecast')
ax.fill_between(forecast_dates, forecast_ci_original.iloc[:, 0], forecast_ci_original.iloc[:, 1],
                color=COLORS['secondary'], alpha=0.3, label='95% CI')
ax.axvline(x=target_date, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
ax.scatter([target_date], [march1_pred], color='red', s=100, zorder=5, marker='*')
ax.annotate(f'Mar 1, 2023\n{march1_pred:,.0f}\n[{march1_lower:,.0f}, {march1_upper:,.0f}]',
            xy=(target_date, march1_pred), xytext=(10, 30), textcoords='offset points',
            fontsize=10, ha='left', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Number of Reported Results', fontsize=12)
ax.legend(loc='upper right')
ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
save_fig(fig, 'fig8_forecast.pdf')

# ============================================================
# 图9: Bootstrap分布
# ============================================================

np.random.seed(42)
n_bootstrap = 1000
resid_std = residuals.std()
bootstrap_predictions = []

for i in range(n_bootstrap):
    noise = np.random.normal(0, resid_std, forecast_steps)
    perturbed_forecast = forecast_mean.values + np.cumsum(noise) * 0.1
    bootstrap_predictions.append(np.exp(perturbed_forecast[-1]))

bootstrap_predictions = np.array(bootstrap_predictions)
bs_mean = np.mean(bootstrap_predictions)
bs_lower = np.percentile(bootstrap_predictions, 2.5)
bs_upper = np.percentile(bootstrap_predictions, 97.5)

fig, ax = plt.subplots(figsize=FIGSIZE_NORMAL)
ax.hist(bootstrap_predictions, bins=50, color=COLORS['primary'], edgecolor='black', alpha=0.7, density=True)
ax.axvline(x=bs_lower, color='red', linestyle='--', linewidth=2, label=f'2.5% ({bs_lower:,.0f})')
ax.axvline(x=bs_upper, color='red', linestyle='--', linewidth=2, label=f'97.5% ({bs_upper:,.0f})')
ax.axvline(x=bs_mean, color=COLORS['accent'], linestyle='-', linewidth=2, label=f'Mean ({bs_mean:,.0f})')
ax.set_xlabel('Predicted Number of Reported Results', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.legend(loc='upper right')
save_fig(fig, 'fig9_bootstrap_distribution.pdf')

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
