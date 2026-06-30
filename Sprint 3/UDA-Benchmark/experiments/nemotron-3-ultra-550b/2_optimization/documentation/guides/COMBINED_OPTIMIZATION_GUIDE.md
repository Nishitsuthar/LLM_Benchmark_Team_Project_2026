# 🎯 Combined Parameter Optimization - Ready to Run

**Date:** June 29, 2026  
**Phase:** Phase 2 - Stacked Optimizations  
**Status:** 3 Combined notebooks created and ready to test

---

## ✅ What We Created

### **3 Combined Optimization Notebooks:**

All notebooks **stack TOP_K=10** (our validated baseline) with additional optimizations:

| Notebook | Dataset | Parameters | Expected Impact | Time | Cost |
|----------|---------|------------|----------------|------|------|
| **1. tathybrid_topk10_chunk1500** | TatHybrid | TOP_K=10 + CHUNK_SIZE=1500 | +5-8% (tables) | 60-90 min | $13-20 |
| **2. finhybrid_topk10_chunk1500** | FinHybrid | TOP_K=10 + CHUNK_SIZE=1500 | +5-10% (tables) | 15-20 min | $3-5 |
| **3. finhybrid_topk10_temp03** | FinHybrid | TOP_K=10 + TEMPERATURE=0.3 | +3-5% (less conservative) | 15-20 min | $3-5 |

**Total Expected:** ~90-130 min, ~$19-30

---

## 📊 Optimization Strategy

### **Why Stack Optimizations?**

1. ✅ **TOP_K=10 validated** - Already proven to work (+3.8% overall)
2. ✅ **Cumulative effects** - Multiple optimizations should compound
3. ✅ **Fewer notebooks** - Easier to manage than separate single-parameter tests
4. ✅ **Realistic scenario** - Production would use best combination

### **What Each Parameter Does:**

#### **CHUNK_SIZE=1500 (vs baseline 3000)**
- **Effect:** Smaller chunks = more precise retrieval
- **Best for:** Table-heavy datasets (finance reports)
- **Why:** Financial tables get split more precisely, reducing noise
- **Trade-off:** More chunks to process, but better granularity

#### **TEMPERATURE=0.3 (vs baseline 0.1)**
- **Effect:** Less conservative generation
- **Best for:** High empty-rate datasets (FinHybrid 40%)
- **Why:** Model less likely to refuse answering
- **Trade-off:** Slightly less deterministic, but more answers

---

## 🎯 **Recommended Running Order**

### **Option A: Quick Wins First (Recommended)**

Run the two **FinHybrid** experiments first (both quick):

```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark/experiments/nemotron-3-ultra-550b/2_optimization"

# 1. TEMPERATURE test (quickest)
jupyter notebook finhybrid_topk10_temp03_experiment.ipynb
# Expected: 15-20 min, $3-5, +3-5% improvement

# 2. CHUNK_SIZE test
jupyter notebook finhybrid_topk10_chunk1500_experiment.ipynb
# Expected: 15-20 min, $3-5, +5-10% improvement

# 3. TatHybrid CHUNK_SIZE (longest)
jupyter notebook tathybrid_topk10_chunk1500_experiment.ipynb
# Expected: 60-90 min, $13-20, +5-8% improvement
```

**Total:** ~90-130 min, ~$19-30

---

### **Option B: High Impact First**

Test biggest expected improvement first:

```bash
# 1. FinHybrid CHUNK_SIZE (highest expected %)
jupyter notebook finhybrid_topk10_chunk1500_experiment.ipynb

# 2. TatHybrid CHUNK_SIZE (large dataset validation)
jupyter notebook tathybrid_topk10_chunk1500_experiment.ipynb

# 3. FinHybrid TEMPERATURE (additional boost)
jupyter notebook finhybrid_topk10_temp03_experiment.ipynb
```

---

## 📈 **Expected Results**

### **Baseline (TOP_K=10 only):**
| Dataset | Empty Rate | Score |
|---------|-----------|-------|
| **TatHybrid** | 21.0% (34/162) | ~43-44% |
| **FinHybrid** | 40.4% (19/47) | ~23-24% |

### **Expected After Combined Optimization:**

#### **TatHybrid + CHUNK_SIZE=1500:**
- **Empty:** 21.0% → **15-18%** (-3-6%)
- **Score:** 43-44% → **48-52%** (+5-8%)
- **Why:** Smaller chunks better for table extraction
- **Questions:** +3-6 more answered

#### **FinHybrid + CHUNK_SIZE=1500:**
- **Empty:** 40.4% → **30-35%** (-5-10%)
- **Score:** 23-24% → **28-33%** (+5-9%)
- **Why:** Financial tables need precise chunking
- **Questions:** +2-5 more answered

#### **FinHybrid + TEMPERATURE=0.3:**
- **Empty:** 40.4% → **35-37%** (-3-5%)
- **Score:** 23-24% → **26-29%** (+3-5%)
- **Why:** Less conservative model = fewer refusals
- **Questions:** +1-2 more answered

---

## 💡 **What We'll Learn**

### **From CHUNK_SIZE Tests:**
1. Does smaller chunk size help table extraction?
2. Is the improvement worth the trade-off (more chunks)?
3. Should we make 1500 the new standard for table datasets?

### **From TEMPERATURE Test:**
1. Does higher temperature reduce empty responses?
2. Do we sacrifice accuracy for coverage?
3. Is 0.3 the sweet spot or should we test 0.5?

### **From Combined Results:**
1. Do optimizations stack (cumulative) or interfere?
2. Which parameter has bigger impact?
3. What's the best overall configuration?

---

## 🎯 **Success Metrics**

### **Minimum Success:**
- At least 2/3 experiments show improvement
- Combined effect ≥ sum of individual effects - 20%
- No dramatic quality degradation

### **Target Success:**
- All 3 experiments show clear improvement
- TatHybrid reaches >50% score
- FinHybrid drops below 35% empty rate
- Stacked optimizations work as expected

### **Stretch Success:**
- TatHybrid >52% score (<15% empty)
- FinHybrid <30% empty (>30% score)
- Combined optimizations exceed individual sum

---

## 📋 **Comparison Table**

After running all 3, we'll have:

| Configuration | TatHybrid Empty | TatHybrid Score | FinHybrid Empty | FinHybrid Score |
|---------------|----------------|----------------|----------------|----------------|
| **Baseline (TOP_K=5)** | 22.8% | 43.5% | 44.7% | 23.4% |
| **TOP_K=10 only** | 21.0% | ~44% | 40.4% | ~24% |
| **TOP_K=10 + CHUNK=1500** | 15-18%? | 48-52%? | 30-35%? | 28-33%? |
| **TOP_K=10 + TEMP=0.3** | - | - | 35-37%? | 26-29%? |

---

## ✅ **Before Running Checklist**

- [x] All 3 combined notebooks created
- [x] Parameters correctly updated
- [x] OUTPUT_DIR points to new result folders
- [ ] API credits available (~$19-30 needed)
- [ ] ~90-130 minutes available
- [ ] Clear what to expect from each experiment

---

## 🔍 **What to Watch For**

### **During CHUNK_SIZE Experiments:**
- Does chunk count increase significantly?
- Are more table-related questions answered?
- Does quality stay consistent?

### **During TEMPERATURE Experiment:**
- Are there more "attempted answers" (less empty)?
- Does response format stay consistent?
- Any increase in obviously wrong answers?

### **Overall:**
- Document empty rate per document
- Note which types of questions improve
- Check if runtime increases significantly

---

## 📊 **After Completion**

### **Immediate Analysis:**
1. Count empty responses for each experiment
2. Compare vs TOP_K=10 baseline
3. Calculate improvement percentages
4. Note any unexpected patterns

### **Comprehensive Analysis:**
1. Run evaluation metrics (scores)
2. Compare stacked vs individual optimizations
3. Identify best overall configuration
4. Document recommendations

### **Decision Points:**
1. Should CHUNK_SIZE=1500 become baseline for finance?
2. Should TEMPERATURE=0.3 become standard?
3. What's the optimal configuration per domain?
4. Ready for Phase 3 (better PDF parsing)?

---

## 🚀 **Next Phase Preview**

After these combined optimizations, Phase 3 will focus on:

1. **Better PDF Parsing** (pdfplumber)
   - Expected +10-15% on table datasets
   - Requires code changes to framework

2. **Domain Embeddings** (FinBERT)
   - Expected +5-8% on finance datasets
   - Better semantic understanding

3. **Prompt Engineering** (few-shot, CoT)
   - Expected +3-7% overall
   - Better instruction following

**Target:** 45-50% average score, <15% empty rate

---

## 💬 **Quick Commands**

### **Navigate to optimization folder:**
```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark/experiments/nemotron-3-ultra-550b/2_optimization"
```

### **List all notebooks:**
```bash
ls -lh *experiment.ipynb
```

### **Run a specific notebook:**
```bash
jupyter notebook <notebook_name>.ipynb
```

### **Check results after running:**
```bash
ls -lh results/*/
```

---

## 📁 **File Organization**

```
2_optimization/
├── Notebooks (TOP_K=10 only):
│   ├── tathybrid_topk10_experiment.ipynb ✅
│   ├── finhybrid_topk10_experiment.ipynb ✅
│   ├── nqtext_topk10_experiment.ipynb ✅
│   ├── fetatab_topk10_experiment.ipynb ✅
│   ├── papertext_topk10_experiment.ipynb ✅
│   └── papertab_topk10_experiment.ipynb ✅
│
├── Notebooks (Combined Optimizations - NEW):
│   ├── tathybrid_topk10_chunk1500_experiment.ipynb ✅ NEW!
│   ├── finhybrid_topk10_chunk1500_experiment.ipynb ✅ NEW!
│   └── finhybrid_topk10_temp03_experiment.ipynb ✅ NEW!
│
├── Results:
│   ├── tathybrid_topk10/ ✅
│   ├── finhybrid_topk10/ ✅
│   ├── nqtext_topk10/ ✅
│   ├── fetatab_topk10/ ✅
│   ├── papertext_topk10/ ✅
│   ├── papertab_topk10/ ✅
│   ├── tathybrid_topk10_chunk1500/ 🔄 After running
│   ├── finhybrid_topk10_chunk1500/ 🔄 After running
│   └── finhybrid_topk10_temp03/ 🔄 After running
│
└── Documentation:
    ├── COMPLETE_TOPK10_FINAL_REPORT.md ✅
    ├── TOPK10_COMPLETE_SUMMARY.csv ✅
    ├── create_combined_optimizations.py ✅
    └── THIS FILE (Combined optimization guide)
```

---

## 🎉 **Ready to Run!**

**You have:**
- ✅ 3 combined optimization notebooks ready
- ✅ Clear strategy and expectations
- ✅ Estimated time and cost
- ✅ Success metrics defined

**Next step:**
```bash
cd experiments/nemotron-3-ultra-550b/2_optimization
jupyter notebook finhybrid_topk10_temp03_experiment.ipynb
```

**Let's test if stacked optimizations work!** 🚀

---

**Created:** June 29, 2026  
**Status:** Ready to run  
**Expected Total:** ~90-130 min, ~$19-30, +8-15 more questions answered
