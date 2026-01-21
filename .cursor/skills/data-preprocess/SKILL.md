---
name: data-preprocess
description: 数学建模数据预处理指南。用于数据加载、清洗、缺失值处理、异常值检测、特征工程等场景。当用户提到预处理、清洗数据、处理缺失值、数据泄露、特征工程、data preprocessing、data cleaning时触发。
---

# 数据预处理指南

## 核心工作流程

```
拿到数据 → 万能Prompt生成代码 → 对照检查清单 → 保存处理后数据
```

---

## 1. 万能Prompt模板

将以下Prompt复制，**替换【】中的内容**，发给AI生成定制化代码：

```markdown
**Role**: 你是一位精通数据科学的教练，擅长撰写可解释、可复现的Jupyter Notebook。

**Background**:
- **题目**: 【填写比赛题目名称和简要描述】
- **数据文件**: 【列出所有数据文件名，如: data1.csv, data2.xlsx】
- **核心需求**: 创建一个数据预处理的 `.ipynb` 文件，代码与Markdown说明比例约1:1

**Task**:
请按以下结构创建Notebook，每一步都要有**Markdown说明业务逻辑**：

### 第一步：数据加载与初探
1. 读取所有数据文件
2. 用 `.info()` 和 `.head()` 查看结构
3. 总结观察到的数据特点（类型、缺失、异常等）

### 第二步：数据清洗
1. **缺失值处理**：说明为什么选择删除/填充/插值
2. **重复值处理**：检查并处理
3. **数据类型转换**：确保类型正确
4. **异常值处理**：识别并说明处理策略

### 第三步：数据合并与关联
1. 识别各表之间的关联键
2. 说明选择哪种JOIN方式及原因
3. 验证合并结果的正确性

### 第四步：特征工程
根据题目需求，考虑创建以下特征：
- 时序特征（滞后值、滚动平均、变化率）
- 分类编码（One-Hot、Label Encoding）
- 数值变换（标准化、对数变换）
- 业务衍生特征

### 第五步：数据验证与保存
1. 检查处理后数据的完整性
2. 保存为CSV供后续建模使用
3. 总结处理流程和关键决策

**Output Requirements**:
- 每段代码前必须有Markdown说明"为什么这样做"
- 代码中包含清晰的注释
- 在关键节点输出验证信息
```

---

## 2. 预处理检查清单

### 数据加载阶段
- [ ] 所有数据文件都已加载
- [ ] 检查了文件编码（UTF-8/GBK/Latin-1）
- [ ] 查看了每个表的 `.info()` 和 `.head()`
- [ ] 记录了各表的行数和列数

### 数据质量阶段
- [ ] 检查了缺失值 `.isnull().sum()`
- [ ] 明确了缺失值的业务含义（"未知"还是"不适用"?）
- [ ] 检查了重复值 `.duplicated()`
- [ ] 检查了数据类型是否正确
- [ ] 识别了可能的异常值

### 数据合并阶段
- [ ] 明确了各表之间的关联关系（一对一/一对多/多对多）
- [ ] 选择了合适的JOIN方式
- [ ] 验证了合并后的行数是否合理
- [ ] 检查了合并后的缺失值

### 特征工程阶段
- [ ] 创建了必要的时序特征
- [ ] 处理了分类变量
- [ ] 检查了特征与目标的相关性
- [ ] **避免了数据泄露**

### 最终验证阶段
- [ ] 无缺失值或已合理处理
- [ ] 数据类型全部正确
- [ ] 保存了处理后的数据
- [ ] 记录了所有处理决策

---

## 3. 数据泄露警示

**数据泄露是比赛中最易犯的错误，会导致模型过拟合！**

| 场景 | 错误做法 | 正确做法 |
|------|----------|---------|
| 时序特征 | `shift(-1)` 获取下一期 | `shift(1)` 获取上一期 |
| 滚动特征 | `rolling(3).mean()` 包含当期 | `rolling(3).mean().shift(1)` 排除当期 |
| 标准化 | 用全部数据 fit_transform | 只用训练集 fit，测试集 transform |
| 目标编码 | 用包含测试集的统计值 | 只用训练集计算统计值 |

**自检方法**：
```python
# 假设要预测2028年数据，检查：特征在2024年时是否已可计算？

# 错误：使用了2028年的信息
df['avg_medals'] = df.groupby('country')['medals'].transform('mean')

# 正确：只使用历史数据
df['avg_medals'] = df.groupby('country')['medals'].transform(
    lambda x: x.shift(1).expanding().mean()
)
```

---

## 4. 常用代码片段

### 标准导入
```python
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', 50)
pd.set_option('display.float_format', '{:.2f}'.format)
```

### 智能读取CSV
```python
def smart_read_csv(filepath, **kwargs):
    """智能读取CSV，自动尝试不同编码"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1', 'cp1252']
    for encoding in encodings:
        try:
            df = pd.read_csv(filepath, encoding=encoding, **kwargs)
            print(f"✅ 成功读取 {filepath} (编码: {encoding})")
            return df
        except UnicodeDecodeError:
            continue
    print(f"❌ 所有编码尝试失败: {filepath}")
    return None
```

### 数据质量报告
```python
def data_quality_report(df, name="DataFrame"):
    """生成数据质量报告"""
    print(f"📊 数据质量报告: {name}")
    print(f"📏 形状: {df.shape[0]} 行 × {df.shape[1]} 列")
    
    # 缺失值
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({'缺失数': missing, '缺失率%': missing_pct})
    missing_df = missing_df[missing_df['缺失数'] > 0].sort_values('缺失率%', ascending=False)
    
    if len(missing_df) > 0:
        print(f"⚠️ 缺失值统计 ({len(missing_df)} 列有缺失):")
        print(missing_df)
    else:
        print("✅ 无缺失值")
    
    # 重复值
    dup_count = df.duplicated().sum()
    print(f"🔄 重复行数: {dup_count} ({dup_count/len(df)*100:.2f}%)")
```

### 缺失值处理策略
```python
# 删除（缺失率高或无法推断）
df = df.dropna(subset=['关键列'])

# 填充固定值
df['col'] = df['col'].fillna(0)           # 数值
df['col'] = df['col'].fillna('Unknown')   # 分类

# 填充统计值
df['col'] = df['col'].fillna(df['col'].median())  # 中位数（对异常值鲁棒）

# 分组填充
df['col'] = df.groupby('group')['col'].transform(lambda x: x.fillna(x.median()))

# 时序插值
df['col'] = df['col'].interpolate(method='linear')
```

### 特征工程模板
```python
# 滞后特征（使用shift(1)避免泄露）
df['value_lag1'] = df.groupby('entity')['value'].shift(1)

# 滚动特征（shift(1)排除当期）
df['value_rolling3'] = df.groupby('entity')['value'].transform(
    lambda x: x.rolling(window=3, min_periods=1).mean().shift(1)
)

# 变化率
df['value_pct_change'] = df.groupby('entity')['value'].pct_change()

# One-Hot编码
df = pd.get_dummies(df, columns=['category_col'], prefix='cat')

# 对数变换（处理右偏分布）
df['value_log'] = np.log1p(df['value'])
```

### 合并验证
```python
def validate_merge(df_left, df_right, df_result, key, merge_type='left'):
    """验证合并结果"""
    print(f"🔍 合并验证 ({merge_type.upper()} JOIN on '{key}')")
    print(f"左表: {len(df_left)} | 右表: {len(df_right)} | 结果: {len(df_result)}")
    
    if merge_type == 'left':
        if len(df_result) == len(df_left):
            print("✅ 行数正常（一对一匹配）")
        elif len(df_result) > len(df_left):
            print(f"⚠️ 行数增加 {len(df_result) - len(df_left)} 行（存在一对多）")
```

---

## 5. 深度参考

- 完整预处理指南：[data_analysis/preprocessing/数据预处理指南.ipynb](data_analysis/preprocessing/数据预处理指南.ipynb)
- 实战案例：[data_analysis/preprocessing/2025C示例/](data_analysis/preprocessing/2025C示例/)
