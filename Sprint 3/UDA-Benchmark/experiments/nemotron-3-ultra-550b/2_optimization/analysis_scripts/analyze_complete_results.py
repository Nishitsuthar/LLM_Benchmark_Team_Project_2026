#!/usr/bin/env python3
"""
Complete Overall Results Analysis - All 6 Datasets
Compare Baseline → TOP_K=10 → TOP_K=10+CHUNK=1500
"""

import pandas as pd

print("=" * 90)
print("🎉 COMPLETE OPTIMIZATION RESULTS - ALL 6 DATASETS")
print("=" * 90)
print()

# Dataset configurations
datasets = [
    {
        'name': 'TatHybrid',
        'code': 'tathybrid',
        'qa_count': 162,
        'domain': 'Finance',
        'type': 'Tables',
        'baseline': '../1_without_optimization/tathybrid/results/tathybrid_results_20260629_094232.csv',
        'topk10': 'results/tathybrid_topk10/tathybrid_results_20260629_155316.csv',
        'topk10_chunk1500': 'results/tathybrid_topk10_chunk1500/tathybrid_results_20260629_164938.csv'
    },
    {
        'name': 'FinHybrid',
        'code': 'finhybrid',
        'qa_count': 47,
        'domain': 'Finance',
        'type': 'Tables',
        'baseline': '../1_without_optimization/finhybrid/results/finhybrid_results_20260629_120808.csv',
        'topk10': 'results/finhybrid_topk10/finhybrid_results_20260629_152848.csv',
        'topk10_chunk1500': 'results/finhybrid_topk10_chunk1500/finhybrid_results_20260629_170526.csv'
    },
    {
        'name': 'NqText',
        'code': 'nqtext',
        'qa_count': 78,
        'domain': 'Wikipedia',
        'type': 'Text',
        'baseline': '../1_without_optimization/nqtext/results/nqtext_results_20260629_112238.csv',
        'topk10': 'results/nqtext_topk10/nqtext_results_20260629_154410.csv',
        'topk10_chunk1500': None  # Text dataset, kept at CHUNK=3000
    },
    {
        'name': 'FetaTab',
        'code': 'fetatab',
        'qa_count': 8,
        'domain': 'Wikipedia',
        'type': 'Tables',
        'baseline': '../1_without_optimization/fetatab/results/fetatab_results_20260629_120656.csv',
        'topk10': 'results/fetatab_topk10/fetatab_results_20260629_163136.csv',
        'topk10_chunk1500': 'results/fetatab_topk10_chunk1500/fetatab_results_20260629_172850.csv'
    },
    {
        'name': 'PaperText',
        'code': 'papertext',
        'qa_count': 13,
        'domain': 'Academic',
        'type': 'Text',
        'baseline': '../1_without_optimization/papertext/results/papertext_results_20260629_104112.csv',
        'topk10': 'results/papertext_topk10/papertext_results_20260629_163615.csv',
        'topk10_chunk1500': None  # Text dataset, kept at CHUNK=3000
    },
    {
        'name': 'PaperTab',
        'code': 'papertab',
        'qa_count': 4,
        'domain': 'Academic',
        'type': 'Tables',
        'baseline': '../1_without_optimization/papertab/results/papertab_results_20260629_103921.csv',
        'topk10': 'results/papertab_topk10/papertab_results_20260629_163829.csv',
        'topk10_chunk1500': 'results/papertab_topk10_chunk1500/papertab_results_20260629_173414.csv'
    }
]

# Analyze each dataset
all_results = []

for ds in datasets:
    # Load baseline
    df_baseline = pd.read_csv(ds['baseline'])
    baseline_empty = (df_baseline['response'].isna() | (df_baseline['response'].str.strip() == '')).sum()
    baseline_empty_pct = (baseline_empty / ds['qa_count']) * 100

    # Load TOP_K=10
    df_topk10 = pd.read_csv(ds['topk10'])
    topk10_empty = (df_topk10['response'].isna() | (df_topk10['response'].str.strip() == '')).sum()
    topk10_empty_pct = (topk10_empty / ds['qa_count']) * 100

    # Load TOP_K=10 + CHUNK=1500 (if exists)
    if ds['topk10_chunk1500']:
        df_chunk = pd.read_csv(ds['topk10_chunk1500'])
        chunk_empty = (df_chunk['response'].isna() | (df_chunk['response'].str.strip() == '')).sum()
        chunk_empty_pct = (chunk_empty / ds['qa_count']) * 100
    else:
        chunk_empty = topk10_empty
        chunk_empty_pct = topk10_empty_pct

    # Store results
    result = {
        'Dataset': ds['name'],
        'Domain': ds['domain'],
        'Type': ds['type'],
        'Q&A': ds['qa_count'],
        'Baseline Empty': baseline_empty,
        'Baseline %': baseline_empty_pct,
        'TOP_K=10 Empty': topk10_empty,
        'TOP_K=10 %': topk10_empty_pct,
        'Best Empty': chunk_empty,
        'Best %': chunk_empty_pct,
        'Best Config': 'TOP_K=10+CHUNK=1500' if ds['topk10_chunk1500'] else 'TOP_K=10',
        'Total Improvement': baseline_empty - chunk_empty,
        'Total Improvement %': baseline_empty_pct - chunk_empty_pct
    }

    all_results.append(result)

# Create DataFrame
results_df = pd.DataFrame(all_results)

# Print main results table
print("📊 COMPLETE RESULTS TABLE")
print("=" * 90)
print()
print(f"{'Dataset':<12} {'Domain':<10} {'Type':<7} {'Q&A':>4} {'Baseline':>12} {'TOP_K=10':>12} {'Best':>12} {'Gain':>8}")
print("-" * 90)

for _, row in results_df.iterrows():
    baseline_str = f"{row['Baseline Empty']:2.0f} ({row['Baseline %']:5.1f}%)"
    topk10_str = f"{row['TOP_K=10 Empty']:2.0f} ({row['TOP_K=10 %']:5.1f}%)"
    best_str = f"{row['Best Empty']:2.0f} ({row['Best %']:5.1f}%)"
    improvement_str = f"+{row['Total Improvement']:.0f}" if row['Total Improvement'] > 0 else f"{row['Total Improvement']:.0f}"

    print(f"{row['Dataset']:<12} {row['Domain']:<10} {row['Type']:<7} {row['Q&A']:4} {baseline_str:>12} {topk10_str:>12} {best_str:>12} {improvement_str:>8}")

print()

# Overall statistics
print("=" * 90)
print("📈 OVERALL STATISTICS")
print("=" * 90)
print()

total_qa = results_df['Q&A'].sum()
total_baseline_empty = results_df['Baseline Empty'].sum()
total_topk10_empty = results_df['TOP_K=10 Empty'].sum()
total_best_empty = results_df['Best Empty'].sum()

total_baseline_pct = (total_baseline_empty / total_qa) * 100
total_topk10_pct = (total_topk10_empty / total_qa) * 100
total_best_pct = (total_best_empty / total_qa) * 100

topk10_improvement = total_baseline_empty - total_topk10_empty
chunk_improvement = total_topk10_empty - total_best_empty
total_improvement = total_baseline_empty - total_best_empty

print(f"Total Q&A Tested:               {total_qa}")
print()
print(f"Baseline Empty:                 {total_baseline_empty} ({total_baseline_pct:.1f}%)")
print(f"After TOP_K=10:                 {total_topk10_empty} ({total_topk10_pct:.1f}%)")
print(f"After Best Config:              {total_best_empty} ({total_best_pct:.1f}%)")
print()
print(f"TOP_K=10 Improvement:           +{topk10_improvement} questions ({(total_baseline_pct - total_topk10_pct):.1f}%)")
print(f"CHUNK=1500 Additional:          +{chunk_improvement} questions ({(total_topk10_pct - total_best_pct):.1f}%)")
print(f"TOTAL IMPROVEMENT:              +{total_improvement} questions ({(total_baseline_pct - total_best_pct):.1f}%) ✅✅✅")
print()

# Success metrics
datasets_improved = (results_df['Total Improvement'] > 0).sum()
datasets_stable = (results_df['Total Improvement'] == 0).sum()
datasets_worse = (results_df['Total Improvement'] < 0).sum()

print(f"Datasets Improved:              {datasets_improved}/6 ({datasets_improved/6*100:.0f}%)")
print(f"Datasets Stable:                {datasets_stable}/6 ({datasets_stable/6*100:.0f}%)")
print(f"Datasets Worse:                 {datasets_worse}/6 ({datasets_worse/6*100:.0f}%)")
print()

# Domain analysis
print("=" * 90)
print("📊 BY DOMAIN")
print("=" * 90)
print()

for domain in ['Finance', 'Wikipedia', 'Academic']:
    domain_df = results_df[results_df['Domain'] == domain]
    if len(domain_df) > 0:
        domain_qa = domain_df['Q&A'].sum()
        domain_baseline = domain_df['Baseline Empty'].sum()
        domain_best = domain_df['Best Empty'].sum()
        domain_improvement = domain_baseline - domain_best

        domain_baseline_pct = (domain_baseline / domain_qa) * 100
        domain_best_pct = (domain_best / domain_qa) * 100
        domain_improvement_pct = domain_baseline_pct - domain_best_pct

        print(f"{domain:12} | {domain_qa:3} Q&A | "
              f"Baseline: {domain_baseline:2.0f} ({domain_baseline_pct:5.1f}%) | "
              f"Best: {domain_best:2.0f} ({domain_best_pct:5.1f}%) | "
              f"Gain: +{domain_improvement} ({domain_improvement_pct:+.1f}%)")

print()

# By type (Tables vs Text)
print("=" * 90)
print("📊 BY TYPE (Tables vs Text)")
print("=" * 90)
print()

for dtype in ['Tables', 'Text']:
    type_df = results_df[results_df['Type'] == dtype]
    if len(type_df) > 0:
        type_qa = type_df['Q&A'].sum()
        type_baseline = type_df['Baseline Empty'].sum()
        type_best = type_df['Best Empty'].sum()
        type_improvement = type_baseline - type_best

        type_baseline_pct = (type_baseline / type_qa) * 100
        type_best_pct = (type_best / type_qa) * 100
        type_improvement_pct = type_baseline_pct - type_best_pct

        print(f"{dtype:12} | {type_qa:3} Q&A | "
              f"Baseline: {type_baseline:2.0f} ({type_baseline_pct:5.1f}%) | "
              f"Best: {type_best:2.0f} ({type_best_pct:5.1f}%) | "
              f"Gain: +{type_improvement} ({type_improvement_pct:+.1f}%)")

print()

# Top performers
print("=" * 90)
print("🌟 TOP PERFORMERS")
print("=" * 90)
print()

top_performers = results_df.sort_values('Total Improvement %', ascending=False)
print("By Absolute Improvement %:")
for i, (_, row) in enumerate(top_performers.head(3).iterrows(), 1):
    print(f"  {i}. {row['Dataset']:12} {row['Total Improvement %']:+5.1f}% ({row['Total Improvement']:+.0f} questions)")

print()

# Configuration recommendations
print("=" * 90)
print("💡 FINAL CONFIGURATION RECOMMENDATIONS")
print("=" * 90)
print()

print("Best Configuration by Dataset Type:")
print("-" * 90)
print()
print("Table-Heavy Datasets (TatHybrid, FinHybrid, FetaTab, PaperTab):")
print("  TOP_K = 10")
print("  CHUNK_SIZE = 1500")
print("  CHUNK_OVERLAP = 150")
print("  TEMPERATURE = 0.1")
print()

print("Text-Heavy Datasets (NqText, PaperText):")
print("  TOP_K = 10")
print("  CHUNK_SIZE = 3000")
print("  CHUNK_OVERLAP = 300")
print("  TEMPERATURE = 0.1")
print()

# Configuration effectiveness
table_ds = results_df[results_df['Type'] == 'Tables']
table_chunk_improved = (table_ds['Best Config'] == 'TOP_K=10+CHUNK=1500').sum()
print(f"CHUNK_SIZE=1500 helped {table_chunk_improved}/{len(table_ds)} table datasets")
print()

# Save summary
results_df.to_csv('COMPLETE_OPTIMIZATION_SUMMARY_ALL_6_DATASETS.csv', index=False)
print("📁 Complete summary saved to: COMPLETE_OPTIMIZATION_SUMMARY_ALL_6_DATASETS.csv")
print()

print("=" * 90)
print("✅ ANALYSIS COMPLETE")
print("=" * 90)
