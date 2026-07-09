"""
Task 1 — Question categorisation via LLM-as-judge.

Run once to classify all questions in the failure list, then cache results.
Re-running is safe: already-classified question IDs are skipped.

Usage:
    python categorize_questions.py \
        --input  questions/sprint3_all_failures.csv \
        --output categorization/question_categories.csv \
        --cache  categorization/cache.json

Output columns:
    q_uid, dataset, question, hop_type, reasoning_type,
    answer_format, hop_count
"""

import argparse
import json
import os
import sys
import time

import pandas as pd
from together import Together

# ── resolve Sprint 3 path so we can import access_config ─────────────────────
_here        = os.path.dirname(os.path.abspath(__file__))
_sprint4     = os.path.abspath(os.path.join(_here, '..'))
_sprint3_uda = os.path.abspath(os.path.join(_sprint4, '..', 'Sprint 3', 'UDA-Benchmark'))
for _p in [_sprint4, _sprint3_uda]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from uda.utils.access_config import TOGETHER_API_KEY  # noqa: E402

TOGETHER_MODEL = 'nvidia/nemotron-3-ultra-550b-a55b'

# ── few-shot classification prompt ───────────────────────────────────────────
SYSTEM_PROMPT = """\
You are an expert question analyst for financial document QA benchmarks.
Classify each question into EXACTLY these categories.
Respond with a JSON object only — no prose, no markdown fences.

Fields:
  hop_type       : "single-hop" | "multi-hop"
  reasoning_type : list, one or more of ["arithmetic", "comparative", "causal", "extractive"]
  answer_format  : "numerical" | "binary" | "span"
  hop_count      : integer (1 if single-hop, 2/3/4 if multi-hop)

Rules:
  single-hop  — answered by one fact or cell lookup
  multi-hop   — requires combining 2+ values or facts
  arithmetic  — addition, subtraction, division, ratio, change
  comparative — comparing two or more values ("greater than", "which year", "higher")
  causal      — "why", "reason", "because", "due to"
  extractive  — copy a span from the document verbatim
  numerical   — answer is a number or list of numbers
  binary      — yes/no or true/false answer
  span        — answer is a text phrase
"""

FEW_SHOT_EXAMPLES = [
    {
        "question": "What was the change in total revenue from 2018 to 2019?",
        "answer": {
            "hop_type": "multi-hop",
            "reasoning_type": ["arithmetic"],
            "answer_format": "numerical",
            "hop_count": 2
        }
    },
    {
        "question": "In which year was operating income greater than 50,000?",
        "answer": {
            "hop_type": "multi-hop",
            "reasoning_type": ["comparative"],
            "answer_format": "span",
            "hop_count": 2
        }
    },
    {
        "question": "What is the name of the company's primary auditor?",
        "answer": {
            "hop_type": "single-hop",
            "reasoning_type": ["extractive"],
            "answer_format": "span",
            "hop_count": 1
        }
    },
    {
        "question": "What was the interest expense and depreciation in 2019 and 2018 respectively?",
        "answer": {
            "hop_type": "multi-hop",
            "reasoning_type": ["extractive", "arithmetic"],
            "answer_format": "numerical",
            "hop_count": 4
        }
    },
    {
        "question": "Did the company report a net loss in 2020?",
        "answer": {
            "hop_type": "single-hop",
            "reasoning_type": ["extractive"],
            "answer_format": "binary",
            "hop_count": 1
        }
    },
]


def _build_messages(question: str) -> list:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for ex in FEW_SHOT_EXAMPLES:
        messages.append({"role": "user",      "content": ex["question"]})
        messages.append({"role": "assistant", "content": json.dumps(ex["answer"])})
    messages.append({"role": "user", "content": question})
    return messages


def _classify_one(client: Together, question: str, retries: int = 3) -> dict:
    for attempt in range(retries):
        try:
            resp = client.chat.completions.create(
                model=TOGETHER_MODEL,
                messages=_build_messages(question),
                temperature=0.0,
                max_tokens=128,
            )
            raw = resp.choices[0].message.content.strip()
            # strip markdown fences if model adds them
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            return json.loads(raw)
        except (json.JSONDecodeError, Exception) as e:
            if attempt == retries - 1:
                print(f"  [WARN] classify failed after {retries} attempts: {e}")
                return {
                    "hop_type": "unknown",
                    "reasoning_type": ["unknown"],
                    "answer_format": "unknown",
                    "hop_count": -1,
                }
            time.sleep(2 ** attempt)


def categorize(input_csv: str, output_csv: str, cache_path: str) -> pd.DataFrame:
    df = pd.read_csv(input_csv)
    required = {"q_uid", "dataset", "question"}
    if not required.issubset(df.columns):
        raise ValueError(f"Input CSV must have columns: {required}")

    # load existing cache
    cache = {}
    if os.path.exists(cache_path):
        with open(cache_path) as f:
            cache = json.load(f)
        print(f"Loaded {len(cache)} cached classifications from {cache_path}")

    client    = Together(api_key=TOGETHER_API_KEY)
    new_count = 0

    for _, row in df.iterrows():
        uid = row["q_uid"]
        if uid in cache:
            continue
        print(f"  Classifying [{row['dataset']}] {uid[:8]}… {row['question'][:60]}")
        result      = _classify_one(client, row["question"])
        cache[uid]  = result
        new_count  += 1

        # persist after every question so a crash doesn't lose work
        with open(cache_path, "w") as f:
            json.dump(cache, f, indent=2)

        time.sleep(0.3)  # light rate-limit courtesy pause

    print(f"\nClassified {new_count} new questions ({len(cache)} total in cache)")

    # build output dataframe
    records = []
    for _, row in df.iterrows():
        uid  = row["q_uid"]
        cats = cache.get(uid, {})
        records.append({
            "q_uid":          uid,
            "dataset":        row["dataset"],
            "question":       row["question"],
            "doc_name":       row.get("doc_name", ""),
            "ground_truth":   row.get("ground_truth", ""),
            "failure_type":   row.get("failure_type", ""),
            "max_f1_sprint3": row.get("max_f1_sprint3", ""),
            "hop_type":       cats.get("hop_type", "unknown"),
            "reasoning_type": json.dumps(cats.get("reasoning_type", [])),
            "answer_format":  cats.get("answer_format", "unknown"),
            "hop_count":      cats.get("hop_count", -1),
        })

    out_df = pd.DataFrame(records)
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    out_df.to_csv(output_csv, index=False)
    print(f"Saved {len(out_df)} rows → {output_csv}")
    return out_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify questions via LLM-as-judge")
    parser.add_argument("--input",  default="questions/sprint3_all_failures.csv")
    parser.add_argument("--output", default="categorization/question_categories.csv")
    parser.add_argument("--cache",  default="categorization/cache.json")
    args = parser.parse_args()

    # resolve relative to this script's directory
    _base = os.path.dirname(os.path.abspath(__file__))
    categorize(
        input_csv  = os.path.join(_base, args.input),
        output_csv = os.path.join(_base, args.output),
        cache_path = os.path.join(_base, args.cache),
    )
