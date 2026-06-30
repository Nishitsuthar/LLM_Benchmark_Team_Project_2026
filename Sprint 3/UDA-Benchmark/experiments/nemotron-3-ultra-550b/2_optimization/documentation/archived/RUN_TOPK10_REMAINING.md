# 🚀 Run Remaining TOP_K=10 Experiments

**Date:** June 29, 2026  
**Status:** 3/6 Complete, 3/6 Remaining  
**Goal:** Complete TOP_K=10 validation across all 6 datasets

---

## ✅ Already Complete (3/6)

| Dataset | Status | Empty Improvement | Time | Cost | Result File |
|---------|--------|------------------|------|------|-------------|
| **FinHybrid** | ✅ | 44.7% → 40.4% (+4.3%) | ~15-20 min | ~$3-5 | `finhybrid_results_20260629_152848.csv` |
| **NqText** | ✅ | 14.1% → 7.7% (+6.4%) 🌟 | ~30-40 min | ~$5-8 | `nqtext_results_20260629_154410.csv` |
| **TatHybrid** | ✅ | 22.8% → 21.0% (+1.9%) | ~60-90 min | ~$13-20 | `tathybrid_results_20260629_155316.csv` |

**Total so far:** 287 Q&A, +10 questions answered, ~2-3 hours, ~$22-33

---

## 🔄 Remaining (3/6)

### 1. PaperText (Academic - Text)
- **Q&A:** 13 pairs
- **Baseline:** 43.0% score, 7.7% empty (already best retrieval!)
- **Expected:** Small improvement or stable (already very good)
- **Time:** ~5-10 minutes
- **Cost:** ~$2-3
- **Priority:** Medium (good for completeness)
- **Notebook:** `papertext_topk10_experiment.ipynb` ✅ Ready

### 2. PaperTab (Academic - Tables)  
- **Q&A:** 4 pairs (small sample)
- **Baseline:** 38.0% score, 75% empty (3/4 empty!)
- **Expected:** Could improve OR stay similar (small sample variance)
- **Time:** ~3-5 minutes
- **Cost:** ~$1-2
- **Priority:** Low (small sample, high variance)
- **Notebook:** `papertab_topk10_experiment.ipynb` ✅ Ready

### 3. FetaTab (Wikipedia - Tables)
- **Q&A:** 8 pairs
- **Baseline:** 31.3% score, ~20% empty
- **Expected:** Modest improvement (+2-4% fewer empty)
- **Time:** ~5-10 minutes
- **Cost:** ~$2-3
- **Priority:** High (good sample size, moderate empty rate)
- **Notebook:** `fetatab_topk10_experiment.ipynb` ✅ Ready

---

## 🎯 Recommended Running Order

### Option A: Quick Finish (All 3 Together)
**Best for:** Getting complete picture ASAP

```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark/experiments/nemotron-3-ultra-550b/2_optimization"

# Run all 3 in sequence (total ~15-25 min)
jupyter notebook papertext_topk10_experiment.ipynb  # 5-10 min
# After complete, run:
jupyter notebook fetatab_topk10_experiment.ipynb    # 5-10 min
# After complete, run:
jupyter notebook papertab_topk10_experiment.ipynb   # 3-5 min
```

**Total:** ~15-25 minutes, ~$5-8

---

### Option B: Priority Order (Test Most Interesting First)
**Best for:** Getting actionable insights quickly

**Order:**
1. **FetaTab first** - Good sample size, moderate empty rate, likely to show clear improvement
2. **PaperText second** - Already best performer, validate it stays good/improves
3. **PaperTab last** - Small sample, just for completeness

---

## 📊 Expected Final Results (All 6 Datasets)

After completing these 3:

### Overall Metrics
- **Total Q&A:** 312 (all datasets)
- **Current empty (3 tested):** 24.0% → 20.6% (-3.5%)
- **Expected empty (all 6):** 24.4% → ~20-21% (-4-5%)
- **Expected improvement:** +15-20 total questions answered

### By Dataset
| Dataset | Baseline Empty | Expected Optimized | Expected Change |
|---------|---------------|-------------------|-----------------|
| FinHybrid ✅ | 44.7% | 40.4% | +4.3% ✅ |
| NqText ✅ | 14.1% | 7.7% | +6.4% 🌟 |
| TatHybrid ✅ | 22.8% | 21.0% | +1.9% ✅ |
| PaperText 🔄 | 7.7% | 5-7% | +0-1 question |
| FetaTab 🔄 | ~20% | 15-18% | +0-1 question |
| PaperTab 🔄 | 75% | 50-75% | 0-1 question (high variance) |

---

## ✅ After Completion Checklist

Once all 3 experiments complete:

- [ ] All 6 result CSV files exist in `results/*/`
- [ ] Check total improvement: Count total questions answered
- [ ] Update `COMPREHENSIVE_RESULTS_TOPK10.md` with all 6 datasets
- [ ] Create final comparison visualization
- [ ] Decide: Make TOP_K=10 the new baseline? (likely YES!)
- [ ] Document decision and reasoning

---

## 🚀 Next Phase (After This)

Once TOP_K=10 is validated on all 6 datasets:

### Immediate Next Tests:
1. **CHUNK_SIZE=1500** on TatHybrid (table-heavy, expected high impact)
2. **CHUNK_SIZE=1500** on FinHybrid (table-heavy, needs help)
3. **TOP_K=15** on NqText (push best performer further)
4. **TEMPERATURE=0.3** on FinHybrid (quick test, reduce conservatism)

### Combined Optimizations:
5. **TOP_K=10 + CHUNK_SIZE=1500** on TatHybrid
6. **TOP_K=10 + CHUNK_SIZE=1500** on FinHybrid

---

## 💡 Tips for Running

### Before Each Notebook:
1. ✅ **Restart kernel** (Kernel → Restart & Clear Output)
2. ✅ **Check API credits** (Together AI account)
3. ✅ **Monitor progress** (watch for empty warnings)

### During Run:
- ⏱️ Small datasets (FetaTab, PaperTab): Watch in real-time (3-10 min)
- ⏱️ Medium datasets (PaperText): Can step away (5-10 min)
- 📊 Track empty responses per document (printed during run)

### After Run:
- ✅ Check results CSV was created in `results/{dataset}_topk10/`
- ✅ Compare empty rate vs baseline
- ✅ Note any interesting patterns (which documents improved most)

---

## 📈 Success Metrics

### Minimum Success:
- [ ] All 3 experiments complete without errors
- [ ] At least 2/3 show improvement (maintain 100% success rate)
- [ ] Overall empty rate <21%

### Target Success:
- [ ] All 3 experiments show improvement OR stay stable (if already good)
- [ ] Overall empty rate <20%
- [ ] +2-4 more questions answered

### Stretch Success:
- [ ] All experiments show clear improvement
- [ ] Overall empty rate <19%
- [ ] +5+ more questions answered

---

## 🎯 Current Progress

**Phase 1:** ✅✅✅✅✅✅ (6/6 datasets baseline complete)  
**Phase 2 TOP_K=10:** ✅✅✅ 🔄🔄🔄 (3/6 complete, 3/6 remaining)

**Next:** Run the remaining 3 notebooks to complete TOP_K=10 validation!

---

**Created:** June 29, 2026  
**Status:** Ready to run  
**Estimated Total Time:** 15-25 minutes  
**Estimated Total Cost:** $5-8  
**Expected Outcome:** Complete TOP_K=10 validation, establish new baseline
