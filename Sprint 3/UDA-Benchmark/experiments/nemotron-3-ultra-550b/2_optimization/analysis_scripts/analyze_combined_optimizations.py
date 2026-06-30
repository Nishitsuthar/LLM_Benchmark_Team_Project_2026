#!/usr/bin/env python3
"""
Analyze combined optimization results vs TOP_K=10 baseline
Compare CHUNK_SIZE and TEMPERATURE optimizations
"""

import pandas as pd
import os

print("=" * 80)
print("📊 COMBINED OPTIMIZATION RESULTS ANALYSIS")
print("=" * 80)
print()

# Paths
baseline_dir = "results"

# Define comparisons
comparisons = [
    {
        "name": "TatHybrid",
        "dataset": "tathybrid",
        "qa_count": 162,
        "experiments": [
            {
                "label": "Baseline (TOP_K=5)",
                "path": "../1_without_optimization/tathybrid/results/tathybrid_results_20260629_094232.csv",
                "config": "TOP_K=5, CHUNK=3000"
            },
            {
                "label": "TOP_K=10 only",
                "path": "results/tathybrid_topk10/tathybrid_results_20260629_155316.csv",
                "config": "TOP_K=10, CHUNK=3000"
            },
            {
                "label": "TOP_K=10 + CHUNK=1500",
                "path": "results/tathybrid_topk10_chunk1500/tathybrid_results_20260629_164938.csv",
                "config": "TOP_K=10, CHUNK=1500"
            }
        ]
    },
    {
        "name": "FinHybrid",
        "dataset": "finhybrid",
        "qa_count": 47,
        "experiments": [
            {
                "label": "Baseline (TOP_K=5)",
                "path": "../1_without_optimization/finhybrid/results/finhybrid_results_20260629_120808.csv",
                "config": "TOP_K=5, CHUNK=3000"
            },
            {
                "label": "TOP_K=10 only",
                "path": "results/finhybrid_topk10/finhybrid_results_20260629_152848.csv",
                "config": "TOP_K=10, CHUNK=3000"
            },
            {
                "label": "TOP_K=10 + CHUNK=1500",
                "path": "results/finhybrid_topk10_chunk1500/finhybrid_results_20260629_170526.csv",
                "config": "TOP_K=10, CHUNK=1500"
            },
            {
                "label": "TOP_K=10 + TEMP=0.3",
                "path": "results/finhybrid_topk10_temp03/finhybrid_results_20260629_170936.csv",
                "config": "TOP_K=10, TEMP=0.3"
            }
        ]
    }
]

# Analyze each dataset
all_results = []

for comp in comparisons:
    print(f"{'='*80}")
    print(f"Dataset: {comp['name']} ({comp['qa_count']} Q&A)")
    print(f"{'='*80}")
    print()

    dataset_results = []

    for exp in comp['experiments']:
        # Load results
        df = pd.read_csv(exp['path'])

        # Count empty responses
        empty_count = (df['response'].isna() | (df['response'].str.strip() == '')).sum()
        empty_pct = (empty_count / comp['qa_count']) * 100
        answered = comp['qa_count'] - empty_count
        answered_pct = (answered / comp['qa_count']) * 100

        result = {
            'Dataset': comp['name'],
            'Configuration': exp['label'],
            'Config Details': exp['config'],
            'Total Q&A': comp['qa_count'],
            'Empty': empty_count,
            'Empty %': empty_pct,
            'Answered': answered,
            'Answered %': answered_pct
        }

        dataset_results.append(result)
        all_results.append(result)

    # Print table for this dataset
    print(f"{'Configuration':<30} {'Empty':<15} {'Answered':<15}")
    print("-" * 60)

    baseline_empty = dataset_results[0]['Empty']

    for result in dataset_results:
        empty_str = f"{result['Empty']} ({result['Empty %']:.1f}%)"
        answered_str = f"{result['Answered']} ({result['Answered %']:.1f}%)"

        # Calculate improvement vs baseline
        improvement = baseline_empty - result['Empty']
        if improvement > 0:
            status = f"+{improvement} ✅"
        elif improvement < 0:
            status = f"{improvement} ⚠️"
        else:
            status = "±0"

        print(f"{result['Configuration']:<30} {empty_str:<15} {answered_str:<15} {status}")

    print()

    # Calculate incremental improvements
    print("Incremental Improvements:")
    print("-" * 60)

    for i in range(1, len(dataset_results)):
        prev = dataset_results[i-1]
        curr = dataset_results[i]

        improvement = prev['Empty'] - curr['Empty']
        improvement_pct = prev['Empty %'] - curr['Empty %']

        if improvement > 0:
            status = "✅ IMPROVEMENT"
        elif improvement < 0:
            status = "⚠️ WORSE"
        else:
            status = "➖ SAME"

        print(f"{prev['Configuration']} → {curr['Configuration']}")
        print(f"  Change: {improvement:+d} questions ({improvement_pct:+.1f}%) {status}")
        print()

    print()

# Overall summary
print("=" * 80)
print("📈 OVERALL SUMMARY")
print("=" * 80)
print()

# Summarize by optimization type
print("CHUNK_SIZE=1500 Impact (vs TOP_K=10 baseline):")
print("-" * 60)

tathybrid_topk10 = next(r for r in all_results if r['Dataset'] == 'TatHybrid' and r['Configuration'] == 'TOP_K=10 only')
tathybrid_chunk = next(r for r in all_results if r['Dataset'] == 'TatHybrid' and 'CHUNK=1500' in r['Configuration'])
tat_improvement = tathybrid_topk10['Empty'] - tathybrid_chunk['Empty']
tat_improvement_pct = tathybrid_topk10['Empty %'] - tathybrid_chunk['Empty %']
print(f"TatHybrid:  {tat_improvement:+2d} questions ({tat_improvement_pct:+.1f}%)")

finhybrid_topk10 = next(r for r in all_results if r['Dataset'] == 'FinHybrid' and r['Configuration'] == 'TOP_K=10 only')
finhybrid_chunk = next(r for r in all_results if r['Dataset'] == 'FinHybrid' and 'CHUNK=1500' in r['Configuration'])
fin_chunk_improvement = finhybrid_topk10['Empty'] - finhybrid_chunk['Empty']
fin_chunk_improvement_pct = finhybrid_topk10['Empty %'] - finhybrid_chunk['Empty %']
print(f"FinHybrid:  {fin_chunk_improvement:+2d} questions ({fin_chunk_improvement_pct:+.1f}%)")

total_chunk_improvement = tat_improvement + fin_chunk_improvement
print(f"Total:      {total_chunk_improvement:+2d} questions")
print()

print("TEMPERATURE=0.3 Impact (vs TOP_K=10 baseline):")
print("-" * 60)

finhybrid_temp = next(r for r in all_results if r['Dataset'] == 'FinHybrid' and 'TEMP=0.3' in r['Configuration'])
fin_temp_improvement = finhybrid_topk10['Empty'] - finhybrid_temp['Empty']
fin_temp_improvement_pct = finhybrid_topk10['Empty %'] - finhybrid_temp['Empty %']
print(f"FinHybrid:  {fin_temp_improvement:+2d} questions ({fin_temp_improvement_pct:+.1f}%)")
print()

# Compare which optimization works better for FinHybrid
print("FinHybrid: Which optimization works better?")
print("-" * 60)
if fin_chunk_improvement > fin_temp_improvement:
    print(f"✅ CHUNK_SIZE=1500 wins: {fin_chunk_improvement:+d} vs {fin_temp_improvement:+d} questions")
    winner = "CHUNK_SIZE=1500"
elif fin_temp_improvement > fin_chunk_improvement:
    print(f"✅ TEMPERATURE=0.3 wins: {fin_temp_improvement:+d} vs {fin_chunk_improvement:+d} questions")
    winner = "TEMPERATURE=0.3"
else:
    print(f"➖ TIE: Both improved by {fin_chunk_improvement} questions")
    winner = "TIE"
print()

# Cumulative improvements from baseline
print("=" * 80)
print("🎯 CUMULATIVE IMPROVEMENTS (from original baseline)")
print("=" * 80)
print()

for comp in comparisons:
    baseline = next(r for r in all_results if r['Dataset'] == comp['name'] and 'Baseline' in r['Configuration'])
    best = min([r for r in all_results if r['Dataset'] == comp['name']], key=lambda x: x['Empty'])

    total_improvement = baseline['Empty'] - best['Empty']
    total_improvement_pct = baseline['Empty %'] - best['Empty %']

    print(f"{comp['name']}:")
    print(f"  Baseline:       {baseline['Empty']} empty ({baseline['Empty %']:.1f}%)")
    print(f"  Best Config:    {best['Empty']} empty ({best['Empty %']:.1f}%)")
    print(f"  Configuration:  {best['Configuration']}")
    print(f"  Total Gain:     {total_improvement:+d} questions ({total_improvement_pct:+.1f}%) ✅")
    print()

# Grand total
total_baseline_empty = sum(r['Empty'] for r in all_results if 'Baseline' in r['Configuration'])
total_best_empty = sum(min([r for r in all_results if r['Dataset'] == comp['name']], key=lambda x: x['Empty'])['Empty'] for comp in comparisons)
total_qa = sum(comp['qa_count'] for comp in comparisons)

grand_improvement = total_baseline_empty - total_best_empty
grand_improvement_pct = (total_baseline_empty / total_qa * 100) - (total_best_empty / total_qa * 100)

print("=" * 80)
print(f"GRAND TOTAL (TatHybrid + FinHybrid only):")
print(f"  Baseline Empty:     {total_baseline_empty} ({total_baseline_empty/total_qa*100:.1f}%)")
print(f"  Best Config Empty:  {total_best_empty} ({total_best_empty/total_qa*100:.1f}%)")
print(f"  Total Improvement:  {grand_improvement:+d} questions ({grand_improvement_pct:+.1f}%) ✅✅")
print("=" * 80)
print()

# Recommendations
print("=" * 80)
print("💡 RECOMMENDATIONS")
print("=" * 80)
print()

print("Best Configuration per Dataset:")
print("-" * 60)
for comp in comparisons:
    best = min([r for r in all_results if r['Dataset'] == comp['name']], key=lambda x: x['Empty'])
    print(f"{comp['name']:12} → {best['Configuration']}")
    print(f"               {best['Config Details']}")
    print()

print("General Recommendations:")
print("-" * 60)
if total_chunk_improvement > 0:
    print(f"✅ CHUNK_SIZE=1500 helps table-heavy datasets (+{total_chunk_improvement} questions)")
    print("   → Recommend for: TatHybrid, FinHybrid, FetaTab, PaperTab")
else:
    print(f"➖ CHUNK_SIZE=1500 had no clear benefit")

print()

if fin_temp_improvement > 0:
    print(f"✅ TEMPERATURE=0.3 reduces empty responses (+{fin_temp_improvement} questions)")
    print("   → Recommend for: Datasets with high empty rate (>35%)")
else:
    print(f"➖ TEMPERATURE=0.3 had no clear benefit")

print()
print("Optimal Configuration Matrix:")
print("-" * 60)
print("Table-heavy datasets:      TOP_K=10 + CHUNK_SIZE=1500")
print("High empty rate datasets:  TOP_K=10 + TEMPERATURE=0.3")
print("Text-heavy datasets:       TOP_K=10 + CHUNK_SIZE=3000")
print()

# Save summary
summary_df = pd.DataFrame(all_results)
summary_df.to_csv('COMBINED_OPTIMIZATION_SUMMARY.csv', index=False)
print("📁 Summary saved to: COMBINED_OPTIMIZATION_SUMMARY.csv")
print()

print("=" * 80)
print("✅ ANALYSIS COMPLETE")
print("=" * 80)
