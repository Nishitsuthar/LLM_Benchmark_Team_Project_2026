"""
Retroactively Add Per-Question Scores to Sprint 3 Result CSVs

This script uses the UDA authors' evaluation methods to calculate
F1/EM scores for each question in your result CSVs.

Author: Sprint 3 Analysis
Date: 2026-07-01
"""

import pandas as pd
import json
import sys
import os
from pathlib import Path

# Add UDA code to path
sys.path.append(str(Path(__file__).parent.parent))

# Import UDA evaluation modules
from uda.eval.utils.tat_eval import get_metrics as tat_get_metrics
from uda.eval.utils.fin_eval import get_metrics as fin_get_metrics, extract_gold_answers
from uda.eval.utils.basic_utils import token_f1_score

# Dataset-specific evaluation functions
def evaluate_tat_question(response_text, ground_truth_dict):
    """
    Evaluate TatHybrid question (Numeracy F1 score)

    Args:
        response_text: Model's response (e.g., "The answer is: 1,737.5")
        ground_truth_dict: Ground truth from CSV (e.g., {'answer': ['1737.5'], ...})

    Returns:
        (exact_match, f1_score) tuple
    """
    # Handle empty/NaN responses
    if pd.isna(response_text) or not str(response_text).strip():
        return 0.0, 0.0

    response_text = str(response_text)

    # Extract answer from "The answer is: XXX" format
    pred = response_text.split("The answer is: ")[-1].strip()

    # Get ground truth answers
    if isinstance(ground_truth_dict, str):
        try:
            ground_truth_dict = eval(ground_truth_dict)
        except:
            return 0.0, 0.0

    gold = ground_truth_dict.get('answer', [])
    if not gold:
        return 0.0, 0.0

    # Calculate metrics using UDA's TatQA evaluation
    try:
        em, f1 = tat_get_metrics(pred, gold)
        return em, f1
    except Exception as e:
        print(f"Error evaluating TatQA: {e}")
        print(f"  Pred: {pred}")
        print(f"  Gold: {gold}")
        return 0.0, 0.0


def evaluate_fin_question(response_text, ground_truth_dict):
    """
    Evaluate FinHybrid question (Exact Match ±1%)

    Args:
        response_text: Model's response
        ground_truth_dict: Ground truth from CSV

    Returns:
        (exact_match, f1_score) tuple
    """
    # Handle empty/NaN responses
    if pd.isna(response_text) or not str(response_text).strip():
        return 0.0, 0.0

    response_text = str(response_text)

    # Extract answer
    pred = response_text.split("The answer is: ")[-1].strip()

    # Get ground truth
    if isinstance(ground_truth_dict, str):
        try:
            ground_truth_dict = eval(ground_truth_dict)
        except:
            return 0.0, 0.0

    # FinHybrid uses exe_answer and str_answer
    try:
        gold_exe = ground_truth_dict.get('exe_answer', '')
        gold_str = ground_truth_dict.get('str_answer', '')

        # Try exe_answer first (numerical answer)
        if gold_exe:
            result = fin_get_metrics(pred, gold_exe)
            # Handle case where fin_get_metrics returns single 0 instead of tuple
            if isinstance(result, tuple):
                em, f1 = result
                return em, f1
            else:
                # Single 0 means failed comparison
                pass

        # Try str_answer
        if gold_str:
            result = fin_get_metrics(pred, gold_str)
            if isinstance(result, tuple):
                em, f1 = result
                return em, f1

        return 0.0, 0.0

    except Exception as e:
        print(f"Error evaluating FinQA: {e}")
        return 0.0, 0.0


def evaluate_text_question(response_text, ground_truth_dict):
    """
    Evaluate text-based questions (NqText, FetaTab, PaperText/Tab)
    Uses Span F1 score

    Args:
        response_text: Model's response
        ground_truth_dict: Ground truth from CSV

    Returns:
        (exact_match, f1_score) tuple
    """
    # Handle empty/NaN responses
    if pd.isna(response_text) or not str(response_text).strip():
        return 0.0, 0.0

    response_text = str(response_text)

    # Extract answer
    pred = response_text.split("The answer is: ")[-1].strip()

    # Get ground truth - handle both dict format and list format
    gold = []

    if isinstance(ground_truth_dict, str):
        try:
            # Try to evaluate as Python literal
            ground_truth_dict = eval(ground_truth_dict)
        except:
            # If it fails, treat the string itself as the answer
            gold = [ground_truth_dict]

    # Now extract the answer based on the type
    if isinstance(ground_truth_dict, dict):
        # Check for different answer field names
        if 'answer' in ground_truth_dict:
            # Dictionary format: {'answer': ['...']}
            gold = ground_truth_dict['answer']
        elif 'short_answer' in ground_truth_dict:
            # NqText format: {'short_answer': '...', 'long_answer': '...'}
            gold = [ground_truth_dict['short_answer']]
            # Also add long answer for comparison
            if 'long_answer' in ground_truth_dict:
                gold.append(ground_truth_dict['long_answer'])
        else:
            # Try to get any value that looks like an answer
            gold = list(ground_truth_dict.values())

        if not isinstance(gold, list):
            gold = [gold]
    elif isinstance(ground_truth_dict, list):
        # Already a list of answers
        gold = ground_truth_dict
    else:
        # Single value
        gold = [str(ground_truth_dict)]

    # Remove empty strings
    gold = [str(g).strip() for g in gold if str(g).strip()]

    if not gold:
        return 0.0, 0.0

    # Calculate F1 using basic span overlap
    try:
        # Use UDA's basic F1 evaluation - compare against all gold answers, take max
        max_f1 = 0.0
        for gold_answer in gold:
            f1 = token_f1_score(pred, str(gold_answer))
            max_f1 = max(max_f1, f1)
        em = 1.0 if max_f1 > 0.95 else 0.0  # Consider EM if F1 > 0.95
        return em, max_f1
    except Exception as e:
        print(f"Error evaluating text question: {e}")
        print(f"  Pred: {pred}")
        print(f"  Gold: {gold}")
        return 0.0, 0.0


def add_scores_to_csv(csv_path, dataset_name, output_path=None):
    """
    Add per-question scores to a result CSV

    Args:
        csv_path: Path to result CSV
        dataset_name: 'tat', 'fin', 'nq', 'feta', 'paper_text', 'paper_tab'
        output_path: Optional output path (default: adds '_scored' to filename)

    Returns:
        DataFrame with added score columns
    """
    print(f"\n{'='*60}")
    print(f"Processing: {csv_path}")
    print(f"Dataset: {dataset_name}")
    print(f"{'='*60}")

    # Read CSV
    df = pd.read_csv(csv_path)
    print(f"Total questions: {len(df)}")

    # Choose evaluation function based on dataset
    if dataset_name == 'tat':
        eval_func = evaluate_tat_question
    elif dataset_name == 'fin':
        eval_func = evaluate_fin_question
    else:  # nq, feta, paper_text, paper_tab
        eval_func = evaluate_text_question

    # Calculate scores for each question
    em_scores = []
    f1_scores = []

    for idx, row in df.iterrows():
        response = row['response']
        answers = row['answers']

        em, f1 = eval_func(response, answers)
        em_scores.append(em)
        f1_scores.append(f1)

        # Progress indicator
        if (idx + 1) % 20 == 0:
            print(f"  Processed {idx + 1}/{len(df)} questions...")

    # Add score columns
    df['em_score'] = em_scores
    df['f1_score'] = f1_scores
    df['is_empty'] = df['response'].apply(lambda x: x == '' or pd.isna(x))
    df['is_correct'] = df['f1_score'] > 0.8
    df['is_partial'] = (df['f1_score'] > 0.3) & (df['f1_score'] <= 0.8)
    df['is_wrong'] = (df['f1_score'] > 0) & (df['f1_score'] <= 0.3)

    # Calculate statistics
    print(f"\n{'='*60}")
    print(f"RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"Total questions: {len(df)}")
    print(f"\nAnswer Status:")
    print(f"  Empty: {df['is_empty'].sum()} ({df['is_empty'].mean()*100:.1f}%)")
    print(f"  Answered: {(~df['is_empty']).sum()} ({(~df['is_empty']).mean()*100:.1f}%)")

    print(f"\nQuality Distribution (of answered questions):")
    answered_df = df[~df['is_empty']]
    if len(answered_df) > 0:
        print(f"  Correct (F1 > 0.8): {answered_df['is_correct'].sum()} ({answered_df['is_correct'].mean()*100:.1f}%)")
        print(f"  Partial (0.3 < F1 <= 0.8): {answered_df['is_partial'].sum()} ({answered_df['is_partial'].mean()*100:.1f}%)")
        print(f"  Wrong (F1 <= 0.3): {answered_df['is_wrong'].sum()} ({answered_df['is_wrong'].mean()*100:.1f}%)")

        print(f"\nAccuracy Metrics:")
        print(f"  Average EM (all): {df['em_score'].mean():.3f}")
        print(f"  Average F1 (all): {df['f1_score'].mean():.3f}")
        print(f"  Average F1 (answered only): {answered_df['f1_score'].mean():.3f}")

    # Save to new CSV
    if output_path is None:
        # Add '_scored' before .csv extension
        output_path = csv_path.replace('.csv', '_scored.csv')

    df.to_csv(output_path, index=False)
    print(f"\n✅ Saved scored CSV to: {output_path}")
    print(f"{'='*60}\n")

    return df


def process_all_phase_csvs(experiments_dir, output_dir=None):
    """
    Process all result CSVs across all phases

    Args:
        experiments_dir: Path to experiments/nemotron-3-ultra-550b/
        output_dir: Optional directory for scored CSVs (default: same location)
    """
    experiments_path = Path(experiments_dir)

    # Define dataset name mapping
    dataset_mapping = {
        'tathybrid': 'tat',
        'finhybrid': 'fin',
        'nqtext': 'nq',
        'fetatab': 'feta',
        'papertext': 'paper_text',
        'papertab': 'paper_tab'
    }

    # Find all result CSVs - look in results directories at any depth
    # Pattern matches both:
    # - 1_without_optimization/dataset/results/*.csv
    # - 2_optimization/results/dataset_config/*.csv
    # - 3_advanced_optimization/technique/results/dataset_config/*.csv
    result_csvs = []

    # Find all directories named 'results' at any depth
    for results_dir in experiments_path.glob('**/results'):
        if results_dir.is_dir():
            # Get all CSV files in this results directory and its subdirectories
            result_csvs.extend(results_dir.glob('**/*.csv'))

    # Filter out already-scored CSVs and checkpoint files
    result_csvs = [f for f in result_csvs if '_scored' not in f.name and '.ipynb_checkpoints' not in str(f)]

    # Group by directory and keep only the latest timestamp
    from collections import defaultdict
    csv_by_dir = defaultdict(list)
    for csv_file in result_csvs:
        # Group by parent directory (e.g., tathybrid_topk10_chunk1500)
        dir_key = csv_file.parent
        csv_by_dir[dir_key].append(csv_file)

    # Keep only the latest file from each directory (highest timestamp)
    result_csvs = []
    for dir_key, files in csv_by_dir.items():
        # Sort by filename (which includes timestamp) and take the last one
        latest_file = sorted(files, key=lambda x: x.name)[-1]
        result_csvs.append(latest_file)
        if len(files) > 1:
            print(f"📌 Multiple files in {dir_key.name}, using latest: {latest_file.name}")

    print(f"\n{'='*60}")
    print(f"BATCH PROCESSING: {len(result_csvs)} CSV files found")
    print(f"{'='*60}\n")

    results_summary = []

    for csv_path in result_csvs:
        # Determine dataset from path
        dataset_key = None
        for key in dataset_mapping.keys():
            if key in str(csv_path).lower():
                dataset_key = key
                break

        if dataset_key is None:
            print(f"⚠️  Skipping {csv_path.name} - couldn't determine dataset")
            continue

        dataset_name = dataset_mapping[dataset_key]

        try:
            df = add_scores_to_csv(str(csv_path), dataset_name)

            # Store summary
            results_summary.append({
                'file': csv_path.name,
                'dataset': dataset_name,
                'total': len(df),
                'empty': df['is_empty'].sum(),
                'empty_pct': df['is_empty'].mean() * 100,
                'avg_f1_all': df['f1_score'].mean(),
                'avg_f1_answered': df[~df['is_empty']]['f1_score'].mean() if (~df['is_empty']).sum() > 0 else 0,
                'correct': df['is_correct'].sum(),
                'partial': df['is_partial'].sum(),
                'wrong': df['is_wrong'].sum()
            })
        except Exception as e:
            print(f"❌ Error processing {csv_path.name}: {e}")
            continue

    # Create summary report
    if results_summary:
        summary_df = pd.DataFrame(results_summary)
        summary_path = experiments_path / 'SCORING_SUMMARY.csv'
        summary_df.to_csv(summary_path, index=False)

        print(f"\n{'='*60}")
        print(f"BATCH PROCESSING COMPLETE")
        print(f"{'='*60}")
        print(f"Processed {len(results_summary)} files successfully")
        print(f"Summary saved to: {summary_path}")
        print(f"\nOverall Statistics:")
        print(f"  Total questions: {summary_df['total'].sum()}")
        print(f"  Average empty rate: {summary_df['empty_pct'].mean():.1f}%")
        print(f"  Average F1 (all): {summary_df['avg_f1_all'].mean():.3f}")
        print(f"  Average F1 (answered): {summary_df['avg_f1_answered'].mean():.3f}")
    else:
        print(f"\n{'='*60}")
        print(f"BATCH PROCESSING COMPLETE")
        print(f"{'='*60}")
        print(f"⚠️ No files were processed successfully.")
        summary_df = pd.DataFrame()

    return summary_df


if __name__ == "__main__":
    # Example usage

    # Option 1: Process a single CSV
    # csv_path = "experiments/nemotron-3-ultra-550b/1_without_optimization/tathybrid/results/tathybrid_results_20260629_094232.csv"
    # df = add_scores_to_csv(csv_path, 'tat')

    # Option 2: Process all CSVs
    experiments_dir = "experiments/nemotron-3-ultra-550b"
    summary = process_all_phase_csvs(experiments_dir)

    print("\n✅ All done! Check the '_scored.csv' files for per-question scores.")
