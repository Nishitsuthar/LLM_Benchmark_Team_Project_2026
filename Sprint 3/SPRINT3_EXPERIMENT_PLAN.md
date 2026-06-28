# Sprint 3: UDA-Benchmark Experiment Plan

**Model Under Test:** NVIDIA Nemotron-3 Ultra (550B parameters)  
**API Provider:** Together AI  
**Start Date:** 2026-06-28  
**Dataset:** UDA-QA (Unstructured Document Analysis)

---

## Executive Summary

Sprint 3 evaluates NVIDIA Nemotron on **real-world document analysis** using the UDA-Benchmark suite. Unlike Sprint 2's clean structured data, this tests RAG (Retrieval Augmented Generation) on messy PDFs with mixed text and tables.

---

## Model Information

**NVIDIA Nemotron-3 Ultra 550B**
- **Parameters:** 550 billion (one of the largest open models)
- **Architecture:** Aligned variant (A55B checkpoint)
- **API:** Together AI (`nvidia/nemotron-3-ultra-550b-a55b`)
- **Context Window:** Likely 4K-8K tokens
- **Strengths:** Instruction following, reasoning, financial analysis

---

## Dataset: UDA-QA Overview

| Sub-Dataset | Domain | Docs | Q&A Pairs | Avg Pages | Size | Metric |
|------------|--------|------|-----------|-----------|------|--------|
| **FinHybrid** | Finance Reports | 788 | 8,190 | 147.8 | 2.61 GB | Exact Match ±1% |
| **TatHybrid** | Finance Reports | 170 | 14,703 | 148.5 | 0.58 GB | Numeracy F1 |
| **PaperTab** | Academia (tables) | 307 | 393 | 11.0 | 0.22 GB | Span F1 |
| **PaperText** | Academia (text) | 1,087 | 2,804 | 10.6 | 0.87 GB | Span F1 |
| **FetaTab** | Wikipedia (tables) | 878 | 1,023 | 14.9 | 0.92 GB | Span F1 |
| **NqText** | Wikipedia (text) | 645 | 2,477 | 14.9 | 0.68 GB | Span F1 |
| **TOTAL** | — | 2,965 | 29,590 | — | 5.88 GB | — |

---

## Experiment Phases

### **Phase 1: Baseline Evaluation (Current Examples Only)** ✅ PRIORITY

**Goal:** Establish baseline performance on example documents (fast, low cost)

**Scope:**
- Use **example documents only** (dataset/src_doc_files_example/)
- Test all 6 sub-datasets
- Default parameters:
  - `chunk_size=3000` characters
  - `chunk_overlap=300` (10%)
  - `top_k=5` retrieved chunks
  - `temperature=0.1` (deterministic)

**Expected Results:**
- FinHybrid: 5-10 example Q&A pairs
- TatHybrid: 5-10 example Q&A pairs
- PaperTab: 3-5 example Q&A pairs
- PaperText: 3-5 example Q&A pairs
- FetaTab: 3-5 example Q&A pairs
- NqText: 3-5 example Q&A pairs

**Output:**
- `PHASE1_BASELINE_RESULTS.md` - Performance breakdown by dataset
- `phase1_results.csv` - Individual Q&A scores

---

### **Phase 2: Parameter Optimization** (Optional)

**Goal:** Find optimal RAG parameters for Nemotron

**Variables to Test:**

| Parameter | Baseline | Variants |
|-----------|----------|----------|
| `chunk_size` | 3000 | 1500, 6000 |
| `top_k` | 5 | 3, 10 |
| `temperature` | 0.1 | 0.0, 0.3 |

**Experiment Design:**
- Pick 1-2 representative documents from FinHybrid
- Run 3×3×3 = 27 configurations
- Measure impact on Exact Match accuracy

**Expected Insights:**
- Optimal chunk size for financial documents
- Retrieval precision vs recall tradeoff (top_k)
- Temperature impact on numerical extraction

---

### **Phase 3: Full Dataset Evaluation** (If Budget Allows)

**Goal:** Comprehensive evaluation across all 29,590 Q&A pairs

**Cost Estimate:**
- 29,590 questions × ~$0.001 per call = ~$30-50
- Time: ~8-12 hours runtime

**Priority Order:**
1. **FinHybrid** (8,190 Q&A) - Most relevant to Nemotron's strengths
2. **TatHybrid** (14,703 Q&A) - Financial reasoning
3. **PaperTab** (393 Q&A) - Table extraction
4. **NqText** (2,477 Q&A) - Factual extraction
5. **PaperText** (2,804 Q&A) - Academic reasoning
6. **FetaTab** (1,023 Q&A) - Wikipedia tables

**Note:** Download full dataset from HuggingFace first:
```bash
cd dataset/src_doc_files
# Download from: https://huggingface.co/datasets/qinchuanhui/UDA-QA/tree/main/src_doc_files
```

---

## Technical Setup

### **1. Dependencies Installed**
```bash
pip install together langchain chromadb sentence-transformers PyPDF2 pandas tqdm
```

### **2. API Configuration**
- File: `uda/utils/access_config.py`
- API Key: ✅ Already configured
- Model: `nvidia/nemotron-3-ultra-550b-a55b`

### **3. RAG Pipeline Components**

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────┐
│   PDF Doc   │ --> │ PyPDF2       │ --> │ Text        │ --> │ ChromaDB │
│             │     │ Extract Text │     │ Chunking    │     │ Vector   │
│ (Financial  │     │              │     │ (3000 chars)│     │ Index    │
│  Report)    │     │              │     │             │     │          │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────┘
                                                                    │
                                                                    ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────┐
│   Answer    │ <-- │   Nemotron   │ <-- │  Prompt:    │ <-- │ Retrieve │
│             │     │   550B       │     │  Question + │     │ Top-5    │
│ "The answer │     │  (Together)  │     │  Context    │     │ Chunks   │
│  is: -27%"  │     │              │     │             │     │          │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────┘
```

---

## Key Differences from Sprint 2

| Aspect | Sprint 2 | Sprint 3 |
|--------|----------|----------|
| **Task Type** | Direct table analysis | RAG (retrieve + generate) |
| **Data Source** | Synthetic music DB | Real financial reports |
| **Format** | Clean CSV/HTML/JSON/XML | Raw PDFs (text + tables) |
| **Document Size** | 567 records | 76K words, 148 pages avg |
| **Questions** | 20 questions, 4 formats = 80 tests | 29,590 questions total |
| **Challenge** | SQL-like queries | Multi-hop reasoning, table extraction |
| **Metric** | Exact match | Exact Match / Numeracy F1 / Span F1 |
| **Model** | Gemini 3.1 Pro Extended | NVIDIA Nemotron-3 Ultra 550B |

---

## Success Metrics

### **Phase 1 Targets (Example Documents)**

| Sub-Dataset | Expected Accuracy | Reasoning |
|-------------|-------------------|-----------|
| FinHybrid | 70-85% | Nemotron's strength (financial) |
| TatHybrid | 65-80% | Numeracy-focused, harder |
| PaperTab | 60-75% | Table extraction challenging |
| PaperText | 65-80% | Factual extraction |
| FetaTab | 60-75% | Wikipedia tables |
| NqText | 70-85% | Short factual answers |

### **Comparison Baseline**
- GPT-4: Typically 75-85% on UDA-Benchmark (paper reports)
- Goal: Match or exceed GPT-4 on financial subsets

---

## Output Artifacts

### **Phase 1 Deliverables:**
1. ✅ `SPRINT3_EXPERIMENT_PLAN.md` (this file)
2. 🔄 `PHASE1_BASELINE_RESULTS.md` - Performance analysis
3. 🔄 `phase1_results.csv` - Raw scores (Question | Predicted | Ground Truth | Score | Dataset)
4. 🔄 `nemotron_phase1_experiment.ipynb` - Executable notebook
5. 🔄 `PHASE1_SUMMARY.csv` - Aggregated metrics by dataset

### **Phase 2 Deliverables (Optional):**
- `PHASE2_PARAMETER_TUNING.md`
- `parameter_sweep_results.csv`

### **Phase 3 Deliverables (Future):**
- `PHASE3_FULL_EVALUATION.md`
- `full_dataset_results.csv`

---

## Timeline Estimate

| Phase | Estimated Time | Status |
|-------|---------------|--------|
| **Phase 1:** Baseline (examples) | 2-4 hours | 🔄 Ready to start |
| **Phase 2:** Parameter tuning | 4-6 hours | ⏳ Optional |
| **Phase 3:** Full evaluation | 8-12 hours runtime | ⏳ Future |
| **Analysis & Documentation** | 3-5 hours | ⏳ After experiments |

---

## Next Steps

### **Immediate (Phase 1):**
1. ✅ Review this plan
2. 🔄 Run `nemotron_phase1_experiment.ipynb` on example documents
3. 🔄 Analyze results and document in `PHASE1_BASELINE_RESULTS.md`
4. 🔄 Compare with Sprint 2 findings

### **Short-term (Phase 2):**
- Decide if parameter optimization is worth the cost
- If yes, implement parameter sweep experiment

### **Long-term (Phase 3):**
- Download full dataset from HuggingFace
- Plan budget for full evaluation (~$30-50)
- Schedule 12-hour runtime window

---

## Questions to Consider

1. **Budget:** What's the API cost tolerance for this sprint?
2. **Scope:** Should we focus on financial datasets (Nemotron's strength)?
3. **Comparison:** Do we want to benchmark against GPT-4 or other models?
4. **Error Analysis:** Should we track error categories like Sprint 2?

---

**Created:** 2026-06-28  
**Last Updated:** 2026-06-28  
**Status:** Plan finalized, ready for Phase 1 execution
