"""
配色方案示例图表生成
使用用户提供的学术配色方案
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ============================================
# 新配色方案定义
# ============================================

# 专业学术风（分组类图表）
COLORS_ACADEMIC = {
    'primary_blue': '#367DB0',      # 深蓝 - 主色
    'primary_green': '#3D9F3C',     # 深绿 - 副色
    'light_green': '#9ED17B',       # 浅绿
    'light_blue': '#9DC7DD',        # 浅蓝
    'gray_blue': '#5385BD',         # 灰蓝
    'gray_green': '#519D78',        # 灰绿
}

# 色盲友好版
COLORS_COLORBLIND = {
    'blue': '#1F77B4',
    'orange': '#FF7F0E',
    'green': '#2CA02C',
    'red': '#D62728',
}

# 对比类配色
COLORS_CONTRAST = {
    'blue': '#367DB0',
    'green': '#3D9F3C',
    'light_orange': '#FFA07A',
    'light_gray': '#D3D3D3',
    'light_purple': '#9370DB',
}

# 连续数值渐变（蓝绿）
CMAP_BLUE_GREEN = ['#04579B', '#3492B2', '#58B8D1', '#6FC8CA', '#ACEEFE', '#D6F6FF']

# 连续数值渐变（红橙）
CMAP_RED_ORANGE = ['#A61C3C', '#D92B4B', '#F15A6C', '#F78B9A', '#FBBCC3', '#FDE1E4']

# ============================================
# 全局绑图设置
# ============================================
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
    'legend.frameon': True,
    'legend.fancybox': True,
    'legend.edgecolor': 'lightgray',
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ============================================
# 加载数据
# ============================================
df_long = pd.read_csv('../数据预处理/data_long_format.csv')
df_summary = pd.read_csv('../数据预处理/data_season_summary.csv')

print(f"数据加载完成: {len(df_long)} 条记录")

# ============================================
# 图1: 分层一致性分析（4子图 - 分组对比类）
# 展示：专业学术风配色
# ============================================
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 计算各维度的一致性率（模拟数据）
np.random.seed(42)

# 子图1: 按投票方式
ax1 = axes[0, 0]
methods = ['Rank Method', 'Percentage Method']
consistency = [85.2, 78.6]
colors = [COLORS_ACADEMIC['primary_blue'], COLORS_ACADEMIC['primary_green']]
bars = ax1.bar(methods, consistency, color=colors, edgecolor='white', width=0.6)
ax1.set_ylabel('Consistency Rate (%)')
ax1.set_title('By Voting Method')
ax1.set_ylim(0, 100)
# 添加数值标签
for bar, val in zip(bars, consistency):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
             f'{val:.1f}%', ha='center', va='bottom', fontsize=10)

# 子图2: 按赛季阶段
ax2 = axes[0, 1]
phases = ['Early (S1-10)', 'Middle (S11-20)', 'Late (S21-34)']
consistency = [72.3, 81.5, 88.9]
colors = [COLORS_ACADEMIC['light_blue'], COLORS_ACADEMIC['gray_blue'], COLORS_ACADEMIC['primary_blue']]
bars = ax2.bar(phases, consistency, color=colors, edgecolor='white', width=0.6)
ax2.set_ylabel('Consistency Rate (%)')
ax2.set_title('By Season Phase')
ax2.set_ylim(0, 100)
for bar, val in zip(bars, consistency):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
             f'{val:.1f}%', ha='center', va='bottom', fontsize=10)

# 子图3: 按比赛阶段
ax3 = axes[1, 0]
stages = ['Early (W1-3)', 'Middle (W4-7)', 'Finals (W8+)']
consistency = [68.5, 79.2, 91.3]
colors = [COLORS_ACADEMIC['light_green'], COLORS_ACADEMIC['gray_green'], COLORS_ACADEMIC['primary_green']]
bars = ax3.bar(stages, consistency, color=colors, edgecolor='white', width=0.6)
ax3.set_ylabel('Consistency Rate (%)')
ax3.set_title('By Competition Stage')
ax3.set_ylim(0, 100)
for bar, val in zip(bars, consistency):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
             f'{val:.1f}%', ha='center', va='bottom', fontsize=10)

# 子图4: 按选手数量
ax4 = axes[1, 1]
n_contestants = ['3-5', '6-8', '9-12', '12+']
consistency = [92.1, 84.5, 76.8, 69.2]
# 使用渐变色
from matplotlib.colors import LinearSegmentedColormap
colors_gradient = [COLORS_ACADEMIC['primary_blue'], COLORS_ACADEMIC['gray_blue'], 
                   COLORS_ACADEMIC['light_blue'], '#C5E3F0']
bars = ax4.bar(n_contestants, consistency, color=colors_gradient, edgecolor='white', width=0.6)
ax4.set_xlabel('Number of Contestants')
ax4.set_ylabel('Consistency Rate (%)')
ax4.set_title('By Number of Contestants')
ax4.set_ylim(0, 100)
for bar, val in zip(bars, consistency):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
             f'{val:.1f}%', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig('fig_sample_1_stratified_consistency.pdf', format='pdf')
plt.savefig('fig_sample_1_stratified_consistency.png', dpi=150)
print("✓ 图1已保存: fig_sample_1_stratified_consistency.pdf")
plt.close()

# ============================================
# 图2: 行业对比分析（分组对比 + 双轴）
# 展示：2组对比配色
# ============================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 按行业统计
industry_stats = df_summary.groupby('celebrity_industry').agg({
    'placement': 'mean',
    'total_score_mean': 'mean'
}).dropna().sort_values('placement').head(8)

# 子图1: 堆叠条形图
ax1 = axes[0]
industries = industry_stats.index.tolist()
y_pos = np.arange(len(industries))

# 归一化分数用于展示
judge_scores = industry_stats['total_score_mean'].values
judge_scores_norm = (judge_scores - judge_scores.min()) / (judge_scores.max() - judge_scores.min())
placement_scores = 1 - (industry_stats['placement'].values - 1) / (industry_stats['placement'].max() - 1)

bar_width = 0.35
bars1 = ax1.barh(y_pos - bar_width/2, judge_scores_norm, bar_width, 
                 label='Judge Score (normalized)', color=COLORS_ACADEMIC['primary_blue'], edgecolor='white')
bars2 = ax1.barh(y_pos + bar_width/2, placement_scores, bar_width,
                 label='Fan Vote Share (normalized)', color=COLORS_CONTRAST['light_orange'], edgecolor='white')

ax1.set_yticks(y_pos)
ax1.set_yticklabels(industries, fontsize=9)
ax1.set_xlabel('Normalized Value (0-1)')
ax1.set_title('Judge Score vs Fan Vote by Industry')
ax1.legend(loc='upper right', frameon=True, fancybox=True, edgecolor='lightgray')

# 子图2: 差异分析
ax2 = axes[1]
gap = judge_scores_norm - placement_scores
colors = [COLORS_ACADEMIC['primary_blue'] if g > 0 else COLORS_CONTRAST['light_orange'] for g in gap]
bars = ax2.barh(y_pos, gap, color=colors, edgecolor='white')
ax2.axvline(0, color='gray', linestyle='-', linewidth=1)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(industries, fontsize=9)
ax2.set_xlabel('Gap (Judge Score - Fan Vote, normalized)')
ax2.set_title('Judge-Fan Gap by Industry')

# 添加图例说明
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=COLORS_ACADEMIC['primary_blue'], label='Judge > Fan'),
                   Patch(facecolor=COLORS_CONTRAST['light_orange'], label='Fan > Judge')]
ax2.legend(handles=legend_elements, loc='upper right', frameon=True, fancybox=True, edgecolor='lightgray')

plt.tight_layout()
plt.savefig('fig_sample_2_industry_comparison.pdf', format='pdf')
plt.savefig('fig_sample_2_industry_comparison.png', dpi=150)
print("✓ 图2已保存: fig_sample_2_industry_comparison.pdf")
plt.close()

# ============================================
# 图3: 热力图（连续数值）
# 展示：蓝绿渐变配色
# ============================================
from matplotlib.colors import LinearSegmentedColormap

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 创建自定义colormap（反转：浅→深，数值越大越深）
CMAP_BLUE_GREEN_REVERSED = CMAP_BLUE_GREEN[::-1]  # 反转颜色顺序
cmap_blue_green = LinearSegmentedColormap.from_list('blue_green', CMAP_BLUE_GREEN_REVERSED)

# 子图1: 参数网格搜索热力图
ax1 = axes[0]
base_alphas = np.arange(0.3, 0.7, 0.1)
increments = np.arange(0.02, 0.10, 0.02)
np.random.seed(42)
scores = np.random.uniform(0.7, 0.95, (len(base_alphas), len(increments)))
scores = np.sort(scores.flatten()).reshape(scores.shape)  # 让数值更有规律

im1 = ax1.imshow(scores, cmap=cmap_blue_green, aspect='auto', vmin=0.7, vmax=0.95)
ax1.set_xticks(range(len(increments)))
ax1.set_xticklabels([f'{x:.2f}' for x in increments])
ax1.set_yticks(range(len(base_alphas)))
ax1.set_yticklabels([f'{x:.1f}' for x in base_alphas])
ax1.set_xlabel('Increment')
ax1.set_ylabel('Base Alpha')
ax1.set_title('Grid Search Score Heatmap')

# 添加数值标注（深色背景用白字，浅色背景用黑字）
for i in range(len(base_alphas)):
    for j in range(len(increments)):
        # 数值越大颜色越深，所以高值用白字
        text_color = 'white' if scores[i,j] > 0.82 else 'black'
        ax1.text(j, i, f'{scores[i,j]:.2f}', ha='center', va='center', 
                fontsize=9, fontweight='bold', color=text_color)

cbar1 = plt.colorbar(im1, ax=ax1, shrink=0.8)
cbar1.set_label('Score')

# 子图2: 相关性矩阵热力图（使用红橙渐变展示负相关到正相关）
ax2 = axes[1]
# 模拟相关性矩阵
variables = ['Age', 'Score', 'Rank', 'Votes', 'Weeks']
np.random.seed(123)
corr_matrix = np.random.uniform(-0.5, 0.8, (5, 5))
np.fill_diagonal(corr_matrix, 1.0)
corr_matrix = (corr_matrix + corr_matrix.T) / 2  # 对称化

# 使用发散型配色：蓝(-1) -> 白(0) -> 红(+1)
cmap_diverging = LinearSegmentedColormap.from_list('diverging', 
    [COLORS_ACADEMIC['primary_blue'], '#FFFFFF', '#D62728'])

im2 = ax2.imshow(corr_matrix, cmap=cmap_diverging, aspect='auto', vmin=-1, vmax=1)
ax2.set_xticks(range(len(variables)))
ax2.set_xticklabels(variables, rotation=45, ha='right')
ax2.set_yticks(range(len(variables)))
ax2.set_yticklabels(variables)
ax2.set_title('Correlation Matrix')

for i in range(len(variables)):
    for j in range(len(variables)):
        ax2.text(j, i, f'{corr_matrix[i,j]:.2f}', ha='center', va='center', 
                fontsize=9, color='white' if abs(corr_matrix[i,j]) > 0.5 else 'black')

cbar2 = plt.colorbar(im2, ax=ax2, shrink=0.8)
cbar2.set_label('Correlation')

plt.tight_layout()
plt.savefig('fig_sample_3_heatmaps.pdf', format='pdf')
plt.savefig('fig_sample_3_heatmaps.png', dpi=150)
print("✓ 图3已保存: fig_sample_3_heatmaps.pdf")
plt.close()

# ============================================
# 图4: 折线图对比（多组对比）
# 展示：高对比度配色 + 不同线型
# ============================================
fig, ax = plt.subplots(figsize=(10, 6))

# 模拟跨赛季验证数据
seasons = np.arange(1, 35)
np.random.seed(42)

# 3种方法的表现
method1 = 0.7 + 0.005 * seasons + np.random.normal(0, 0.03, len(seasons))
method2 = 0.65 + 0.006 * seasons + np.random.normal(0, 0.03, len(seasons))
method3 = 0.6 + 0.004 * seasons + np.random.normal(0, 0.03, len(seasons))

# 高对比度配色：深蓝、橙色、紫色（色盲友好）
COLOR_LINE1 = '#1F77B4'  # 深蓝
COLOR_LINE2 = '#FF7F0E'  # 橙色
COLOR_LINE3 = '#9467BD'  # 紫色

# 使用不同线型增强区分：实线、虚线、点划线
ax.plot(seasons, method1, marker='o', markersize=5, linewidth=2.5, 
        color=COLOR_LINE1, linestyle='-', label='Rank Method')
ax.plot(seasons, method2, marker='s', markersize=5, linewidth=2.5, 
        color=COLOR_LINE2, linestyle='--', label='Percentage Method')
ax.plot(seasons, method3, marker='^', markersize=5, linewidth=2.5, 
        color=COLOR_LINE3, linestyle='-.', label='Hybrid Method')

# 添加填充区域显示置信区间
ax.fill_between(seasons, method1 - 0.05, method1 + 0.05, 
                color=COLOR_LINE1, alpha=0.15)
ax.fill_between(seasons, method2 - 0.05, method2 + 0.05, 
                color=COLOR_LINE2, alpha=0.15)
ax.fill_between(seasons, method3 - 0.05, method3 + 0.05, 
                color=COLOR_LINE3, alpha=0.15)

ax.set_xlabel('Season')
ax.set_ylabel('Prediction Accuracy')
ax.set_title('Cross-Season Validation: Method Comparison')
ax.legend(loc='upper right', frameon=True, fancybox=True, edgecolor='lightgray')
ax.set_xlim(0, 35)
ax.set_ylim(0.5, 1.0)

# 添加网格线（淡灰色）
ax.grid(True, linestyle='--', alpha=0.3, color=COLORS_CONTRAST['light_gray'])

plt.tight_layout()
plt.savefig('fig_sample_4_line_comparison.pdf', format='pdf')
plt.savefig('fig_sample_4_line_comparison.png', dpi=150)
print("✓ 图4已保存: fig_sample_4_line_comparison.pdf")
plt.close()

print("\n" + "="*60)
print("配色示例图表生成完成！")
print("="*60)
print("\n生成的文件：")
print("  1. fig_sample_1_stratified_consistency.pdf - 分层一致性（4子图分组对比）")
print("  2. fig_sample_2_industry_comparison.pdf - 行业对比（双轴分组对比）")
print("  3. fig_sample_3_heatmaps.pdf - 热力图（连续数值渐变）")
print("  4. fig_sample_4_line_comparison.pdf - 折线对比（多组对比）")
print("\n配色方案说明：")
print("  • 分组对比: 深蓝(#367DB0) + 深绿(#3D9F3C) 为主色")
print("  • 连续数值: 蓝绿渐变 #04579B → #D6F6FF")
print("  • 多组对比: 蓝 + 绿 + 浅橙(#FFA07A)")
print("  • 图例统一: 右上角带边框")
