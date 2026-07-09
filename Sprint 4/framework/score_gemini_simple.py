"""
Score Gemini simple-prompt results against UDA eval metrics.
Joins results CSVs back to raw QA files to build the answers dicts
that eval_main() expects.

Run from Sprint 3/UDA-Benchmark directory:
    cd "Sprint 3/UDA-Benchmark"
    python3 ../../Sprint\ 4/framework/score_gemini_simple.py
"""

import sys, os, ast
import pandas as pd

S4_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
S3_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Sprint 3/UDA-Benchmark'))
sys.path.insert(0, S4_ROOT)
sys.path.insert(0, S3_ROOT)

RESULTS_BASE = os.path.join(S4_ROOT, 'experiments/gemini-3.1-flash-lite/results/')
QA_BASE      = os.path.join(S3_ROOT, 'dataset/qa/')


def _extract_raw_quid(row):
    """Parse the raw q_uid from the notes field (e.g. 'phases_tested=6; q_uid=abc123')."""
    import re
    notes = str(row.get('notes', '') or '')
    m = re.search(r'q_uid=(.+?)(?:;|$)', notes)
    if m:
        return m.group(1).strip()
    # Fallback: strip known prefix from question_id
    qid = str(row['question_id'])
    for prefix in ('S3_TATHYBRID_', 'S3_FINHYBRID_', 'S3_NQTEXT_',
                   'S3_FETATAB_', 'S3_PAPERTAB_', 'S3_PAPERTEXT_'):
        if qid.startswith(prefix):
            return qid[len(prefix):]
    return qid


# ── answers loaders (return {q_uid: <answers_dict_or_list>}) ───────────────

def _load_tat_answers(qa_path):
    df = pd.read_csv(qa_path, sep='|')
    out = {}
    for _, row in df.iterrows():
        raw = row['answer']
        try:
            answer_list = ast.literal_eval(str(raw))
        except Exception:
            answer_list = [str(raw)]
        scale = '' if pd.isna(row.get('answer_scale')) else str(row['answer_scale'])
        out[str(row['q_uid'])] = {
            'answer':      answer_list,
            'answer_type': str(row['answer_type']),
            'scale':       scale,
        }
    return out


def _load_fin_answers(qa_path):
    df = pd.read_csv(qa_path, sep='|')
    out = {}
    for _, row in df.iterrows():
        out[str(row['q_uid'])] = {
            'str_answer': str(row['answer_1']),
            'exe_answer': str(row['answer_2']),
        }
    return out


def _load_nq_answers(qa_path):
    df = pd.read_csv(qa_path, sep='|')
    out = {}
    for _, row in df.iterrows():
        # nq_evaluate reads gold[q_uid]['long_answer'] and ['short_answer']
        out[str(row['q_uid'])] = {
            'short_answer': str(row['short_answer']),
            'long_answer':  str(row['long_answer']),
        }
    return out


def _load_feta_answers(qa_path):
    df = pd.read_csv(qa_path, sep='|')
    out = {}
    for _, row in df.iterrows():
        # feta_evaluate reads gold[q_uid] directly as a string
        out[str(row['q_uid'])] = str(row['answer'])
    return out


def _load_paper_answers(qa_path):
    df = pd.read_csv(qa_path, sep='|')
    out = {}
    for _, row in df.iterrows():
        answers = [str(row['answer_1'])]
        for col in ['answer_2', 'answer_3']:
            v = str(row.get(col, '')).strip()
            if v and v not in ('nan', ' '):
                answers.append(v)
        # paper_evaluate iterates gold[q_uid] as a list of references
        out[str(row['q_uid'])] = answers
    return out


# ── per-question F1 helpers ─────────────────────────────────────────────────

def _token_f1(pred, ref):
    from uda.eval.utils.basic_utils import token_f1_score
    return token_f1_score(pred, ref)


def _per_q_f1_nq(pred, answers_dict):
    f1 = max(
        _token_f1(pred, answers_dict.get('long_answer', '')),
        _token_f1(pred, answers_dict.get('short_answer', '')),
    )
    return f1


def _per_q_f1_feta(pred, answer_str):
    return _token_f1(pred, answer_str)


def _per_q_f1_paper(pred, answers_list):
    if not answers_list:
        return 0.0
    return max(_token_f1(pred, str(ref)) for ref in answers_list)


# ── main scoring function ────────────────────────────────────────────────────

def score_dataset(dataset, results_file, qa_file, uda_name, answers_loader):
    print(f"\n{'='*60}")
    print(f"Scoring: {dataset}  (uda={uda_name})")
    print(f"{'='*60}")

    df = pd.read_csv(results_file)
    answers_map = answers_loader(qa_file)

    # Build raw_quid column by parsing notes
    df = df.copy()
    df['raw_quid'] = df.apply(_extract_raw_quid, axis=1)

    empty_count = df['response'].fillna('').str.strip().eq('').sum()
    missing_gt  = sum(1 for qid in df['raw_quid'] if qid not in answers_map)
    print(f"Total: {len(df)} | Empty responses: {empty_count} | Missing GT: {missing_gt}")

    per_q_em = []
    per_q_f1 = []

    if dataset == 'tathybrid':
        from uda.eval.utils.tat_eval import TaTQAEmAndF1
        ev = TaTQAEmAndF1()
        for _, row in df.iterrows():
            raw_quid = row['raw_quid']
            response = str(row.get('response', '') or '')
            gt       = answers_map.get(raw_quid, {'answer': [], 'answer_type': 'span', 'scale': ''})
            ev({'response': response, 'answers': gt, 'q_uid': raw_quid})
        for d in ev._details:
            per_q_em.append(float(d.get('em', 0)))
            per_q_f1.append(float(d.get('f1', 0)))
        gem, gf1, _, _ = ev.get_overall_metric()
        print(f"\nNumeracy F1:  {gf1*100:.2f}%")
        print(f"Exact Match:  {gem*100:.2f}%")

    elif dataset == 'finhybrid':
        from uda.eval.utils.fin_eval import FinQAEm
        ev = FinQAEm()
        for _, row in df.iterrows():
            raw_quid = row['raw_quid']
            response = str(row.get('response', '') or '')
            gt       = answers_map.get(raw_quid, {'str_answer': '', 'exe_answer': ''})
            ev({'response': response, 'answers': gt, 'q_uid': raw_quid})
        for d in ev._details:
            em = float(d.get('em', 0))
            per_q_em.append(em)
            per_q_f1.append(em)
        gem = ev.get_overall_metric()
        print(f"\nExact Match:  {gem*100:.2f}%")

    else:
        # nq, feta, papertab, papertext — token F1
        from uda.eval.utils.paper_eval import paper_evaluate
        from uda.eval.utils.feta_eval import feta_evaluate
        from uda.eval.utils.nq_eval import nq_evaluate

        eval_fn = {'nq': nq_evaluate, 'feta': feta_evaluate,
                   'paper_tab': paper_evaluate, 'paper_text': paper_evaluate}[uda_name]

        answers_gold = {}
        preds_dict   = {}
        per_q_map    = {}

        for _, row in df.iterrows():
            raw_quid = row['raw_quid']
            response = str(row.get('response', '') or '')
            pred     = response.split("The answer is: ")[-1] if response else ""
            gt       = answers_map.get(raw_quid)
            if gt is None:
                per_q_map[raw_quid] = 0.0
                continue
            answers_gold[raw_quid] = gt
            preds_dict[raw_quid]   = {"answer": pred}

            if dataset == 'nqtext':
                f1 = _per_q_f1_nq(pred, gt)
            elif dataset == 'fetatab':
                f1 = _per_q_f1_feta(pred, gt)
            else:
                f1 = _per_q_f1_paper(pred, gt)
            per_q_map[raw_quid] = f1

        # Aggregate via official evaluator
        agg = eval_fn(answers_gold, preds_dict)
        print(f"\n{agg}")

        for _, row in df.iterrows():
            f1 = per_q_map.get(row['raw_quid'], 0.0)
            per_q_f1.append(f1)
            per_q_em.append(1.0 if f1 >= 1.0 else 0.0)

    # Attach per-question scores and save
    df['em_score'] = per_q_em
    df['f1_score'] = per_q_f1
    df['is_empty'] = df['response'].fillna('').str.strip() == ''

    out_path = results_file.replace('.csv', '_scored.csv')
    df.to_csv(out_path, index=False)
    print(f"Saved → {os.path.basename(out_path)}")
    return df


if __name__ == '__main__':
    configs = [
        ('tathybrid',  RESULTS_BASE + 'tathybrid_gemini-3.1-flash-lite_simple_20260708_210305.csv',
                       QA_BASE + 'tat_qa.csv',        'tat',        _load_tat_answers),
        ('finhybrid',  RESULTS_BASE + 'finhybrid_gemini-3.1-flash-lite_simple_20260708_205022.csv',
                       QA_BASE + 'fin_qa.csv',        'fin',        _load_fin_answers),
        ('nqtext',     RESULTS_BASE + 'nqtext_gemini-3.1-flash-lite_simple_20260708_205543.csv',
                       QA_BASE + 'nq_qa.csv',         'nq',         _load_nq_answers),
        ('fetatab',    RESULTS_BASE + 'fetatab_gemini-3.1-flash-lite_simple_20260708_204437.csv',
                       QA_BASE + 'feta_qa.csv',       'feta',       _load_feta_answers),
        ('papertab',   RESULTS_BASE + 'papertab_gemini-3.1-flash-lite_simple_20260708_205810.csv',
                       QA_BASE + 'paper_tab_qa.csv',  'paper_tab',  _load_paper_answers),
        ('papertext',  RESULTS_BASE + 'papertext_gemini-3.1-flash-lite_simple_20260708_205909.csv',
                       QA_BASE + 'paper_text_qa.csv', 'paper_text', _load_paper_answers),
    ]

    all_dfs = {}
    for dataset, results_file, qa_file, uda_name, loader in configs:
        all_dfs[dataset] = score_dataset(dataset, results_file, qa_file, uda_name, loader)

    # Final summary table
    print('\n\n' + '='*60)
    print('FINAL SUMMARY — Gemini 3.1 Flash-Lite  (simple prompt)')
    print('='*60)
    print(f"{'Dataset':<20} {'N':>4}  {'Empty':>5}  {'Avg F1':>8}  {'Avg EM':>8}")
    print('-'*60)
    for ds, df in all_dfs.items():
        n     = len(df)
        empty = int(df['is_empty'].sum())
        f1    = df['f1_score'].mean() * 100
        em    = df['em_score'].mean() * 100
        print(f"{ds:<20} {n:>4}  {empty:>5}  {f1:>7.1f}%  {em:>7.1f}%")
