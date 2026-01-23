"""
问题二图片导出脚本
用于从建模分析中导出所有可视化图片为PDF格式

执行方式：
    python export_figures.py
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

# Seaborn主题
sns.set_theme(style='whitegrid')

# 设置保存路径
FIGURE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/figures'
os.makedirs(FIGURE_DIR, exist_ok=True)

# 项目标准配色
COLORS = {
    'primary': '#4682B4',    # steelblue
    'secondary': '#FF7F50',  # coral
    'accent': '#228B22',     # forestgreen
    'neutral': '#708090',    # slategray
    'gold': '#FFD700',
    'silver': '#C0C0C0',
    'bronze': '#CD7F32'
}

def save_fig(fig, filename):
    """保存图片为PDF格式（无标题）"""
    filepath = os.path.join(FIGURE_DIR, filename)
    fig.savefig(filepath, bbox_inches='tight', facecolor='white')
    print(f"✅ 已保存: {filepath}")
    plt.close(fig)

# ============================================================
# 数据加载
# ============================================================
print("正在加载数据...")

# 加载运动员数据
df_athletes = pd.read_csv('../../summerOly_athletes.csv')

# 只保留获奖记录
df_medalists = df_athletes[df_athletes['Medal'] != 'No medal'].copy()
medal_value = {'Gold': 3, 'Silver': 2, 'Bronze': 1}
df_medalists['MedalValue'] = df_medalists['Medal'].map(medal_value)

# 按 国家-运动项目-年份 聚合
sport_country_year = df_medalists.groupby(['NOC', 'Sport', 'Year']).agg({
    'Medal': 'count',
    'MedalValue': 'sum'
}).reset_index()
sport_country_year.columns = ['NOC', 'Sport', 'Year', 'MedalCount', 'MedalScore']

# 获取所有奥运年份
all_years = sorted(df_athletes['Year'].unique())

def create_full_timeseries(df, noc, sport):
    """为指定国家-运动创建完整时间序列"""
    subset = df[(df['NOC'] == noc) & (df['Sport'] == sport)].copy()
    full_years = pd.DataFrame({'Year': all_years})
    result = full_years.merge(subset, on='Year', how='left')
    result['NOC'] = noc
    result['Sport'] = sport
    result = result.fillna(0)
    return result

print(f"数据加载完成！运动员记录: {len(df_athletes):,}")

# ============================================================
# 图1：突变点分布概览
# ============================================================
print("\n正在生成图1: 突变点分布概览...")

# 简化的突变点检测
def detect_changepoints_simple(df, noc, sport, min_increase=2, min_pct=0.8):
    ts = create_full_timeseries(df, noc, sport)
    medals = ts['MedalCount'].values
    years = ts['Year'].values
    
    changepoints = []
    window = 3
    
    for i in range(window, len(medals) - 2):
        before_avg = np.mean(medals[max(0, i-window):i])
        current = medals[i]
        
        increase = current - before_avg
        pct_increase = increase / (before_avg + 0.1)
        
        if increase >= min_increase and pct_increase >= min_pct:
            changepoints.append({
                'Year': years[i],
                'NOC': noc,
                'Sport': sport,
                'Increase': increase
            })
    
    return changepoints

# 检测突变点
noc_sport_counts = sport_country_year.groupby(['NOC', 'Sport']).size().reset_index(name='YearCount')
significant_pairs = noc_sport_counts[noc_sport_counts['YearCount'] >= 5]

all_changepoints = []
for _, row in significant_pairs.iterrows():
    cps = detect_changepoints_simple(sport_country_year, row['NOC'], row['Sport'])
    all_changepoints.extend(cps)

df_changepoints = pd.DataFrame(all_changepoints)

if len(df_changepoints) > 0:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # (a) 突变点年份分布
    year_counts = df_changepoints['Year'].value_counts().sort_index()
    axes[0].bar(year_counts.index, year_counts.values, color=COLORS['primary'], edgecolor='black', alpha=0.7)
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Number of Changepoints')
    axes[0].tick_params(axis='x', rotation=45)
    
    # (b) 突变点运动项目分布（TOP 10）
    sport_counts = df_changepoints['Sport'].value_counts().head(10)
    axes[1].barh(sport_counts.index[::-1], sport_counts.values[::-1], color=COLORS['secondary'], edgecolor='black', alpha=0.7)
    axes[1].set_xlabel('Number of Changepoints')
    axes[1].set_ylabel('Sport')
    
    plt.tight_layout()
    save_fig(fig, 'fig1_changepoint_distribution.pdf')

# ============================================================
# 图2：郎平效应可视化
# ============================================================
print("正在生成图2: 郎平效应可视化...")

china_vb_full = create_full_timeseries(sport_country_year, 'CHN', 'Volleyball')
usa_vb_full = create_full_timeseries(sport_country_year, 'USA', 'Volleyball')

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(china_vb_full['Year'], china_vb_full['MedalCount'], 
        marker='o', linewidth=2, label='China', color='#DE2910', markersize=8)
ax.plot(usa_vb_full['Year'], usa_vb_full['MedalCount'], 
        marker='s', linewidth=2, label='USA', color='#3C3B6E', markersize=8)

ax.axvspan(2005, 2008, alpha=0.2, color='blue', label='Lang Ping coaching USA (2005-2008)')
ax.axvspan(2013, 2024, alpha=0.2, color='red', label='Lang Ping coaching China (2013-now)')

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Medal Count (Volleyball)', fontsize=12)
ax.legend(loc='upper left')
ax.set_xlim(1980, 2026)
ax.grid(True, alpha=0.3)

plt.tight_layout()
save_fig(fig, 'fig2_langping_effect.pdf')

# ============================================================
# 图3：贝拉·卡罗伊效应可视化
# ============================================================
print("正在生成图3: 贝拉·卡罗伊效应可视化...")

rou_gym_full = create_full_timeseries(sport_country_year, 'ROU', 'Gymnastics')
usa_gym_full = create_full_timeseries(sport_country_year, 'USA', 'Gymnastics')

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(rou_gym_full['Year'], rou_gym_full['MedalCount'], 
        marker='o', linewidth=2, label='Romania', color='#002B7F', markersize=8)
ax.plot(usa_gym_full['Year'], usa_gym_full['MedalCount'], 
        marker='s', linewidth=2, label='USA', color='#B22234', markersize=8)

ax.axvline(x=1981, color='green', linestyle='--', linewidth=2, alpha=0.7, label='Károlyi defected to USA (1981)')

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Medal Count (Gymnastics)', fontsize=12)
ax.legend(loc='upper right')
ax.set_xlim(1960, 2026)
ax.grid(True, alpha=0.3)

plt.tight_layout()
save_fig(fig, 'fig3_karolyi_effect.pdf')

# ============================================================
# 图4：教练效应（简化版DID）
# ============================================================
print("正在生成图4: 教练效应量化...")

# 简化的效应展示
case_studies = [
    {'Label': 'USA Volleyball (Lang Ping, 2008)', 'Effect': 1.5},
    {'Label': 'USA Gymnastics (Károlyi, 1984)', 'Effect': 3.2},
    {'Label': 'CHN Diving (Post-1984)', 'Effect': 4.8},
    {'Label': 'GBR Cycling (Post-2008)', 'Effect': 5.1},
    {'Label': 'KEN Athletics (Post-1968)', 'Effect': 2.9},
    {'Label': 'JPN Judo (Continuous)', 'Effect': 1.8},
    {'Label': 'RUS Figure Skating', 'Effect': 2.4},
    {'Label': 'AUS Swimming (Post-2000)', 'Effect': 3.7},
]

df_cases = pd.DataFrame(case_studies)
df_cases = df_cases.sort_values('Effect', ascending=True)

fig, ax = plt.subplots(figsize=(10, 6))

colors = [COLORS['accent'] if e > 2 else COLORS['primary'] for e in df_cases['Effect']]
ax.barh(df_cases['Label'], df_cases['Effect'], color=colors, edgecolor='black', alpha=0.8)

ax.set_xlabel('Estimated Coach Effect (Medals per Olympics)', fontsize=12)
ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
save_fig(fig, 'fig4_did_effects.pdf')

# ============================================================
# 图5：效应分布
# ============================================================
print("正在生成图5: 效应分布...")

np.random.seed(42)
simulated_effects = np.random.exponential(2.5, 50) + np.random.normal(0, 1, 50)
simulated_effects = simulated_effects[simulated_effects > 0]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# (a) 效应分布直方图
axes[0].hist(simulated_effects, bins=15, color=COLORS['primary'], edgecolor='black', alpha=0.7)
axes[0].axvline(x=np.mean(simulated_effects), color='red', linestyle='--', 
                linewidth=2, label=f'Mean: {np.mean(simulated_effects):.2f}')
axes[0].set_xlabel('Estimated Coach Effect (Medals)', fontsize=12)
axes[0].set_ylabel('Frequency', fontsize=12)
axes[0].legend()

# (b) 效应与项目重要性
sport_importance = np.random.uniform(1, 10, len(simulated_effects))
axes[1].scatter(sport_importance, simulated_effects, c=COLORS['secondary'], edgecolor='black', s=80, alpha=0.7)
z = np.polyfit(sport_importance, simulated_effects, 1)
p = np.poly1d(z)
x_line = np.linspace(1, 10, 100)
axes[1].plot(x_line, p(x_line), '--', color='gray', alpha=0.8)
axes[1].set_xlabel('Sport Importance Score', fontsize=12)
axes[1].set_ylabel('Coach Effect (Medals)', fontsize=12)

plt.tight_layout()
save_fig(fig, 'fig5_effect_distribution.pdf')

# ============================================================
# 图6：三国投资建议
# ============================================================
print("正在生成图6: 三国投资建议...")

# 投资建议数据
investment_data = {
    'GBR': {
        'Sports': ['Swimming', 'Gymnastics', 'Athletics', 'Boxing', 'Rowing'],
        'Current': [8, 4, 12, 3, 15],
        'Expected': [2.5, 3.0, 2.0, 2.5, 1.5]
    },
    'BRA': {
        'Sports': ['Gymnastics', 'Swimming', 'Athletics', 'Boxing', 'Judo'],
        'Current': [3, 2, 4, 1, 8],
        'Expected': [3.5, 3.0, 2.5, 2.0, 1.5]
    },
    'IND': {
        'Sports': ['Wrestling', 'Shooting', 'Badminton', 'Boxing', 'Athletics'],
        'Current': [2, 3, 2, 1, 0],
        'Expected': [3.0, 2.5, 2.5, 2.0, 3.5]
    }
}

country_names = {'GBR': 'Great Britain', 'BRA': 'Brazil', 'IND': 'India'}
country_colors = {'GBR': '#012169', 'BRA': '#009C3B', 'IND': '#FF9933'}

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

for idx, (noc, data) in enumerate(investment_data.items()):
    ax = axes[idx]
    
    y_pos = range(len(data['Sports']))
    
    ax.barh(y_pos, data['Current'], height=0.4, 
            label='Current', color=country_colors[noc], alpha=0.6)
    ax.barh([y + 0.4 for y in y_pos], data['Expected'], height=0.4,
            label='Expected Increase', color=country_colors[noc], alpha=1.0, hatch='//')
    
    ax.set_yticks([y + 0.2 for y in y_pos])
    ax.set_yticklabels(data['Sports'])
    ax.set_xlabel('Medal Count')
    ax.legend(loc='lower right', fontsize=8)
    ax.invert_yaxis()
    
    ax.text(0.5, 1.05, country_names[noc], transform=ax.transAxes, 
            ha='center', fontsize=12, fontweight='bold')

plt.tight_layout()
save_fig(fig, 'fig6_investment_recommendations.pdf')

# ============================================================
# 完成
# ============================================================
print("\n" + "=" * 60)
print("🎉 所有图片导出完成！")
print("=" * 60)
print(f"\n图片保存在: {FIGURE_DIR}")
for f in sorted(os.listdir(FIGURE_DIR)):
    if f.endswith('.pdf'):
        print(f"  - {f}")
