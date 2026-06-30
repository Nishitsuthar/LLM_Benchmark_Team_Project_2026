# UDA-Benchmark Experiments

**Sprint 3:** NVIDIA Nemotron-3 Ultra 550B on UDA-QA Benchmark

This directory contains organized experiments for all 6 UDA-Benchmark datasets.

---

## 📁 Directory Structure

```
experiments/
├── README.md                  ← You are here
├── finhybrid/                 ← Financial reports (Exact Match)
│   ├── finhybrid_experiment.ipynb
│   └── results/
├── tathybrid/                 ← Financial reports (Numeracy F1)
│   ├── tathybrid_experiment.ipynb
│   └── results/
├── nqtext/                    ← Wikipedia (Span F1)
│   ├── nqtext_experiment.ipynb
│   └── results/
├── fetatab/                   ← Wikipedia tables (Span F1)
│   ├── fetatab_experiment.ipynb
│   └── results/
├── papertab/                  ← Academic papers - tables (Span F1)
│   ├── papertab_experiment.ipynb
│   └── results/
└── papertext/                 ← Academic papers - text (Span F1)
    ├── papertext_experiment.ipynb
    └── results/
```

---

## 📊 Datasets Overview

| Dataset | Domain | Docs | Metric | Status | Expected Accuracy |
|---------|--------|------|--------|--------|-------------------|
| **FinHybrid** | Finance | 4 | Exact Match ±1% | ✅ Tested | 70-85% |
| **TatHybrid** | Finance | 4 | Numeracy F1 | ⏳ Pending | 65-80% |
| **NqText** | Wikipedia | 4 | Span F1 | ⚠️ Partial | 70-85% |
| **FetaTab** | Wikipedia | 4 | Span F1 | ❌ Not tested | 60-75% |
| **PaperTab** | Academia | 7 | Span F1 | ❌ Not tested | 60-75% |
| **PaperText** | Academia | 7 | Span F1 | ❌ Not tested | 65-80% |

**Total:** 29 example documents (full dataset has 29,590 Q&A pairs)

---

## 🚀 Quick Start

### 1. **Choose a dataset** and navigate to its directory:

```bash
cd experiments/finhybrid     # Financial reports (Exact Match)
cd experiments/tathybrid     # Financial reports (Numeracy F1)
cd experiments/nqtext        # Wikipedia factual Q&A
cd experiments/fetatab       # Wikipedia tables
cd experiments/papertab      # Academic papers - tables
cd experiments/papertext     # Academic papers - text
```

### 2. **Open the notebook:**

```bash
jupyter notebook finhybrid_experiment.ipynb   # or corresponding notebook
```

### 3. **Run all cells** to process the entire dataset

---

## 🔧 Configuration

All notebooks use the same baseline parameters:

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Model** | `nvidia/nemotron-3-ultra-550b-a55b` | Via Together AI |
| **Chunk Size** | 3000 characters | Can be varied: 1500, 6000 |
| **Chunk Overlap** | 300 characters | 10% overlap |
| **Top-K** | 5 | Can be varied: 3, 10, 15 |
| **Temperature** | 0.1 | Low for factual accuracy |
| **Max Tokens** | 512 | Sufficient for most answers |
| **Embedding** | `all-MiniLM-L6-v2` | Local, free |

### API Configuration

API keys are configured in: `../../uda/utils/access_config.py`

```python
TOGETHER_API_KEY = "tgp_v1_..."
TOGETHER_MODEL = "nvidia/nemotron-3-ultra-550b-a55b"
```

---

## 📈 Current Results (Phase 1)

### FinHybrid (Complete)
- **Accuracy:** 23.4% (Expected: 70-85%) ❌
- **Empty responses:** 40.4%
- **Q&A processed:** 47/47
- **Docs:** 4/4 (ADI_2009, ABMD_2012, GS_2016, JKHY_2015)

### NqText (Partial)
- **F1 Score:** 24.8% (Expected: 70-85%) ❌
- **Empty responses:** 17.3%
- **Q&A processed:** 52/71
- **Docs:** 3/4 (Supreme Court, Tour de France, Hannah John-Kamen)

### Key Findings
1. **Performance below expectations** - 20-25% vs expected 70-85%
2. **High empty response rate** - Model is overly conservative
3. **Wikipedia easier than financial** - Lower empty rate (17% vs 40%)
4. **RAG pipeline issues** - Context retrieval or prompt engineering needed

---

## 🎯 Experiment Workflows

### Standard Workflow (each notebook)

1. **Load Q&A data** - Read questions and ground truth
2. **Process each document:**
   - Extract PDF text
   - Chunk into 3000-character segments
   - Build ChromaDB vector index
   - For each question:
     - Retrieve top-5 relevant chunks
     - Generate answer with Nemotron
     - Store result
3. **Evaluate** - Automatic metric calculation
4. **Save results** - CSV with all Q&A pairs
5. **Statistics** - Empty rate, answer length, accuracy

### Expected Runtime

| Dataset | Q&A Count | Runtime (est.) | Cost (est.) |
|---------|-----------|----------------|-------------|
| FinHybrid | 47 | 15-20 min | $3-5 |
| TatHybrid | ~150 | 45-60 min | $10-15 |
| NqText | 71 | 25-30 min | $5-8 |
| FetaTab | ~10 | 5-10 min | $2-3 |
| PaperTab | ~5 | 3-5 min | $1-2 |
| PaperText | ~10 | 5-10 min | $2-3 |

**Total: ~90-135 min, $23-36**

---

## 🔬 Parameter Optimization

After baseline testing, try optimizing these parameters:

### Chunk Size
```python
CHUNK_SIZE = 1500  # Smaller, more focused chunks
CHUNK_SIZE = 3000  # Default baseline
CHUNK_SIZE = 6000  # Larger, capture full tables
```

### Top-K Retrieval
```python
TOP_K = 3   # Less context, faster
TOP_K = 5   # Default baseline
TOP_K = 10  # More context, may help
TOP_K = 15  # Maximum context
```

### Temperature
```python
TEMPERATURE = 0.0   # Deterministic
TEMPERATURE = 0.1   # Default baseline
TEMPERATURE = 0.3   # More creative
```

### Embedding Model
```python
# Current: Local free
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Alternative: Together AI (paid, better)
# See basic_demo_together.ipynb for implementation
```

---

## 📝 Output Files

Each experiment saves results to:

```
experiments/{dataset}/results/{dataset}_results_{timestamp}.csv
```

**CSV Columns:**
- `question` - The question asked
- `response` - Model's answer
- `doc` - Source document name
- `q_uid` - Question unique ID
- `answers` - Ground truth (JSON)
- `dataset` - Dataset code (fin, tat, nq, etc.)

---

## 🔍 Debugging Poor Performance

If accuracy is low (<30%), check:

1. **Empty response rate** - High rate suggests retrieval issues
   - Try increasing `TOP_K` to 10 or 15
   - Try smaller `CHUNK_SIZE` (1500)

2. **Wrong answers** - Model sees context but extracts incorrectly
   - Check prompt template in `uda/utils/llm.py`
   - Try different `temperature` (0.0 for deterministic)

3. **PDF extraction quality** - Tables may not parse well
   - Check `pdf_text` variable in notebook
   - Consider alternative PDF parsers (pdfplumber, camelot)

4. **Embedding quality** - May not capture financial/technical terms
   - Try Together AI embeddings (paid but better)
   - Try domain-specific embeddings

---

## 🎓 Dataset Characteristics

### Financial (FinHybrid, TatHybrid)
- **Hardest**: Complex calculations, multi-table joins
- **Challenge**: Table extraction from PDFs
- **Empty rate**: 17-40% (highest)
- **Strategy**: Increase context (TOP_K=10), smaller chunks (1500)

### Wikipedia (NqText, FetaTab)
- **Easiest**: Factual answers, cleaner text
- **Challenge**: Long documents (Supreme Court: 57 Q&A)
- **Empty rate**: 17% (lowest)
- **Strategy**: Default parameters should work well

### Academic (PaperTab, PaperText)
- **Medium**: Technical jargon, dense content
- **Challenge**: Small sample size (2-7 docs)
- **Empty rate**: Unknown (not tested)
- **Strategy**: Test with defaults first

---

## 📚 References

- **Paper:** [UDA: A Benchmark Suite for RAG](https://arxiv.org/abs/2406.15187)
- **Dataset:** [HuggingFace - qinchuanhui/UDA-QA](https://huggingface.co/datasets/qinchuanhui/UDA-QA)
- **Code:** [GitHub - qinchuanhui/UDA-Benchmark](https://github.com/qinchuanhui/UDA-Benchmark)
- **Model:** [Together AI - Nemotron](https://docs.together.ai/docs/nemotron-models)

---

## ✅ Checklist

### Phase 1: Baseline (Current)
- [x] FinHybrid complete (47 Q&A)
- [x] NqText partial (52/71 Q&A)
- [ ] TatHybrid (4 docs)
- [ ] FetaTab (4 docs)
- [ ] PaperTab (7 docs)
- [ ] PaperText (7 docs)

### Phase 2: Optimization (Future)
- [ ] Parameter sweep (chunk_size × top_k)
- [ ] Better embeddings (Together AI)
- [ ] Prompt engineering
- [ ] Alternative models (GPT-4, Claude)

### Phase 3: Full Dataset (Future)
- [ ] Download full UDA-QA (29,590 Q&A)
- [ ] Run comprehensive evaluation
- [ ] Compare with paper baselines

---

## 🤝 Contributing

To add a new experiment configuration:

1. Edit `create_all_notebooks.py`
2. Add new dataset to `DATASETS` dict
3. Run: `python3 create_all_notebooks.py`

---

**Created:** 2026-06-29  
**Status:** Phase 1 in progress (2/6 datasets tested)  
**Next:** Complete remaining datasets, then optimize parameters
