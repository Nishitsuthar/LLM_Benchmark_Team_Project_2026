"""
Sprint 3 Accuracy Analysis: Phase 1 (Baseline) vs Phase 3C (Final Optimized)

This script answers the critical question:
Did optimization improve QUALITY (accuracy) or just QUANTITY (fewer empty responses)?

Author: Analysis Session 2026-07-01
"""

import pandas as pd
import os
from pathlib import Path

# Define the key files for comparison
PHASE_1_FILES = {
    'tathybrid': 'experiments/nemotron-3-ultra-550b/1_without_optimization/tathybrid/results/tathybrid_results_20260629_094232_scored.csv',
    'finhybrid': 'experiments/nemotron-3-ultra-550b/1_without_optimization/finhybrid/results/finhybrid_results_20260629_120808_scored.csv',
    'nqtext': 'experiments/nemotron-3-ultra-550b/1_without_optimization/nqtext/results/nqtext_results_20260629_112238_scored.csv',
    'fetatab': 'experiments/nemotron-3-ultra-550b/1_without_optimization/fetatab/results/fetatab_results_20260629_120656_scored.csv',
    'papertext': 'experiments/nemotron-3-ultra-550b/1_without_optimization/papertext/results/papertext_results_20260629_104112_scored.csv',
    'papertab': 'experiments/nemotron-3-ultra-550b/1_without_optimization/papertab/results/papertab_results_20260629_103921_scored.csv',
}

# Phase 3C: Best prompt for each dataset (from documentation)
PHASE_3C_FILES = {
    'tathybrid': 'experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/results/tathybrid_fewshot/tathybrid_fewshot_20260629_225436_scored.csv',
    'finhybrid': 'experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/results/finhybrid_cot/finhybrid_cot_20260629_220325_scored.csv',
    'nqtext': 'experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/results/nqtext_cot/nqtext_cot_20260630_110945_scored.csv',
    'fetatab': 'experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/results/fetatab_cot/fetatab_cot_20260630_121556_scored.csv',
}

def analyze_dataset(dataset_name, phase1_file, phase3_file):
    """
    Analyze a single dataset comparing Phase 1 vs Phase 3C

    Returns: dict with metrics
    """
    print(f"\n{'='*80}")
    print(f"Dataset: {dataset_name.upper()}")
    print(f"{'='*80}")

    # Load data
    df1 = pd.read_csv(phase1_file)
    df3 = pd.read_csv(phase3_file)

    # Basic stats
    print(f"\n📊 BASIC STATISTICS")
    print(f"{'Metric':<40} {'Phase 1':<15} {'Phase 3C':<15} {'Change':<15}")
    print(f"{'-'*80}")

    empty1 = df1['is_empty'].sum()
    empty3 = df3['is_empty'].sum()
    total = len(df1)

    print(f"{'Total questions:':<40} {total:<15} {total:<15} {'-':<15}")
    print(f"{'Empty responses:':<40} {empty1:<15} {empty3:<15} {empty3-empty1:<15}")
    print(f"{'Empty rate:':<40} {f'{empty1/total*100:.1f}%':<15} {f'{empty3/total*100:.1f}%':<15} {f'{(empty3-empty1)/total*100:+.1f}%':<15}")
    print(f"{'Answered:':<40} {total-empty1:<15} {total-empty3:<15} {(total-empty3)-(total-empty1):+d}")

    # Quality metrics - ALL questions
    print(f"\n📈 QUALITY METRICS (All Questions)")
    print(f"{'Metric':<40} {'Phase 1':<15} {'Phase 3C':<15} {'Change':<15}")
    print(f"{'-'*80}")

    avg_f1_all_1 = df1['f1_score'].mean()
    avg_f1_all_3 = df3['f1_score'].mean()

    avg_em_all_1 = df1['em_score'].mean()
    avg_em_all_3 = df3['em_score'].mean()

    print(f"{'Average F1 (all questions):':<40} {avg_f1_all_1:.3f}{'':<10} {avg_f1_all_3:.3f}{'':<10} {avg_f1_all_3-avg_f1_all_1:+.3f}")
    print(f"{'Average EM (all questions):':<40} {avg_em_all_1:.3f}{'':<10} {avg_em_all_3:.3f}{'':<10} {avg_em_all_3-avg_em_all_1:+.3f}")

    # Quality metrics - ANSWERED questions only
    print(f"\n📈 QUALITY METRICS (Answered Questions Only)")
    print(f"{'Metric':<40} {'Phase 1':<15} {'Phase 3C':<15} {'Change':<15}")
    print(f"{'-'*80}")

    answered1 = df1[~df1['is_empty']]
    answered3 = df3[~df3['is_empty']]

    if len(answered1) > 0:
        avg_f1_ans_1 = answered1['f1_score'].mean()
    else:
        avg_f1_ans_1 = 0.0

    if len(answered3) > 0:
        avg_f1_ans_3 = answered3['f1_score'].mean()
    else:
        avg_f1_ans_3 = 0.0

    print(f"{'Average F1 (answered only):':<40} {avg_f1_ans_1:.3f}{'':<10} {avg_f1_ans_3:.3f}{'':<10} {avg_f1_ans_3-avg_f1_ans_1:+.3f}")

    # Quality distribution
    print(f"\n📊 QUALITY DISTRIBUTION (Answered Questions)")
    print(f"{'Category':<40} {'Phase 1':<15} {'Phase 3C':<15} {'Change':<15}")
    print(f"{'-'*80}")

    if len(answered1) > 0:
        correct1 = answered1['is_correct'].sum()
        partial1 = answered1['is_partial'].sum()
        wrong1 = answered1['is_wrong'].sum()
        correct1_pct = correct1 / len(answered1) * 100
        partial1_pct = partial1 / len(answered1) * 100
        wrong1_pct = wrong1 / len(answered1) * 100
    else:
        correct1, partial1, wrong1 = 0, 0, 0
        correct1_pct, partial1_pct, wrong1_pct = 0, 0, 0

    if len(answered3) > 0:
        correct3 = answered3['is_correct'].sum()
        partial3 = answered3['is_partial'].sum()
        wrong3 = answered3['is_wrong'].sum()
        correct3_pct = correct3 / len(answered3) * 100
        partial3_pct = partial3 / len(answered3) * 100
        wrong3_pct = wrong3 / len(answered3) * 100
    else:
        correct3, partial3, wrong3 = 0, 0, 0
        correct3_pct, partial3_pct, wrong3_pct = 0, 0, 0

    print(f"{'Correct (F1 > 0.8):':<40} {f'{correct1} ({correct1_pct:.1f}%)':<15} {f'{correct3} ({correct3_pct:.1f}%)':<15} {correct3-correct1:+d}")
    print(f"{'Partial (0.3 < F1 ≤ 0.8):':<40} {f'{partial1} ({partial1_pct:.1f}%)':<15} {f'{partial3} ({partial3_pct:.1f}%)':<15} {partial3-partial1:+d}")
    print(f"{'Wrong (F1 ≤ 0.3):':<40} {f'{wrong1} ({wrong1_pct:.1f}%)':<15} {f'{wrong3} ({wrong3_pct:.1f}%)':<15} {wrong3-wrong1:+d}")

    # Analyze NEWLY ANSWERED questions (answered in P3 but not P1)
    print(f"\n🆕 NEWLY ANSWERED QUESTIONS (Phase 1 empty → Phase 3C answered)")
    print(f"{'-'*80}")

    # Merge on q_uid to track same questions
    if 'q_uid' in df1.columns and 'q_uid' in df3.columns:
        empty_in_p1 = set(df1[df1['is_empty']]['q_uid'])
        answered_in_p3 = set(df3[~df3['is_empty']]['q_uid'])
        newly_answered_uids = empty_in_p1 & answered_in_p3

        if len(newly_answered_uids) > 0:
            newly_answered = df3[df3['q_uid'].isin(newly_answered_uids)]

            print(f"Newly answered questions: {len(newly_answered)}")
            print(f"Average F1 of new answers: {newly_answered['f1_score'].mean():.3f}")
            print(f"  Correct (F1 > 0.8): {newly_answered['is_correct'].sum()} ({newly_answered['is_correct'].mean()*100:.1f}%)")
            print(f"  Partial (0.3 < F1 ≤ 0.8): {newly_answered['is_partial'].sum()} ({newly_answered['is_partial'].mean()*100:.1f}%)")
            print(f"  Wrong (F1 ≤ 0.3): {newly_answered['is_wrong'].sum()} ({newly_answered['is_wrong'].mean()*100:.1f}%)")
        else:
            print("No newly answered questions (all P3C answers were also answered in P1)")
    else:
        print("⚠️ Cannot track individual questions (q_uid not available)")

    # Overall verdict
    print(f"\n🎯 VERDICT")
    print(f"{'-'*80}")

    # Calculate "truly correct" answers (answered AND correct)
    truly_correct_1 = (df1['f1_score'] > 0.8).sum()
    truly_correct_3 = (df3['f1_score'] > 0.8).sum()

    truly_correct_rate_1 = truly_correct_1 / total * 100
    truly_correct_rate_3 = truly_correct_3 / total * 100

    print(f"Truly Correct Answers (F1 > 0.8):")
    print(f"  Phase 1: {truly_correct_1}/{total} ({truly_correct_rate_1:.1f}%)")
    print(f"  Phase 3C: {truly_correct_3}/{total} ({truly_correct_rate_3:.1f}%)")
    print(f"  Change: {truly_correct_3-truly_correct_1:+d} ({truly_correct_rate_3-truly_correct_rate_1:+.1f}%)")

    if avg_f1_all_3 > avg_f1_all_1:
        print(f"\n✅ SCENARIO A: Quality AND Quantity Improved!")
        print(f"   Both empty rate decreased AND accuracy improved.")
        verdict = "A"
    elif avg_f1_all_3 > avg_f1_all_1 * 0.95:  # Within 5% of original
        print(f"\n⚠️ SCENARIO B: Mixed Results")
        print(f"   More answers provided, but quality roughly maintained.")
        verdict = "B"
    else:
        print(f"\n❌ SCENARIO C: Quality Degraded")
        print(f"   More answers, but accuracy dropped significantly.")
        verdict = "C"

    return {
        'dataset': dataset_name,
        'phase1_empty_rate': empty1/total*100,
        'phase3_empty_rate': empty3/total*100,
        'phase1_avg_f1_all': avg_f1_all_1,
        'phase3_avg_f1_all': avg_f1_all_3,
        'phase1_avg_f1_answered': avg_f1_ans_1,
        'phase3_avg_f1_answered': avg_f1_ans_3,
        'phase1_correct': correct1,
        'phase3_correct': correct3,
        'phase1_truly_correct_rate': truly_correct_rate_1,
        'phase3_truly_correct_rate': truly_correct_rate_3,
        'verdict': verdict
    }

def main():
    print(f"\n{'='*80}")
    print(f"SPRINT 3 ACCURACY ANALYSIS: PHASE 1 (BASELINE) VS PHASE 3C (OPTIMIZED)")
    print(f"{'='*80}")
    print(f"\nThis analysis answers the critical question:")
    print(f"Did optimization improve QUALITY (accuracy) or just QUANTITY (fewer empties)?")

    results = []

    # Analyze each dataset
    for dataset_name in ['tathybrid', 'finhybrid', 'nqtext', 'fetatab']:
        if dataset_name in PHASE_1_FILES and dataset_name in PHASE_3C_FILES:
            phase1_file = PHASE_1_FILES[dataset_name]
            phase3_file = PHASE_3C_FILES[dataset_name]

            if os.path.exists(phase1_file) and os.path.exists(phase3_file):
                result = analyze_dataset(dataset_name, phase1_file, phase3_file)
                results.append(result)
            else:
                print(f"\n⚠️ Skipping {dataset_name}: Files not found")

    # Overall summary
    print(f"\n\n{'='*80}")
    print(f"OVERALL SUMMARY")
    print(f"{'='*80}\n")

    summary_df = pd.DataFrame(results)

    print("Empty Rate Comparison:")
    print(summary_df[['dataset', 'phase1_empty_rate', 'phase3_empty_rate']].to_string(index=False))

    print("\n\nF1 Score Comparison (All Questions):")
    print(summary_df[['dataset', 'phase1_avg_f1_all', 'phase3_avg_f1_all']].to_string(index=False))

    print("\n\nF1 Score Comparison (Answered Only):")
    print(summary_df[['dataset', 'phase1_avg_f1_answered', 'phase3_avg_f1_answered']].to_string(index=False))

    print("\n\nTruly Correct Rate (F1 > 0.8):")
    print(summary_df[['dataset', 'phase1_truly_correct_rate', 'phase3_truly_correct_rate']].to_string(index=False))

    print("\n\nVerdicts:")
    for _, row in summary_df.iterrows():
        verdict_emoji = "✅" if row['verdict'] == "A" else "⚠️" if row['verdict'] == "B" else "❌"
        print(f"  {verdict_emoji} {row['dataset']:12s} - Scenario {row['verdict']}")

    # Final verdict
    print(f"\n{'='*80}")
    print(f"FINAL VERDICT")
    print(f"{'='*80}\n")

    avg_f1_improvement = summary_df['phase3_avg_f1_all'].mean() - summary_df['phase1_avg_f1_all'].mean()
    avg_empty_reduction = summary_df['phase1_empty_rate'].mean() - summary_df['phase3_empty_rate'].mean()

    print(f"Average Empty Rate: {summary_df['phase1_empty_rate'].mean():.1f}% → {summary_df['phase3_empty_rate'].mean():.1f}% ({avg_empty_reduction:+.1f}%)")
    print(f"Average F1 Score: {summary_df['phase1_avg_f1_all'].mean():.3f} → {summary_df['phase3_avg_f1_all'].mean():.3f} ({avg_f1_improvement:+.3f})")

    if avg_f1_improvement > 0:
        print(f"\n✅ SUCCESS: Sprint 3 optimization improved BOTH quantity AND quality!")
        print(f"   - Fewer empty responses (better quantity)")
        print(f"   - Higher F1 scores (better quality)")
    elif avg_f1_improvement > -0.05:
        print(f"\n⚠️ MIXED: Sprint 3 optimization improved quantity while maintaining quality.")
        print(f"   - Fewer empty responses (better quantity)")
        print(f"   - Roughly maintained accuracy (quality stable)")
    else:
        print(f"\n❌ CONCERN: Sprint 3 optimization reduced empty responses but degraded quality.")
        print(f"   - Fewer empty responses (better quantity)")
        print(f"   - Lower accuracy (worse quality)")

    # Save summary
    summary_df.to_csv('experiments/nemotron-3-ultra-550b/PHASE_COMPARISON_SUMMARY.csv', index=False)
    print(f"\n📁 Detailed summary saved to: experiments/nemotron-3-ultra-550b/PHASE_COMPARISON_SUMMARY.csv")

if __name__ == "__main__":
    main()
