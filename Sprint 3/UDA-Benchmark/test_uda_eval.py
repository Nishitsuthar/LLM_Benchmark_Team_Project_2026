"""
Test UDA Authors' Evaluation Method vs Our Scoring Script

This script runs the EXACT evaluation method used by UDA authors
on a sample CSV to verify if our scoring is correct.
"""

import pandas as pd
import json
import sys
sys.path.append('.')

from uda.eval.my_eval import eval_main

# Test on Phase 1 TatHybrid
print("="*80)
print("TESTING UDA AUTHORS' EVALUATION METHOD")
print("="*80)

# Load CSV
csv_path = 'experiments/nemotron-3-ultra-550b/1_without_optimization/tathybrid/results/tathybrid_results_20260629_094232.csv'
df = pd.read_csv(csv_path)

print(f"\nLoaded {len(df)} questions from TatHybrid Phase 1")
print(f"Empty responses: {df['response'].isna().sum()}")
print(f"Answered: {(~df['response'].isna()).sum()}")

# Convert to format expected by eval_main
data_list = []
for idx, row in df.iterrows():
    # Convert CSV row to the format expected by UDA eval
    item = {
        'question': row['question'],
        'response': row['response'] if pd.notna(row['response']) else None,
        'doc': row['doc'],
        'q_uid': row['q_uid'],
        'answers': eval(row['answers']),  # Convert string to dict
        'dataset': row['dataset']
    }
    data_list.append(item)

print("\n" + "="*80)
print("RUNNING UDA AUTHORS' OFFICIAL EVAL_MAIN() FUNCTION")
print("="*80)
eval_main('tat', data_list, CODE_GEN=False)

print("\n" + "="*80)
print("NOW TESTING OUR SCORED CSV RESULTS")
print("="*80)

# Load our scored version
scored_csv_path = 'experiments/nemotron-3-ultra-550b/1_without_optimization/tathybrid/results/tathybrid_results_20260629_094232_scored.csv'
df_scored = pd.read_csv(scored_csv_path)

answered = df_scored[~df_scored['is_empty']]

print(f"\nOur Scoring Results:")
print(f"  Average F1 (all): {df_scored['f1_score'].mean():.3f}")
print(f"  Average F1 (answered): {answered['f1_score'].mean():.3f}")
print(f"  Average EM (all): {df_scored['em_score'].mean():.3f}")
print(f"  Correct (F1>0.8): {(df_scored['f1_score']>0.8).sum()}")

print("\n" + "="*80)
print("COMPARISON")
print("="*80)
print("\nThe UDA authors' eval_main() prints aggregate F1 score.")
print("Our per-question scoring should match when aggregated.")
print("\nIf the numbers match, our scoring is correct.")
print("If they differ, we have a bug in our evaluation logic.")

# Test FinHybrid
print("\n\n" + "="*80)
print("TESTING FINHYBRID (The problematic 0.0 F1 dataset)")
print("="*80)

csv_path = 'experiments/nemotron-3-ultra-550b/1_without_optimization/finhybrid/results/finhybrid_results_20260629_120808.csv'
df = pd.read_csv(csv_path)

print(f"\nLoaded {len(df)} questions from FinHybrid Phase 1")
print(f"Empty responses: {df['response'].isna().sum()}")
print(f"Answered: {(~df['response'].isna()).sum()}")

# Show a sample answer
sample = df[df['response'].notna()].iloc[0]
print(f"\nSample Question: {sample['question']}")
print(f"Sample Response: {sample['response']}")
print(f"Sample Answer: {sample['answers']}")

# Convert to format expected by eval_main
data_list = []
for idx, row in df.iterrows():
    item = {
        'question': row['question'],
        'response': row['response'] if pd.notna(row['response']) else None,
        'doc': row['doc'],
        'q_uid': row['q_uid'],
        'answers': eval(row['answers']),
        'dataset': row['dataset']
    }
    data_list.append(item)

print("\n" + "="*80)
print("RUNNING UDA AUTHORS' OFFICIAL EVAL_MAIN() FOR FINHYBRID")
print("="*80)
eval_main('fin', data_list, CODE_GEN=False)

# Test our scoring on a single question
print("\n" + "="*80)
print("TESTING OUR EVALUATION ON A SINGLE FINHYBRID QUESTION")
print("="*80)

from uda.eval.utils.fin_eval import get_metrics

sample_response = "The answer is: 4,094 (in thousands)"
sample_pred = sample_response.split("The answer is: ")[-1].strip()
sample_answers = eval("{'str_answer': '380', 'exe_answer': '3.8'}")

print(f"Response: {sample_response}")
print(f"Extracted pred: {sample_pred}")
print(f"Gold exe_answer: {sample_answers['exe_answer']}")
print(f"Gold str_answer: {sample_answers['str_answer']}")

# Try evaluating with exe_answer
try:
    result = get_metrics(sample_pred, sample_answers['exe_answer'])
    print(f"\nget_metrics(pred, exe_answer) returned: {result}")
    print(f"Type: {type(result)}")
except Exception as e:
    print(f"\nget_metrics(pred, exe_answer) raised error: {e}")

# Try evaluating with str_answer
try:
    result = get_metrics(sample_pred, sample_answers['str_answer'])
    print(f"\nget_metrics(pred, str_answer) returned: {result}")
    print(f"Type: {type(result)}")
except Exception as e:
    print(f"\nget_metrics(pred, str_answer) raised error: {e}")

print("\n" + "="*80)
print("DIAGNOSIS")
print("="*80)
print("\nThe issue is likely that fin_eval.get_metrics() returns:")
print("  - Single value (0 or 1.0) for exact match")
print("  - Does NOT return a tuple (em, f1)")
print("\nOur script expected a tuple (em, f1) but got a single value.")
print("This caused the 'cannot unpack non-iterable' error.")
