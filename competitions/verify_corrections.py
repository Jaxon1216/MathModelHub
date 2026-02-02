#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证论文修正是否正确
"""

import re

print("="*80)
print("论文Industry ANOVA数据修正验证")
print("="*80)

# 读取论文
with open('person1/main.tex', 'r', encoding='utf-8') as f:
    content = f.read()

# 检查点
checks = []

# 1. Abstract中的F值
if 'F_{\\text{judge}}=5.41' in content and 'F_{\\text{fan}}=5.48' in content:
    checks.append(("✓", "Abstract: F值已更新为5.41和5.48"))
else:
    checks.append(("✗", "Abstract: F值未正确更新"))

# 2. ANOVA Results
if '$F = 5.41$' in content and '$F = 5.48$' in content:
    checks.append(("✓", "ANOVA Results: F值已更新"))
else:
    checks.append(("✗", "ANOVA Results: F值未更新"))

# 3. 旧的错误F值不应存在
if '8.08' in content or '2.81' in content:
    # 找到所有包含这些数字的行
    lines_808 = [i+1 for i, line in enumerate(content.split('\n')) if '8.08' in line]
    lines_281 = [i+1 for i, line in enumerate(content.split('\n')) if '2.81' in line]
    checks.append(("✗", f"警告: 仍包含旧F值 (8.08在行{lines_808}, 2.81在行{lines_281})"))
else:
    checks.append(("✓", "旧F值已全部移除"))

# 4. Key Finding更新
if 'similarly' in content and 'difference 1.3' in content:
    checks.append(("✓", "Key Finding: 已改为'similarly'"))
else:
    checks.append(("✗", "Key Finding: 未正确更新"))

# 5. Table中的Stronger On列
if 'Similar' in content or 'similar' in content:
    table_section = content[content.find('\\begin{tabular}{lccc}'):content.find('\\end{tabular}', content.find('\\begin{tabular}{lccc}'))]
    if 'Similar' in table_section or 'Both' in table_section:
        checks.append(("✓", "Table: Stronger On列已更新"))
    else:
        checks.append(("?", "Table: 需手动检查Stronger On列"))
else:
    checks.append(("✗", "Table: 未找到Similar标记"))

# 6. "Judges show stronger industry bias"不应存在
if 'Judges show stronger industry bias' in content or 'stronger industry bias' in content:
    checks.append(("✗", "旧结论'Judges show stronger industry bias'仍存在"))
else:
    checks.append(("✓", "旧结论已移除"))

# 7. 新结论应该存在
if 'Industry bias affects judges and fans similarly' in content:
    checks.append(("✓", "新结论'Industry bias affects judges and fans similarly'已添加"))
else:
    checks.append(("✗", "新结论未正确添加"))

# 输出检查结果
print("\n检查结果:")
print("-"*80)
for symbol, message in checks:
    print(f"{symbol} {message}")

# 统计
passed = sum(1 for s, _ in checks if s == "✓")
failed = sum(1 for s, _ in checks if s == "✗")
total = len(checks)

print("\n" + "="*80)
print(f"总计: {passed}/{total} 通过, {failed} 失败")
print("="*80)

if failed == 0:
    print("\n✓ 所有修正已正确完成！")
else:
    print(f"\n✗ 仍有 {failed} 项需要修正")

# 详细定位
print("\n" + "="*80)
print("关键位置检查:")
print("="*80)

# 查找所有F统计量
f_stats = re.findall(r'F.*?=.*?(\d+\.\d+)', content)
print(f"\n找到的F统计量: {set(f_stats)}")

# 查找Industry相关的关键句子
industry_lines = []
for i, line in enumerate(content.split('\n'), 1):
    if 'Industry' in line and ('Judge' in line or 'Fan' in line or 'bias' in line):
        if len(line.strip()) > 0 and not line.strip().startswith('%'):
            industry_lines.append((i, line.strip()[:100]))

if industry_lines:
    print(f"\nIndustry相关行（前100字符）:")
    for line_num, text in industry_lines[:10]:
        print(f"  Line {line_num}: {text}...")
