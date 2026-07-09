"""
Task 3 — Weak-spot diagnostic.

For the 2–3 worst-performing categories, prints 5 failing examples each:
  question | retrieved context (truncated) | model answer | ground truth

Usage:
    python weak_spot_diagnostic.py \
        --scores   path/to/any_scored.csv \
        --cats     categorization/question_categories.csv \
        --dataset  finhybrid \
        --top-n    3 \
        --examples 5

Requires the scored CSV to also have a 'response' column (all Sprint 3 result CSVs do).
Context is re-retrieved from the original PDFs using the same ChromaDB pipeline as Sprint 3.
"""

import argparse
import json
import os
import sys

import pandas as pd

_here        = os.path.dirname(os.path.abspath(__file__))
_sprint4     = os.path.abspath(os.path.join(_here, '..'))
_sprint3_uda = os.path.abspath(os.path.join(_sprint4, '..', 'Sprint 3', 'UDA-Benchmark'))
for _p in [_sprint4, _sprint3_uda]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from uda.utils import retrieve as rt, preprocess as pre  # noqa: E402
from uda.utils.access_config import TOGETHER_API_KEY     # noqa: E402  (unused here, kept for parity)


def _get_worst_categories(
    scores_csv: str,
    cats_csv: str,
    dataset: str,
    top_n: int,
    dim: str = "reasoning_type",
) -> list:
    """Return the top_n category names with the lowest mean F1."""
    scores = pd.read_csv(scores_csv)
    cats   = pd.read_csv(cats_csv)
    if dataset:
        cats = cats[cats["dataset"] == dataset]

    merged = scores.merge(cats[["q_uid", dim]], on="q_uid", how="inner")

    if dim == "reasoning_type":
        # explode list
        rows = []
        for _, r in merged.iterrows():
            rt_val = r[dim]
            if isinstance(rt_val, str) and rt_val.startswith("["):
                rt_val = json.loads(rt_val)
            if isinstance(rt_val, list):
                for v in rt_val:
                    rows.append({**r.to_dict(), dim: v})
            else:
                rows.append(r.to_dict())
        merged = pd.DataFrame(rows)

    worst = (
        merged.groupby(dim)["f1_score"]
        .mean()
        .sort_values()
        .head(top_n)
        .index.tolist()
    )
    return worst


def _retrieve_context(dataset: str, doc_name: str, question: str, top_k: int = 5) -> str:
    """Re-retrieve context for a question using the Sprint 3 pipeline."""
    # map scored-CSV dataset name to UDA internal name
    dataset_map = {
        "tathybrid": "tat", "finhybrid": "fin", "nqtext": "nq",
        "fetatab": "feta", "papertext": "paper_text", "papertab": "paper_tab",
    }
    uda_name = dataset_map.get(dataset, dataset)
    try:
        pdf_path   = pre.get_example_pdf_path(uda_name, doc_name)
        collection = rt.prepare_collection(pdf_path, f"diag_{doc_name}", "all-MiniLM-L6-v2")
        contexts   = rt.get_contexts(collection, question, "all-MiniLM-L6-v2", top_k=top_k)
        rt.reset_collection(f"diag_{doc_name}", "all-MiniLM-L6-v2")
        return "\n---\n".join(contexts)
    except Exception as e:
        return f"[context retrieval failed: {e}]"


def _parse_answer(answers_str: str) -> str:
    try:
        d = eval(answers_str)  # answers column is a dict literal in the scored CSVs
        if isinstance(d, dict):
            return ", ".join(d.get("answer", []))
        return str(d)
    except Exception:
        return str(answers_str)


def diagnose(
    scores_csv: str,
    cats_csv: str,
    dataset: str = None,
    top_n: int = 3,
    n_examples: int = 5,
    retrieve_context: bool = True,
) -> None:
    scores = pd.read_csv(scores_csv)
    cats   = pd.read_csv(cats_csv)
    if dataset:
        cats = cats[cats["dataset"] == dataset]

    # explode reasoning_type for per-type analysis
    exploded_cats = []
    for _, r in cats.iterrows():
        rt_val = r["reasoning_type"]
        if isinstance(rt_val, str) and rt_val.startswith("["):
            rt_val = json.loads(rt_val)
        if isinstance(rt_val, list):
            for v in rt_val:
                exploded_cats.append({**r.to_dict(), "reasoning_type_single": v})
        else:
            exploded_cats.append({**r.to_dict(), "reasoning_type_single": str(rt_val)})
    exploded = pd.DataFrame(exploded_cats)

    merged = scores.merge(
        exploded[["q_uid", "reasoning_type_single", "hop_type", "answer_format"]],
        on="q_uid", how="inner"
    )

    worst_cats = (
        merged.groupby("reasoning_type_single")["f1_score"]
        .mean()
        .sort_values()
        .head(top_n)
        .index.tolist()
    )

    print(f"\n{'='*60}")
    print(f"WEAK-SPOT DIAGNOSTIC")
    if dataset:
        print(f"Dataset : {dataset}")
    print(f"Showing top-{top_n} worst reasoning categories, {n_examples} examples each")
    print(f"{'='*60}")

    for cat in worst_cats:
        cat_rows = merged[merged["reasoning_type_single"] == cat].copy()
        # failing = wrong answers (f1 < 0.3) or empty
        failing = cat_rows[cat_rows["f1_score"] < 0.3].sort_values("f1_score").head(n_examples)

        cat_f1 = cat_rows["f1_score"].mean()
        print(f"\n\n{'─'*60}")
        print(f"Category : {cat}  (mean F1={cat_f1:.3f}, n={len(cat_rows)})")
        print(f"Showing {len(failing)} failing examples:")
        print(f"{'─'*60}")

        for i, (_, row) in enumerate(failing.iterrows(), 1):
            gt = _parse_answer(str(row.get("answers", "")))

            if retrieve_context:
                doc   = str(row.get("doc", row.get("doc_name", "")))
                dname = dataset or str(row.get("dataset", ""))
                ctx   = _retrieve_context(dname, doc, row["question"], top_k=3)
                ctx_display = ctx[:600] + "…" if len(ctx) > 600 else ctx
            else:
                ctx_display = "[context retrieval disabled]"

            print(f"\n  [{i}] Q : {row['question']}")
            print(f"      GT: {gt}")
            print(f"      A : {str(row.get('response', ''))[:300]}")
            print(f"      F1: {row['f1_score']:.3f}  |  hop={row.get('hop_type','')}  fmt={row.get('answer_format','')}")
            print(f"      Context snippet:")
            for line in ctx_display.split("\n")[:6]:
                print(f"        {line}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Weak-spot diagnostic for failing categories")
    parser.add_argument("--scores",          required=True)
    parser.add_argument("--cats",            required=True)
    parser.add_argument("--dataset",         default=None)
    parser.add_argument("--top-n",           type=int,  default=3)
    parser.add_argument("--examples",        type=int,  default=5)
    parser.add_argument("--no-context",      action="store_true",
                        help="Skip context re-retrieval (faster, less informative)")
    args = parser.parse_args()

    diagnose(
        scores_csv       = args.scores,
        cats_csv         = args.cats,
        dataset          = args.dataset,
        top_n            = args.top_n,
        n_examples       = args.examples,
        retrieve_context = not args.no_context,
    )
