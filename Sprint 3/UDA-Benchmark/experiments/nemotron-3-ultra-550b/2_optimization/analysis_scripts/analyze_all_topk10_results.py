#!/usr/bin/env python3
"""
Analyze all TOP_K=10 optimization results vs baseline
Compare all 6 datasets and generate comprehensive summary
"""

import pandas as pd
import os
from pathlib import Path

# Paths
baseline_dir = "../1_without_optimization"
optimized_dir = "results"

# Dataset configurations
datasets = [
    {
        "name": "TatHybrid",
        "code": "tathybrid",
        "baseline_file": "tathybrid_results_20260629_094232.csv",
        "optimized_file": "tathybrid_results_20260629_155316.csv",
        "qa_count": 162,
        "domain": "Finance"
    },
    {
        "name": "FinHybrid",
        "code": "finhybrid",
        "baseline_file": "finhybrid_results_20260629_120808.csv",
        "optimized_file": "finhybrid_results_20260629_152848.csv",
        "qa_count": 47,
        "domain": "Finance"
    },
    {
        "name": "NqText",
        "code": "nqtext",
        "baseline_file": "nqtext_results_20260629_112238.csv",
        "optimized_file": "nqtext_results_20260629_154410.csv",
        "qa_count": 78,
        "domain": "Wikipedia"
    },
    {
        "name": "FetaTab",
        "code": "fetatab",
        "baseline_file": "fetatab_results_20260629_120656.csv",
        "optimized_file": "fetatab_results_20260629_163136.csv",
        "qa_count": 8,
        "domain": "Wikipedia"
    },
    {
        "name": "PaperText",
        "code": "papertext",
        "baseline_file": "papertext_results_20260629_104112.csv",
        "optimized_file": "papertext_results_20260629_163615.csv",
        "qa_count": 13,
        "domain": "Academic"
    },
    {
        "name": "PaperTab",
        "code": "papertab",
        "baseline_file": "papertab_results_20260629_103921.csv",
        "optimized_file": "papertab_results_20260629_163829.csv",
        "qa_count": 4,
        "domain": "Academic"
    }
]

print("=" * 80)
print("📊 TOP_K=10 OPTIMIZATION - COMPLETE RESULTS (ALL 6 DATASETS)")
print("=" * 80)
print()

# Collect all results
all_results = []

for dataset in datasets:
    print(f"Analyzing {dataset['name']}...")

    # Load baseline
    baseline_path = f"{baseline_dir}/{dataset['code']}/results/{dataset['baseline_file']}"
    baseline_df = pd.read_csv(baseline_path)

    # Load optimized
    optimized_path = f"{optimized_dir}/{dataset['code']}_topk10/{dataset['optimized_file']}"
    optimized_df = pd.read_csv(optimized_path)

    # Count empty responses (NaN or empty string)
    baseline_empty = (baseline_df['response'].isna() | (baseline_df['response'].str.strip() == '')).sum()
    optimized_empty = (optimized_df['response'].isna() | (optimized_df['response'].str.strip() == '')).sum()

    # Calculate metrics
    total = dataset['qa_count']
    baseline_empty_pct = (baseline_empty / total) * 100
    optimized_empty_pct = (optimized_empty / total) * 100
    improvement = baseline_empty - optimized_empty
    improvement_pct = baseline_empty_pct - optimized_empty_pct

    # Store results
    result = {
        'Dataset': dataset['name'],
        'Domain': dataset['domain'],
        'Q&A': total,
        'Baseline Empty': baseline_empty,
        'Baseline Empty %': baseline_empty_pct,
        'Optimized Empty': optimized_empty,
        'Optimized Empty %': optimized_empty_pct,
        'Improvement': improvement,
        'Improvement %': improvement_pct,
        'Status': '✅' if improvement >= 0 else '⚠️'
    }

    all_results.append(result)

# Create summary dataframe
summary_df = pd.DataFrame(all_results)

print()
print("=" * 80)
print("📋 SUMMARY TABLE - ALL 6 DATASETS")
print("=" * 80)
print()

# Print table
for _, row in summary_df.iterrows():
    print(f"{row['Dataset']:12} | {row['Domain']:10} | {row['Q&A']:3} Q&A | "
          f"Baseline: {row['Baseline Empty']:2.0f} ({row['Baseline Empty %']:5.1f}%) | "
          f"Optimized: {row['Optimized Empty']:2.0f} ({row['Optimized Empty %']:5.1f}%) | "
          f"Change: {row['Improvement']:+2.0f} ({row['Improvement %']:+5.1f}%) {row['Status']}")

print()
print("=" * 80)
print("📊 OVERALL STATISTICS")
print("=" * 80)
print()

# Calculate overall stats
total_qa = summary_df['Q&A'].sum()
total_baseline_empty = summary_df['Baseline Empty'].sum()
total_optimized_empty = summary_df['Optimized Empty'].sum()
total_improvement = total_baseline_empty - total_optimized_empty

overall_baseline_pct = (total_baseline_empty / total_qa) * 100
overall_optimized_pct = (total_optimized_empty / total_qa) * 100
overall_improvement_pct = overall_baseline_pct - overall_optimized_pct

print(f"Total Q&A Tested:           {total_qa}")
print(f"Total Baseline Empty:       {total_baseline_empty} ({overall_baseline_pct:.1f}%)")
print(f"Total Optimized Empty:      {total_optimized_empty} ({overall_optimized_pct:.1f}%)")
print(f"Total Improvement:          {total_improvement:+d} questions ({overall_improvement_pct:+.1f}%)")
print()
print(f"Questions Answered Before:  {total_qa - total_baseline_empty}")
print(f"Questions Answered After:   {total_qa - total_optimized_empty}")
print(f"Additional Questions:       {total_improvement:+d}")
print()

# Success rate
datasets_improved = (summary_df['Improvement'] > 0).sum()
datasets_stable = (summary_df['Improvement'] == 0).sum()
datasets_worse = (summary_df['Improvement'] < 0).sum()

print(f"Datasets Improved:          {datasets_improved}/6 ✅")
print(f"Datasets Stable:            {datasets_stable}/6 ➖")
print(f"Datasets Worse:             {datasets_worse}/6 ⚠️")
print()

# Domain breakdown
print("=" * 80)
print("📊 BY DOMAIN")
print("=" * 80)
print()

for domain in ['Finance', 'Wikipedia', 'Academic']:
    domain_df = summary_df[summary_df['Domain'] == domain]
    if len(domain_df) > 0:
        domain_qa = domain_df['Q&A'].sum()
        domain_baseline = domain_df['Baseline Empty'].sum()
        domain_optimized = domain_df['Optimized Empty'].sum()
        domain_improvement = domain_baseline - domain_optimized

        domain_baseline_pct = (domain_baseline / domain_qa) * 100
        domain_optimized_pct = (domain_optimized / domain_qa) * 100
        domain_improvement_pct = domain_baseline_pct - domain_optimized_pct

        print(f"{domain:12} | {domain_qa:3} Q&A | "
              f"Baseline: {domain_baseline:2.0f} ({domain_baseline_pct:5.1f}%) | "
              f"Optimized: {domain_optimized:2.0f} ({domain_optimized_pct:5.1f}%) | "
              f"Change: {domain_improvement:+2.0f} ({domain_improvement_pct:+5.1f}%)")

print()
print("=" * 80)
print("🌟 TOP PERFORMERS")
print("=" * 80)
print()

# Sort by improvement
top_performers = summary_df.sort_values('Improvement %', ascending=False)
print("By Absolute Improvement %:")
for i, (_, row) in enumerate(top_performers.head(3).iterrows(), 1):
    print(f"  {i}. {row['Dataset']:12} {row['Improvement %']:+5.1f}% ({row['Improvement']:+2.0f} questions)")

print()

# Best by domain
print("Best Per Domain:")
for domain in ['Finance', 'Wikipedia', 'Academic']:
    domain_best = summary_df[summary_df['Domain'] == domain].sort_values('Improvement %', ascending=False).iloc[0]
    print(f"  {domain:12}: {domain_best['Dataset']:12} {domain_best['Improvement %']:+5.1f}%")

print()
print("=" * 80)
print("💰 COST & TIME ESTIMATE")
print("=" * 80)
print()

# Estimate based on known costs
cost_estimates = {
    'TatHybrid': (60, 90, 13, 20),
    'FinHybrid': (15, 20, 3, 5),
    'NqText': (30, 40, 5, 8),
    'FetaTab': (5, 10, 2, 3),
    'PaperText': (5, 10, 2, 3),
    'PaperTab': (3, 5, 1, 2)
}

total_min_time = sum(est[0] for est in cost_estimates.values())
total_max_time = sum(est[1] for est in cost_estimates.values())
total_min_cost = sum(est[2] for est in cost_estimates.values())
total_max_cost = sum(est[3] for est in cost_estimates.values())

print(f"Estimated Total Runtime:    {total_min_time}-{total_max_time} minutes (~{total_min_time//60}-{total_max_time//60} hours)")
print(f"Estimated Total Cost:       ${total_min_cost}-${total_max_cost}")
print(f"Cost per Question Answered: ${total_min_cost/total_improvement:.2f}-${total_max_cost/total_improvement:.2f} per question")
print()

print("=" * 80)
print("✅ VERDICT")
print("=" * 80)
print()

if datasets_improved >= 5:
    verdict = "EXCELLENT SUCCESS! ✅✅✅"
elif datasets_improved >= 4:
    verdict = "STRONG SUCCESS! ✅✅"
elif datasets_improved >= 3:
    verdict = "GOOD SUCCESS! ✅"
else:
    verdict = "MIXED RESULTS"

print(f"Overall: {verdict}")
print()
print(f"TOP_K=10 improved {datasets_improved}/6 datasets ({datasets_improved/6*100:.0f}%)")
print(f"Total improvement: {total_improvement} more questions answered ({overall_improvement_pct:+.1f}%)")
print()

if overall_improvement_pct > 4:
    recommendation = "STRONGLY RECOMMEND making TOP_K=10 the new baseline"
elif overall_improvement_pct > 2:
    recommendation = "RECOMMEND making TOP_K=10 the new baseline"
elif overall_improvement_pct > 0:
    recommendation = "Consider making TOP_K=10 the new baseline"
else:
    recommendation = "Keep TOP_K=5 as baseline"

print(f"Recommendation: {recommendation}")
print()

# Save summary
summary_df.to_csv('TOPK10_COMPLETE_SUMMARY.csv', index=False)
print(f"📁 Summary saved to: TOPK10_COMPLETE_SUMMARY.csv")
print()

print("=" * 80)
print("🚀 NEXT STEPS")
print("=" * 80)
print()
print("1. Review detailed per-document breakdowns in individual result files")
print("2. Update COMPREHENSIVE_RESULTS_TOPK10.md with new datasets")
print("3. Make decision: Adopt TOP_K=10 as new baseline?")
print("4. Test next optimization: CHUNK_SIZE=1500 on table-heavy datasets")
print("5. Stack optimizations: TOP_K=10 + CHUNK_SIZE=1500")
print()
print("=" * 80)
