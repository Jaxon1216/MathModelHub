# =============================================================================
# MCM 2026 - DWTS Paper: Unified Figure Style Configuration
# =============================================================================
# 配图统一样式配置
# - 色盲友好配色
# - 高对比度设计
# - 统一的线型/标记系统
# - 专业学术风格
# =============================================================================

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# =============================================================================
# 统一配色方案 (色盲友好 + 高对比度)
# =============================================================================
COLORS = {
    # 主要对比色 - 用于方法对比
    'rank_method': '#2C3E50',      # 深蓝色 - Rank Method
    'pct_method': '#E67E22',       # 橙色 - Percentage Method
    'dwvs': '#27AE60',             # 深绿色 - DWVS (新系统)
    
    # 强调色
    'highlight': '#E74C3C',        # 红色 - 关键数据点高亮
    'positive': '#1ABC9C',         # 蓝绿色 - 正向指标
    'negative': '#9B59B6',         # 紫红色 - 负向指标
    
    # 辅助色
    'neutral': '#95A5A6',          # 灰色 - 辅助/参考线
    'light_fill': '#D5E8D4',       # 浅绿色填充
    'light_blue': '#DAE8FC',       # 浅蓝色填充
    'light_orange': '#FFE6CC',     # 浅橙色填充
    
    # 分类色板 (8色，色盲友好)
    'cat1': '#2C3E50',  # 深蓝
    'cat2': '#E67E22',  # 橙色
    'cat3': '#27AE60',  # 深绿
    'cat4': '#9B59B6',  # 紫色
    'cat5': '#1ABC9C',  # 青色
    'cat6': '#E74C3C',  # 红色
    'cat7': '#3498DB',  # 蓝色
    'cat8': '#F39C12',  # 黄色
    
    # 热力图配色
    'heatmap_cmap': 'YlGnBu',
}

# 分类色板列表 (用于多类别对比)
CATEGORY_COLORS = [
    COLORS['cat1'], COLORS['cat2'], COLORS['cat3'], COLORS['cat4'],
    COLORS['cat5'], COLORS['cat6'], COLORS['cat7'], COLORS['cat8']
]

# =============================================================================
# 线型与标记系统 (用于黑白打印兼容)
# =============================================================================
LINE_STYLES = {
    'rank_method': '-',      # 实线
    'pct_method': '--',      # 虚线
    'dwvs': '-.',            # 点划线
    'reference': ':',        # 点线 (参考线)
}

MARKERS = {
    'rank_method': 'o',      # 圆形
    'pct_method': 's',       # 方形
    'dwvs': '^',             # 三角形
    'highlight': '*',        # 星形 (关键点)
}

MARKER_SIZE = {
    'default': 6,
    'small': 4,
    'large': 8,
    'highlight': 12,
}

LINE_WIDTH = {
    'default': 2.0,
    'thin': 1.5,
    'thick': 2.5,
    'reference': 1.0,
}

# =============================================================================
# 图表尺寸标准
# =============================================================================
FIG_SIZES = {
    'single': (5, 4),           # 单栏图
    'double': (10, 4),          # 双栏图
    'triple': (12, 4),          # 三栏图
    'square': (5, 5),           # 正方形
    'wide': (8, 4),             # 宽图
    'tall': (5, 6),             # 高图
    'heatmap': (6, 5),          # 热力图
}

# =============================================================================
# 全局样式设置函数
# =============================================================================
def setup_style():
    """应用统一的matplotlib样式设置"""
    plt.rcParams.update({
        # 字体设置
        'font.family': 'Arial',
        'font.size': 11,
        'axes.titlesize': 12,
        'axes.titleweight': 'bold',
        'axes.labelsize': 11,
        'axes.labelweight': 'normal',
        
        # 坐标轴设置
        'axes.linewidth': 1.2,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.grid': False,  # 默认关闭网格
        
        # 刻度设置
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'xtick.major.width': 1.0,
        'ytick.major.width': 1.0,
        'xtick.major.size': 4,
        'ytick.major.size': 4,
        
        # 图例设置
        'legend.fontsize': 10,
        'legend.frameon': False,
        'legend.loc': 'best',
        
        # 图像质量
        'figure.dpi': 150,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.1,
        
        # 线条默认设置
        'lines.linewidth': 2.0,
        'lines.markersize': 6,
    })
    
    # 中文字体回退
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

# =============================================================================
# 辅助绑图函数
# =============================================================================
def add_subplot_label(ax, label, x=-0.08, y=1.05, fontsize=12, fontweight='bold'):
    """添加子图标签 (a), (b), (c) 等 - 放在图表外侧避免遮挡"""
    if label:  # 只有label非空时才添加
        ax.text(x, y, f'({label})', transform=ax.transAxes, 
                fontsize=fontsize, fontweight=fontweight, va='bottom', ha='left')

def add_grid(ax, axis='y', color='#E0E0E0', linewidth=0.5, alpha=0.7):
    """添加轻量级网格线"""
    ax.grid(True, axis=axis, color=color, linewidth=linewidth, alpha=alpha)
    ax.set_axisbelow(True)  # 网格线在数据下方

def highlight_point(ax, x, y, text, color=None, fontsize=9, offset=(10, 10)):
    """高亮标注关键数据点"""
    if color is None:
        color = COLORS['highlight']
    ax.scatter([x], [y], s=MARKER_SIZE['highlight']**2, c=color, 
               marker=MARKERS['highlight'], zorder=10, edgecolors='white', linewidths=1)
    ax.annotate(text, (x, y), xytext=offset, textcoords='offset points',
                fontsize=fontsize, fontweight='bold', color=color,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='none'),
                arrowprops=dict(arrowstyle='->', color=color, lw=1))

def highlight_region(ax, x_start, x_end, color=None, alpha=0.2, label=None):
    """高亮某个区域"""
    if color is None:
        color = COLORS['highlight']
    ax.axvspan(x_start, x_end, alpha=alpha, color=color, label=label)

def add_reference_line(ax, value, axis='y', color=None, linestyle=':', label=None):
    """添加参考线"""
    if color is None:
        color = COLORS['neutral']
    if axis == 'y':
        ax.axhline(y=value, color=color, linestyle=linestyle, 
                   linewidth=LINE_WIDTH['reference'], alpha=0.7, label=label)
    else:
        ax.axvline(x=value, color=color, linestyle=linestyle,
                   linewidth=LINE_WIDTH['reference'], alpha=0.7, label=label)

def format_axis_ticks(ax, axis='x', interval=None, format_str=None):
    """格式化坐标轴刻度"""
    from matplotlib.ticker import MultipleLocator, FormatStrFormatter
    
    if interval is not None:
        if axis == 'x':
            ax.xaxis.set_major_locator(MultipleLocator(interval))
        else:
            ax.yaxis.set_major_locator(MultipleLocator(interval))
    
    if format_str is not None:
        if axis == 'x':
            ax.xaxis.set_major_formatter(FormatStrFormatter(format_str))
        else:
            ax.yaxis.set_major_formatter(FormatStrFormatter(format_str))

def save_figure(fig, filename, formats=['pdf'], dpi=300):
    """保存图表到指定格式"""
    import os
    for fmt in formats:
        filepath = filename if filename.endswith(f'.{fmt}') else f'{filename}.{fmt}'
        fig.savefig(filepath, format=fmt, dpi=dpi, bbox_inches='tight')
    print(f'Figure saved: {filename}')

# =============================================================================
# 颜色获取函数
# =============================================================================
def get_method_color(method):
    """根据方法名获取对应颜色"""
    method_lower = method.lower()
    if 'rank' in method_lower:
        return COLORS['rank_method']
    elif 'pct' in method_lower or 'percent' in method_lower:
        return COLORS['pct_method']
    elif 'dwvs' in method_lower or 'new' in method_lower or 'dynamic' in method_lower:
        return COLORS['dwvs']
    else:
        return COLORS['neutral']

def get_method_style(method):
    """根据方法名获取对应的线型和标记"""
    method_lower = method.lower()
    if 'rank' in method_lower:
        return LINE_STYLES['rank_method'], MARKERS['rank_method']
    elif 'pct' in method_lower or 'percent' in method_lower:
        return LINE_STYLES['pct_method'], MARKERS['pct_method']
    elif 'dwvs' in method_lower or 'new' in method_lower or 'dynamic' in method_lower:
        return LINE_STYLES['dwvs'], MARKERS['dwvs']
    else:
        return '-', 'o'

# =============================================================================
# 初始化
# =============================================================================
# 自动应用样式
setup_style()

print("✅ Figure style configuration loaded successfully!")
print(f"   Main colors: Rank={COLORS['rank_method']}, Pct={COLORS['pct_method']}, DWVS={COLORS['dwvs']}")
