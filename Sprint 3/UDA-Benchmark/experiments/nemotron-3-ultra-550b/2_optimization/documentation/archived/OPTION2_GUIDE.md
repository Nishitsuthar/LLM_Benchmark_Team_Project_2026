# 🚀 Option 2: Validate TOP_K=10 Across Datasets

**Goal:** Test if TOP_K=10 helps other datasets too  
**Experiments:** NqText and TatHybrid with TOP_K=10  
**Status:** ✅ Ready to run

---

## 📊 What We're Testing

We confirmed TOP_K=10 improves FinHybrid by 4.3%. Now we test if it helps:

1. **NqText** (Wikipedia articles) - Currently 14.1% empty
2. **TatHybrid** (Finance tables) - Currently 22.8% empty

This validates whether TOP_K=10 is a good default across different domains.

---

## 📋 Experiment Details

### Experiment 1: NqText (Wikipedia)

**Baseline Performance:**
- Score: 27.6% Span F1
- Empty: 11/78 (14.1%) ← Already pretty good!
- Documents: 4 Wikipedia PDFs
- Runtime: ~30-40 minutes
- Cost: ~$5-8

**Expected with TOP_K=10:**
- Empty: 14.1% → ~10-12% (-2 to -4%)
- Score: 27.6% → ~29-31% (+2-4%)
- 2-3 more questions answered

**Why test this?**
- Different domain (Wikipedia vs Finance)
- Already low empty rate (can we make it even better?)
- Medium-sized dataset (validates on different scale)

---

### Experiment 2: TatHybrid (Finance - Tables)

**Baseline Performance:**
- Score: 43.5% Numeracy F1 ⭐ (best performer!)
- Empty: 37/162 (22.8%)
- Documents: 4 financial PDFs
- Runtime: ~60-90 minutes
- Cost: ~$13-20

**Expected with TOP_K=10:**
- Empty: 22.8% → ~18-20% (-3 to -5%)
- Score: 43.5% → ~45-48% (+2-5%)
- 5-8 more questions answered

**Why test this?**
- Largest dataset (162 Q&A) - best statistical significance
- Table-heavy documents (tests retrieval on structured data)
- Best baseline score (can we push it even higher?)

---

## 🎯 Success Criteria

### Minimum Success (Validates Approach):
- ✅ Both datasets show ANY improvement in empty rate
- ✅ Neither dataset gets significantly worse
- ✅ Confirms TOP_K=10 is broadly helpful

### Good Success:
- ✅ Both datasets improve by ≥3%
- ✅ NqText gets below 12% empty
- ✅ TatHybrid gets below 20% empty

### Excellent Success:
- ✅ Both datasets improve by ≥5%
- ✅ NqText gets below 10% empty
- ✅ TatHybrid gets below 18% empty and above 46% score

---

## 🚀 How to Run

### Option A: Run Sequentially (Recommended)

**Start with NqText (faster, cheaper):**

```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark/experiments/nemotron-3-ultra-550b/2_optimization"

jupyter notebook nqtext_topk10_experiment.ipynb
```

1. Kernel → Restart & Clear Output
2. Cell → Run All
3. Wait ~30-40 minutes
4. Check results

**Then run TatHybrid (longer):**

```bash
jupyter notebook tathybrid_topk10_experiment.ipynb
```

1. Kernel → Restart & Clear Output
2. Cell → Run All
3. Wait ~60-90 minutes (can run overnight!)
4. Check results

**Total Time:** ~90-130 minutes  
**Total Cost:** ~$18-28

---

### Option B: Run in Parallel (If You Have Time)

Open two Jupyter tabs and run both simultaneously:

**Tab 1:** NqText (finishes in 30-40 min)  
**Tab 2:** TatHybrid (finishes in 60-90 min)

**Total Wall-Clock Time:** ~60-90 minutes (saves ~30 min)  
**Total Cost:** Same (~$18-28)

---

## 📊 Baseline Comparisons

### NqText Baseline to Beat:

| Document | Empty Responses | Baseline |
|----------|----------------|----------|
| Supreme Court | 0/57 (0%) | ⭐ Perfect! |
| Hannah John-Kamen | 2/4 (50%) | ⚠️ High |
| Oklahoma | 0/4 (0%) | ⭐ Perfect! |
| Tour de France | 9/13 (69%) | ⚠️⚠️ Very high |
| **TOTAL** | **11/78 (14.1%)** | Good overall |

**Key insight:** Tour de France has 69% empty! If TOP_K=10 fixes even 2-3 of those, it's a big win.

---

### TatHybrid Baseline to Beat:

| Metric | Baseline |
|--------|----------|
| Score | 43.5% Numeracy F1 |
| Empty | 37/162 (22.8%) |
| Documents | 4 financial reports |
| Best Performer | Already #1! |

**Key insight:** TatHybrid already performs best. If TOP_K=10 improves it further, that validates the optimization strongly!

---

## 📝 What to Watch For

### While Running NqText:

**Cell 3:** Should show working directory ending in "UDA-Benchmark"  
**Cell 4:** Should show "✓ All imports successful"  
**Cell 12:** Processing 4 documents (Supreme Court, Tour de France, etc.)  
**Cell 13:** Watch empty count - aim for <10/78

**Key Question:** Does Tour de France improve? (Currently 69% empty!)

---

### While Running TatHybrid:

**Cell 3:** Should show working directory ending in "UDA-Benchmark"  
**Cell 4:** Should show "✓ All imports successful"  
**Cell 12:** Processing 4 financial documents, 162 Q&A total  
**Cell 13:** Watch empty count - aim for <35/162  
**Cell 14:** Watch Numeracy F1 score - aim for >45%

**This will take a while (60-90 min) - perfect for running overnight or during lunch!**

---

## 🎯 Expected Results Summary

### Conservative Estimate:

```
NqText:
  Baseline:  27.6% score, 14.1% empty (11/78)
  Optimized: 29-30% score, 11-12% empty (9-10/78)
  Improvement: +2-4% score, -2-3 empty responses ✅

TatHybrid:
  Baseline:  43.5% score, 22.8% empty (37/162)
  Optimized: 45-46% score, 19-21% empty (31-34/162)
  Improvement: +2-3% score, -3-6 empty responses ✅
```

### Optimistic Estimate:

```
NqText:
  Baseline:  27.6% score, 14.1% empty
  Optimized: 30-32% score, 9-10% empty (7-8/78)
  Improvement: +3-5% score, -3-4 empty responses ✅✅

TatHybrid:
  Baseline:  43.5% score, 22.8% empty
  Optimized: 46-48% score, 18-19% empty (29-31/162)
  Improvement: +3-5% score, -6-8 empty responses ✅✅
```

---

## 📈 What This Tells Us

### If Both Improve (Expected):
✅ **Confirms TOP_K=10 is a good universal improvement**  
✅ **Can confidently apply to remaining datasets**  
✅ **Should make it the new default for all experiments**

### If Only One Improves:
⚠️ **TOP_K=10 is dataset-dependent**  
✅ **Still useful, but need to test per dataset**  
⚠️ **May need different values for different domains**

### If Neither Improve:
⚠️ **FinHybrid improvement might have been lucky**  
⚠️ **Need to try different optimization approach**  
✅ **Still learned something valuable!**

---

## 🚀 After These Experiments

Once both are complete, you'll have:

1. **3 datasets tested with TOP_K=10**
   - FinHybrid: ✅ 4.3% improvement
   - NqText: ? (testing now)
   - TatHybrid: ? (testing now)

2. **Clear data on whether TOP_K=10 helps broadly**

3. **Decision point:**
   - If yes → Apply to all 6 datasets
   - If no → Try different optimization (CHUNK_SIZE, TEMPERATURE)

---

## 💡 Tips

### For NqText:
- Should finish in 30-40 minutes
- Watch Tour de France document (69% empty baseline)
- Even 2-3 improvements = success

### For TatHybrid:
- Will take 60-90 minutes (longest experiment)
- Great to run overnight or during lunch
- Large sample (162 Q&A) = most statistically significant
- Currently best performer - any improvement is impressive!

### General:
- ✅ Restart kernel before running
- ✅ Run all cells from beginning
- ✅ Don't close browser while running
- ✅ Check Cell 3 shows correct working directory

---

## 📊 Files That Will Be Created

**NqText Results:**
`experiments/nemotron-3-ultra-550b/2_optimization/results/nqtext_topk10/nqtext_results_*.csv`

**TatHybrid Results:**
`experiments/nemotron-3-ultra-550b/2_optimization/results/tathybrid_topk10/tathybrid_results_*.csv`

---

## ✅ Ready to Start!

**Recommended order:**

1. **Start NqText** (~30-40 min)
2. **While NqText runs:** Take a break, grab coffee ☕
3. **After NqText finishes:** Review results (I can help!)
4. **Start TatHybrid** (~60-90 min)
5. **While TatHybrid runs:** Dinner, or run overnight 🌙
6. **After both complete:** Compare all 3 datasets!

**Let's go!** Open Jupyter and start with NqText:

```bash
cd experiments/nemotron-3-ultra-550b/2_optimization
jupyter notebook nqtext_topk10_experiment.ipynb
```

---

**Good luck!** 🚀 Let me know when the results are ready and I'll analyze them!
