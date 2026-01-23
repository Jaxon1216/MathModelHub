"""
敏感性分析图片导出脚本
用于生成敏感性分析相关图表（PDF格式）
"""

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

warnings.filterwarnings('ignore')

# 中文显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style='whitegrid')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', '..')
FIGURE_DIR = os.path.join(BASE_DIR, 'figures')
os.makedirs(FIGURE_DIR, exist_ok=True)


def save_fig(fig, filename):
    filepath = os.path.join(FIGURE_DIR, filename)
    fig.savefig(filepath, bbox_inches='tight', facecolor='white')
    print(f"✅ 已保存: {filepath}")
    plt.close(fig)


def load_data():
    medal_path = os.path.join(DATA_DIR, 'processed_medal_data.csv')
    if not os.path.exists(medal_path):
        raise FileNotFoundError(f'未找到数据文件: {medal_path}')

    df = pd.read_csv(medal_path)
    feature_columns = [
        'total_rolling3_mean',
        'gold_lag1',
        'total_lag1',
        'total_lag2',
        'is_host',
        'total_events',
        'participation_count'
    ]

    X = df[feature_columns]
    y = df['Total']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled


def plot_alpha_sensitivity(X_train_scaled, X_test_scaled, y_train, y_test):
    alpha_grid = np.logspace(-3, 2, 12)
    records = []
    for alpha in alpha_grid:
        ridge = Ridge(alpha=alpha)
        ridge.fit(X_train_scaled, y_train)
        ridge_pred = ridge.predict(X_test_scaled)
        records.append({
            'model': 'Ridge',
            'alpha': alpha,
            'rmse': np.sqrt(mean_squared_error(y_test, ridge_pred))
        })

        lasso = Lasso(alpha=alpha, max_iter=5000)
        lasso.fit(X_train_scaled, y_train)
        lasso_pred = lasso.predict(X_test_scaled)
        records.append({
            'model': 'Lasso',
            'alpha': alpha,
            'rmse': np.sqrt(mean_squared_error(y_test, lasso_pred))
        })

    sens_df = pd.DataFrame(records)
    fig, ax = plt.subplots(figsize=(8, 5))
    for name, g in sens_df.groupby('model'):
        ax.plot(g['alpha'], g['rmse'], marker='o', label=name)
    ax.set_xscale('log')
    ax.set_xlabel('alpha (log scale)')
    ax.set_ylabel('RMSE')
    ax.legend()
    save_fig(fig, 'fig_sensitivity_alpha_rmse.pdf')


def plot_model_sensitivity(X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled):
    metrics = []
    models = {
        'Linear': LinearRegression(),
        'Ridge(alpha=1.0)': Ridge(alpha=1.0),
        'Lasso(alpha=0.1)': Lasso(alpha=0.1, max_iter=5000),
    }
    for name, model in models.items():
        model.fit(X_train_scaled, y_train)
        pred = model.predict(X_test_scaled)
        metrics.append({
            'model': name,
            'r2': r2_score(y_test, pred)
        })

    rf = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        min_samples_leaf=2
    )
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    metrics.append({
        'model': 'Random Forest',
        'r2': r2_score(y_test, rf_pred)
    })

    metric_df = pd.DataFrame(metrics)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(metric_df['model'], metric_df['r2'], color='steelblue')
    ax.set_ylabel('R2')
    ax.tick_params(axis='x', rotation=20)
    save_fig(fig, 'fig_sensitivity_model_r2.pdf')


def plot_bootstrap_rmse(X_train_scaled, X_test_scaled, y_train, y_test):
    np.random.seed(42)
    n_boot = 200
    bootstrap_rmse = []
    for _ in range(n_boot):
        idx = np.random.choice(len(X_train_scaled), len(X_train_scaled), replace=True)
        Xb = X_train_scaled[idx]
        yb = y_train.iloc[idx]
        model = Lasso(alpha=0.1, max_iter=5000)
        model.fit(Xb, yb)
        pred = model.predict(X_test_scaled)
        bootstrap_rmse.append(np.sqrt(mean_squared_error(y_test, pred)))

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(bootstrap_rmse, bins=25, color='steelblue', edgecolor='black', alpha=0.75)
    ax.set_xlabel('RMSE (bootstrap)')
    ax.set_ylabel('Frequency')
    save_fig(fig, 'fig_sensitivity_bootstrap_rmse.pdf')


def main():
    X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled = load_data()
    plot_alpha_sensitivity(X_train_scaled, X_test_scaled, y_train, y_test)
    plot_model_sensitivity(X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled)
    plot_bootstrap_rmse(X_train_scaled, X_test_scaled, y_train, y_test)

    print("\n" + "=" * 60)
    print("🎉 所有图片导出完成！")
    print("=" * 60)
    for f in sorted(os.listdir(FIGURE_DIR)):
        print(f"  - {f}")


if __name__ == '__main__':
    main()
