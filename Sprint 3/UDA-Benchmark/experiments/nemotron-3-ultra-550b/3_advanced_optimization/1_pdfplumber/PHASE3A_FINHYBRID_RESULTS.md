# 📊 Phase 3A Results - FinHybrid pdfplumber Experiment

**Date:** June 29, 2026  
**Experiment:** Phase 3A - pdfplumber PDF extraction  
**Dataset:** FinHybrid (47 Q&A, Financial Reports)  
**Status:** ✅ COMPLETE - ⚠️ **MAJOR REGRESSION**

---

## 🚨 CRITICAL FINDING: pdfplumber HURT FinHybrid Performance

### **Overall Performance**

| Metric | Phase 2 Baseline | Phase 3A (pdfplumber) | Change |
|--------|------------------|----------------------|--------|
| **Empty Rate** | 36.2% (17/47) | **48.9% (23/47)** | **+12.7%** ❌❌❌ |
| **Answered** | 30/47 (63.8%) | **24/47 (51.1%)** | **-6 questions** ❌❌❌ |
| **Avg Response Length** | 34 chars | **57 chars** | **+68%** ⚠️ |

### **Net Result: -6 Questions (REGRESSION)**

---

## 📉 DETAILED BREAKDOWN

### **By Document:**

| Document | Phase 2 Empty | Phase 3A Empty | Change | Assessment |
|----------|---------------|----------------|--------|------------|
| **GS_2016** | 5/23 (21.7%) | **12/23 (52.2%)** | **+7 empty** | ❌❌❌ TERRIBLE |
| **ADI_2009** | 5/9 (55.6%) | **6/9 (66.7%)** | **+1 empty** | ❌ WORSE |
| **ABMD_2012** | 6/12 (50%) | **5/12 (41.7%)** | **-1 empty** | ✅ SLIGHT IMPROVE |
| **JKHY_2015** | 1/3 (33.3%) | **0/3 (0%)** | **-1 empty** | ✅ IMPROVE |

**Disaster:** GS_2016 lost 7 questions (half the dataset became empty!)

---

## 📊 QUESTION-BY-QUESTION ANALYSIS

### **Trade-offs:**
- ✅ **+3 questions** now answered (were empty in Phase 2)
- ❌ **-9 questions** now empty (were answered in Phase 2)
- 🎯 **Net: -6 questions** (MAJOR REGRESSION)

### **Examples of Regressed Questions:**

1. **"What percentage did the balance increase from 2007 to 2009?"**
   - Phase 2: "The balance increased from $9,889 in 2007 to $18,161..." ✅
   - Phase 3A: [EMPTY] ❌

2. **"What percentage of total long-term assets under supervision are comprised of equity...?"**
   - Phase 2: "The answer is: 57.72%" ✅
   - Phase 3A: [EMPTY] ❌

3. **"What percentage of total loans receivable gross in 2016 were loans backed by...?"**
   - Phase 2: "The answer is: 9.49%" ✅
   - Phase 3A: [EMPTY] ❌

4. **"In billions, for 2016, 2015, and 2014, what are total alternative investments?"**
   - Phase 2: "2016: $154 billion, 2015: $148 billion, 2014: $143 billion" ✅
   - Phase 3A: [EMPTY] ❌

**Pattern:** Questions requiring precise numerical extraction and table aggregation FAILED with pdfplumber.

---

## 🔍 WHY DID pdfplumber FAIL ON FinHybrid?

### **Theory 1: Different Text Structure Disrupted Retrieval**
- pdfplumber adds page markers, table separators (`|`), and section headers
- Changed chunk boundaries → different Top-K retrieval results
- Context that was retrieved in Phase 2 wasn't retrieved in Phase 3A

### **Theory 2: Table Formatting Confused the Model**
- pdfplumber's `|` separators may have confused Nemotron
- More structured format paradoxically harder to parse
- Model trained on natural text, not pipe-delimited tables

### **Theory 3: Chunk Boundary Issues**
- Better structure = different chunking
- Critical context split across chunks
- Questions that spanned tables got fragmented

### **Theory 4: Document-Specific Issue (GS_2016)**
- GS_2016 lost 7 questions (30% of total regression)
- This PDF may have complex tables that pdfplumber handled poorly
- Or PyPDF2 happened to work well on this specific document

---

## 📊 COMBINED RESULTS: TatHybrid + FinHybrid

### **Phase 3A Summary Across Both Datasets:**

| Dataset | Phase 2 Empty | Phase 3A Empty | Change | Assessment |
|---------|---------------|----------------|--------|------------|
| **TatHybrid** | 16.0% (26/162) | 14.8% (24/162) | **+2 questions** | ✅ Modest win |
| **FinHybrid** | 36.2% (17/47) | 48.9% (23/47) | **-6 questions** | ❌ Major loss |
| **COMBINED** | 20.6% (43/209) | 22.5% (47/209) | **-4 questions** | ❌ Net negative |

**Overall verdict:** pdfplumber is **NOT beneficial** for this pipeline.

---

## 💡 KEY INSIGHTS

### **What We Learned:**

1. **❌ pdfplumber is not universally better**
   - Helped slightly on TatHybrid (+2)
   - Hurt significantly on FinHybrid (-6)
   - Net negative overall (-4)

2. **⚠️ Different datasets react differently**
   - TatHybrid: Already decent baseline (16%), small gain
   - FinHybrid: Worse baseline (36%), but pdfplumber made it WORSE

3. **🔍 Structure changes affect retrieval**
   - pdfplumber's better structure paradoxically hurt retrieval
   - Chunk boundaries and separators matter for ChromaDB
   - Model may not benefit from pipe-delimited tables

4. **📊 Document-specific effects**
   - Some PDFs work better with PyPDF2
   - GS_2016 was disaster with pdfplumber (-7 questions)
   - Can't predict which documents benefit without testing

---

## 🎯 VERDICT: pdfplumber NOT RECOMMENDED

### **Evidence:**
- ✅ TatHybrid: +2 questions (marginal)
- ❌ FinHybrid: -6 questions (major regression)
- ❌ Combined: -4 questions net
- ⚠️ Unpredictable: Helps some docs, hurts others
- ⚠️ Adds complexity for negative ROI

### **Recommendation: ABANDON pdfplumber, MOVE TO PHASE 3B/3C**

---

## 📋 DECISION MATRIX

### **Should we continue with pdfplumber?**

**NO - for these reasons:**

1. **Net negative results** (-4 questions overall)
2. **Unpredictable behavior** (helps TatHybrid, hurts FinHybrid)
3. **Major regression on worst performer** (FinHybrid got 12.7% WORSE)
4. **Not worth the complexity** for marginal TatHybrid gain
5. **Better opportunities available** (Prompts, FinBERT)

---

## 🚀 RECOMMENDED NEXT STEPS

### **Option 1: Move to Phase 3C (Prompts)** ⭐ **RECOMMENDED**

**Why prompts next:**
- **Universal benefit** (helps all datasets)
- **Expected: +10-20 questions** (much better than pdfplumber)
- **Simpler to implement** than FinBERT
- **No extraction changes** (works with existing PyPDF2)
- **Can fix both TatHybrid AND FinHybrid**

**Implementation:**
- Instruction-enhanced prompts
- Few-shot examples
- Domain-specific guidance
- Estimated time: 2-3 hours

---

### **Option 2: Move to Phase 3B (FinBERT)**

**Why FinBERT:**
- **Domain-specific** for financial datasets
- **Expected: +5-9 questions**
- **Works with PyPDF2** (no extraction changes)
- **May help FinHybrid specifically**

**But:**
- Smaller expected gain than prompts
- More complex to implement
- Slower runtime (free but heavier model)

---

### **Option 3: Combine Prompts + FinBERT (Skip pdfplumber)**

**Best long-term strategy:**
1. Implement prompts first (+10-20 questions expected)
2. Then add FinBERT (+5-9 questions expected)
3. Combined: +15-29 questions total
4. Skip pdfplumber entirely (proven negative ROI)

---

## 📊 UPDATED ROADMAP

### **Revised Phase 3 Plan:**

```
Phase 1 (Baseline):           24.0% empty ✅
Phase 2 (Parameters):         16.7% empty ✅
Phase 3A (pdfplumber):        ABANDONED ❌

Phase 3B (Prompts):           ⏳ NEXT
  - Expected: +10-20 questions
  - Universal benefit
  - Highest priority

Phase 3C (FinBERT):           ⏳ AFTER PROMPTS
  - Expected: +5-9 questions
  - Domain-specific help
  - Stack with prompts
```

---

## 💰 COST-BENEFIT ANALYSIS

### **Phase 3A (pdfplumber) - COMPLETED:**
- **Time invested:** ~4 hours (setup + 2 experiments)
- **Cost:** ~$45-55 (209 total Q&A across both datasets)
- **Return:** -4 questions (NET NEGATIVE)
- **ROI:** NEGATIVE ❌
- **Decision:** ABANDON

### **Phase 3B/3C (Prompts + FinBERT) - PLANNED:**
- **Time:** 3-5 hours
- **Cost:** $30-50
- **Expected return:** +15-29 questions
- **Expected ROI:** $1.03-$3.33 per question ✅
- **Decision:** PROCEED

---

## 📁 FILES SAVED

**Results:**
- TatHybrid: `.../1_pdfplumber/results/tathybrid_pdfplumber/tathybrid_results_20260629_181257.csv`
- FinHybrid: `.../1_pdfplumber/results/finhybrid_pdfplumber/finhybrid_results_20260629_183434.csv`

**Analysis:**
- TatHybrid: +2 questions (16.0% → 14.8%)
- FinHybrid: -6 questions (36.2% → 48.9%)
- Combined: -4 questions NET

---

## 🏁 CONCLUSION

**Phase 3A (pdfplumber) is COMPLETE with clear verdict:**

### **Finding:**
pdfplumber does NOT improve performance on this pipeline. It shows:
- Marginal gain on one dataset (+2)
- Major regression on another (-6)
- Net negative overall (-4)
- Unpredictable behavior
- Not worth the complexity

### **Decision:**
**ABANDON pdfplumber. Move to Phase 3C (Prompts) immediately.**

### **Reasoning:**
- Prompts have much higher expected ROI (+10-20 vs -4)
- Universal benefit (all datasets)
- Simpler implementation
- Proven track record in literature
- Can be combined with FinBERT later

### **Action:**
Skip remaining pdfplumber tests (FetaTab, PaperTab, PaperText). Implement Phase 3C (Prompt Engineering) next.

---

**Date:** June 29, 2026  
**Status:** ✅ Phase 3A Complete - ❌ pdfplumber ABANDONED  
**Net Result:** -4 questions (regression)  
**Next:** Phase 3C - Prompt Engineering (+10-20 expected)
