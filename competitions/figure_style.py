"""
统一配色方案配置文件
美赛论文专用 - 学术风格
"""

import matplotlib.pyplot as plt
import numpy as np

# ============================================
# 配色方案定义
# ============================================

# 专业学术风（分组类图表）- 主配色
COLORS = {
    # 主色调
    'primary': '#367DB0',           # 深蓝 - 主色
    'secondary': '#3D9F3C',         # 深绿 - 副色
    
    # 浅色变体
    'light_blue': '#9DC7DD',        # 浅蓝
    'light_green': '#9ED17B',       # 浅绿
    
    # 灰色调
    'gray_blue': '#5385BD',         # 灰蓝
    'gray_green': '#519D78',        # 灰绿
    
    # 强调色
    'orange': '#FF7F0E',            # 橙色（对比/警示）
    'purple': '#9467BD',            # 紫色（第三组）
    'red': '#D62728',               # 红色（负值/警示）
    
    # 中性色
    'neutral': '#7D8491',           # 灰色
    'light_gray': '#D3D3D3',        # 浅灰
    
    # 填充色
    'fill_blue': '#DAE8FC',         # 浅蓝填充
    'fill_green': '#E8F5E9',        # 浅绿填充
    'fill_orange': '#FFF3E0',       # 浅橙填充
}

# 折线图专用配色（高对比度 + 色盲友好）
LINE_COLORS = {
    'line1': '#1F77B4',             # 深蓝
    'line2': '#FF7F0E',             # 橙色
    'line3': '#9467BD',             # 紫色
    'line4': '#2CA02C',             # 绿色
}

# 折线图线型
LINE_STYLES = {
    'line1': '-',                   # 实线
    'line2': '--',                  # 虚线
    'line3': '-.',                  # 点划线
    'line4': ':',                   # 点线
}

# 折线图标记
LINE_MARKERS = {
    'line1': 'o',                   # 圆点
    'line2': 's',                   # 方块
    'line3': '^',                   # 三角
    'line4': 'D',                   # 菱形
}

# 连续数值渐变（蓝绿，浅→深）
CMAP_BLUE_GREEN = ['#D6F6FF', '#ACEEFE', '#6FC8CA', '#58B8D1', '#3492B2', '#04579B']

# 发散型配色（相关性矩阵：蓝(-1) → 白(0) → 红(+1)）
CMAP_DIVERGING = ['#367DB0', '#9DC7DD', '#FFFFFF', '#F8B4B4', '#D62728']

# ============================================
# 图表尺寸标准
# ============================================
FIG_SINGLE = (6, 4.5)              # 单图
FIG_DOUBLE = (12, 5)               # 双图并排
FIG_TRIPLE = (14, 4.5)             # 三图并排
FIG_QUAD = (12, 10)                # 2x2四图
FIG_WIDE = (10, 4)                 # 宽图
FIG_SQUARE = (6, 6)                # 正方形

# ============================================
# 全局样式设置函数
# ============================================
def setup_style():
    """设置全局绑图样式"""
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

def add_legend(ax, loc='upper right', **kwargs):
    """添加统一样式的图例"""
    return ax.legend(loc=loc, frameon=True, fancybox=True, 
                     edgecolor='lightgray', **kwargs)

def get_cmap_blue_green():
    """获取蓝绿渐变colormap（浅→深）"""
    from matplotlib.colors import LinearSegmentedColormap
    return LinearSegmentedColormap.from_list('blue_green', CMAP_BLUE_GREEN)

def get_cmap_diverging():
    """获取发散型colormap"""
    from matplotlib.colors import LinearSegmentedColormap
    return LinearSegmentedColormap.from_list('diverging', CMAP_DIVERGING)

# ============================================
# 初始化
# ============================================
setup_style()
print('统一配色方案已加载')
