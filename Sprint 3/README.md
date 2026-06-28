# Sprint 3: NVIDIA Nemotron on UDA-Benchmark

**Model Under Test:** NVIDIA Nemotron-3 Ultra 550B (via Together AI)  
**Benchmark:** UDA-QA (Unstructured Document Analysis)  
**Status:** Ready to start Phase 1  
**Start Date:** 2026-06-28

---

## Quick Start

### 1. Review the Experiment Plan
📄 **[SPRINT3_EXPERIMENT_PLAN.md](SPRINT3_EXPERIMENT_PLAN.md)** - Full experiment design, phases, and success metrics

### 2. Run Phase 1 Baseline Evaluation
```bash
cd UDA-Benchmark
jupyter notebook nemotron_phase1_experiment.ipynb
```

**Expected Runtime:** 1-2 hours (example documents only)  
**Expected Cost:** ~$5-10 in API calls

### 3. Review Results
Results will be saved in:
- `phase1_results_[timestamp].csv` - Individual Q&A scores
- `phase1_summary_[timestamp].csv` - Aggregated metrics
- Console output - Real-time evaluation metrics

---

## What is UDA-Benchmark?

**UDA (Unstructured Document Analysis)** is a NeurIPS 2024 benchmark for evaluating **RAG (Retrieval Augmented Generation)** systems on real-world documents.

### Key Characteristics:
- ✅ **Real-world PDFs** - Financial reports, academic papers, Wikipedia
- ✅ **Mixed content** - Text + tables together (not cleaned)
- ✅ **Large documents** - Average 147 pages, 76K words
- ✅ **Expert annotations** - 29,590 Q&A pairs by domain experts
- ✅ **Multiple metrics** - Exact Match, Numeracy F1, Span F1

### Datasets:

| Dataset | Domain | Docs | Q&A | Pages | Metric |
|---------|--------|------|-----|-------|--------|
| **FinHybrid** | Finance | 788 | 8,190 | 147.8 | Exact Match ±1% |
| **TatHybrid** | Finance | 170 | 14,703 | 148.5 | Numeracy F1 |
| **PaperTab** | Academia | 307 | 393 | 11.0 | Span F1 |
| **PaperText** | Academia | 1,087 | 2,804 | 10.6 | Span F1 |
| **FetaTab** | Wikipedia | 878 | 1,023 | 14.9 | Span F1 |
| **NqText** | Wikipedia | 645 | 2,477 | 14.9 | Span F1 |

---

## Why NVIDIA Nemotron?

**Nemotron-3 Ultra 550B** is one of the largest open models available:
- 🚀 **550 billion parameters** - Massive capacity for reasoning
- 💡 **Aligned for instructions** - A55B checkpoint optimized for Q&A
- 💰 **Together AI access** - Fast inference via API
- 🎯 **Financial strength** - Expected to excel on FinHybrid/TatHybrid

---

## Experiment Phases

### ✅ Phase 1: Baseline Evaluation (READY)
- **Goal:** Establish baseline performance on example documents
- **Scope:** All 6 datasets, ~30-50 Q&A pairs
- **Time:** 1-2 hours
- **Cost:** ~$5-10
- **Notebook:** `nemotron_phase1_experiment.ipynb`

### ⏳ Phase 2: Parameter Optimization (OPTIONAL)
- **Goal:** Find optimal RAG parameters
- **Variables:** chunk_size (1500/3000/6000), top_k (3/5/10), temperature (0.0/0.1/0.3)
- **Time:** 4-6 hours
- **Cost:** ~$20-30

### ⏳ Phase 3: Full Dataset Evaluation (FUTURE)
- **Goal:** Comprehensive evaluation on all 29,590 Q&A pairs
- **Time:** 8-12 hours runtime
- **Cost:** ~$30-50
- **Note:** Requires downloading full dataset from HuggingFace

---

## Technical Setup

### API Configuration ✅
- **File:** `UDA-Benchmark/uda/utils/access_config.py`
- **API Key:** Already configured
- **Model ID:** `nvidia/nemotron-3-ultra-550b-a55b`

### Dependencies ✅
```bash
pip install together langchain chromadb sentence-transformers PyPDF2 pandas tqdm
```

### RAG Pipeline:
```
PDF → PyPDF2 Extract → Text Chunking → ChromaDB Index → 
Retrieve Top-K → Nemotron Generation → Evaluation
```

---

## Key Differences from Sprint 2

| Aspect | Sprint 2 (Gemini) | Sprint 3 (Nemotron) |
|--------|------------------|---------------------|
| **Model** | Gemini 3.1 Pro Extended | NVIDIA Nemotron-3 Ultra 550B |
| **Task** | Direct table analysis | RAG pipeline (retrieve + generate) |
| **Data** | Synthetic music DB | Real financial reports / papers |
| **Format** | Clean CSV/HTML/JSON/XML | Raw PDFs (text + tables mixed) |
| **Size** | 567 records | 76K words, 148 pages avg |
| **Questions** | 20 questions × 4 formats = 80 tests | 29,590 questions (Phase 3) |
| **Complexity** | SQL-like queries | Multi-hop reasoning, table extraction |
| **Best Result** | JSON 80%, All formats 80% (individual) | TBD |

---

## Expected Results

### Phase 1 Targets (Example Documents):

| Dataset | Expected Accuracy | Reasoning |
|---------|-------------------|-----------|
| FinHybrid | **70-85%** | Nemotron's strength (financial) |
| TatHybrid | **65-80%** | Numeracy-focused, harder |
| PaperTab | 60-75% | Table extraction challenging |
| PaperText | 65-80% | Factual extraction |
| FetaTab | 60-75% | Wikipedia tables |
| NqText | 70-85% | Short factual answers |

### Comparison:
- **GPT-4 baseline:** 75-85% on UDA-Benchmark (from paper)
- **Goal:** Match or exceed GPT-4 on financial subsets

---

## Files in This Directory

```
Sprint 3/
├── README.md                           ← You are here
├── SPRINT3_EXPERIMENT_PLAN.md          ← Detailed experiment design
├── UDA-Benchmark/                      ← Benchmark repository
│   ├── nemotron_phase1_experiment.ipynb ← Phase 1 notebook (RUN THIS)
│   ├── basic_demo_together.ipynb       ← Reference implementation
│   ├── uda/utils/access_config.py      ← API keys configured ✅
│   ├── dataset/
│   │   ├── qa/                         ← Q&A CSV files
│   │   ├── src_doc_files_example/      ← Example PDFs (Phase 1)
│   │   └── src_doc_files/              ← Full dataset (Phase 3)
│   └── ...
├── phase1_results_[timestamp].csv      ← Individual scores (after Phase 1)
├── phase1_summary_[timestamp].csv      ← Aggregated metrics (after Phase 1)
└── PHASE1_BASELINE_RESULTS.md          ← Analysis document (after Phase 1)
```

---

## Next Steps

### Immediate:
1. ✅ Review `SPRINT3_EXPERIMENT_PLAN.md`
2. 🔄 Run `nemotron_phase1_experiment.ipynb`
3. 🔄 Analyze results
4. 🔄 Document findings in `PHASE1_BASELINE_RESULTS.md`

### Short-term:
- Compare results with Sprint 2 (Gemini)
- Identify Nemotron's strengths/weaknesses
- Decide if Phase 2 parameter tuning is worth the cost

### Long-term:
- Download full UDA-QA dataset from HuggingFace
- Plan Phase 3 full evaluation
- Consider testing other models (Gemini, GPT-4, Claude) for comparison

---

## Questions?

- **Budget:** Estimate ~$5-10 for Phase 1, ~$30-50 for Phase 3
- **Time:** Phase 1 can run in 1-2 hours
- **Scope:** Starting with examples only, can scale to full dataset
- **Comparison:** Can benchmark against other models later

---

## References

- **Paper:** [UDA: A Benchmark Suite for RAG in Real-world Document Analysis](https://arxiv.org/abs/2406.15187)
- **Dataset:** [HuggingFace - qinchuanhui/UDA-QA](https://huggingface.co/datasets/qinchuanhui/UDA-QA)
- **Code:** [GitHub - qinchuanhui/UDA-Benchmark](https://github.com/qinchuanhui/UDA-Benchmark)
- **License:** CC BY-SA 4.0

---

**Created:** 2026-06-28  
**Status:** Phase 1 ready to execute  
**Next Milestone:** Complete Phase 1 baseline evaluation
