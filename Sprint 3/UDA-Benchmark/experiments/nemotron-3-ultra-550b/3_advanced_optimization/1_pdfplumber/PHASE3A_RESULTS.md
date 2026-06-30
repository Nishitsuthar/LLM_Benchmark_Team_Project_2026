# 📊 Phase 3A Results - TatHybrid pdfplumber Experiment

**Date:** June 29, 2026  
**Experiment:** Phase 3A - pdfplumber PDF extraction  
**Dataset:** TatHybrid (162 Q&A, Financial Reports)  
**Status:** ✅ COMPLETE

---

## 🎯 RESULTS SUMMARY

### **Overall Performance**

| Metric | Phase 2 Baseline | Phase 3A (pdfplumber) | Change |
|--------|------------------|----------------------|--------|
| **Empty Rate** | 16.0% (26/162) | **14.8% (24/162)** | **-1.2%** ✅ |
| **Answered** | 136/162 (84.0%) | **138/162 (85.2%)** | **+2 questions** ✅ |
| **Avg Response Length** | 51 chars | **76 chars** | **+49%** ✅ |

### **Net Improvement: +2 Questions Answered**

---

## 📈 DETAILED ANALYSIS

### **Question-by-Question Comparison:**

- **✅ Improved:** 13 questions now answered (were empty in Phase 2)
- **⚠️ Regressed:** 11 questions now empty (were answered in Phase 2)
- **🎯 Net Gain:** +2 questions

### **By Document:**

| Document | Total | Answered | Empty | Empty % | Phase 2 Empty % | Change |
|----------|-------|----------|-------|---------|-----------------|--------|
| **viavi-solutions-inc_2019** | 24 | 23 | 1 | **4.2%** | 16.7% | **-12.5%** ✅✅✅ |
| **lifeway-foods-inc_2019** | 60 | 52 | 8 | **13.3%** | 13.3% | **0%** ➖ |
| **inpixon_2019** | 18 | 15 | 3 | **16.7%** | 16.7% | **0%** ➖ |
| **overseas-shipholding-group-inc_2019** | 60 | 48 | 12 | **20.0%** | 20.0% | **0%** ➖ |

**⭐ Star Performer:** viavi-solutions-inc improved dramatically (-12.5% empty)!

---

## ✅ QUESTIONS THAT pdfplumber HELPED ANSWER

**Examples of newly answered questions (13 total):**

1. **"In which year was Vessels, at cost less than 900,000?"**
   - Phase 2: [EMPTY]
   - Phase 3A: "The answer is: 2018" ✅

2. **"What is the change in Balance of unrecognized tax benefits..."**
   - Phase 2: [EMPTY]
   - Phase 3A: "The balance as of January 1, 2019 is $1,226..." ✅

3. **"What is the change in Net deferred tax liabilities from December 31, 2018 to 2019?"**
   - Phase 2: [EMPTY]
   - Phase 3A: "The answer is: -$532" ✅

4. **"Which year has a higher value of net intangible assets?"**
   - Phase 2: [EMPTY]
   - Phase 3A: "The answer is: 2018" ✅

5. **"What is the percentage difference of the total compensation between Timothy Campbell and Bill Zerella?"**
   - Phase 2: [EMPTY]
   - Phase 3A: "The answer is: 4.07%" ✅

6. **"What was the change in maximum possible value of MSU's using grant date fair value?"**
   - Phase 2: [EMPTY]
   - Phase 3A: "The answer is: 18.5%" ✅

7. **"What was the average Software development costs, net for 2018 and 2019?"**
   - Phase 2: [EMPTY]
   - Phase 3A: "The answer is: $1,617 thousand" ✅

**Pattern:** pdfplumber helped with numerical/table-based questions requiring precise data extraction.

---

## ⚠️ QUESTIONS THAT REGRESSED

**Examples (11 total):**

1. **"In which year was Operating Leases greater than 100,000?"**
   - Phase 2: "The answer is: 2019" ✅
   - Phase 3A: [EMPTY] ❌

2. **"How much did revenues increased for the year ended December 31, 2018..."**
   - Phase 2: "The answer is: $1,418" ✅
   - Phase 3A: [EMPTY] ❌

3. **"How much did net income increased for the year ended December 31, 2018..."**
   - Phase 2: "The answer is: $1,101" ✅
   - Phase 3A: [EMPTY] ❌

4. **"How much did the company paid (net of refunds received) of income taxes..."**
   - Phase 2: "The answer is: $1,293 for 2019 and $1,313 for 2018" ✅
   - Phase 3A: [EMPTY] ❌

**Pattern:** Some previously answered questions lost due to different chunk boundaries or retrieval changes.

---

## 🔍 KEY INSIGHTS

### **What Worked:**

1. **✅ Better table extraction:** viavi-solutions showed dramatic improvement (-12.5% empty)
2. **✅ Longer responses:** Average response length increased 49% (51 → 76 chars)
3. **✅ More precise answers:** 13 previously unanswerable questions now answered
4. **✅ Better numerical extraction:** Questions about specific values improved

### **What Didn't Work as Expected:**

1. **⚠️ Mixed results across documents:** 3/4 documents showed no change
2. **⚠️ Some regressions:** 11 questions that were answered in Phase 2 became empty
3. **⚠️ Chunking trade-offs:** Better structure may have split some context differently
4. **⚠️ Lower than expected gain:** +2 vs target of +6-10

### **Possible Reasons for Lower Gain:**

1. **PyPDF2 wasn't as bad as expected** on these particular PDFs
2. **pdfplumber's different structure** changed chunk boundaries (helped some, hurt others)
3. **Retrieval changes:** Different chunks → different Top-K results
4. **TatHybrid already had decent baseline** (16% empty vs FinHybrid's 36%)

---

## 💡 RECOMMENDATIONS

### **Option 1: Proceed Cautiously** ⚠️
- Small improvement (+2) but not dramatic
- Test on **FinHybrid** (36% empty, more problematic)
- pdfplumber might help more on worse-performing datasets

### **Option 2: Investigate Before Scaling**
- Analyze the 11 regressions to understand why
- Check if chunk sizes need adjustment for pdfplumber
- Verify table detection quality on sample PDFs

### **Option 3: Combine with Other Optimizations** ✅ (Recommended)
- **Current:** pdfplumber alone = +2 questions
- **Next:** Add FinBERT embeddings (might help retrieval)
- **Then:** Add better prompts (might help both old and new questions)
- **Combined effect might be stronger than individual**

---

## 📊 VERDICT: MODEST SUCCESS ✅ (but proceed carefully)

**Pros:**
- ✅ Net positive improvement (+2 questions)
- ✅ One document showed strong improvement (viavi: -12.5%)
- ✅ Better response quality (longer, more detailed)
- ✅ Helped with numerical/table questions
- ✅ No major issues or errors

**Cons:**
- ⚠️ Smaller gain than expected (+2 vs target +6-10)
- ⚠️ Mixed results across documents
- ⚠️ 11 regressions need investigation
- ⚠️ May not be worth the complexity for marginal gain

---

## 🎯 NEXT STEPS

### **Immediate:**
1. **Decision Point:** Continue with pdfplumber or pivot?

### **If Continue with pdfplumber:**
2. ✅ Test on **FinHybrid** (36% empty, more room for improvement)
3. ✅ Document FinHybrid results
4. ✅ Compare: Is improvement bigger on worse datasets?

### **If Pivot:**
2. ⏭️ Move to **Phase 3B: FinBERT** (domain embeddings)
3. ⏭️ Then **Phase 3C: Prompts** (universal benefit)
4. ⏭️ Combine all 3 at end for maximum effect

### **Recommended Path:** 🌟
**Test pdfplumber on FinHybrid (worst performer), then move to Phase 3B+3C**

**Rationale:**
- FinHybrid has 36% empty (vs TatHybrid's 16%)
- More room for improvement
- If pdfplumber helps more there → keep it
- If not → still have FinBERT and prompts as backup

---

## 📁 FILES SAVED

**Results:**
- `experiments/nemotron-3-ultra-550b/3_advanced_optimization/1_pdfplumber/results/tathybrid_pdfplumber/tathybrid_results_20260629_181257.csv`

**Comparison Data:**
- Phase 2: 26 empty (16.0%)
- Phase 3A: 24 empty (14.8%)
- Improvement: +2 questions

---

## 🏁 CONCLUSION

**Phase 3A (pdfplumber) achieved a modest improvement:**
- +2 questions answered (net)
- +13 new answers, -11 regressions
- Best improvement on viavi-solutions document (-12.5% empty)
- Mixed results overall

**Not the dramatic win we hoped for (+6-10), but still positive.**

**Recommendation:** Test on FinHybrid to see if pdfplumber helps more on datasets with worse baselines, then proceed to Phase 3B (FinBERT) and 3C (prompts) regardless of result.

---

**Date:** June 29, 2026  
**Status:** ✅ Phase 3A Complete  
**Net Result:** +2 questions (modest success)  
**Next:** Test on FinHybrid or move to Phase 3B
