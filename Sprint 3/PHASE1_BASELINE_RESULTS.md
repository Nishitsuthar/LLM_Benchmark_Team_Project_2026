# Sprint 3 Phase 1: NVIDIA Nemotron Baseline Results

**Date:** 2026-06-28  
**Model:** NVIDIA Nemotron-3 Ultra 550B (via Together AI)  
**Test Scope:** 2 financial documents, 27 Q&A pairs  
**Status:** ✅ COMPLETE

---

## Executive Summary

**Overall Performance:**
- **FinHybrid (ADI_2009):** 11.11% accuracy (1/9 correct)
- **TatHybrid (inpixon_2019):** 34.44% F1 score (18 questions)
- **Combined:** 27 questions processed successfully

⚠️ **Key Finding:** Performance significantly below expectations (target was 70-85%)

---

## Detailed Results

### FinHybrid Dataset (Financial Reports - Exact Match Metric)

**Document:** ADI_2009 (Analog Devices 2009 Annual Report)  
**Questions:** 9  
**Correct:** 1  
**Accuracy:** 11.11%

| Question | Nemotron Answer | Ground Truth | Match? |
|----------|----------------|--------------|--------|
| Interest expense in 2009? | 4,094 (thousands) | 380 (or 3.8) | ❌ Wrong |
| Growth rate in amortization 2010? | *(empty)* | -27.0% | ❌ No answer |
| Net difference in hedging instruments? | *(empty)* | 247 | ❌ No answer |
| Growth rate in amortization 2009? | -20.4% | -20.4% | ✅ **CORRECT** |
| Net change uncertain tax positions 2007-2009? | *(empty)* | 8272 | ❌ No answer |
| % increase interest expense 2009? | *(empty)* | 30.8% | ❌ No answer |
| LOBOR rate Oct 31, 2009? | *(empty)* | 29.0% (or 0.0029) | ❌ No answer |
| % balance increase 2007-2009? | *(empty)* | 83.6% | ❌ No answer |
| Potential tax liability balance? | *(empty)* | $17,966 million | ❌ No answer |

**Issues Identified:**
- 7/9 questions returned empty responses
- 1/9 questions answered incorrectly (wrong number)
- 1/9 questions answered correctly

---

### TatHybrid Dataset (Financial Reports - Numeracy F1 Metric)

**Document:** inpixon_2019 (Inpixon 2019 Annual Report)  
**Questions:** 18  
**F1 Score:** 34.44%

#### Correct Answers (8/18):
1. ✅ Weighted avg amortization period: **1.61 years** (correct)
2. ✅ Net software dev costs 2019: **$1,544,000** (correct)
3. ✅ Capitalized software 2019: **$6,029,000** (correct)
4. ✅ Year < 6000 thousands: **2018** (correct)
5. ✅ Average software costs: **1,617 thousands** (correct)
6. ✅ Year restricted cash < 70: **2019** (correct)
7. ✅ Change in cash & equivalents: **$3,769** (correct)
8. ✅ How company accounts for options: *Detailed explanation* (correct)

#### Empty Responses (5/18):
- Change in accumulated amortization
- Escrow restricted cash amounts  
- Cash & equivalents 2019/2018
- Average restricted cash
- Average professional fees

#### Incorrect Answers (5/18):
- Cash equivalents definition (partial match)
- Options/warrants for non-employees (partial match)
- Compensation benefits 2019/2018 (wrong values)
- Year professional fees < 500 ("info not available" vs "2019")
- Change in compensation benefits (wrong calculation)

---

## Error Analysis

### Error Categories:

1. **Empty Responses (44%):** 12/27 questions
   - Model failed to extract answer from context
   - Retrieval may have missed relevant chunks
   - Model may have insufficient confidence

2. **Wrong Numerical Values (15%):** 4/27 questions
   - Retrieved wrong table or section
   - Misread financial statements
   - Calculation errors

3. **Correct Answers (33%):** 9/27 questions
   - Mostly simple extraction tasks
   - Clear, unambiguous questions
   - Direct answers in retrieved context

---

## Comparison with Expectations

| Metric | Expected | Actual | Delta |
|--------|----------|--------|-------|
| **FinHybrid Accuracy** | 70-85% | 11.11% | **-59% to -74%** ❌ |
| **TatHybrid F1** | 65-80% | 34.44% | **-31% to -46%** ❌ |
| **Empty Responses** | <10% | 44% | **+34%** ❌ |

**Verdict:** Significantly underperformed expectations

---

## Possible Causes

### 1. **Context Retrieval Issues**
- Top-5 chunks may not contain the relevant information
- Financial tables may not be well-represented in chunks
- PDF text extraction quality (PyPDF2 limitations)

### 2. **Model Limitations**
- Nemotron may struggle with financial document structure
- Model may be overly cautious (returns empty vs wrong answer)
- Prompt template may not be optimal for Nemotron

### 3. **RAG Pipeline Issues**
- Chunk size (3000 chars) may be too large for tables
- Local embeddings (all-MiniLM-L6-v2) may not capture financial semantics
- Retrieval scoring may prioritize wrong sections

### 4. **Evaluation Methodology**
- Exact Match metric is very strict (no tolerance for formatting)
- Empty responses heavily penalize the score
- Some "wrong" answers may be partially correct

---

## Sprint 2 Comparison

| Aspect | Sprint 2 (Gemini) | Sprint 3 (Nemotron) |
|--------|------------------|---------------------|
| **Task** | Direct table analysis | RAG on PDFs |
| **Format** | Clean CSV | Raw financial reports |
| **Best Accuracy** | 80% (JSON, all formats individual mode) | 34.44% F1 (TatHybrid) |
| **Empty Responses** | Rare | 44% of questions |
| **Challenge** | Stale metadata, filtering | Context retrieval, extraction |

**Key Insight:** Gemini performed much better on clean structured data. Nemotron + RAG on messy PDFs is significantly harder.

---

## Recommendations

### Immediate Fixes (Can Test Now):

1. **Adjust Chunk Size**
   - Try 1500 characters (smaller, more focused chunks)
   - Try 6000 characters (capture full tables)

2. **Increase Retrieval**
   - Increase top_k from 5 to 10 or 15
   - More context may help

3. **Better Embeddings**
   - Try financial-specific embeddings (if available)
   - Or use Together AI embeddings (paid but better)

4. **Prompt Engineering**
   - Add "If you cannot find the answer in the context, say 'Information not found'"
   - Encourage the model to extract even uncertain answers

### Next Steps:

**Option A: Debug & Optimize (Recommended)**
- Run parameter sweep: chunk_size × top_k combinations
- Test different embedding models
- Improve prompt templates
- **Cost:** ~$10-20, **Time:** 2-3 hours

**Option B: Test Different Model**
- Try GPT-4 on same documents for comparison
- See if it's a Nemotron issue or RAG pipeline issue
- **Cost:** ~$5-10, **Time:** 30 mins

**Option C: Test on More Documents**
- Current test is limited (2 docs, 27 Q&A)
- Test on all 17 available example documents
- **Cost:** ~$15-25, **Time:** 1-2 hours

---

## Cost Analysis

**Phase 1 Actual Cost:**
- 27 LLM calls × ~$0.10-0.15 per call = **~$3-4**
- Local embeddings: **Free**
- **Total: ~$3-4** (well under budget)

**Remaining Budget:** ~$6-16 for additional tests

---

## Conclusions

1. ✅ **RAG Pipeline Works:** Successfully processed 27 questions
2. ❌ **Performance Below Target:** 11-34% vs expected 70-85%
3. ⚠️ **High Empty Response Rate:** 44% of questions returned no answer
4. 🔍 **Root Cause Unclear:** Could be retrieval, model, or prompt issues
5. 💡 **More Testing Needed:** 2 documents insufficient for conclusions

**Next Action:** Run Option A (parameter optimization) to identify if this is fixable, or Option B (compare with GPT-4) to determine if it's a Nemotron-specific issue.

---

## Files Generated

- `phase1_simple_results_20260628_201919.csv` - Raw results (27 Q&A pairs)
- Output log with detailed question-by-question results

---

**Report Generated:** 2026-06-28 20:19  
**Status:** Phase 1 baseline complete, debugging needed  
**Recommendation:** Investigate retrieval quality before scaling up
