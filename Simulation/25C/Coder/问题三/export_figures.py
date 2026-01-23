"""
图片导出脚本
用于从问题三建模分析中导出所有可视化图片为PDF格式
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
from scipy import stats

warnings.filterwarnings('ignore')

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Seaborn主题
sns.set_theme(style='whitegrid')

# 标准尺寸
FIGSIZE_NORMAL = (10, 6)
FIGSIZE_WIDE = (12, 6)

# 项目标准配色
COLORS = {
    'primary': '#4682B4',
    'secondary': '#FF7F50',
    'accent': '#228B22',
    'neutral': '#708090',
    'gold': '#FFD700'
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
print("=" * 60)
print("📊 加载数据...")
print("=" * 60)

script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, '..', '..')

df_medals = pd.read_csv(os.path.join(DATA_DIR, 'processed_medal_data.csv'))
df_raw = pd.read_csv(os.path.join(DATA_DIR, 'summerOly_medal_counts.csv'))
df_raw['NOC'] = df_raw['NOC'].str.replace('\xa0', '', regex=False).str.strip()
df_athletes = pd.read_csv(os.path.join(DATA_DIR, 'summerOly_athletes.csv'))

print(f"数据加载完成: {df_medals.shape}")

# ============================================================
# 辅助函数
# ============================================================

def calculate_gini(values):
    """计算Gini系数"""
    values = np.array(values)
    values = values[values > 0]
    if len(values) == 0:
        return 0
    sorted_values = np.sort(values)
    n = len(sorted_values)
    cumulative = np.cumsum(sorted_values)
    gini = (2 * np.sum((np.arange(1, n+1) * sorted_values))) / (n * np.sum(sorted_values)) - (n + 1) / n
    return gini

# 计算集中度数据
years = sorted(df_medals['Year'].unique())
concentration_data = []

for year in years:
    year_data = df_medals[df_medals['Year'] == year]
    totals = year_data['Total'].values
    golds = year_data['Gold'].values
    
    concentration_data.append({
        'Year': year,
        'Gini_Total': calculate_gini(totals),
        'Gini_Gold': calculate_gini(golds),
        'Num_Countries': len(year_data),
        'Top3_Share': year_data.nlargest(3, 'Total')['Total'].sum() / year_data['Total'].sum(),
        'Top10_Share': year_data.nlargest(10, 'Total')['Total'].sum() / year_data['Total'].sum()
    })

df_concentration = pd.DataFrame(concentration_data)

# ============================================================
# 图1：奖牌集中度演变
# ============================================================
print("\n生成图1：奖牌集中度演变...")

fig, axes = plt.subplots(1, 2, figsize=FIGSIZE_WIDE)

# 左图：Gini系数趋势
axes[0].plot(df_concentration['Year'], df_concentration['Gini_Total'], 
             marker='o', color=COLORS['primary'], label='Total Medals', linewidth=2, markersize=4)
axes[0].plot(df_concentration['Year'], df_concentration['Gini_Gold'], 
             marker='s', color=COLORS['secondary'], label='Gold Medals', linewidth=2, markersize=4)

z = np.polyfit(df_concentration['Year'], df_concentration['Gini_Total'], 1)
p = np.poly1d(z)
axes[0].plot(df_concentration['Year'], p(df_concentration['Year']), 
             '--', color=COLORS['primary'], alpha=0.5)

axes[0].set_xlabel('Year')
axes[0].set_ylabel('Gini Coefficient')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# 右图：Top国家奖牌占比
axes[1].fill_between(df_concentration['Year'], 0, df_concentration['Top3_Share'], 
                      alpha=0.3, color=COLORS['secondary'], label='Top 3')
axes[1].fill_between(df_concentration['Year'], df_concentration['Top3_Share'], 
                      df_concentration['Top10_Share'], 
                      alpha=0.3, color=COLORS['primary'], label='Top 4-10')
axes[1].plot(df_concentration['Year'], df_concentration['Top10_Share'], 
             color=COLORS['primary'], linewidth=2)

axes[1].set_xlabel('Year')
axes[1].set_ylabel('Medal Share')
axes[1].legend()
axes[1].grid(True, alpha=0.3)
axes[1].set_ylim(0, 1)

plt.tight_layout()
save_fig(fig, 'fig1_concentration_trend.pdf')

# ============================================================
# 图2：获奖国家数量与平均奖牌
# ============================================================
print("生成图2：获奖国家数量与平均奖牌...")

fig, axes = plt.subplots(1, 2, figsize=FIGSIZE_WIDE)

axes[0].bar(df_concentration['Year'], df_concentration['Num_Countries'], 
            color=COLORS['primary'], alpha=0.7)
axes[0].set_xlabel('Year')
axes[0].set_ylabel('Number of Medal-Winning Countries')
axes[0].tick_params(axis='x', rotation=45)

yearly_total = df_medals.groupby('Year')['Total'].sum()
avg_per_country = yearly_total / df_concentration.set_index('Year')['Num_Countries']

axes[1].plot(avg_per_country.index, avg_per_country.values, 
             marker='o', color=COLORS['secondary'], linewidth=2)
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Average Medals per Country')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
save_fig(fig, 'fig2_countries_medals.pdf')

# ============================================================
# 图3：黑马国家案例分析
# ============================================================
print("生成图3：黑马国家案例分析...")

case_countries = ['China', 'South Korea', 'Japan', 'Australia']
colors_case = [COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['neutral']]

fig, ax = plt.subplots(figsize=FIGSIZE_NORMAL)

for i, country in enumerate(case_countries):
    country_data = df_medals[df_medals['NOC'] == country].sort_values('Year')
    if len(country_data) > 0:
        ax.plot(country_data['Year'], country_data['Total'], 
                marker='o', label=country, color=colors_case[i], linewidth=2, markersize=4)

ax.set_xlabel('Year')
ax.set_ylabel('Total Medals')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
save_fig(fig, 'fig3_rising_stars.pdf')

# ============================================================
# 图4：项目竞争格局
# ============================================================
print("生成图4：项目竞争格局...")

df_medal_athletes = df_athletes[df_athletes['Medal'] != 'No medal'].copy()

sport_analysis = df_medal_athletes.groupby('Sport').agg({
    'NOC': 'nunique',
    'Medal': 'count',
    'Year': 'nunique'
}).reset_index()
sport_analysis.columns = ['Sport', 'Num_Countries', 'Total_Medals', 'Num_Years']

def calc_top3_share(sport):
    sport_data = df_medal_athletes[df_medal_athletes['Sport'] == sport]
    country_counts = sport_data.groupby('NOC').size()
    total = country_counts.sum()
    if total == 0:
        return 0
    top3 = country_counts.nlargest(3).sum()
    return top3 / total

sport_analysis['Top3_Monopoly'] = sport_analysis['Sport'].apply(calc_top3_share)

fig, ax = plt.subplots(figsize=FIGSIZE_NORMAL)

major_sports = sport_analysis[sport_analysis['Total_Medals'] > 500].copy()

scatter = ax.scatter(major_sports['Num_Countries'], 
                     major_sports['Top3_Monopoly'],
                     s=major_sports['Total_Medals'] / 20,
                     alpha=0.6,
                     c=range(len(major_sports)),
                     cmap='viridis')

for idx, row in major_sports.iterrows():
    ax.annotate(row['Sport'], (row['Num_Countries'], row['Top3_Monopoly']),
                fontsize=8, alpha=0.8)

ax.set_xlabel('Number of Medal-Winning Countries')
ax.set_ylabel('Top 3 Countries Medal Share')
ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='50% Monopoly Line')
ax.grid(True, alpha=0.3)

plt.tight_layout()
save_fig(fig, 'fig4_sport_competition.pdf')

# ============================================================
# 图5：项目投资效率矩阵
# ============================================================
print("生成图5：项目投资效率矩阵...")

country_total_medals = df_medals.groupby('NOC')['Total'].sum()
small_countries = country_total_medals[country_total_medals < 100].index.tolist()

def calc_small_country_share(sport):
    sport_data = df_medal_athletes[df_medal_athletes['Sport'] == sport]
    total = len(sport_data)
    if total == 0:
        return 0
    small_count = len(sport_data[sport_data['NOC'].isin(small_countries)])
    return small_count / total

sport_analysis['Small_Country_Share'] = sport_analysis['Sport'].apply(calc_small_country_share)

fig, ax = plt.subplots(figsize=FIGSIZE_NORMAL)

plot_sports = sport_analysis[sport_analysis['Total_Medals'] > 300].copy()

colors_list = []
for _, row in plot_sports.iterrows():
    if row['Top3_Monopoly'] > 0.5 and row['Small_Country_Share'] < 0.2:
        colors_list.append('red')
    elif row['Top3_Monopoly'] < 0.4 and row['Small_Country_Share'] > 0.3:
        colors_list.append('green')
    else:
        colors_list.append('gray')

ax.scatter(plot_sports['Top3_Monopoly'], plot_sports['Small_Country_Share'],
           s=plot_sports['Total_Medals'] / 10, c=colors_list, alpha=0.6)

for idx, row in plot_sports.iterrows():
    ax.annotate(row['Sport'], (row['Top3_Monopoly'], row['Small_Country_Share']),
                fontsize=7, alpha=0.8)

ax.set_xlabel('Top 3 Countries Monopoly (Higher = More Concentrated)')
ax.set_ylabel('Small Countries Medal Share (Higher = More Opportunity)')
ax.axhline(y=0.25, color='gray', linestyle='--', alpha=0.3)
ax.axvline(x=0.45, color='gray', linestyle='--', alpha=0.3)
ax.grid(True, alpha=0.3)

plt.tight_layout()
save_fig(fig, 'fig5_investment_matrix.pdf')

# ============================================================
# 图6：强国市场份额演变
# ============================================================
print("生成图6：强国市场份额演变...")

def calc_market_share(year, noc):
    year_total = df_medals[df_medals['Year'] == year]['Total'].sum()
    country_total = df_medals[(df_medals['Year'] == year) & (df_medals['NOC'] == noc)]['Total'].sum()
    return country_total / year_total if year_total > 0 else 0

share_data = []
for year in years:
    row = {'Year': year}
    for country in ['United States', 'Soviet Union', 'Russia', 'China', 'Great Britain', 'Germany']:
        row[country] = calc_market_share(year, country)
    share_data.append(row)

df_shares = pd.DataFrame(share_data)

fig, ax = plt.subplots(figsize=FIGSIZE_WIDE)

countries_to_plot = ['United States', 'Soviet Union', 'Russia', 'China', 'Great Britain']
colors_plot = [COLORS['primary'], 'red', '#FF6B6B', COLORS['secondary'], COLORS['accent']]

for i, country in enumerate(countries_to_plot):
    if country in df_shares.columns:
        data = df_shares[df_shares[country] > 0]
        ax.plot(data['Year'], data[country], marker='o', label=country, 
                color=colors_plot[i], linewidth=2, markersize=4)

ax.set_xlabel('Year')
ax.set_ylabel('Medal Market Share')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)

ax.axvline(x=1991, color='gray', linestyle=':', alpha=0.5)
ax.annotate('USSR Dissolved', xy=(1991, 0.35), fontsize=8, alpha=0.7)

plt.tight_layout()
save_fig(fig, 'fig6_market_share.pdf')

# ============================================================
# 图7：国家类型分布
# ============================================================
print("生成图7：国家类型分布...")

def classify_country(noc):
    total = country_total_medals.get(noc, 0)
    if total > 500:
        return 'Superpower'
    elif total > 200:
        return 'Major Power'
    elif total > 50:
        return 'Rising Power'
    elif total > 10:
        return 'Emerging'
    else:
        return 'Developing'

country_types = {noc: classify_country(noc) for noc in df_medals['NOC'].unique()}
df_country_types = pd.DataFrame([{'NOC': k, 'Type': v} for k, v in country_types.items()])

type_stats = []
for ctype in ['Superpower', 'Major Power', 'Rising Power', 'Emerging', 'Developing']:
    countries = df_country_types[df_country_types['Type'] == ctype]['NOC'].tolist()
    type_stats.append({
        'Type': ctype,
        'Count': len(countries)
    })

df_type_stats = pd.DataFrame(type_stats)

fig, ax = plt.subplots(figsize=FIGSIZE_NORMAL)

colors_bar = [COLORS['gold'], COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['neutral']]
bars = ax.barh(df_type_stats['Type'], df_type_stats['Count'], color=colors_bar, alpha=0.7)

for bar, count in zip(bars, df_type_stats['Count']):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
            f'{count}', va='center', fontsize=10)

ax.set_xlabel('Number of Countries')
ax.set_ylabel('Country Type')

plt.tight_layout()
save_fig(fig, 'fig7_country_types.pdf')

# ============================================================
# 完成
# ============================================================
print("\n" + "=" * 60)
print("🎉 所有图片导出完成！")
print("=" * 60)
print(f"\n图片保存在: {FIGURE_DIR}")
for f in sorted(os.listdir(FIGURE_DIR)):
    print(f"  - {f}")
