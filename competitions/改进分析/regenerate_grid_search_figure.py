"""
重新生成网格搜索图表（使用真实CSV数据）
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# 设置matplotlib中文支持
plt.rcParams.update({
    'font.family': 'Arial',
    'font.size': 11,
    'axes.titlesize': 12,
    'axes.titleweight': 'bold',
    'axes.labelsize': 11,
    'axes.labelweight': 'bold',
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

print("=" * 80)
print("重新生成网格搜索图表（使用真实数据）")
print("=" * 80)

# 读取真实的网格搜索结果
grid_df = pd.read_csv('grid_search_results.csv')
print(f"\n读取数据：{len(grid_df)} 行")
print(f"base_alpha 范围: {grid_df['base_alpha'].unique()}")
print(f"increment 范围: {grid_df['increment'].unique()}")

# Top 5
print("\nTop 5 配置：")
top5 = grid_df.nlargest(5, 'score')[['base_alpha', 'increment', 'final_alpha', 'score']]
print(top5.to_string(index=False))

# 创建图表
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 左图：得分热力图
ax1 = axes[0]
pivot_score = grid_df.pivot(index='base_alpha', columns='increment', values='score')
# 反转索引使base_alpha从小到大从上到下
pivot_score = pivot_score.iloc[::-1]

sns.heatmap(pivot_score, annot=True, fmt='.3f', cmap='YlOrRd', ax=ax1, 
            cbar_kws={'label': 'Score'}, vmin=0.88, vmax=1.0,
            linewidths=0.5, linecolor='white')
ax1.set_xlabel('Increment', fontweight='bold')
ax1.set_ylabel('Base Alpha', fontweight='bold')
ax1.set_title('(a) Grid Search Score Heatmap', fontweight='bold', pad=10)

# 右图：最终权重热力图
ax2 = axes[1]
pivot_alpha = grid_df.pivot(index='base_alpha', columns='increment', values='final_alpha')
# 反转索引
pivot_alpha = pivot_alpha.iloc[::-1]

sns.heatmap(pivot_alpha, annot=True, fmt='.2f', cmap='Blues', ax=ax2,
            cbar_kws={'label': 'Final Alpha'}, vmin=0.5, vmax=0.9,
            linewidths=0.5, linecolor='white')
ax2.set_xlabel('Increment', fontweight='bold')
ax2.set_ylabel('Base Alpha', fontweight='bold')
ax2.set_title('(b) Final Alpha Values', fontweight='bold', pad=10)

plt.tight_layout()

# 保存
output_path = 'figures/IMP_fig6_grid_search.pdf'
plt.savefig(output_path, bbox_inches='tight', format='pdf')
print(f"\n✅ 图表已保存: {output_path}")

# 同时保存PNG用于预览
png_path = 'figures/IMP_fig6_grid_search.png'
plt.savefig(png_path, bbox_inches='tight', format='png', dpi=150)
print(f"✅ PNG版本: {png_path}")

# plt.show()  # 注释掉以避免阻塞
plt.close()

# 验证最优参数
best_idx = grid_df['score'].idxmax()
best = grid_df.loc[best_idx]
print("\n" + "=" * 80)
print("✅ 真实最优参数验证：")
print("=" * 80)
print(f"base_alpha = {best['base_alpha']}")
print(f"increment = {best['increment']:.2f}")
print(f"final_alpha = {best['final_alpha']:.2f}")
print(f"score = {best['score']:.3f}")
print("\n计算初始权重：")
print(f"Week 1: α = {best['base_alpha']:.2f} → Judge: {best['base_alpha']*100:.0f}%, Fan: {(1-best['base_alpha'])*100:.0f}%")
print(f"Week 10: α = {best['final_alpha']:.2f} → Judge: {best['final_alpha']*100:.0f}%, Fan: {(1-best['final_alpha'])*100:.0f}%")

print("\n论文中使用的参数(0.30, 0.04):")
paper_row = grid_df[(grid_df['base_alpha'] == 0.3) & (grid_df['increment'] == 0.04)]
if len(paper_row) > 0:
    print(f"score = {paper_row['score'].values[0]:.3f} (排名第{grid_df['score'].rank(ascending=False)[paper_row.index[0]]:.0f}名)")
    print(f"final_alpha = {paper_row['final_alpha'].values[0]:.2f}")

print("\n" + "=" * 80)
