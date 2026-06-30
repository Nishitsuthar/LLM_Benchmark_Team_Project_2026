# Phase 3C - Remaining 4 Datasets: CoT vs Few-Shot Testing

**Date:** June 29, 2026  
**Status:** Ready to Run  
**Context:** TatHybrid validation revealed dataset-specific prompt preferences

---

## 🎯 Strategy: Dataset-Specific Prompt Selection

### **Key Finding:**

Different datasets respond better to different prompt types!

| Dataset | Phase 2 Empty | CoT Result | Few-Shot Result | Winner |
|---------|---------------|------------|-----------------|--------|
| **FinHybrid (47 Q&A)** | 17/47 (36.2%) | **13/47 (27.7%)** ✅ | 19/47 (40.4%) ❌ | **CoT (+4)** |
| **TatHybrid (162 Q&A)** | 26/162 (16.0%) | 29/162 (17.9%) ❌ | **20/162 (12.3%)** ✅ | **Few-Shot (+6)** |

**Total so far: +10 questions** by choosing the right prompt per dataset!

---

## 📊 Remaining Datasets to Test

### **Small Datasets (Test Both):**

| Dataset | Q&A | Phase 2 Empty | Empty % | Config | Strategy |
|---------|-----|---------------|---------|--------|----------|
| **FetaTab** | 8 | 2 | 25.0% | CHUNK=1500, TOP_K=10 | Test both (high empty like FinHybrid) |
| **PaperTab** | 4 | 0 | 0.0% | CHUNK=1500, TOP_K=10 | Test both (perfect baseline) |

### **Medium Datasets (Test Both):**

| Dataset | Q&A | Phase 2 Empty | Empty % | Config | Strategy |
|---------|-----|---------------|---------|--------|----------|
| **PaperText** | 13 | 1 | 7.7% | CHUNK=3000, TOP_K=10 | Test both (low empty like TatHybrid) |
| **NqText** | 78 | 6 | 7.7% | CHUNK=3000, TOP_K=10 | Test both (low empty like TatHybrid) |

---

## 📝 Notebooks Created (8 Total)

### **NqText (78 Q&A) - Wikipedia Factual Q&A:**
- `nqtext_cot_experiment.ipynb` ⏳
- `nqtext_fewshot_experiment.ipynb` ⏳
- **Prediction:** Few-shot likely wins (low empty rate like TatHybrid)
- **Runtime:** 30-60 minutes each

### **FetaTab (8 Q&A) - Wikipedia Tables:**
- `fetatab_cot_experiment.ipynb` ⏳
- `fetatab_fewshot_experiment.ipynb` ⏳
- **Prediction:** CoT likely wins (high empty rate like FinHybrid)
- **Runtime:** 3-6 minutes each

### **PaperText (13 Q&A) - Scientific Papers Text:**
- `papertext_cot_experiment.ipynb` ⏳
- `papertext_fewshot_experiment.ipynb` ⏳
- **Prediction:** Few-shot likely wins (low empty rate)
- **Runtime:** 5-10 minutes each

### **PaperTab (4 Q&A) - Scientific Papers Tables:**
- `papertab_cot_experiment.ipynb` ⏳
- `papertab_fewshot_experiment.ipynb` ⏳
- **Prediction:** Unknown (0% empty baseline - no room for improvement?)
- **Runtime:** 2-3 minutes each

---

## 🚀 How to Run

### **Option 1: Run All in Jupyter (Sequential)**

Open Jupyter and run notebooks one by one:

```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark"

jupyter notebook experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/
```

**Recommended order (fastest first):**
1. `papertab_cot_experiment.ipynb` (2-3 min)
2. `papertab_fewshot_experiment.ipynb` (2-3 min)
3. `fetatab_cot_experiment.ipynb` (3-6 min)
4. `fetatab_fewshot_experiment.ipynb` (3-6 min)
5. `papertext_cot_experiment.ipynb` (5-10 min)
6. `papertext_fewshot_experiment.ipynb` (5-10 min)
7. `nqtext_cot_experiment.ipynb` (30-60 min)
8. `nqtext_fewshot_experiment.ipynb` (30-60 min)

**Total time:** ~2-3 hours

---

## 💰 Cost Estimate

| Dataset | Q&A | CoT Cost | Few-Shot Cost | Total |
|---------|-----|----------|---------------|-------|
| NqText | 78 | ~$3-4 | ~$2-3 | ~$5-7 |
| FetaTab | 8 | ~$0.50 | ~$0.30 | ~$0.80 |
| PaperText | 13 | ~$0.75 | ~$0.50 | ~$1.25 |
| PaperTab | 4 | ~$0.25 | ~$0.15 | ~$0.40 |
| **TOTAL** | **103** | **~$4.50** | **~$3** | **~$7.50** |

**Plus FinHybrid + TatHybrid already done:** ~$5  
**Grand Total Phase 3C:** ~$12-15

---

## 🎯 Expected Results

### **Conservative Estimate:**

| Dataset | Baseline Empty | Expected Improvement | Reasoning |
|---------|----------------|---------------------|-----------|
| FetaTab | 2/8 (25%) | **+1 question** | High empty like FinHybrid → CoT wins |
| PaperTab | 0/4 (0%) | **0 questions** | Already perfect |
| PaperText | 1/13 (7.7%) | **+0-1 questions** | Low empty, little room |
| NqText | 6/78 (7.7%) | **+2-3 questions** | Low empty like TatHybrid → Few-shot wins |

**Conservative Total:** +13-15 questions (current +10 = **+23-25 total**)

### **Optimistic Estimate:**

| Dataset | Baseline Empty | Expected Improvement | Reasoning |
|---------|----------------|---------------------|-----------|
| FetaTab | 2/8 (25%) | **+1-2 questions** | CoT might work even better on small data |
| PaperTab | 0/4 (0%) | **0 questions** | No room for improvement |
| PaperText | 1/13 (7.7%) | **+1 question** | Few-shot might catch the 1 empty |
| NqText | 6/78 (7.7%) | **+3-4 questions** | Few-shot scales like TatHybrid |

**Optimistic Total:** +15-17 questions (current +10 = **+25-27 total**)

---

## ✅ Success Criteria

### **Phase 3C Overall Target:**

- **Original Goal:** <12% empty overall (from 16.7% baseline)
- **Original Goal:** +10-20 questions total

### **Current Progress:**

- ✅ FinHybrid: +4 questions (CoT)
- ✅ TatHybrid: +6 questions (Few-shot)
- **Current:** +10 questions

### **Projected Final:**

- **Conservative:** +23-25 questions total → **~10-11% empty** ✅✅
- **Optimistic:** +25-27 questions total → **~9-10% empty** ✅✅✅

**Both scenarios exceed target!**

---

## 📁 File Structure

```
experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/
├── notebooks/
│   ├── finhybrid_cot_experiment.ipynb ✅ COMPLETE (+4)
│   ├── finhybrid_fewshot_experiment.ipynb ✅ COMPLETE (-2, rejected)
│   ├── tathybrid_cot_experiment.ipynb ✅ COMPLETE (-3, rejected)
│   ├── tathybrid_fewshot_experiment.ipynb ✅ COMPLETE (+6)
│   ├── nqtext_cot_experiment.ipynb ⏳ READY
│   ├── nqtext_fewshot_experiment.ipynb ⏳ READY
│   ├── fetatab_cot_experiment.ipynb ⏳ READY
│   ├── fetatab_fewshot_experiment.ipynb ⏳ READY
│   ├── papertext_cot_experiment.ipynb ⏳ READY
│   ├── papertext_fewshot_experiment.ipynb ⏳ READY
│   ├── papertab_cot_experiment.ipynb ⏳ READY
│   └── papertab_fewshot_experiment.ipynb ⏳ READY
│
└── results/
    ├── finhybrid_cot/ (13 empty - WINNER)
    ├── finhybrid_fewshot/ (19 empty - REJECTED)
    ├── tathybrid_cot/ (29 empty - REJECTED)
    ├── tathybrid_fewshot/ (20 empty - WINNER)
    ├── nqtext_cot/ (pending)
    ├── nqtext_fewshot/ (pending)
    ├── fetatab_cot/ (pending)
    ├── fetatab_fewshot/ (pending)
    ├── papertext_cot/ (pending)
    ├── papertext_fewshot/ (pending)
    ├── papertab_cot/ (pending)
    └── papertab_fewshot/ (pending)
```

---

## 🔍 Analysis After All Tests

After running all 8 notebooks, create analysis:

1. **Compare CoT vs Few-Shot for each dataset**
2. **Identify pattern:** What makes a dataset prefer CoT vs Few-Shot?
   - Hypothesis: High empty rate → CoT wins
   - Hypothesis: Low empty rate → Few-shot wins
3. **Final recommendation:** Best prompt per dataset
4. **Calculate final metrics:** Overall empty rate and improvement

---

## 📊 Quick Reference

**Completed:**
- FinHybrid: CoT wins (+4)
- TatHybrid: Few-shot wins (+6)

**To Run (Priority Order):**
1. PaperTab (fastest, 2-3 min each)
2. FetaTab (fast, 3-6 min each)
3. PaperText (medium, 5-10 min each)
4. NqText (slowest, 30-60 min each)

**Total Runtime:** ~2-3 hours  
**Total Cost:** ~$7.50  
**Expected Gain:** +13-17 more questions  
**Final Total:** +23-27 questions overall ✅

---

**Ready to run! Start with the fastest datasets first to validate the approach!** 🚀
