# LLM Benchmark Team Project 2026

**Project Duration:** April - August 2026  
**Team:** LLM Benchmark Research Team  
**Team Member:** Nishit Suthar  
**GitHub:** https://github.com/Nishitsuthar/LLM_Benchmark_Team_Project_2026

---

## Project Overview

Comprehensive benchmarking study evaluating Large Language Model (LLM) performance across multiple data formats, document types, and optimization techniques. The project spans five sprints from April to August 2026, progressing from data preparation through structured data benchmarking to advanced RAG optimization.

---

## Project Objectives

1. Establish LLM Baselines: Measure LLM performance on tabular and document analysis
2. Format Comparison: Identify optimal data formats for LLM processing
3. RAG Optimization: Optimize Retrieval Augmented Generation pipelines
4. Methodology Development: Create reusable benchmarking frameworks
5. Practical Insights: Provide actionable recommendations for LLM deployment

---

## Progress Summary

| Sprint | Focus | Status |
|--------|-------|--------|
| [Sprint 1](./Sprint%201/README.md) | Data Preparation & Sampling | Complete |
| [Sprint 2](./Sprint%202/README.md) | LLM Format Comparison Benchmark | Complete |
| [Sprint 3](./Sprint%203/README.md) | RAG Optimization on UDA-Benchmark | Complete |
| Sprint 4 | Planning Phase | Pending |
| Sprint 5 | Planning Phase | Pending |

Completed: 3/5 Sprints

For detailed information about each sprint, see the individual README files linked above.

---

## Key Results Summary

### Sprint 1: Data Preparation
- 870 movie records sampled and formatted
- Multiple formats: CSV, Excel, Unstructured Text
- [Full Details](./Sprint%201/README.md)

### Sprint 2: Format Comparison
- Model: Google Gemini 3.1 Pro Extended
- Best Format: JSON (80% accuracy in batch mode)
- Key Finding: All formats achieve 80% in individual mode
- [Full Details](./Sprint%202/README.md)

### Sprint 3: RAG Optimization
- Model: NVIDIA Nemotron-3 Ultra 550B
- Success Rate: 87.8% (65% improvement from baseline)
- Optimal Config: TOP_K=10, CHUNK_SIZE=1500
- [Full Details](./Sprint%203/README.md)

---

## Repository Structure

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
```

---

## Technologies Used

- LLM Models: Google Gemini 3.1 Pro Extended, NVIDIA Nemotron-3 Ultra 550B
- RAG Framework: LangChain, ChromaDB, Sentence-Transformers
- Data Processing: Pandas, PyPDF2
- Infrastructure: NeonDB (PostgreSQL), Together AI API, Jupyter Notebooks

---

## Credits & References

### Datasets & Benchmarks

**UDA-QA Benchmark**
- Paper: "UDA: A Benchmark Suite for Retrieval Augmented Generation in Real-world Document Analysis"
- Authors: Jialie Zeng, Yucheng Xu, Xiaoyu Zhang, et al.
- Source: [UDA-QA GitHub Repository](https://github.com/qinchuanhui/UDA-QA)
- Usage: Sprint 3 RAG optimization experiments

**MovieLens Dataset**
- Source: GroupLens Research
- Usage: Sprint 1 data preparation and sampling

### Frameworks & Libraries

**LangChain**
- Purpose: RAG pipeline implementation
- Website: https://langchain.com
- Usage: Document processing, retrieval, and LLM integration (Sprint 3)

**ChromaDB**
- Purpose: Vector database for embeddings
- Website: https://www.trychroma.com
- Usage: Semantic search and retrieval (Sprint 3)

**Sentence-Transformers**
- Paper: "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"
- Authors: Nils Reimers and Iryna Gurevych
- Model Used: all-MiniLM-L6-v2
- Usage: Document embeddings (Sprint 3)

### LLM Models

**Google Gemini 3.1 Pro Extended**
- Provider: Google AI
- Usage: Format comparison benchmark (Sprint 2)

**NVIDIA Nemotron-3 Ultra 550B**
- Provider: NVIDIA (via Together AI)
- Usage: RAG optimization on document analysis (Sprint 3)

### Tools & Infrastructure

**NeonDB**
- Purpose: Serverless PostgreSQL database
- Usage: Ground truth validation (Sprint 2)

**Together AI**
- Purpose: LLM API access
- Usage: NVIDIA Nemotron model deployment (Sprint 3)

---

## Timeline

- April 2026: Sprint 1 - Data Preparation
- May 2026: Sprint 2 - Format Comparison
- June 2026: Sprint 3 - RAG Optimization
- July 2026: Sprint 4 - Planning Phase
- August 2026: Sprint 5 - Planning Phase

Total Project Duration: 5 months (April - August 2026)  
Completed Sprints: 3/5

---

**Repository:** https://github.com/Nishitsuthar/LLM_Benchmark_Team_Project_2026

---

For detailed information about each sprint, please see the individual README files in each sprint directory.
