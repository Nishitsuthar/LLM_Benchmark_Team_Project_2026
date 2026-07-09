"""
Task 2 — Stratified evaluation report.

Joins per-question scores against category labels from Task 1 and produces:
  - F1 / EM per category
  - Sample count per category
  - Flags for categories > X% below overall average (default X=10)

Usage:
    python stratified_eval.py \
        --scores   path/to/any_scored.csv \
        --cats     categorization/question_categories.csv \
        --dataset  finhybrid \
        --drop-threshold 10

Output:
    Prints a report table; also saves *_stratified_report.csv next to the scores file.
"""

import argparse
import json
import os
import sys

import pandas as pd

_here    = os.path.dirname(os.path.abspath(__file__))
_sprint4 = os.path.abspath(os.path.join(_here, '..'))
if _sprint4 not in sys.path:
    sys.path.insert(0, _sprint4)


def _load_scores(scores_csv: str) -> pd.DataFrame:
    df = pd.read_csv(scores_csv)
    required = {"q_uid", "f1_score"}
    if not required.issubset(df.columns):
        raise ValueError(f"Scores CSV must have columns: {required}. Found: {list(df.columns)}")
    return df


def _load_categories(cats_csv: str) -> pd.DataFrame:
    df = pd.read_csv(cats_csv)
    # parse reasoning_type back from JSON string if needed
    if "reasoning_type" in df.columns:
        df["reasoning_type"] = df["reasoning_type"].apply(
            lambda x: json.loads(x) if isinstance(x, str) and x.startswith("[") else x
        )
    return df


def _explode_reasoning(df: pd.DataFrame) -> pd.DataFrame:
    """Return one row per (q_uid, reasoning_type_value) for breakdown."""
    rows = []
    for _, r in df.iterrows():
        rt = r["reasoning_type"]
        if isinstance(rt, list):
            for t in rt:
                rows.append({**r.to_dict(), "reasoning_type_single": t})
        else:
            rows.append({**r.to_dict(), "reasoning_type_single": str(rt)})
    return pd.DataFrame(rows)


def stratified_report(
    scores_csv: str,
    cats_csv: str,
    dataset: str = None,
    drop_threshold: float = 10.0,
) -> pd.DataFrame:

    scores = _load_scores(scores_csv)
    cats   = _load_categories(cats_csv)

    if dataset:
        cats = cats[cats["dataset"] == dataset].copy()

    # join on q_uid
    merged = scores.merge(cats[["q_uid", "hop_type", "reasoning_type", "answer_format", "hop_count"]],
                          on="q_uid", how="inner")

    if merged.empty:
        print("WARNING: No matching q_uids between scores and categories. Check dataset filter.")
        return pd.DataFrame()

    overall_f1 = merged["f1_score"].mean()
    overall_em = merged["em_score"].mean() if "em_score" in merged.columns else None
    n_total    = len(merged)

    print(f"\n{'='*60}")
    print(f"STRATIFIED EVALUATION REPORT")
    if dataset:
        print(f"Dataset   : {dataset}")
    print(f"Questions : {n_total}")
    print(f"Overall F1: {overall_f1:.3f}")
    if overall_em is not None:
        print(f"Overall EM: {overall_em:.3f}")
    print(f"Drop flag threshold: >{drop_threshold}% below overall F1")
    print(f"{'='*60}")

    dimension_dfs = []

    def _make_breakdown(group_col: str, label: str):
        grp = merged.groupby(group_col).agg(
            n        = ("f1_score", "count"),
            mean_f1  = ("f1_score", "mean"),
            mean_em  = ("em_score", "mean") if "em_score" in merged.columns else ("f1_score", lambda x: None),
        ).reset_index()
        grp["dimension"]  = label
        grp["category"]   = grp[group_col].astype(str)
        grp["drop_flag"]  = grp["mean_f1"] < (overall_f1 * (1 - drop_threshold / 100))
        grp = grp[["dimension", "category", "n", "mean_f1", "mean_em", "drop_flag"]]
        return grp

    # hop_type breakdown
    dim1 = _make_breakdown("hop_type", "hop_type")
    dimension_dfs.append(dim1)

    # answer_format breakdown
    dim2 = _make_breakdown("answer_format", "answer_format")
    dimension_dfs.append(dim2)

    # hop_count breakdown (only multi-hop)
    multi = merged[merged["hop_type"] == "multi-hop"].copy()
    if not multi.empty:
        dim3 = multi.groupby("hop_count").agg(
            n       = ("f1_score", "count"),
            mean_f1 = ("f1_score", "mean"),
            mean_em = ("em_score", "mean") if "em_score" in multi.columns else ("f1_score", lambda x: None),
        ).reset_index()
        dim3["dimension"] = "hop_count"
        dim3["category"]  = dim3["hop_count"].astype(str) + "-hop"
        dim3["drop_flag"] = dim3["mean_f1"] < (overall_f1 * (1 - drop_threshold / 100))
        dim3 = dim3[["dimension", "category", "n", "mean_f1", "mean_em", "drop_flag"]]
        dimension_dfs.append(dim3)

    # reasoning_type breakdown (exploded)
    exploded = _explode_reasoning(merged)
    dim4 = exploded.groupby("reasoning_type_single").agg(
        n       = ("f1_score", "count"),
        mean_f1 = ("f1_score", "mean"),
        mean_em = ("em_score", "mean") if "em_score" in exploded.columns else ("f1_score", lambda x: None),
    ).reset_index()
    dim4["dimension"] = "reasoning_type"
    dim4["category"]  = dim4["reasoning_type_single"]
    dim4["drop_flag"] = dim4["mean_f1"] < (overall_f1 * (1 - drop_threshold / 100))
    dim4 = dim4[["dimension", "category", "n", "mean_f1", "mean_em", "drop_flag"]]
    dimension_dfs.append(dim4)

    report = pd.concat(dimension_dfs, ignore_index=True).sort_values(
        ["dimension", "mean_f1"]
    )

    for dim_name, grp in report.groupby("dimension"):
        print(f"\n── {dim_name} ──")
        for _, row in grp.iterrows():
            flag = " ⚠ BELOW AVG" if row["drop_flag"] else ""
            em_str = f"  EM={row['mean_em']:.3f}" if row["mean_em"] is not None else ""
            print(f"  {row['category']:<20}  n={row['n']:>3}  F1={row['mean_f1']:.3f}{em_str}{flag}")

    # save report
    out_path = scores_csv.replace(".csv", "_stratified_report.csv")
    report.to_csv(out_path, index=False)
    print(f"\nReport saved → {out_path}")

    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stratified evaluation report")
    parser.add_argument("--scores",         required=True,  help="Path to a *_scored.csv file")
    parser.add_argument("--cats",           required=True,  help="Path to question_categories.csv")
    parser.add_argument("--dataset",        default=None,   help="Filter to one dataset (e.g. finhybrid)")
    parser.add_argument("--drop-threshold", type=float, default=10.0,
                        help="Flag categories this %% below overall F1 (default 10)")
    args = parser.parse_args()

    stratified_report(
        scores_csv     = args.scores,
        cats_csv       = args.cats,
        dataset        = args.dataset,
        drop_threshold = args.drop_threshold,
    )
