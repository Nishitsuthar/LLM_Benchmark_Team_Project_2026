# LLM Benchmark Team Project 2026

**Project Duration:** April - June 2026  
**Team:** LLM Benchmark Research Team  
**Team Member:** Nishit Suthar  
**GitHub:** https://github.com/Nishitsuthar/LLM_Benchmark_Team_Project_2026

---

## 📋 Project Overview

Comprehensive benchmarking study evaluating Large Language Model (LLM) performance across multiple data formats, document types, and optimization techniques. The project spans three sprints, progressing from data preparation through structured data benchmarking to advanced RAG optimization.

---

## 🎯 Project Objectives

1. **Establish LLM Baselines:** Measure LLM performance on tabular and document analysis
2. **Format Comparison:** Identify optimal data formats for LLM processing
3. **RAG Optimization:** Optimize Retrieval Augmented Generation pipelines
4. **Methodology Development:** Create reusable benchmarking frameworks
5. **Practical Insights:** Provide actionable recommendations for LLM deployment

---

## 📈 Quick Progress Summary

| Sprint | Focus | Status | Key Metric | Achievement |
|--------|-------|--------|------------|-------------|
| **[Sprint 1](#sprint-1-data-preparation--sampling)** | Data Preparation | ✅ Complete | 870 movies | Sampled & formatted |
| **[Sprint 2](#sprint-2-llm-format-comparison-benchmark)** | Format Benchmark | ✅ Complete | 80% accuracy | JSON best format |
| **[Sprint 3](#sprint-3-rag-optimization-on-uda-benchmark)** | RAG Optimization | ✅ Complete | 87.8% success | 65% improvement |

**Overall:** 3/3 Sprints Complete | All Objectives Met | Production-Ready Results

---

## 🚀 Sprint Summaries

### Sprint 1: Data Preparation & Sampling

**📁 Directory:** [`Sprint 1/`](./Sprint%201/) | **[Full README](./Sprint%201/README.md)**

**Objective:** Prepare movie dataset for LLM benchmarking

**Key Deliverables:**
- 870 sampled movie records
- Multiple formats: CSV, Excel, Unstructured Text
- Cast/crew enrichment
- Quality validation

**Outputs:**
- `Sampled_870_Movies.csv` - Structured data
- `Final_Movies_With_Cast.xlsx` - Enriched dataset  
- `Unstructured_870_Movies.txt` - Natural language format
- Python sampling and merging scripts

**Status:** ✅ Complete

---

### Sprint 2: LLM Format Comparison Benchmark

**📁 Directory:** [`Sprint 2/`](./Sprint%202/) | **[Full README](./Sprint%202/README.md)**

**Objective:** Benchmark Google Gemini 3.1 Pro Extended across data formats

**Test Configuration:**
- **Model:** Google Gemini 3.1 Pro Extended
- **Formats:** CSV, HTML, JSON, XML
- **Questions:** 20 (Medium, Hard, Extremely Hard)
- **Modes:** Batch (all questions) + Individual (one at a time)

**Key Results:**

**Batch Mode:**
- **JSON:** 80% accuracy ✅ (WINNER)
- **HTML:** 70% accuracy
- **XML:** 65% accuracy  
- **CSV:** 55% accuracy

**Individual Mode:**
- **All Formats:** 80% accuracy (format-agnostic ceiling)

**Key Findings:**
1. JSON 45% better than CSV in batch mode
2. Individual mode eliminates format differences
3. 80% accuracy ceiling for zero-shot prompting
4. Context window size critical for performance

**Visualizations:**
- Benchmark comparison charts
- Difficulty distribution analysis
- Format performance heatmaps

**Status:** ✅ Complete

---

### Sprint 3: RAG Optimization on UDA-Benchmark

**📁 Directory:** [`Sprint 3/`](./Sprint%203/) | **[Full README](./Sprint%203/README.md)**

**Objective:** Optimize NVIDIA Nemotron-3 Ultra 550B on real-world documents using RAG

**Test Configuration:**
- **Model:** NVIDIA Nemotron-3 Ultra 550B (via Together AI)
- **Benchmark:** UDA-QA (financial reports, academic papers, Wikipedia)
- **Scope:** 312 Q&A pairs across 6 datasets
- **Optimization:** 5 phases testing hyperparameters and prompts

**Experiment Phases:**

| Phase | Focus | Result | Status |
|-------|-------|--------|--------|
| **Phase 1** | Baseline | 35% empty | ✅ Complete |
| **Phase 2** | Hyperparameters | 16.7% empty (↓18.3%) | ✅ Complete |
| **Phase 3A** | PDFPlumber | No improvement | ❌ Abandoned |
| **Phase 3B** | FinBERT | 14.4% empty (regression) | ❌ Failed |
| **Phase 3C** | Prompts | **12.2% empty** (↓4.5%) | ✅ FINAL |

**Final Results:**
- **Success Rate:** 87.8% (274/312 questions)
- **Empty Rate:** 12.2% (38/312 questions)
- **Improvement:** 65% reduction from baseline
- **Cost:** $0.048 per question

**Performance by Dataset:**
- NqText (Wikipedia): 4.2% empty ✅
- FetaTab (Tables): 6.2% empty ✅
- TatHybrid (Finance): 12.3% empty ⚠️
- FinHybrid (Complex): 27.7% empty ❌

**Optimal Configuration:**
```python
TOP_K = 10                    # Retrieve 10 chunks
CHUNK_SIZE = 1500             # 1500 characters per chunk
EMBEDDING = "all-MiniLM-L6-v2"  # Generic embeddings
PROMPTS = {
    "complex_reasoning": "Chain-of-Thought",
    "extraction_tasks": "Few-shot with examples"
}
```

**Key Learnings:**
1. Hyperparameter tuning crucial (18.3% improvement)
2. Dataset-specific prompts essential (no universal solution)
3. Generic embeddings beat domain-specific (FinBERT failed)
4. Diminishing returns beyond Phase 2

**Deliverables:**
- 7 presentation visuals (300 DPI)
- 6 custom Claude Code skills
- Comprehensive documentation
- Clean, organized structure

**Status:** ✅ Complete

---

## 📊 Project-Wide Metrics

### Models Tested
1. **Google Gemini 3.1 Pro Extended** (Sprint 2)
2. **NVIDIA Nemotron-3 Ultra 550B** (Sprint 3)

### Data Coverage
- **Structured Data:** 567 records, 12 tables (Sprint 2)
- **Unstructured Documents:** 312 Q&A, 6 datasets (Sprint 3)
- **Total Test Cases:** 80 (Sprint 2) + 2,855 (Sprint 3) = 2,935

### Cost Efficiency
- **Sprint 2:** ~$10 (80 tests)
- **Sprint 3:** ~$138 (2,855 tests)
- **Total:** ~$148 for comprehensive benchmarking

### Performance Achievements
- **Structured Data:** 80% accuracy (JSON format)
- **Document RAG:** 87.8% success rate (optimized)
- **Improvement:** 65% reduction in failures (Sprint 3)

---

## 🔑 Key Insights Across Sprints

### 1. Format Matters (Sprint 2)
- JSON superior for batch processing (+45% vs CSV)
- Format differences vanish in individual mode
- Context window size determines format impact

### 2. RAG Optimization Critical (Sprint 3)
- Hyperparameters: 18.3% improvement
- Prompting strategies: 4.5% improvement
- Total optimization: 65% improvement

### 3. Model-Specific Behavior
- **Gemini:** Strong on structured data (80% ceiling)
- **Nemotron:** Excellent on documents with RAG (87.8%)
- Both benefit from optimization

### 4. Practical Recommendations
- **For tabular data:** Use JSON, test individually
- **For documents:** Optimize RAG (TOP_K=10, CHUNK_SIZE=1500)
- **For prompts:** Match strategy to task (CoT vs Few-shot)
- **For embeddings:** Start with generic, test domain-specific

---

## 📁 Repository Structure

```
LLM_Benchmark_Team_Project_2026/
├── README.md (this file)
│
├── Sprint 1/ (Data Preparation)
│   ├── README.md
│   ├── Sampled_870_Movies.csv
│   ├── Final_Movies_With_Cast.xlsx
│   ├── Unstructured_870_Movies.txt
│   └── Scripts (sample_movies.py, merge_cast.py, etc.)
│
├── Sprint 2/ (Format Comparison)
│   ├── README.md
│   ├── synthetic_data_from_LLM/ (12 CSV tables)
│   ├── Visualizations/
│   └── Sprint2_Presentation_Nishit_Suthar.pptx
│
├── Sprint 3/ (RAG Optimization)
│   ├── README.md
│   ├── documentation/ (planning, results, presentation)
│   ├── notebooks/ (demos + archives)
│   ├── scripts/ (utilities)
│   ├── results/ (archived data)
│   └── UDA-Benchmark/
│       ├── presentation_visuals/ (7 charts)
│       └── experiments/ (notebooks + results)
│
└── .claude/
    └── skills/ (6 custom Sprint 3 skills)
```

---

## 🎓 Academic Contributions

### Methodologies Developed
1. **Multi-format LLM benchmarking** (Sprint 2)
2. **Systematic RAG optimization** (Sprint 3)
3. **Dataset-specific prompt selection** (Sprint 3)
4. **Cost-effective testing strategies** (all sprints)

### Reusable Frameworks
- Format comparison test harness
- RAG parameter tuning methodology
- Prompt strategy selection guidelines
- Quality validation procedures

### Open Questions for Future Research
1. Can we break the 12% empty response ceiling?
2. Do results generalize to other LLM models?
3. How does fine-tuning compare to prompt optimization?
4. What's the optimal balance between cost and performance?

---

## 🚀 Quick Start

### Navigate by Sprint
- **Sprint 1:** [`cd "Sprint 1"` → See README](./Sprint%201/README.md)
- **Sprint 2:** [`cd "Sprint 2"` → See README](./Sprint%202/README.md)
- **Sprint 3:** [`cd "Sprint 3"` → See README](./Sprint%203/README.md)

### View Key Results
- **Sprint 2 Results:** `Sprint 2/comprehensive_benchmark_analysis.png`
- **Sprint 3 Results:** `Sprint 3/documentation/2_final_results/FINAL_RESULTS_PHASE3C.md`
- **Sprint 3 Visuals:** `Sprint 3/UDA-Benchmark/presentation_visuals/`

### Run Experiments
- **Sprint 2:** See `Sprint 2/README.md` for dataset access
- **Sprint 3 Demo:** `Sprint 3/notebooks/demos/basic_demo_together.ipynb`
- **Sprint 3 Final:** `Sprint 3/UDA-Benchmark/experiments/.../3_prompts/notebooks/`

---

## 📊 Presentation Materials

### Sprint 2
- **PowerPoint:** `Sprint 2/Sprint2_Presentation_Nishit_Suthar.pptx`
- **Charts:** `Sprint 2/` (PNG visualizations)

### Sprint 3
- **Presentation Guide:** `Sprint 3/documentation/3_presentation/PRESENTATION_GUIDE.md`
- **Executive Summary:** `Sprint 3/documentation/3_presentation/PRESENTATION_SUMMARY.md`
- **7 High-Res Charts:** `Sprint 3/UDA-Benchmark/presentation_visuals/`

---

## 🛠️ Technologies Used

### LLM Models
- Google Gemini 3.1 Pro Extended
- NVIDIA Nemotron-3 Ultra 550B (via Together AI)

### Frameworks & Libraries
- LangChain (RAG pipeline)
- ChromaDB (vector storage)
- Sentence-Transformers (embeddings)
- PyPDF2 (PDF extraction)
- Pandas (data processing)

### Infrastructure
- NeonDB (PostgreSQL) for ground truth
- Together AI API (model access)
- Jupyter Notebooks (experiments)

---

## 🏆 Project Achievements

✅ **3 Comprehensive Sprints** completed on schedule  
✅ **2 LLM Models** benchmarked (Gemini, Nemotron)  
✅ **4 Data Formats** compared (CSV, HTML, JSON, XML)  
✅ **2,935 Total Tests** conducted  
✅ **87.8% Success Rate** achieved on RAG  
✅ **65% Improvement** through optimization  
✅ **13 Visualizations** created  
✅ **6 Custom Skills** developed  
✅ **Professional Documentation** for all sprints  

---

## 📅 Timeline

- **April 2026:** Sprint 1 - Data Preparation
- **May 2026:** Sprint 2 - Format Comparison
- **June 2026:** Sprint 3 - RAG Optimization

**Total Duration:** 3 months  
**Status:** ✅ All Sprints Complete

---

## 🔮 Future Work

1. **Model Expansion:** Test GPT-4, Claude, Llama models
2. **Format Extension:** Test more formats (Parquet, Avro, Protocol Buffers)
3. **Scale Up:** Test on full UDA-QA dataset (29,590 Q&A)
4. **Fine-Tuning:** Train custom models on domain data
5. **Hybrid Approaches:** Combine RAG with fine-tuning
6. **Real-World Deployment:** Production testing and monitoring

---

**Last Updated:** June 30, 2026  
**Project Status:** ✅ Complete & Production-Ready  
**Repository:** https://github.com/Nishitsuthar/LLM_Benchmark_Team_Project_2026

---

**🎉 Thank you for exploring the LLM Benchmark Team Project 2026!**

For detailed information about each sprint, please see the individual README files in each sprint directory.
