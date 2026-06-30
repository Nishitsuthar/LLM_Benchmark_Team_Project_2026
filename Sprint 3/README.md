# Sprint 3: RAG Optimization on UDA-Benchmark

**Duration:** June 2026  
**Status:** Complete  
**Team Member:** Nishit Suthar

---

## Objective

Optimize NVIDIA Nemotron-3 Ultra 550B performance on real-world document analysis using Retrieval Augmented Generation (RAG) and advanced prompting techniques on the UDA-Benchmark dataset.

---

## Goals

1. Establish Baseline: Test Nemotron on real financial/academic PDFs
2. Optimize RAG Pipeline: Tune hyperparameters (TOP_K, CHUNK_SIZE)
3. Advanced Prompting: Test Chain-of-Thought, Few-shot, Self-consistency
4. Achieve Target: Reduce empty responses to <12%

---

## Experiment Phases & Results

### Phase 1: Baseline Evaluation
Status: Complete  
Result: 35% empty response rate

- Scope: 312 Q&A pairs across 6 datasets
- Method: Zero-shot prompts, default parameters
- Finding: Poor performance - significant optimization needed

---

### Phase 2: Hyperparameter Optimization
Status: Complete  
Result: 16.7% empty response rate (18.3% improvement)

Variables Tested:
- TOP_K: 3, 5, 10 chunks - Optimal: 10
- CHUNK_SIZE: 500, 1000, 1500 characters - Optimal: 1500

Key Insight: Retrieving more, larger chunks significantly improves accuracy

---

### Phase 3A: PDFPlumber Extraction
Status: ABANDONED  
Result: No significant improvement

- Goal: Better PDF text extraction vs PyPDF2
- Finding: Added complexity without performance gain
- Decision: Stick with PyPDF2

---

### Phase 3B: FinBERT Domain Embeddings
Status: FAILED  
Result: 14.4% empty (REGRESSION from 12.2%)

- Goal: Domain-specific financial embeddings
- Model Used: `yiyanghkust/finbert-tone`
- Problem: Sentiment model (not retrieval model)
- Finding: Domain-specific not always better
- Lesson: Match model purpose to use case

---

### Phase 3C: Prompt Optimization
Status: COMPLETE (FINAL)  
Result: 12.2% empty response rate (4.5% improvement from Phase 2)

Overall Performance:
- Success Rate: 87.8% (274/312 questions answered)
- Empty Rate: 12.2% (38/312 questions)
- Target: <12% (missed by 0.2% / 2 questions)
- Total Improvement: 65% reduction from baseline (35% to 12.2%)

Prompting Techniques Tested:
1. Zero-shot baseline
2. Chain-of-Thought (CoT)
3. Few-shot with examples
4. Instruction prompting
5. Self-consistency

---

## Final Results by Dataset

| Dataset | Domain | Q&A | Empty | % Empty | Best Prompt | Status |
|---------|--------|-----|-------|---------|-------------|--------|
| NqText | Wikipedia | 71 | 3 | 4.2% | CoT | Excellent |
| FetaTab | Wiki Tables | 32 | 2 | 6.2% | CoT | Excellent |
| TatHybrid | Finance Tables | 162 | 20 | 12.3% | Few-shot | At target |
| FinHybrid | Finance Reports | 47 | 13 | 27.7% | CoT | Challenging |
| TOTAL | All | 312 | 38 | 12.2% | Mixed | Close |

---

## Methodology

### Experimental Design
- Baseline: Zero-shot prompts with default RAG parameters
- Phase 2: Systematic hyperparameter tuning (TOP_K, CHUNK_SIZE)
- Phase 3: Advanced optimization (PDF extraction, embeddings, prompts)
- Evaluation: 312 Q&A pairs across 6 datasets

### RAG Pipeline
1. Document ingestion and chunking
2. Embedding generation and vector storage
3. Query-based retrieval
4. LLM response generation
5. Accuracy evaluation

---

## Key Results

### Overall Performance
- Success Rate: 87.8% (274/312 questions answered)
- Empty Rate: 12.2% (38/312 questions)
- Total Improvement: 65% reduction from baseline (35% to 12.2%)

### Best Performing Configuration
- TOP_K: 10 chunks
- CHUNK_SIZE: 1500 characters
- EMBEDDING: all-MiniLM-L6-v2 (generic)
- PROMPTS: Chain-of-Thought for reasoning, Few-shot for extraction

### Results by Dataset
- NqText (Wikipedia): 4.2% empty - Excellent
- FetaTab (Wiki Tables): 6.2% empty - Excellent
- TatHybrid (Finance Tables): 12.3% empty - At target
- FinHybrid (Finance Reports): 27.7% empty - Challenging

---

## Key Learnings

### What Worked
1. Hyperparameter tuning: TOP_K=10 + CHUNK_SIZE=1500 gave 18.3% improvement
2. Chain-of-Thought prompting: Best for complex reasoning tasks
3. Few-shot prompting: Best for structured data extraction
4. Generic embeddings: all-MiniLM-L6-v2 outperformed domain-specific

### What Didn't Work
1. FinBERT embeddings: Wrong model type (sentiment vs retrieval)
2. PDFPlumber extraction: Complexity without benefit
3. Self-consistency: No significant improvement vs CoT
4. One prompt for all: Different datasets need different strategies

### Key Insights
1. Generic embeddings can beat domain-specific models
2. Format differences matter: FinHybrid 4x harder than NqText
3. Diminishing returns: Phase 2 to 3 only gained 4.5%
4. 12.2% likely near model's practical limit for this benchmark

---

## Next Steps

1. Break 12% ceiling: Try hybrid search (semantic + keyword)
2. Test other models: GPT-4, Claude, Gemini for comparison
3. Full dataset: Scale to all 29,590 Q&A pairs
4. Fine-tuning: Train embeddings on domain data
5. Query expansion: Rephrase questions multiple ways
