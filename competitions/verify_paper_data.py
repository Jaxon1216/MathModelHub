#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
论文数据验证脚本
验证 main.tex 中的数值是否与源数据文件一致
"""

import pandas as pd
import numpy as np
import json
import os
from pathlib import Path

# 验证结果收集
verification_results = []

def verify_value(paper_value, actual_value, metric_name, source_file, hypothesis_id, tolerance=0.01):
    """验证单个数值"""
    if isinstance(paper_value, str):
        match = paper_value == actual_value
    else:
        try:
            diff = abs(float(paper_value) - float(actual_value))
            match = diff <= tolerance
        except:
            match = False
    
    result = {
        'metric': metric_name,
        'paper_value': paper_value,
        'actual_value': actual_value,
        'match': match,
        'source': source_file,
        'hypothesis': hypothesis_id
    }
    verification_results.append(result)
    
    return match

print("="*80)
print("论文数据验证报告")
print("="*80)

# ============================================================================
# 假设 A: Problem 1 - 一致性分析
# ============================================================================
print("\n[假设 A] 验证 Problem 1 数据...")

try:
    # 读取分层一致性数据
    stratified_file = '改进分析/stratified_consistency.csv'
    df_strat = pd.read_csv(stratified_file)
    
    # 验证整体一致性 80.7%
    overall_consistency = df_strat[df_strat['Category'] == 'Overall']['Consistency'].values
    if len(overall_consistency) > 0:
        verify_value(80.7, overall_consistency[0], 'Overall Consistency (%)', stratified_file, 'A', tolerance=0.5)
    
    # 验证 rank-based method 38.4%
    rank_consistency = df_strat[df_strat['Category'] == 'Rank-based']['Consistency'].values
    if len(rank_consistency) > 0:
        verify_value(38.4, rank_consistency[0], 'Rank-based Consistency (%)', stratified_file, 'A', tolerance=0.5)
    
    # 验证 percentage-based method 96.0%
    pct_consistency = df_strat[df_strat['Category'] == 'Percentage-based']['Consistency'].values
    if len(pct_consistency) > 0:
        verify_value(96.0, pct_consistency[0], 'Percentage-based Consistency (%)', stratified_file, 'A', tolerance=0.5)
    
except Exception as e:
    print(f"  ❌ Error loading stratified consistency: {e}")

try:
    # 验证 certainty index 0.995
    certainty_file = '问题一/certainty_metrics.csv'
    df_cert = pd.read_csv(certainty_file)
    
    if 'certainty_index' in df_cert.columns:
        certainty_idx = df_cert['certainty_index'].mean()
        verify_value(0.995, certainty_idx, 'Certainty Index', certainty_file, 'A', tolerance=0.005)
    
except Exception as e:
    print(f"  ❌ Error loading certainty metrics: {e}")

try:
    # 验证 controversial contestants 数量: 32 (7.6%)
    controversial_file = '问题一/controversial_contestants.csv'
    df_contro = pd.read_csv(controversial_file)
    
    
    num_controversial = len(df_contro)
    verify_value(32, num_controversial, 'Number of Controversial Contestants', controversial_file, 'A', tolerance=0)
    
    # 验证百分比 7.6% (假设总共421个选手)
    total_contestants = 421
    pct_controversial = (num_controversial / total_contestants) * 100
    verify_value(7.6, pct_controversial, 'Controversial Percentage (%)', controversial_file, 'A', tolerance=0.1)
    
except Exception as e:
    print(f"  ❌ Error loading controversial contestants: {e}")

# ============================================================================
# 假设 B: Problem 2 - 方法比较
# ============================================================================
print("\n[假设 B] 验证 Problem 2 数据...")

try:
    method_file = '问题二/method_comparison.csv'
    df_method = pd.read_csv(method_file)
    
    
    # 验证 identical decisions: 73.1% (245/335)
    total_weeks = len(df_method)
    if 'agreement' in df_method.columns or 'same_elimination' in df_method.columns:
        col_name = 'agreement' if 'agreement' in df_method.columns else 'same_elimination'
        identical_count = df_method[col_name].sum()
        identical_pct = (identical_count / total_weeks) * 100
        
        verify_value(335, total_weeks, 'Total Weeks', method_file, 'B', tolerance=0)
        verify_value(245, identical_count, 'Identical Decisions Count', method_file, 'B', tolerance=0)
        verify_value(73.1, identical_pct, 'Identical Decisions (%)', method_file, 'B', tolerance=0.5)
        
        # 验证不同结果: 90 weeks
        different_count = total_weeks - identical_count
        verify_value(90, different_count, 'Different Outcomes Count', method_file, 'B', tolerance=0)
    
except Exception as e:
    print(f"  ❌ Error loading method comparison: {e}")

try:
    # 验证 tiebreaker 影响: 29.7%
    tiebreaker_file = '问题二/tiebreaker_analysis.csv'
    df_tie = pd.read_csv(tiebreaker_file)
    
    
    if 'tiebreaker_affected' in df_tie.columns or 'affected' in df_tie.columns:
        col_name = 'tiebreaker_affected' if 'tiebreaker_affected' in df_tie.columns else 'affected'
        affected_count = df_tie[col_name].sum()
        affected_pct = (affected_count / len(df_tie)) * 100
        verify_value(29.7, affected_pct, 'Tiebreaker Affected (%)', tiebreaker_file, 'B', tolerance=0.5)
    
except Exception as e:
    print(f"  ❌ Error loading tiebreaker analysis: {e}")

# ============================================================================
# 假设 C: Problem 3 - 因素分析
# ============================================================================
print("\n[假设 C] 验证 Problem 3 数据...")

try:
    # 验证 Industry ANOVA: Judge F=8.08, Fan F=2.81
    industry_file = '问题三/industry_analysis.csv'
    df_industry = pd.read_csv(industry_file)
    
    
    # 查找F统计量
    if 'f_statistic_judge' in df_industry.columns:
        f_judge = df_industry['f_statistic_judge'].iloc[0]
        verify_value(8.08, f_judge, 'Industry F-statistic (Judge)', industry_file, 'C', tolerance=0.1)
    
    if 'f_statistic_fan' in df_industry.columns:
        f_fan = df_industry['f_statistic_fan'].iloc[0]
        verify_value(2.81, f_fan, 'Industry F-statistic (Fan)', industry_file, 'C', tolerance=0.1)
    
except Exception as e:
    print(f"  ❌ Error loading industry analysis: {e}")

try:
    # 验证 Age correlation: Judge |r|=0.302, Fan |r|=0.235
    results_file = '问题三/results_summary.csv'
    df_results = pd.read_csv(results_file)
    
    
    # 查找年龄相关性数据
    age_row = df_results[df_results['Factor'] == 'Age'] if 'Factor' in df_results.columns else None
    if age_row is not None and len(age_row) > 0:
        if 'correlation_judge' in df_results.columns:
            r_judge = abs(age_row['correlation_judge'].iloc[0])
            verify_value(0.302, r_judge, 'Age Correlation (Judge)', results_file, 'C', tolerance=0.01)
        
        if 'correlation_fan' in df_results.columns:
            r_fan = abs(age_row['correlation_fan'].iloc[0])
            verify_value(0.235, r_fan, 'Age Correlation (Fan)', results_file, 'C', tolerance=0.01)
    
except Exception as e:
    print(f"  ❌ Error loading age correlation: {e}")

try:
    # 验证 Pro Dancer CV: Fan=0.255, Judge=0.137
    prodancer_file = '问题三/pro_dancer_analysis.csv'
    df_dancer = pd.read_csv(prodancer_file)
    
    
    if 'cv_judge' in df_dancer.columns and 'cv_fan' in df_dancer.columns:
        cv_judge = df_dancer['cv_judge'].iloc[0] if len(df_dancer) > 0 else None
        cv_fan = df_dancer['cv_fan'].iloc[0] if len(df_dancer) > 0 else None
        
        if cv_judge is not None:
            verify_value(0.137, cv_judge, 'Pro Dancer CV (Judge)', prodancer_file, 'C', tolerance=0.01)
        if cv_fan is not None:
            verify_value(0.255, cv_fan, 'Pro Dancer CV (Fan)', prodancer_file, 'C', tolerance=0.01)
    
except Exception as e:
    print(f"  ❌ Error loading pro dancer CV: {e}")

try:
    # 验证 Random Forest R²=0.11
    model_file = '问题三/model_metrics_cv.csv'
    df_model = pd.read_csv(model_file)
    
    
    if 'r2_score' in df_model.columns or 'r2' in df_model.columns:
        col_name = 'r2_score' if 'r2_score' in df_model.columns else 'r2'
        r2_value = df_model[col_name].mean()
        verify_value(0.11, r2_value, 'Random Forest R²', model_file, 'C', tolerance=0.02)
    
except Exception as e:
    print(f"  ❌ Error loading model metrics: {e}")

# ============================================================================
# 假设 D: Problem 4 - DWVS设计
# ============================================================================
print("\n[假设 D] 验证 Problem 4 数据...")

try:
    # 验证最优参数: base α=0.35, increment=0.03
    grid_file = '改进分析/grid_search_results.csv'
    df_grid = pd.read_csv(grid_file)
    
    
    # 找到最优参数（score最高的）
    if 'score' in df_grid.columns or 'optimization_score' in df_grid.columns:
        score_col = 'score' if 'score' in df_grid.columns else 'optimization_score'
        best_row = df_grid.loc[df_grid[score_col].idxmax()]
        
        if 'base_alpha' in df_grid.columns:
            best_base = best_row['base_alpha']
            verify_value(0.35, best_base, 'DWVS Optimal Base Alpha', grid_file, 'D', tolerance=0.01)
        
        if 'alpha_increment' in df_grid.columns:
            best_inc = best_row['alpha_increment']
            verify_value(0.03, best_inc, 'DWVS Optimal Increment', grid_file, 'D', tolerance=0.01)
    
except Exception as e:
    print(f"  ❌ Error loading grid search: {e}")

try:
    # 验证 DWVS 影响: 78.1%降级, 平均+0.34位置
    dwvs_file = '问题四/dwvs_impact_all_controversial.csv'
    df_dwvs = pd.read_csv(dwvs_file)
    
    
    # 计算降级比例
    if 'rank_change' in df_dwvs.columns or 'placement_change' in df_dwvs.columns:
        change_col = 'rank_change' if 'rank_change' in df_dwvs.columns else 'placement_change'
        rank_lower_count = (df_dwvs[change_col] > 0).sum()
        rank_lower_pct = (rank_lower_count / len(df_dwvs)) * 100
        verify_value(78.1, rank_lower_pct, 'DWVS Lower Rank (%)', dwvs_file, 'D', tolerance=1.0)
        
        # 验证平均调整
        avg_change = df_dwvs[change_col].mean()
        verify_value(0.34, avg_change, 'DWVS Average Adjustment', dwvs_file, 'D', tolerance=0.05)
    
    # 验证 Bobby Bones 排名变化
    bobby_row = df_dwvs[df_dwvs['Name'] == 'Bobby Bones'] if 'Name' in df_dwvs.columns else None
    if bobby_row is not None and len(bobby_row) > 0:
        if 'new_placement' in df_dwvs.columns or 'dwvs_placement' in df_dwvs.columns:
            placement_col = 'new_placement' if 'new_placement' in df_dwvs.columns else 'dwvs_placement'
            bobby_new_rank = bobby_row[placement_col].iloc[0]
            verify_value(2, bobby_new_rank, 'Bobby Bones New Placement', dwvs_file, 'D', tolerance=0)
    
except Exception as e:
    print(f"  ❌ Error loading DWVS impact: {e}")

# ============================================================================
# 假设 E: 敏感性分析和验证
# ============================================================================
print("\n[假设 E] 验证敏感性分析和Cross-Season验证...")

try:
    # 验证 Cross-season R²=0.934
    cross_file = '改进分析/cross_season_validation.csv'
    df_cross = pd.read_csv(cross_file)
    
    
    if 'test_r2' in df_cross.columns or 'r2_test' in df_cross.columns:
        r2_col = 'test_r2' if 'test_r2' in df_cross.columns else 'r2_test'
        test_r2 = df_cross[r2_col].iloc[0] if len(df_cross) > 0 else None
        if test_r2 is not None:
            verify_value(0.934, test_r2, 'Cross-Season Test R²', cross_file, 'E', tolerance=0.01)
    
except Exception as e:
    print(f"  ❌ Error loading cross-season validation: {e}")

try:
    # 验证 5-fold CV: R²=0.942±0.013
    cv_metrics_file = '问题三/model_metrics_cv.csv'
    df_cv = pd.read_csv(cv_metrics_file)
    
    
    if 'r2_mean' in df_cv.columns and 'r2_std' in df_cv.columns:
        r2_mean = df_cv['r2_mean'].iloc[0]
        r2_std = df_cv['r2_std'].iloc[0]
        verify_value(0.942, r2_mean, '5-Fold CV R² Mean', cv_metrics_file, 'E', tolerance=0.01)
        verify_value(0.013, r2_std, '5-Fold CV R² Std', cv_metrics_file, 'E', tolerance=0.005)
    
except Exception as e:
    print(f"  ❌ Error loading CV metrics: {e}")

# ============================================================================
# 输出验证报告
# ============================================================================
print("\n" + "="*80)
print("验证结果汇总")
print("="*80)


df_verify = pd.DataFrame(verification_results)

if len(df_verify) > 0:
    # 按假设分组统计
    for hyp in ['A', 'B', 'C', 'D', 'E']:
        hyp_results = df_verify[df_verify['hypothesis'] == hyp]
        if len(hyp_results) > 0:
            match_count = hyp_results['match'].sum()
            total_count = len(hyp_results)
            match_pct = (match_count / total_count) * 100
            
            print(f"\n假设 {hyp}: {match_count}/{total_count} 匹配 ({match_pct:.1f}%)")
            
            # 显示不匹配的项
            mismatches = hyp_results[~hyp_results['match']]
            if len(mismatches) > 0:
                print("  ❌ 不匹配项:")
                for _, row in mismatches.iterrows():
                    print(f"    - {row['metric']}: 论文={row['paper_value']}, 实际={row['actual_value']} ({row['source']})")
    
    # 总体统计
    total_match = df_verify['match'].sum()
    total_verify = len(df_verify)
    overall_pct = (total_match / total_verify) * 100
    
    print("\n" + "="*80)
    print(f"总体匹配率: {total_match}/{total_verify} ({overall_pct:.1f}%)")
    print("="*80)
    
    # 保存详细报告
    output_file = 'verification_detailed_report.csv'
    df_verify.to_csv(output_file, index=False)
    print(f"\n详细报告已保存至: {output_file}")
    
else:
    print("\n❌ 未能加载任何验证数据！")
