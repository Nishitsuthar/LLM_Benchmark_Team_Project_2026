# Phase 3B: ABANDONED - FinBERT Experiment Results

**Date:** June 30, 2026  
**Status:** ❌ ABANDONED - Regression observed  
**Decision:** Stick with Phase 3C (Generic Embeddings)

---

## Executive Summary

Phase 3B attempted to improve performance on financial datasets (FinHybrid, TatHybrid) by using FinBERT embeddings instead of generic embeddings. **The experiment failed**, showing a **14.9% performance regression** on FinHybrid.

**Final Decision:** Accept Phase 3C results (12.2% empty) as the final baseline.

---

## Results Comparison

| Metric | Phase 3C (Baseline) | Phase 3B (FinBERT) | Change |
|--------|---------------------|-------------------|---------|
| **FinHybrid empty** | 13/47 (27.7%) | 20/47 (42.6%) | **-7 questions** ❌ |
| **Overall impact** | 38/312 (12.2%) | 45/312 (14.4%) | **+2.2%** ❌ |
| **Questions improved** | - | 4 | 📈 |
| **Questions regressed** | - | 11 | 📉 |
| **Net change** | - | **-7 questions** | ❌ |

**Conclusion:** FinBERT made performance significantly worse, not better.

---

## Root Cause Analysis

### Wrong Model Selection

**Model Used:** `yiyanghkust/finbert-tone`

**The Problem:**
- ✅ Good for: Sentiment analysis (positive/negative/neutral classification)
- ❌ Bad for: Semantic search and RAG retrieval
- Embeddings optimized for **sentiment**, not **semantic similarity**

**Warning Sign (Ignored):**
```
WARNING: No sentence-transformers model found with name yiyanghkust/finbert-tone. 
Creating a new one with mean pooling.
```

This warning indicated the model was **not** a proper sentence-transformer model and was being adapted on-the-fly with basic mean pooling, creating suboptimal embeddings.

---

## What Went Wrong

### Hypothesis vs Reality

**Hypothesis:**
- Domain-specific embeddings (financial) would understand financial terminology better
- Better retrieval → Better LLM answers
- Expected: +2-4 questions answered

**Reality:**
- Sentiment model doesn't capture semantic meaning well
- Worse retrieval → Worse LLM answers
- Actual: -7 questions answered (regression)

### Question-by-Question Breakdown

**Stayed Answered:** 23/47 (48.9%)  
**Stayed Empty:** 9/47 (19.1%)  
**Got Better (empty → answered):** 4/47 (8.5%)  
**Got Worse (answered → empty):** 11/47 (23.4%) ❌

**Net Effect:** Lost 7 questions (11 - 4 = 7)

---

## Examples of Regression

Questions that **Phase 3C answered correctly** but **Phase 3B failed on:**

1. ❌ "what is the percentage increase in interest expense and penalties in 2009?"
2. ❌ "what percentage did the balance increase from 2007 to 2009?"
3. ❌ "what is the roi of an investment in abiomed inc from march 2007 to march 2010?"
4. ❌ "what percentage of total long-term assets under supervision are comprised of fixed income?"

All of these are **financial calculation questions** that require finding specific numbers and performing math - exactly the kind of questions where better retrieval should have helped, but instead got worse.

---

## Technical Details

### Embedding Comparison

**Phase 3C (Generic):**
- Model: `sentence-transformers/all-MiniLM-L6-v2`
- Dimension: 384
- Training: General web text, optimized for semantic similarity
- Use case: General-purpose retrieval ✅

**Phase 3B (FinBERT):**
- Model: `yiyanghkust/finbert-tone`
- Dimension: 768
- Training: Financial texts, optimized for sentiment classification
- Use case: Sentiment analysis (positive/negative/neutral) ❌ Wrong use case!

### ChromaDB Integration Issues Fixed

During implementation, we fixed a critical ChromaDB compatibility issue:
- **Issue:** `embed_query()` was returning wrong type
- **Fix:** Changed to delegate to `__call__()` (returns `List[np.ndarray]`)
- **Result:** ChromaDB integration working correctly

The technical implementation was correct - the model choice was wrong.

---

## Lessons Learned

### 1. Domain-Specific ≠ Always Better

Just because a model is trained on financial data doesn't mean it's better for all financial tasks:
- FinBERT-tone: Financial sentiment analysis
- Need: Financial semantic search

**Wrong tool for the job.**

### 2. Model Purpose Matters

Embedding models are optimized for specific tasks:
- **Sentiment models:** Separate positive from negative text
- **Retrieval models:** Find semantically similar text
- **Classification models:** Group similar categories

**Always check the model's training objective before using it.**

### 3. Warnings Are Red Flags

The warning message should have been investigated more carefully:
```
WARNING: No sentence-transformers model found...
Creating a new one with mean pooling.
```

This indicated the model wasn't designed for sentence-transformers usage.

### 4. Test on Small Samples First

We could have saved time by testing on 5-10 questions first before running the full 47-question experiment.

---

## Alternative Approaches (Not Pursued)

If we wanted to continue optimizing, better alternatives would be:

### Better Embedding Models
1. **ProsusAI/finbert** - General financial understanding (not sentiment)
2. **sentence-transformers/all-mpnet-base-v2** - Better general model (768-dim)
3. **BAAI/bge-large-en-v1.5** - State-of-art retrieval (1024-dim)

### Other Optimization Strategies
1. **Query expansion** - Rephrase questions multiple ways
2. **Hybrid search** - Combine semantic + keyword search
3. **Chunk size tuning** - Try different chunk sizes per dataset
4. **Reranking** - Use a reranker model after initial retrieval

**Decision:** Not worth the time investment for marginal potential gains.

---

## Final Recommendation

**✅ ACCEPT Phase 3C as Final Results**

**Rationale:**
1. **Already close to target:** 12.2% vs 12.0% target (only 0.2% away)
2. **Strong performance:** 274/312 questions answered (87.8% success)
3. **Diminishing returns:** Further optimization unlikely to yield significant gains
4. **Time/cost trade-off:** Better to move forward with solid results

**Phase 3C Baseline (FINAL):**
- Overall: 38/312 empty (12.2%)
- FinHybrid: 13/47 empty (27.7%)
- TatHybrid: 20/162 empty (12.3%)
- NqText: 3/71 empty (4.2%)
- FetaTab: 2/32 empty (6.2%)

---

## Cost Summary

**Phase 3B Investment:**
- Time: ~3 hours (implementation + debugging + experiment)
- Cost: ~$3 (LLM API calls for 47 questions)
- Result: -7 questions (regression)
- ROI: **Negative** ❌

**Phase 3C (Sticking with baseline):**
- Additional cost: $0
- Additional time: 0 hours
- Result: Accept 12.2% performance
- ROI: **Optimal** ✅

---

## Files Created (Now Obsolete)

```
uda/utils/embeddings.py - FinBERT embedding wrapper (working, but not useful)
experiments/.../2_finbert/notebooks/finhybrid_finbert_experiment.ipynb
experiments/.../2_finbert/results/finhybrid_finbert/finhybrid_finbert_20260630_140755.csv
```

**Note:** These files can be kept for reference but should not be used in production.

---

## Conclusion

Phase 3B was a **failed experiment** that taught us important lessons about model selection. The generic embeddings in Phase 3C remain the best approach for this task.

**Status:** Phase 3C (12.2% empty) is the FINAL baseline for the UDA-Benchmark project. ✅

---

**Next Steps:**
- Document Phase 3C as final results
- Create presentation/report with findings
- Archive Phase 3B files as reference
- Consider project complete (Sprint 3 finished)
