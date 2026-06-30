# NVIDIA Nemotron-3 Ultra 550B - UDA-Benchmark Results

**Model:** `nvidia/nemotron-3-ultra-550b-a55b` (via Together AI)  
**API Provider:** Together AI  
**Testing Period:** June 29, 2026

## 📊 Overview

This directory contains all experiments for the NVIDIA Nemotron-3 Ultra 550B model, organized into baseline and optimization phases.

## 📁 Structure

```
nemotron-3-ultra-550b/
├── 1_without_optimization/    ← Phase 1: Baseline (COMPLETE ✅)
│   ├── tathybrid/            162 Q&A, 43.5% Numeracy F1
│   ├── finhybrid/            47 Q&A, 23.4% Exact Match
│   ├── nqtext/               78 Q&A, 27.6% Span F1
│   ├── fetatab/              8 Q&A, 31.3% Span F1
│   ├── papertext/            13 Q&A, 43.0% Span F1
│   ├── papertab/             4 Q&A, 38.0% Span F1
│   └── results_analysis/     Visualizations & analysis
└── 2_optimization/           ← Phase 2: Optimized (PLANNED 🔄)
    └── (future experiments)
```

## 🎯 Phase 1: Baseline Results (COMPLETE ✅)

### Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Q&A Processed** | 312 |
| **Average Score** | 34.3% |
| **Average Empty Rate** | 24.4% |
| **Best Dataset** | TatHybrid (43.5%) |
| **Worst Dataset** | FinHybrid (23.4%) |
| **Most Reliable** | PaperText (7.7% empty) |
| **Total Runtime** | ~120-175 minutes |
| **Total Cost** | ~$27-41 |

### Detailed Results by Dataset

#### 1. TatHybrid (Finance - Numeracy) ⭐ Best Performer
- **Q&A:** 162 pairs from 4 PDFs
- **Score:** 43.5% Numeracy F1
- **Empty Rate:** 22.8% (37/162)
- **Documents:** Financial reports (2019)
- **Why it works:** Numeracy-aware metric, structured tables
- **Result File:** `1_without_optimization/tathybrid/results/tathybrid_results_20260629_094232.csv`

#### 2. PaperText (Academic - Text) ⭐ Most Reliable
- **Q&A:** 13 pairs from 7 PDFs
- **Score:** 43.0% Span F1
- **Empty Rate:** 7.7% (1/13) ← Lowest!
- **Documents:** Academic papers (arXiv)
- **Why it works:** Clean structured PDFs, good formatting
- **Result File:** `1_without_optimization/papertext/results/papertext_results_20260629_104112.csv`

#### 3. PaperTab (Academic - Tables)
- **Q&A:** 4 pairs from 7 PDFs
- **Score:** 38.0% Span F1
- **Empty Rate:** 75.0% (3/4) ← Small sample
- **Documents:** Same PDFs as PaperText
- **Note:** Small sample size, high variance
- **Result File:** `1_without_optimization/papertab/results/papertab_results_20260629_103921.csv`

#### 4. FetaTab (Wikipedia - Tables)
- **Q&A:** 8 pairs from 4 PDFs
- **Score:** 31.3% Span F1
- **Empty Rate:** ~20%
- **Documents:** Wikipedia articles
- **Challenges:** Table extraction from varied formats
- **Result File:** `1_without_optimization/fetatab/results/fetatab_results_20260629_120656.csv`

#### 5. NqText (Wikipedia - Text)
- **Q&A:** 78 pairs from 4 PDFs
- **Score:** 27.6% Span F1
- **Empty Rate:** 14.1% (11/78)
- **Documents:** Supreme Court, Tour de France, Hannah John-Kamen, Oklahoma
- **Note:** Supreme Court: 0% empty (best), Tour de France: 69% empty (worst)
- **Result File:** `1_without_optimization/nqtext/results/nqtext_results_20260629_112238.csv`

#### 6. FinHybrid (Finance - Hybrid) ⚠️ Hardest Dataset
- **Q&A:** 47 pairs from 4 PDFs
- **Score:** 23.4% Exact Match ±1%
- **Empty Rate:** 40.4% (19/47) ← Highest!
- **Documents:** Financial reports (2009-2016)
- **Challenges:** Strict metric, poor table extraction, high empty rate
- **Result File:** `1_without_optimization/finhybrid/results/finhybrid_results_20260629_120808.csv`

### Baseline Parameters

All Phase 1 experiments used these standard parameters:

```python
# Retrieval Configuration
CHUNK_SIZE = 3000           # Text chunk size for embeddings
CHUNK_OVERLAP = 300         # 10% overlap between chunks
TOP_K = 5                   # Number of chunks retrieved per query

# Generation Configuration
TEMPERATURE = 0.1           # Low randomness for consistent answers
MAX_TOKENS = 512            # Maximum answer length

# Embeddings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # SentenceTransformer (local, free)

# Vector Database
VECTOR_DB = "ChromaDB"      # In-memory vector store

# PDF Parsing
PDF_PARSER = "PyPDF2"       # Basic PDF text extraction
```

### Key Findings

#### 🎯 Main Bottleneck: Empty Responses
- **Average:** 24.4% of questions receive empty responses
- **Range:** 7.7% (PaperText) to 40.4% (FinHybrid)
- **Impact:** More significant than wrong answers!
- **Cause:** Retrieval failure, noisy context, model conservatism

#### 📊 Performance Patterns

**By Domain:**
1. **Academic:** 40.5% avg score, 41.4% avg empty (best scores, mixed reliability)
2. **Finance:** 33.5% avg score, 31.6% avg empty (specialized domain challenge)
3. **Wikipedia:** 29.5% avg score, 17.1% avg empty (best retrieval quality)

**By Document Type:**
1. **Structured Academic Papers:** Best (7.7% empty)
2. **Government/Legal Docs:** Excellent (Supreme Court: 0% empty)
3. **Financial Tables:** Poor (PyPDF2 mangles tables)
4. **Sports Statistics:** Poor (numbers not in narrative text)

#### 💡 Technical Insights

1. **PDF Quality Matters Most:** Clean formatting > Domain knowledge
2. **Metric Choice Impacts Results:** Numeracy F1 (43.5%) vs Exact Match (23.4%) on similar data
3. **Document-Level Variance:** Same dataset can have 0-69% empty by document
4. **PyPDF2 Limitation:** Poor table extraction is a consistent problem
5. **Generic Embeddings:** MiniLM misses numerical/domain semantics

## 🚀 Phase 2: Optimization Plan (PLANNED 🔄)

### Goal
Reduce empty response rate and improve overall accuracy through systematic optimization.

### Planned Experiments

#### 1. Parameter Optimization
Test different RAG parameters on the hardest datasets (FinHybrid, NqText):

**TOP_K Sweep:**
- Values: 5 (baseline), 10, 15
- Hypothesis: More chunks = better retrieval coverage
- Target: Reduce empty rate by 10-15%

**CHUNK_SIZE Sweep:**
- Values: 1500, 3000 (baseline), 6000
- Hypothesis: Optimal size balances precision vs context
- Target: Reduce empty rate by 5-10%

**TEMPERATURE Sweep:**
- Values: 0.0, 0.1 (baseline), 0.3
- Hypothesis: Slightly higher temp = less conservative
- Target: Reduce empty rate by 3-5%

#### 2. Better PDF Parsing
Switch from PyPDF2 to specialized parsers:

**pdfplumber:**
- Better table extraction
- Preserves layout information
- Target datasets: FinHybrid, TatHybrid, FetaTab
- Expected improvement: 10-20% on table-heavy datasets

**camelot:**
- Specialized table extraction
- Multiple detection modes
- Target: Financial reports with complex tables

#### 3. Better Embeddings
Use paid, domain-specific embeddings:

**Together AI Embeddings:**
- Better semantic understanding
- Domain-aware representations
- Expected improvement: 5-10% overall

**Specialized Models:**
- Financial: FinBERT embeddings
- Academic: SciBERT embeddings
- Expected improvement: 10-15% on specialized domains

#### 4. Prompt Engineering
Improve prompt templates:

**Few-Shot Examples:**
- Add 2-3 examples per question type
- Expected improvement: 5-10%

**Chain-of-Thought:**
- Add reasoning steps
- Expected improvement: 3-5% (but longer, more expensive)

**Domain-Specific Prompts:**
- Financial jargon awareness
- Academic paper structure
- Expected improvement: 5-8%

### Success Metrics

**Primary Goal:** Reduce average empty rate from 24.4% → <15%  
**Secondary Goal:** Improve average score from 34.3% → >40%  
**Stretch Goal:** Match/exceed paper baseline results

### Estimated Resources

**Time:** 3-5 hours of experiment runtime  
**Cost:** $50-100 for parameter sweeps and optimization  
**Timeline:** 1-2 weeks for complete Phase 2

## 📈 Comparison to Baselines

### Sprint 2 (Clean Data Baseline)
- **Task:** Gemini 3.1 Pro on structured database
- **Format:** CSV, HTML, JSON, XML
- **Result:** 80% accuracy
- **Insight:** Clean structured data is MUCH easier

### Sprint 3 Phase 1 (PDF RAG)
- **Task:** Nemotron-3 Ultra on messy PDFs
- **Result:** 34.3% average accuracy
- **Insight:** RAG on real-world PDFs is 35-50% harder!

### Paper Baseline (UDA-Benchmark)
- **Model:** To be compared
- **Status:** Need to look up paper results
- **Purpose:** Validate our implementation

## 🔧 Technical Setup

### API Configuration
```python
# File: uda/utils/access_config.py
TOGETHER_API_KEY = "tgp_v1_9OcdTuqoXTB0_..."
TOGETHER_MODEL = "nvidia/nemotron-3-ultra-550b-a55b"
```

### Framework Integration
- **Preprocessing:** `uda/utils/preprocess.py`
- **Prompting:** `uda/utils/llm.py`
- **Evaluation:** `uda/eval/my_eval.py`
- **Datasets:** `dataset/qa/*.csv`, `dataset/src_doc_files_example/*/`

## 📚 Documentation

### Phase 1 Documentation
- **Complete Handoff:** `../../FINAL_SESSION_HANDOFF.md`
- **Session Summary:** `../../SESSION_SUMMARY.md`
- **Results Analysis:** `1_without_optimization/results_analysis/`
- **Experiment Structure:** `../../EXPERIMENT_STRUCTURE.md`

### Visualizations
Located in `1_without_optimization/results_analysis/`:
- `performance_comparison.png` - Dataset performance overview
- `domain_comparison.png` - Domain-level statistics
- `score_vs_empty_scatter.png` - Correlation analysis
- `document_level_analysis.png` - Per-document breakdown

## 🎓 Lessons Learned

### What Works Well
1. ✅ Clean, structured academic PDFs (7.7% empty)
2. ✅ Legal/government documents (Supreme Court: 0% empty)
3. ✅ Numeracy-aware evaluation (43.5% vs 23.4%)
4. ✅ Document filtering (process only available PDFs)
5. ✅ Diagnostic tracking (empty rate per document)

### What Needs Improvement
1. ❌ Table extraction (PyPDF2 mangles financial tables)
2. ❌ Empty response rate (24.4% is too high)
3. ❌ Generic embeddings (miss domain/numerical context)
4. ❌ Conservative generation (model too cautious)
5. ❌ Parameter optimization (used defaults)

### Critical Insights
1. **Empty responses > Wrong answers:** Focus on retrieval quality
2. **PDF quality > Domain knowledge:** Clean formatting helps more
3. **Metric matters:** Choose evaluation metric carefully
4. **Document variance:** Same dataset can vary wildly by document
5. **Baseline first:** Always establish baseline before optimizing

## 🔗 Quick Commands

### Run Phase 1 Experiments (Complete)
```bash
cd 1_without_optimization/{dataset}
jupyter notebook {dataset}_experiment.ipynb
```

### View Results
```bash
cd 1_without_optimization/results_analysis
jupyter notebook sprint3_results_visualization.ipynb
```

### Check Result Files
```bash
ls -lh 1_without_optimization/*/results/*.csv
```

---

**Model:** NVIDIA Nemotron-3 Ultra 550B  
**Phase 1:** COMPLETE ✅ (312 Q&A, 34.3% avg score)  
**Phase 2:** PLANNED 🔄 (optimization experiments)  
**Last Updated:** June 29, 2026
