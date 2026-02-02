"""
运行DWVS模拟分析 - 使用新参数 (0.35, 0.03)
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# 设置matplotlib为非交互模式
import matplotlib
matplotlib.use('Agg')

# 设置绘图风格
plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 11,
    'axes.titlesize': 12,
    'axes.titleweight': 'bold',
    'axes.labelsize': 11,
    'axes.linewidth': 1.2,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

COLORS = {
    'primary': '#367DB0',
    'secondary': '#3D9F3C',
    'orange': '#FF7F0E',
    'rank_method': '#367DB0',
    'controversial': '#FF7F0E',
}

print("=" * 70)
print("争议选手整体DWVS影响分析 - 新参数 (base_alpha=0.35, increment=0.03)")
print("=" * 70)

# 加载数据并计算争议度
df_summary = pd.read_csv('../数据预处理/data_season_summary.csv')
df_summary['judge_rank'] = df_summary.groupby('season')['total_score_mean'].rank(ascending=False, method='min')
df_summary['controversy_score'] = df_summary['judge_rank'] - df_summary['placement']

# 筛选争议选手
controversial_all = df_summary[df_summary['controversy_score'] >= 3].copy()

print(f"\n📊 共识别出 {len(controversial_all)} 名争议选手 (Controversy Score ≥ 3)")

# DWVS参数（使用优化后的参数）
base_alpha = 0.35
increment = 0.03

# 计算DWVS影响
def calc_dwvs_change(row):
    weeks = row['weeks_competed']
    final_alpha = min(base_alpha + increment * weeks, 0.80)
    judge_rank = row['judge_rank']
    original_placement = row['placement']
    fan_rank_estimate = original_placement  # 假设：人气排名≈最终排名
    # 原系统: ~50%/50% 权重
    # DWVS: final_alpha/fan权重
    original_combined = 0.5 * judge_rank + 0.5 * fan_rank_estimate
    dwvs_combined = final_alpha * judge_rank + (1 - final_alpha) * fan_rank_estimate
    return dwvs_combined - original_combined

controversial_all['dwvs_change'] = controversial_all.apply(calc_dwvs_change, axis=1)

# 统计结果
print(f"\n🎯 DWVS影响统计:")
percentage_worse = (controversial_all['dwvs_change'] > 0).mean() * 100
avg_change = controversial_all['dwvs_change'].mean()
max_change = controversial_all['dwvs_change'].max()

print(f"   排名下降选手比例: {percentage_worse:.1f}%")
print(f"   平均排名变化: +{avg_change:.2f} 位")
print(f"   最大排名变化: +{max_change:.2f} 位")

# 按争议程度分组
high_controversy = controversial_all[controversial_all['controversy_score'] >= 5]
medium_controversy = controversial_all[(controversial_all['controversy_score'] >= 3) & (controversial_all['controversy_score'] < 5)]

print(f"\n📈 分组统计:")
high_avg = high_controversy['dwvs_change'].mean()
medium_avg = medium_controversy['dwvs_change'].mean()
print(f"   高争议组 (≥5): {len(high_controversy)} 人, 平均变化 +{high_avg:.2f} 位")
print(f"   中等争议组 (3-4): {len(medium_controversy)} 人, 平均变化 +{medium_avg:.2f} 位")

# 显示Top 10
print(f"\n🏆 Top 10 争议选手DWVS影响:")
top10 = controversial_all.nlargest(10, 'controversy_score')[['season', 'celebrity_name', 'placement', 'controversy_score', 'dwvs_change']]
print(top10.to_string(index=False))

# Bobby Bones特别检查
bobby = controversial_all[controversial_all['celebrity_name'] == 'Bobby Bones']
if len(bobby) > 0:
    bobby_change = bobby['dwvs_change'].values[0]
    bobby_original = bobby['placement'].values[0]
    bobby_new = bobby_original + bobby_change
    print(f"\n🎯 Bobby Bones 特别分析:")
    print(f"   原排名: {bobby_original:.0f}")
    print(f"   预期变化: +{bobby_change:.2f}")
    print(f"   新排名: {bobby_new:.0f} (取整为 {round(bobby_new):.0f})")

# 保存结果
controversial_all[['season', 'celebrity_name', 'placement', 'judge_rank', 'controversy_score', 'dwvs_change']].to_csv('dwvs_impact_all_controversial.csv', index=False)
print(f"\n💾 详细结果已保存至 dwvs_impact_all_controversial.csv")

# ===== 生成图表 =====
print("\n" + "=" * 70)
print("生成图表")
print("=" * 70)

# 图1: 动态权重演化
fig, ax = plt.subplots(figsize=(10, 4.5))
weeks = np.arange(1, 12)
judge_w = [min(base_alpha + increment * w, 0.80) for w in weeks]
fan_w = [1 - a for a in judge_w]

ax.stackplot(weeks, fan_w, judge_w, labels=['Fan Vote', 'Judge Score'],
            colors=[COLORS['controversial'], COLORS['rank_method']], alpha=0.8)
ax.set_xlabel('Week')
ax.set_ylabel('Weight')
ax.set_ylim(0, 1)
ax.legend(loc='upper right', frameon=True, fancybox=True, edgecolor='lightgray')
ax.set_xticks(weeks)
ax.set_title('Dynamic Weight Evolution (DWVS)', fontweight='bold')
ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('figures/Q4_fig3_dynamic_weight.pdf', format='pdf', bbox_inches='tight')
print("✅ 已生成: figures/Q4_fig3_dynamic_weight.pdf")
plt.close()

# 图2: DWVS整体影响
fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))

# (a) 争议度 vs DWVS调整幅度
ax = axes[0]
ax.scatter(controversial_all['controversy_score'], controversial_all['dwvs_change'], 
           c=COLORS['rank_method'], alpha=0.7, s=60, edgecolor='white')

# 趋势线
z = np.polyfit(controversial_all['controversy_score'], controversial_all['dwvs_change'], 1)
p = np.poly1d(z)
x_line = np.linspace(3, 7, 100)
r = np.corrcoef(controversial_all['controversy_score'], controversial_all['dwvs_change'])[0,1]
ax.plot(x_line, p(x_line), '--', color=COLORS['controversial'], linewidth=2, label=f'Trend (r={r:.2f})')

# 标注关键选手
for _, row in controversial_all.nlargest(3, 'controversy_score').iterrows():
    name = row['celebrity_name'].split()[0][:8]
    ax.annotate(name, (row['controversy_score'], row['dwvs_change']), 
                xytext=(5, 5), textcoords='offset points', fontsize=8,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

ax.set_xlabel('Controversy Score')
ax.set_ylabel('Combined Score Change')
ax.set_title('Controversy vs. DWVS Impact')
ax.axhline(0, color='gray', linestyle=':', alpha=0.5)
ax.legend(loc='upper right', frameon=True, fancybox=True, edgecolor='lightgray')

# (b) Top 10 争议选手条形图
ax = axes[1]
top10_fig = controversial_all.nlargest(10, 'controversy_score')[['celebrity_name', 'dwvs_change']].copy()
top10_fig['name_short'] = top10_fig['celebrity_name'].apply(lambda x: x[:15] if len(x) > 15 else x)
top10_fig = top10_fig.sort_values('dwvs_change', ascending=True)

colors = [COLORS['controversial'] if x > 0.8 else COLORS['rank_method'] for x in top10_fig['dwvs_change']]
bars = ax.barh(range(len(top10_fig)), top10_fig['dwvs_change'], color=colors, edgecolor='white')
ax.set_yticks(range(len(top10_fig)))
ax.set_yticklabels(top10_fig['name_short'], fontsize=9)
ax.set_xlabel('Combined Score Change (higher = worse ranking)')
ax.set_title('Top 10 Controversial: DWVS Impact')
ax.axvline(0, color='gray', linestyle=':', alpha=0.5)

for i, (bar, val) in enumerate(zip(bars, top10_fig['dwvs_change'])):
    ax.annotate(f'+{val:.2f}', (val, i), xytext=(3, 0), textcoords='offset points', va='center', fontsize=8)

plt.tight_layout()
plt.savefig('figures/Q4_fig5_dwvs_group_impact.pdf', format='pdf', bbox_inches='tight')
print("✅ 已生成: figures/Q4_fig5_dwvs_group_impact.pdf")
plt.close()

print("\n" + "=" * 70)
print("✅ 模拟完成！")
print("=" * 70)
print(f"\n📊 关键数据总结（用于更新论文）：")
print(f"   参数: base_alpha={base_alpha}, increment={increment}")
print(f"   初始权重: Judge {base_alpha*100:.0f}%, Fan {(1-base_alpha)*100:.0f}%")
print(f"   最终权重 (Week 10): Judge {judge_w[-2]*100:.0f}%, Fan {fan_w[-2]*100:.0f}%")
print(f"   争议选手下降比例: {percentage_worse:.1f}%")
print(f"   平均排名变化: +{avg_change:.2f}")
print(f"   高争议组变化: +{high_avg:.2f}")
if len(bobby) > 0:
    print(f"   Bobby Bones新排名: {round(bobby_new):.0f}")
