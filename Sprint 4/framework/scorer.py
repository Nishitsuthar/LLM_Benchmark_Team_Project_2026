"""
Sprint 4 Scorer

Thin wrapper around Sprint 3's UDA eval code.
Takes a results CSV (output of RAGRunner.run()) and computes the appropriate metric.

Usage:
    from framework.scorer import score_results
    score_results("results/tathybrid_nemotron-550b_simple_20260708_120000.csv",
                  dataset="tathybrid")
"""

import os
import sys
import pandas as pd

# Make Sprint 3 eval code importable
_S3_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__),
                 "../../Sprint 3/UDA-Benchmark")
)
if _S3_ROOT not in sys.path:
    sys.path.insert(0, _S3_ROOT)

from uda.eval.my_eval import eval_main
from framework.config import DATASET_UDA_NAMES, DATASET_METRICS


def _build_eval_records(dataset: str, df: pd.DataFrame) -> list:
    """
    Convert results DataFrame rows into the dict format expected by eval_main().
    eval_main expects: [{"response": str, "answers": <dataset-specific>, "q_uid": str, ...}]
    """
    from ast import literal_eval

    records = []
    for _, row in df.iterrows():
        answers_raw = row.get("ground_truth", row.get("answers", ""))

        # Parse answers back from string if needed (CSV serialises dicts as strings)
        if isinstance(answers_raw, str):
            try:
                answers_raw = literal_eval(answers_raw)
            except Exception:
                pass  # leave as string; eval_main handles plain strings for some datasets

        records.append({
            "response": str(row.get("response", "")),
            "answers": answers_raw,
            "q_uid": str(row.get("question_id", row.get("q_uid", ""))),
            "doc": str(row.get("doc_name", row.get("doc", ""))),
            "question": str(row.get("question", "")),
        })
    return records


def score_results(results_csv: str, dataset: str, save: bool = True) -> dict:
    """
    Compute the dataset-appropriate metric for a results CSV.

    Args:
        results_csv: Path to the output CSV from RAGRunner.run()
        dataset:     Sprint 4 dataset key (e.g. "tathybrid", "finhybrid")
        save:        If True, writes a _scored.csv alongside the input file

    Returns:
        Dict with metric name and value, plus empty-response statistics
    """
    df = pd.read_csv(results_csv)
    uda_name = DATASET_UDA_NAMES[dataset]
    metric = DATASET_METRICS[dataset]

    # Empty response stats
    empty_mask = df["response"].fillna("").str.strip() == ""
    empty_count = int(empty_mask.sum())
    total = len(df)

    print(f"\n{'='*60}")
    print(f"Dataset:  {dataset}  ({uda_name})")
    print(f"Metric:   {metric}")
    print(f"Total:    {total}")
    print(f"Empty:    {empty_count} ({empty_count/total*100:.1f}%)")
    print(f"{'='*60}")

    records = _build_eval_records(dataset, df)

    # eval_main prints the score and returns it
    eval_main(uda_name, records)

    # Save per-question scores if requested
    if save:
        out_path = results_csv.replace(".csv", "_scored.csv")
        df["is_empty"] = empty_mask
        df.to_csv(out_path, index=False)
        print(f"Scored CSV → {out_path}")

    return {"metric": metric, "empty_count": empty_count, "total": total}


def score_all(results_dir: str = None) -> pd.DataFrame:
    """
    Score all un-scored CSVs in the results directory.

    Returns a summary DataFrame with one row per experiment.
    """
    if results_dir is None:
        results_dir = os.path.join(os.path.dirname(__file__), "../results")

    rows = []
    for fname in sorted(os.listdir(results_dir)):
        if not fname.endswith(".csv") or "_scored" in fname:
            continue

        parts = fname.replace(".csv", "").split("_")
        # Expected naming: {dataset}_{model}_{prompt}_{timestamp}.csv
        # At minimum 4 parts
        if len(parts) < 4:
            continue

        dataset = parts[0]
        model = parts[1]
        prompt = parts[2]

        if dataset not in DATASET_UDA_NAMES:
            print(f"  Skipping unknown dataset: {fname}")
            continue

        print(f"\nScoring: {fname}")
        path = os.path.join(results_dir, fname)
        info = score_results(path, dataset)
        info.update({"file": fname, "dataset": dataset, "model": model, "prompt": prompt})
        rows.append(info)

    return pd.DataFrame(rows)
