# ✅ Ready to Run - Remaining TOP_K=10 Experiments

**Date:** June 29, 2026  
**Status:** All 3 notebooks created and ready to run  
**Total Time:** ~15-25 minutes  
**Total Cost:** ~$5-8

---

## 🎯 Quick Start

Navigate to optimization folder:
```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark/experiments/nemotron-3-ultra-550b/2_optimization"
```

---

## 📋 Run in This Order

### 1. FetaTab (Priority: High)
**Why first:** Good sample size (8 Q&A), moderate empty rate (~20%), likely clear improvement

```bash
jupyter notebook fetatab_topk10_experiment.ipynb
```

- **Time:** 5-10 minutes
- **Cost:** ~$2-3
- **Baseline:** 31.3% score, ~20% empty
- **Expected:** 15-18% empty (+2-3 questions)

**After complete:** Check `results/fetatab_topk10/fetatab_results_*.csv`

---

### 2. PaperText (Priority: Medium)
**Why second:** Already best performer (7.7% empty), validate it stays good

```bash
jupyter notebook papertext_topk10_experiment.ipynb
```

- **Time:** 5-10 minutes
- **Cost:** ~$2-3
- **Baseline:** 43.0% score, 7.7% empty (best retrieval!)
- **Expected:** Stable or slight improvement (5-7% empty)

**After complete:** Check `results/papertext_topk10/papertext_results_*.csv`

---

### 3. PaperTab (Priority: Low)
**Why last:** Very small sample (4 Q&A), high variance, just for completeness

```bash
jupyter notebook papertab_topk10_experiment.ipynb
```

- **Time:** 3-5 minutes
- **Cost:** ~$1-2
- **Baseline:** 38.0% score, 75% empty (3/4 empty!)
- **Expected:** High variance due to small sample

**After complete:** Check `results/papertab_topk10/papertab_results_*.csv`

---

## 📊 What We'll Know After This

### Complete Picture:
- ✅ **All 6 datasets** tested with TOP_K=10
- ✅ **Universal validation** across domains (Finance, Wikipedia, Academic)
- ✅ **Full statistics** on improvement vs baseline
- ✅ **Decision-ready** data on making TOP_K=10 the new baseline

### Expected Final Results:
| Metric | Baseline (Phase 1) | Optimized (Phase 2) | Improvement |
|--------|-------------------|---------------------|-------------|
| **Total Q&A** | 312 | 312 | Same |
| **Avg Empty Rate** | 24.4% | ~20-21% | **-4-5%** ✅ |
| **Questions Answered** | 236 | ~250-255 | **+15-20** ✅ |
| **Success Rate** | - | 100% (all improved) | ✅ |

---

## ✅ Before Running Checklist

- [x] All 3 notebooks created (`fetatab_topk10`, `papertext_topk10`, `papertab_topk10`)
- [x] Notebooks in correct directory (`2_optimization/`)
- [x] TOP_K=10 parameter set correctly
- [x] OUTPUT_DIR points to optimization results folder
- [ ] API credits available (~$5-8 needed)
- [ ] 15-25 minutes available for all 3 runs

---

## 🚀 After All 3 Complete

### Immediate:
1. ✅ Verify all 3 result CSV files created
2. ✅ Compare each vs baseline (empty rate improvement)
3. ✅ Note any interesting patterns

### Analysis:
4. ✅ Update `COMPREHENSIVE_RESULTS_TOPK10.md` with all 6 datasets
5. ✅ Calculate final overall statistics
6. ✅ Create comparison visualization (optional)
7. ✅ Document decision: Make TOP_K=10 new baseline?

### Next Phase:
8. 🔄 Test other parameters (CHUNK_SIZE, TEMPERATURE)
9. 🔄 Stack optimizations (TOP_K=10 + CHUNK_SIZE=1500)
10. 🔄 Target: 45-50% average score, <15% empty rate

---

## 💡 Running Tips

### During Each Run:
- Watch for empty warnings (normal, informative)
- Note which documents improve most
- Track runtime and cost for planning

### If Something Goes Wrong:
- Restart kernel and try again
- Check API key in `uda/utils/access_config.py`
- Verify paths are correct
- Check PDF files exist

### Success Indicators:
- ✅ Result CSV file created
- ✅ No Python errors
- ✅ Empty rate same or better vs baseline
- ✅ Runtime matches expected (~3-10 min per dataset)

---

## 📈 Progress Tracking

**Phase 1 Baseline:** ✅✅✅✅✅✅ (6/6 complete)  
**Phase 2 TOP_K=10:** ✅✅✅🔄🔄🔄 (3/6 complete, 3/6 ready to run)

**Current Status:**
- ✅ FinHybrid TOP_K=10 complete (44.7% → 40.4% empty, +4.3%)
- ✅ NqText TOP_K=10 complete (14.1% → 7.7% empty, +6.4% 🌟)
- ✅ TatHybrid TOP_K=10 complete (22.8% → 21.0% empty, +1.9%)
- 🔄 FetaTab TOP_K=10 ready to run
- 🔄 PaperText TOP_K=10 ready to run
- 🔄 PaperTab TOP_K=10 ready to run

---

## 🎯 Goal

**Complete TOP_K=10 validation across all 6 datasets to establish new optimized baseline!**

Then we can stack other optimizations (CHUNK_SIZE, TEMPERATURE) on top with confidence.

---

**Ready?** Let's run them! 🚀

```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark/experiments/nemotron-3-ultra-550b/2_optimization"

jupyter notebook fetatab_topk10_experiment.ipynb
```
