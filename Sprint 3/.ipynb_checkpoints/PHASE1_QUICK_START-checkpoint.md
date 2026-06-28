# 🚀 Sprint 3 Phase 1 - Quick Start Guide

**Goal:** Run NVIDIA Nemotron-3 Ultra 550B on UDA-Benchmark example documents

---

## ⚡ Quick Start (3 Steps)

### **Step 1: Navigate to the notebook**
```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark"
```

### **Step 2: Open Jupyter**
```bash
jupyter notebook nemotron_phase1_experiment.ipynb
```

### **Step 3: Run all cells**
- Click: `Kernel` → `Restart & Run All`
- Grab a coffee ☕ (will take 1-2 hours)

---

## 📊 What Will Happen

The notebook will process **294 Q&A pairs** across **17 documents**:

| Dataset | Documents | Questions | Focus |
|---------|-----------|-----------|-------|
| FinHybrid | 4 | 47 | Financial reports |
| TatHybrid | 4 | 162 | Financial numerical reasoning |
| PaperTab | 2 | 2 | Academic paper tables |
| PaperText | 3 | 7 | Academic paper text |
| FetaTab | 2 | 6 | Wikipedia tables |
| NqText | 2 | 70 | Wikipedia factual Q&A |
| **TOTAL** | **17** | **294** | **71% financial** |

---

## 💰 Cost & Time

- **Time:** 1-2 hours (294 questions × ~15-25 seconds each)
- **Cost:** ~$10-20 in Together AI API credits
- **API Calls:** ~1,500 total (294 Q&A + 294 embeddings + retrieval)

---

## 📁 Output Files

After completion, you'll get:

```
Sprint 3/
├── phase1_results_[timestamp].csv      ← Individual Q&A results
│   Columns: question, response, doc, q_uid, answers, dataset
│
└── phase1_summary_[timestamp].csv      ← Aggregated metrics
    Columns: Dataset, Total_QA, Documents, Avg_Response_Length
```

Plus **real-time evaluation metrics** printed in the notebook output.

---

## 🎯 Expected Results

| Dataset | Expected Accuracy | Reasoning |
|---------|-------------------|-----------|
| FinHybrid | 70-85% | Nemotron's financial strength |
| TatHybrid | 65-80% | Numeracy-focused |
| NqText | 70-85% | Factual Wikipedia Q&A |
| PaperText | 65-80% | Academic text extraction |
| FetaTab | 60-75% | Wikipedia tables |
| PaperTab | 50-70% | Limited data (only 2 Q&A) |

**Overall Target:** 65-80% accuracy across all datasets

---

## 🔧 Configuration (Already Set)

The notebook uses these parameters (optimal defaults):

```python
CHUNK_SIZE = 3000        # Characters per chunk
CHUNK_OVERLAP = 300      # 10% overlap
TOP_K = 5                # Retrieved chunks per question
TEMPERATURE = 0.1        # Low = deterministic
MAX_TOKENS = 512         # Answer length limit
```

✅ Together AI API key: Already configured  
✅ Model: `nvidia/nemotron-3-ultra-550b-a55b`  
✅ Embedding model: `togethercomputer/m2-bert-80M-8k-retrieval`

---

## 📈 Progress Monitoring

The notebook shows real-time progress:

```
================================================================================
Starting experiment: FIN
================================================================================

Loaded 788 documents with Q&A pairs

[1] Processing: ADI_2009
    PDF: dataset/src_doc_files_example/fin_docs/ADI_2009.pdf
    Chunks: 141 (avg 437 words/chunk)
    Indexed: ✓
    Questions: 9
    Answering: 100%|██████████| 9/9 [00:45<00:00,  5.12s/it]

✓ Completed fin: 47 Q&A pairs processed

Evaluating fin...
Exact-match accuracy: 74.47
```

---

## ⚠️ Troubleshooting

### **Problem: ModuleNotFoundError**
```bash
# Install missing dependencies
pip install together langchain chromadb sentence-transformers PyPDF2 pandas tqdm
```

### **Problem: API Key Error**
```bash
# Check the API key is set correctly
cd UDA-Benchmark
cat uda/utils/access_config.py | grep TOGETHER_API_KEY
```

### **Problem: Rate Limiting**
The notebook includes `time.sleep(0.3)` between calls. If you hit rate limits, increase to `time.sleep(1.0)`.

---

## 🎉 After Phase 1 Completes

### **1. Review the results:**
```bash
# Open the CSV files
open phase1_results_*.csv
open phase1_summary_*.csv
```

### **2. Analyze the output:**
Look for:
- ✅ Which datasets Nemotron excels at
- ❌ Which question types it struggles with
- 🔍 Error patterns (similar to Sprint 2's "stale metadata" issue)

### **3. Create analysis document:**
Document findings in `PHASE1_BASELINE_RESULTS.md`:
- Overall accuracy by dataset
- Comparison with Sprint 2 (Gemini: 80% on structured data)
- Nemotron strengths/weaknesses
- Error categories

### **4. Decide next steps:**
- Run Phase 2 (parameter optimization)?
- Download full dataset for Phase 3?
- Test other models for comparison?

---

## 📞 Need Help?

If the notebook fails or you see errors:
1. Check the notebook output for error messages
2. Verify API key is working: `test with basic_demo_together.ipynb` first
3. Ensure all dependencies are installed
4. Check disk space (needs ~100 MB for temp ChromaDB indexes)

---

## 🎯 Success Criteria

Phase 1 is successful if:
- ✅ All 294 Q&A pairs processed without crashes
- ✅ Evaluation metrics calculated for each dataset
- ✅ Results saved to CSV files
- ✅ Overall accuracy ≥ 60% (reasonable baseline)
- ✅ FinHybrid + TatHybrid ≥ 70% (Nemotron's strength)

---

**Ready? Let's run Phase 1!** 🚀

```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark"
jupyter notebook nemotron_phase1_experiment.ipynb
```

Then: `Kernel` → `Restart & Run All` → Wait 1-2 hours → Analyze results!

---

**Created:** 2026-06-28  
**Status:** Ready to execute  
**Next:** Run the notebook and analyze results
