#!/usr/bin/env python3
"""
Paper Data Validation Script
Validates all numerical claims in main.tex against source data
"""
import re
import json
import pandas as pd
from pathlib import Path

# Log file configuration
LOG_FILE = Path("/Users/jiangxu/Documents/code/MathModelHub/.cursor/debug.log")

def log_debug(hypothesis_id, location, message, data):
    """Write NDJSON log entry"""
    import time
    log_entry = {
        "sessionId": "debug-session",
        "runId": "validation-run",
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000)
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def extract_tex_values(tex_path):
    """Extract key numerical values from LaTeX"""
    # #region agent log
    log_debug("A", "validate_paper_data.py:35", "Starting LaTeX extraction", {"path": str(tex_path)})
    # #endregion
    
    with open(tex_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    values = {}
    
    # Extract from abstract and memorandum
    abstract_match = re.search(r'\\begin{abstract}(.*?)\\end{abstract}', content, re.DOTALL)
    if abstract_match:
        abstract = abstract_match.group(1)
        values['abstract'] = {
            'consistency_overall': re.search(r'(\d+\.?\d*)\\?%.*?overall consistency', abstract),
            'consistency_percentage': re.search(r'(\d+\.?\d*)\\?%.*?percentage-based', abstract),
            'certainty_index': re.search(r'Certainty Index of (\d+\.?\d*)', abstract),
            'agreement_rate': re.search(r'(\d+\.?\d*)\\?%.*?of cases', abstract),
            'controversial_pct': re.search(r'(\d+\.?\d*)\\?%.*?controversial', abstract),
            'dwvs_improvement': re.search(r'(\d+\.?\d*)\\?%.*?would rank lower', abstract),
        }
    
    # Extract memorandum values
    memo_match = re.search(r'\\section{Memorandum to DWTS Producers}(.*?)(?:\\newpage|\\begin{thebibliography})', content, re.DOTALL)
    if memo_match:
        memo = memo_match.group(1)
        values['memorandum'] = {
            'alpha_base': re.search(r'alpha.*?base.*?(\d+\.?\d*)', memo, re.IGNORECASE),
            'delta': re.search(r'Delta.*?(\d+\.?\d*)', memo, re.IGNORECASE),
            'fan_weight_initial': re.search(r'(\d+)\\?%.*?Fan Vote weight', memo, re.IGNORECASE),
            'judge_weight_final': re.search(r'Judge.*?weight.*?(?:stabilizes at|reaches)\s*(\d+)\\?%', memo, re.IGNORECASE),
            'controversial_improvement': re.search(r'(\d+\.?\d*)\s*\\?%\s+of controversial contestants', memo, re.IGNORECASE),
            'test_r2': re.search(r'Test.*?\$?R.*?\$?[=:\s]*(\d+\.?\d*)', memo, re.IGNORECASE),
        }
        # #region agent log
        log_debug("A", "validate_paper_data.py:72", "Memorandum extracted", {
            "memo_length": len(memo),
            "patterns_found": sum(1 for v in values['memorandum'].values() if v is not None)
        })
        # #endregion
    else:
        # #region agent log
        log_debug("A", "validate_paper_data.py:79", "Memorandum NOT extracted", {"content_length": len(content)})
        # #endregion
    
    # Problem 1 values
    values['problem1'] = {
        'consistency_overall': re.search(r'(\d+\.?\d*)\\?%.*?overall consistency', content),
        'consistency_pct_method': re.search(r'percentage-based method reaching.*?(\d+\.?\d*)\\?%', content),
        'consistency_rank_method': re.search(r'(\d+\.?\d*)\\?%.*?for rank-based method', content),
        'certainty_index': re.search(r'certainty index.*?(\d+\.?\d*)', content),
        'controversial_count': re.search(r'\\textbf{(\d+) controversial contestants}', content),
        'controversial_pct': re.search(r'controversial contestants.*?\((\d+\.?\d*)\\?%\)', content),
    }
    
    # Problem 2 values
    values['problem2'] = {
        'agreement_rate': re.search(r'\\textbf{identical elimination decisions in (\d+\.?\d*)\\?%}', content),
        'tiebreaker_impact': re.search(r'tiebreaker rule affects (\d+\.?\d*)\\?%', content),
    }
    
    # Problem 3 values
    values['problem3'] = {
        'industry_f_judge': re.search(r'Judge Score.*?Industry.*?F = (\d+\.?\d*)', content),
        'industry_f_fan': re.search(r'Fan Vote Share.*?Industry.*?F = (\d+\.?\d*)', content),
        'age_r_judge': re.search(r'Age vs\. Judge Scores.*?r = .*?(\d+\.?\d*)', content),
        'age_r_fan': re.search(r'Age vs\. Fan Votes.*?r = .*?(\d+\.?\d*)', content),
        'r2_external': re.search(r'R\$\^2\$=(\d+\.?\d*).*?external factors', content),
    }
    
    # Problem 4 values  
    values['problem4'] = {
        'alpha_base': re.search(r'base.*?alpha.*?(\d+\.?\d*)', content),
        'increment': re.search(r'increment.*?(\d+\.?\d*)', content),
        'controversial_improvement': re.search(r'(\d+\.?\d*)\\?%.*?controversial contestants would rank lower', content),
        'avg_change': re.search(r'average.*?adjustment.*?\+?(\d+\.?\d*).*?position', content),
    }
    
    # #region agent log
    log_debug("A", "validate_paper_data.py:112", "LaTeX extraction complete", {
        "sections_found": list(values.keys()),
        "total_patterns": sum(len(v) for v in values.values())
    })
    # #endregion
    
    # Convert regex matches to values
    for section, patterns in values.items():
        for key, match in patterns.items():
            if match:
                values[section][key] = float(match.group(1))
            else:
                values[section][key] = None
    
    return values

def load_source_data():
    """Load all source CSV files"""
    # #region agent log
    log_debug("B", "validate_paper_data.py:131", "Loading source data files", {})
    # #endregion
    
    base = Path("/Users/jiangxu/Documents/code/MathModelHub/competitions")
    
    data = {}
    
    # Problem 1 data
    try:
        data['q1_results'] = pd.read_csv(base / "问题一/results_summary.csv")
        data['q1_controversial'] = pd.read_csv(base / "问题一/controversial_contestants.csv")
        data['q1_certainty'] = pd.read_csv(base / "问题一/certainty_metrics.csv")
        # #region agent log
        log_debug("B", "validate_paper_data.py:143", "Q1 data loaded", {
            "results_rows": len(data['q1_results']),
            "controversial_count": len(data['q1_controversial']),
            "certainty_rows": len(data['q1_certainty'])
        })
        # #endregion
    except Exception as e:
        # #region agent log
        log_debug("B", "validate_paper_data.py:151", "Q1 data load failed", {"error": str(e)})
        # #endregion
    
    # Problem 2 data
    try:
        data['q2_results'] = pd.read_csv(base / "问题二/results_summary.csv")
        data['q2_controversial'] = pd.read_csv(base / "问题二/controversial_analysis.csv")
        data['q2_method'] = pd.read_csv(base / "问题二/method_comparison.csv")
        # #region agent log
        log_debug("B", "validate_paper_data.py:161", "Q2 data loaded", {
            "method_comparison_rows": len(data['q2_method']),
            "controversial_rows": len(data['q2_controversial'])
        })
        # #endregion
    except Exception as e:
        # #region agent log
        log_debug("B", "validate_paper_data.py:168", "Q2 data load failed", {"error": str(e)})
        # #endregion
    
    # Problem 3 data
    try:
        data['q3_results'] = pd.read_csv(base / "问题三/results_summary.csv")
        data['q3_industry_anova'] = pd.read_csv(base / "问题三/industry_anova_judge_vs_fan.csv")
        data['q3_feature_importance'] = pd.read_csv(base / "问题三/feature_importance.csv")
        # #region agent log
        log_debug("B", "validate_paper_data.py:178", "Q3 data loaded", {
            "anova_rows": len(data['q3_industry_anova']),
            "feature_importance_rows": len(data['q3_feature_importance'])
        })
        # #endregion
    except Exception as e:
        # #region agent log
        log_debug("B", "validate_paper_data.py:185", "Q3 data load failed", {"error": str(e)})
        # #endregion
    
    # Problem 4 data
    try:
        data['q4_results'] = pd.read_csv(base / "问题四/results_summary.csv")
        # Use the full controversial dataset (all 32)
        data['q4_controversial'] = pd.read_csv(base / "问题四/dwvs_impact_all_controversial.csv")
        data['grid_search'] = pd.read_csv(base / "改进分析/grid_search_results.csv")
        # #region agent log
        log_debug("B", "validate_paper_data.py:195", "Q4 data loaded", {
            "grid_search_rows": len(data['grid_search']),
            "controversial_impact_rows": len(data['q4_controversial'])
        })
        # #endregion
    except Exception as e:
        # #region agent log
        log_debug("B", "validate_paper_data.py:202", "Q4 data load failed", {"error": str(e)})
        # #endregion
    
    # Cross-validation data
    try:
        data['cross_validation'] = pd.read_csv(base / "改进分析/cross_season_validation.csv")
        # #region agent log
        log_debug("B", "validate_paper_data.py:209", "Cross-validation data loaded", {
            "rows": len(data['cross_validation'])
        })
        # #endregion
    except Exception as e:
        # #region agent log
        log_debug("B", "validate_paper_data.py:215", "Cross-validation load failed", {"error": str(e)})
        # #endregion
    
    return data

def validate_problem1(tex_values, source_data):
    """Validate Problem 1 claims"""
    # #region agent log
    log_debug("B", "validate_paper_data.py:223", "Validating Problem 1", {})
    # #endregion
    
    issues = []
    
    # Check controversial contestant count
    tex_count = tex_values['problem1'].get('controversial_count')
    actual_count = len(source_data['q1_controversial'])
    
    # #region agent log
    log_debug("B", "validate_paper_data.py:233", "Checking controversial count", {
        "tex_value": tex_count,
        "actual_value": actual_count,
        "match": tex_count == actual_count
    })
    # #endregion
    
    if tex_count != actual_count:
        issues.append(f"❌ Controversial contestant count: Paper says {tex_count}, data shows {actual_count}")
    else:
        print(f"✓ Controversial contestant count: {tex_count} (matches)")
    
    # Check consistency rates
    if 'q1_results' in source_data and not source_data['q1_results'].empty:
        results = source_data['q1_results']
        if 'overall_consistency' in results.columns:
            actual_consistency = results['overall_consistency'].iloc[0] * 100
            tex_consistency = tex_values['problem1'].get('consistency_overall')
            
            # #region agent log
            log_debug("B", "validate_paper_data.py:253", "Checking overall consistency", {
                "tex_value": tex_consistency,
                "actual_value": actual_consistency,
                "diff": abs(tex_consistency - actual_consistency) if tex_consistency else None
            })
            # #endregion
            
            if tex_consistency and abs(tex_consistency - actual_consistency) > 0.1:
                issues.append(f"❌ Overall consistency: Paper says {tex_consistency}%, data shows {actual_consistency:.1f}%")
            else:
                print(f"✓ Overall consistency: {tex_consistency}% (matches)")
    
    # Check certainty index
    if 'q1_certainty' in source_data and not source_data['q1_certainty'].empty:
        certainty = source_data['q1_certainty']
        if 'certainty_index' in certainty.columns:
            actual_certainty = certainty['certainty_index'].iloc[0]
            tex_certainty = tex_values['problem1'].get('certainty_index')
            
            # #region agent log
            log_debug("B", "validate_paper_data.py:273", "Checking certainty index", {
                "tex_value": tex_certainty,
                "actual_value": actual_certainty,
                "diff": abs(tex_certainty - actual_certainty) if tex_certainty else None
            })
            # #endregion
            
            if tex_certainty and abs(tex_certainty - actual_certainty) > 0.001:
                issues.append(f"❌ Certainty index: Paper says {tex_certainty}, data shows {actual_certainty:.3f}")
            else:
                print(f"✓ Certainty index: {tex_certainty} (matches)")
    
    return issues

def validate_problem2(tex_values, source_data):
    """Validate Problem 2 claims"""
    # #region agent log
    log_debug("C", "validate_paper_data.py:291", "Validating Problem 2", {})
    # #endregion
    
    issues = []
    
    # Check agreement rate
    if 'q2_method' in source_data and not source_data['q2_method'].empty:
        method = source_data['q2_method']
        if 'agreement_rate' in method.columns:
            actual_agreement = method['agreement_rate'].iloc[0] * 100
            tex_agreement = tex_values['problem2'].get('agreement_rate')
            
            # #region agent log
            log_debug("C", "validate_paper_data.py:305", "Checking agreement rate", {
                "tex_value": tex_agreement,
                "actual_value": actual_agreement,
                "diff": abs(tex_agreement - actual_agreement) if tex_agreement else None
            })
            # #endregion
            
            if tex_agreement and abs(tex_agreement - actual_agreement) > 0.1:
                issues.append(f"❌ Agreement rate: Paper says {tex_agreement}%, data shows {actual_agreement:.1f}%")
            else:
                print(f"✓ Agreement rate: {tex_agreement}% (matches)")
    
    return issues

def validate_problem3(tex_values, source_data):
    """Validate Problem 3 claims"""
    # #region agent log
    log_debug("D", "validate_paper_data.py:323", "Validating Problem 3", {})
    # #endregion
    
    issues = []
    
    # Check ANOVA F-statistics
    if 'q3_industry_anova' in source_data and not source_data['q3_industry_anova'].empty:
        anova = source_data['q3_industry_anova']
        
        # Judge score F-statistic
        if 'f_statistic_judge' in anova.columns:
            actual_f_judge = anova['f_statistic_judge'].iloc[0]
            tex_f_judge = tex_values['problem3'].get('industry_f_judge')
            
            # #region agent log
            log_debug("D", "validate_paper_data.py:339", "Checking judge F-statistic", {
                "tex_value": tex_f_judge,
                "actual_value": actual_f_judge,
                "diff": abs(tex_f_judge - actual_f_judge) if tex_f_judge else None
            })
            # #endregion
            
            if tex_f_judge and abs(tex_f_judge - actual_f_judge) > 0.1:
                issues.append(f"❌ Judge F-statistic: Paper says {tex_f_judge}, data shows {actual_f_judge:.2f}")
            else:
                print(f"✓ Judge F-statistic: {tex_f_judge} (matches)")
        
        # Fan vote F-statistic
        if 'f_statistic_fan' in anova.columns:
            actual_f_fan = anova['f_statistic_fan'].iloc[0]
            tex_f_fan = tex_values['problem3'].get('industry_f_fan')
            
            # #region agent log
            log_debug("D", "validate_paper_data.py:358", "Checking fan F-statistic", {
                "tex_value": tex_f_fan,
                "actual_value": actual_f_fan,
                "diff": abs(tex_f_fan - actual_f_fan) if tex_f_fan else None
            })
            # #endregion
            
            if tex_f_fan and abs(tex_f_fan - actual_f_fan) > 0.1:
                issues.append(f"❌ Fan F-statistic: Paper says {tex_f_fan}, data shows {actual_f_fan:.2f}")
            else:
                print(f"✓ Fan F-statistic: {tex_f_fan} (matches)")
    
    return issues

def validate_problem4(tex_values, source_data):
    """Validate Problem 4 claims"""
    # #region agent log
    log_debug("E", "validate_paper_data.py:377", "Validating Problem 4", {})
    # #endregion
    
    issues = []
    
    # Check grid search optimal parameters
    if 'grid_search' in source_data and not source_data['grid_search'].empty:
        grid = source_data['grid_search']
        
        # #region agent log
        log_debug("E", "validate_paper_data.py:383", "Grid search columns", {
            "columns": list(grid.columns)
        })
        # #endregion
        
        # Find optimal parameters (use 'score' column)
        score_col = 'score' if 'score' in grid.columns else 'optimization_score'
        optimal_row = grid.loc[grid[score_col].idxmax()]
        actual_base = optimal_row['base_alpha']
        actual_increment = optimal_row['increment']
        
        tex_base = tex_values['problem4'].get('alpha_base')
        tex_increment = tex_values['problem4'].get('increment')
        
        # #region agent log
        log_debug("E", "validate_paper_data.py:395", "Checking DWVS parameters", {
            "tex_base": tex_base,
            "actual_base": actual_base,
            "tex_increment": tex_increment,
            "actual_increment": actual_increment
        })
        # #endregion
        
        if tex_base and abs(tex_base - actual_base) > 0.01:
            issues.append(f"❌ Base alpha: Paper says {tex_base}, data shows {actual_base:.2f}")
        else:
            print(f"✓ Base alpha: {tex_base} (matches)")
        
        if tex_increment and abs(tex_increment - actual_increment) > 0.01:
            issues.append(f"❌ Increment: Paper says {tex_increment}, data shows {actual_increment:.2f}")
        else:
            print(f"✓ Increment: {tex_increment} (matches)")
    
    # Check controversial improvement rate
    if 'q4_controversial' in source_data and not source_data['q4_controversial'].empty:
        controversial = source_data['q4_controversial']
        
        # Check for either placement_change or dwvs_change column
        change_col = None
        if 'placement_change' in controversial.columns:
            change_col = 'placement_change'
        elif 'dwvs_change' in controversial.columns:
            change_col = 'dwvs_change'
        
        if change_col:
            # Count how many ranked lower (positive change means worse placement)
            total = len(controversial)
            ranked_lower = (controversial[change_col] > 0).sum()
            actual_pct = (ranked_lower / total) * 100
            avg_change = controversial[change_col].mean()
            
            tex_pct = tex_values['problem4'].get('controversial_improvement')
            
            # #region agent log
            log_debug("E", "validate_paper_data.py:427", "Checking controversial improvement", {
                "tex_value": tex_pct,
                "actual_value": actual_pct,
                "ranked_lower": int(ranked_lower),
                "total": int(total),
                "avg_change": float(avg_change),
                "change_column": change_col
            })
            # #endregion
            
            if tex_pct and abs(tex_pct - actual_pct) > 0.5:
                issues.append(f"❌ Controversial improvement: Paper says {tex_pct}%, data shows {actual_pct:.1f}%")
            else:
                print(f"✓ Controversial improvement: {tex_pct}% (matches)")
    
    return issues

def validate_cross_sections(tex_values):
    """Validate consistency between memorandum and main text"""
    # #region agent log
    log_debug("A", "validate_paper_data.py:447", "Validating cross-section consistency", {})
    # #endregion
    
    issues = []
    
    # Compare memorandum vs problem4
    memo_base = tex_values['memorandum'].get('alpha_base')
    p4_base = tex_values['problem4'].get('alpha_base')
    
    # #region agent log
    log_debug("A", "validate_paper_data.py:457", "Comparing memo vs P4 alpha", {
        "memo_value": memo_base,
        "p4_value": p4_base,
        "match": memo_base == p4_base if (memo_base and p4_base) else None
    })
    # #endregion
    
    if memo_base and p4_base and abs(memo_base - p4_base) > 0.01:
        issues.append(f"❌ Memorandum alpha ({memo_base}) ≠ Problem 4 alpha ({p4_base})")
    else:
        print(f"✓ Alpha base consistent across sections")
    
    # Compare memorandum vs problem4 improvement rate
    memo_improvement = tex_values['memorandum'].get('controversial_improvement')
    p4_improvement = tex_values['problem4'].get('controversial_improvement')
    
    # #region agent log
    log_debug("A", "validate_paper_data.py:475", "Comparing improvement rates", {
        "memo_value": memo_improvement,
        "p4_value": p4_improvement,
        "match": memo_improvement == p4_improvement if (memo_improvement and p4_improvement) else None
    })
    # #endregion
    
    if memo_improvement and p4_improvement and abs(memo_improvement - p4_improvement) > 0.5:
        issues.append(f"❌ Memorandum improvement ({memo_improvement}%) ≠ Problem 4 improvement ({p4_improvement}%)")
    else:
        print(f"✓ Improvement rate consistent across sections")
    
    return issues

def main():
    """Main validation function"""
    print("=" * 80)
    print("DWTS Paper Data Validation")
    print("=" * 80)
    
    # #region agent log
    log_debug("MAIN", "validate_paper_data.py:497", "Validation started", {})
    # #endregion
    
    tex_path = Path("/Users/jiangxu/Documents/code/MathModelHub/competitions/person1/main.tex")
    
    print("\n📄 Extracting values from LaTeX...")
    tex_values = extract_tex_values(tex_path)
    
    print("\n📊 Loading source data...")
    source_data = load_source_data()
    
    all_issues = []
    
    print("\n" + "=" * 80)
    print("VALIDATION RESULTS")
    print("=" * 80)
    
    print("\n🔍 Cross-Section Consistency (Memorandum vs Main Text)")
    print("-" * 80)
    issues = validate_cross_sections(tex_values)
    all_issues.extend(issues)
    
    print("\n🔍 Problem 1 Validation")
    print("-" * 80)
    issues = validate_problem1(tex_values, source_data)
    all_issues.extend(issues)
    
    print("\n🔍 Problem 2 Validation")
    print("-" * 80)
    issues = validate_problem2(tex_values, source_data)
    all_issues.extend(issues)
    
    print("\n🔍 Problem 3 Validation")
    print("-" * 80)
    issues = validate_problem3(tex_values, source_data)
    all_issues.extend(issues)
    
    print("\n🔍 Problem 4 Validation")
    print("-" * 80)
    issues = validate_problem4(tex_values, source_data)
    all_issues.extend(issues)
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    # #region agent log
    log_debug("MAIN", "validate_paper_data.py:548", "Validation complete", {
        "total_issues": len(all_issues),
        "issues": all_issues
    })
    # #endregion
    
    if all_issues:
        print(f"\n⚠️  Found {len(all_issues)} issue(s):\n")
        for issue in all_issues:
            print(f"  {issue}")
    else:
        print("\n✅ All validations passed! Paper data is consistent with source data.")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
