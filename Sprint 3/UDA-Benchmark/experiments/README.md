# UDA-Benchmark Experiments - Model Comparison

This directory contains experiments organized by model for easy comparison and tracking.

## 📁 Directory Structure

```
experiments/
└── nemotron-3-ultra-550b/
    ├── 1_without_optimization/    ← Phase 1: Baseline results
    │   ├── tathybrid/
    │   ├── finhybrid/
    │   ├── nqtext/
    │   ├── fetatab/
    │   ├── papertext/
    │   ├── papertab/
    │   └── results_analysis/
    └── 2_optimization/            ← Phase 2: Optimized parameters
        └── (future optimization experiments)
```

## 🎯 Organization Philosophy

### Model-Based Organization
- **Top level:** Model name (e.g., `nemotron-3-ultra-550b/`)
- **Second level:** Experiment phase (baseline vs optimized)
- **Third level:** Dataset-specific experiments

### Why This Structure?
1. **Easy Model Comparison:** Add new models as siblings (e.g., `gpt-4-turbo/`, `claude-3-opus/`)
2. **Clear Phase Separation:** Baseline and optimization results don't mix
3. **Scalable:** Each model can have multiple optimization phases
4. **Organized Results:** All results for one model are together

## 📊 Current Status

### NVIDIA Nemotron-3 Ultra 550B

#### Phase 1: Without Optimization (COMPLETE ✅)
**Status:** All 6 datasets tested with baseline parameters

| Dataset | Q&A | Score | Empty% | Status |
|---------|-----|-------|--------|--------|
| TatHybrid | 162 | 43.5% Numeracy F1 | 22.8% | ✅ |
| FinHybrid | 47 | 23.4% Exact Match | 40.4% | ✅ |
| NqText | 78 | 27.6% Span F1 | 14.1% | ✅ |
| FetaTab | 8 | 31.3% Span F1 | ~20% | ✅ |
| PaperText | 13 | 43.0% Span F1 | 7.7% | ✅ |
| PaperTab | 4 | 38.0% Span F1 | 75% | ✅ |

**Total:** 312 Q&A pairs, Average Empty Rate: 24.4%

**Baseline Parameters:**
```python
CHUNK_SIZE = 3000
CHUNK_OVERLAP = 300
TOP_K = 5
TEMPERATURE = 0.1
MAX_TOKENS = 512
```

#### Phase 2: Optimization (PLANNED 🔄)
**Status:** Ready for optimization experiments

**Planned Optimizations:**
1. **Parameter Sweep:** TOP_K (10, 15), CHUNK_SIZE (1500, 6000), TEMPERATURE (0.0, 0.3)
2. **Better PDF Parsing:** Switch from PyPDF2 to pdfplumber/camelot
3. **Better Embeddings:** Use Together AI paid embeddings instead of MiniLM
4. **Prompt Engineering:** Few-shot examples, CoT prompting

## 🚀 How to Run Experiments

### Phase 1 (Baseline) - Already Complete
```bash
cd experiments/nemotron-3-ultra-550b/1_without_optimization/{dataset}
jupyter notebook {dataset}_experiment.ipynb
```

### Phase 2 (Optimization) - Coming Soon
```bash
cd experiments/nemotron-3-ultra-550b/2_optimization
# Future optimization notebooks will go here
```

## 📈 Adding New Models

To test a different model:

1. **Create model directory:**
   ```bash
   mkdir -p experiments/{model-name}/1_without_optimization
   mkdir -p experiments/{model-name}/2_optimization
   ```

2. **Copy baseline notebooks:**
   ```bash
   cp -r experiments/nemotron-3-ultra-550b/1_without_optimization/* \
         experiments/{model-name}/1_without_optimization/
   ```

3. **Update model configuration:**
   - Edit `uda/utils/access_config.py`
   - Change `TOGETHER_MODEL` or add new provider
   
4. **Update notebook paths:**
   - Update `project_root` path if needed
   - Update `OUTPUT_DIR` to new model directory

5. **Run experiments:**
   - Follow same procedure as Phase 1
   - Compare results across models

## 📚 Documentation

- **Phase 1 Results:** See `1_without_optimization/results_analysis/`
- **Comparison Analysis:** See `FINAL_SESSION_HANDOFF.md` in project root
- **Setup Guide:** See `SESSION_SUMMARY.md` in project root

## 🎓 Key Learnings from Phase 1

1. **Empty responses (24.4%)** are the main bottleneck, not wrong answers
2. **TatHybrid performs best** (43.5%) with numeracy-aware metric
3. **Academic papers work best** (7.7% empty) - clean, structured PDFs
4. **Financial tables struggle** - PyPDF2 mangles table extraction
5. **RAG is 35-50% harder** than clean structured data (vs Sprint 2)

## 🔗 Related Files

- **API Configuration:** `uda/utils/access_config.py`
- **Framework Code:** `uda/utils/preprocess.py`, `uda/utils/llm.py`, `uda/eval/my_eval.py`
- **Dataset Files:** `dataset/qa/*.csv`, `dataset/src_doc_files_example/*/`

---

**Last Updated:** June 29, 2026  
**Current Model:** NVIDIA Nemotron-3 Ultra 550B (via Together AI)  
**Status:** Phase 1 Complete, Phase 2 Planned
