"""修复notebook中的错误代码"""
import json

with open('问题一建模分析.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# 找到并修复代码
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        
        # 修复1: 投票方法判断
        if "return 'rank' if season <= 17 else 'percentage'" in source:
            source = source.replace(
                "return 'rank' if season <= 17 else 'percentage'",
                "return 'rank' if season <= 2 or season >= 28 else 'percentage'"
            )
            print(f'✓ Cell {i}: 修复了投票方法判断')
        
        # 修复2: verify_consistency中的方法判断
        if "method = 'rank' if season <= 17 else 'percentage'" in source:
            source = source.replace(
                "method = 'rank' if season <= 17 else 'percentage'",
                "method = 'rank' if season <= 2 or season >= 28 else 'percentage'"
            )
            print(f'✓ Cell {i}: 修复了verify_consistency中的方法判断')
        
        # 更新cell source
        cell['source'] = [line + '\n' for line in source.split('\n')]
        if cell['source']:
            cell['source'][-1] = cell['source'][-1].rstrip('\n')

with open('问题一建模分析.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=2)

print('\nNotebook已修复')
