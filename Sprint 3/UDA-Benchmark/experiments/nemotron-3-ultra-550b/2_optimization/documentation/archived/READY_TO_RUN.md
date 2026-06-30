# 🚀 First Optimization Experiment - Ready to Run!

**Date:** June 29, 2026  
**Experiment:** FinHybrid with TOP_K=10  
**Status:** Notebook created, ready to execute

---

## 📊 Experiment Details

### What We're Testing
**Parameter:** TOP_K (number of chunks retrieved)  
**Baseline:** TOP_K = 5  
**Optimized:** TOP_K = 10  
**Hypothesis:** Retrieving more chunks will reduce empty responses

### Why This First?
1. **Lowest cost:** ~$3-5, 15-20 minutes
2. **Highest impact:** Targets the main bottleneck (40.4% empty rate)
3. **Quick validation:** Fast feedback on optimization approach
4. **FinHybrid worst performer:** 23.4% accuracy, most room for improvement

---

## 📈 Baseline Performance (Phase 1)

**FinHybrid Baseline Results:**
- **Score:** 23.4% (Exact Match ±1%)
- **Empty Rate:** 40.4% (19 out of 47 questions)
- **Q&A Pairs:** 47 total (from 4 financial PDFs)
- **Documents:** ADI_2009, ABMD_2012, GS_2016, JKHY_2015
- **Result File:** `1_without_optimization/finhybrid/results/finhybrid_results_20260629_120808.csv`

**Main Problem:** Very high empty response rate (40.4%)  
**Root Cause:** TOP_K=5 may be too low, missing relevant information

---

## 🎯 Expected Results

### Conservative Estimate
- **Score:** 23.4% → **26-28%** (+2-5%)
- **Empty Rate:** 40.4% → **30-35%** (-5-10%)
- **Improvement:** Moderate score gain, significant empty reduction

### Optimistic Estimate
- **Score:** 23.4% → **28-30%** (+5-7%)
- **Empty Rate:** 40.4% → **28-32%** (-8-12%)
- **Improvement:** Good score gain, major empty reduction

### Success Criteria
- ✅ Empty rate drops by at least 5%
- ✅ Score improves or stays same
- ✅ No unexpected errors
- ✅ Results are reproducible

---

## 🚀 How to Run (Step by Step)

### Step 1: Navigate to Optimization Directory
```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark/experiments/nemotron-3-ultra-550b/2_optimization"
```

### Step 2: Open Jupyter Notebook
```bash
jupyter notebook finhybrid_topk10_experiment.ipynb
```

### Step 3: In Jupyter
1. **Kernel → Restart & Clear Output** (IMPORTANT!)
2. **Cell → Run All**
3. Wait ~15-20 minutes
4. Monitor for any errors

### Step 4: Check Results
Look for the output at the end of the notebook:
- Overall score (Exact Match ±1%)
- Empty response count and percentage
- Per-document breakdown
- Result CSV saved to: `results/finhybrid_topk10/finhybrid_topk10_results_*.csv`

---

## 📊 What Changed in the Notebook

### Parameter Updates
```python
# Baseline (Phase 1)
TOP_K = 5

# Optimized (Phase 2)
TOP_K = 10  ← Changed!
```

### Output Directory
```python
# Baseline
OUTPUT_DIR = "./experiments/nemotron-3-ultra-550b/1_without_optimization/finhybrid/results"

# Optimized
OUTPUT_DIR = "./experiments/nemotron-3-ultra-550b/2_optimization/results/finhybrid_topk10"  ← Changed!
```

### Everything Else
- CHUNK_SIZE = 3000 (same)
- CHUNK_OVERLAP = 300 (same)
- TEMPERATURE = 0.1 (same)
- MAX_TOKENS = 512 (same)
- All other code identical to baseline

---

## 📋 Monitoring Checklist

While the notebook is running, watch for:

### Cell 2: Project Root
```
Working directory: /Users/I772947/personal work/.../UDA-Benchmark
```
✓ Should show correct project root

### Cell 5: Parameters
```
TOP_K = 10
OUTPUT_DIR = ./experiments/nemotron-3-ultra-550b/2_optimization/results/finhybrid_topk10
```
✓ Verify TOP_K is 10, not 5

### Cell 11: Q&A Loading
```
Total documents loaded: 4
Total Q&A pairs: 47
```
✓ Should match baseline (4 docs, 47 Q&A)

### Cell 13: Main Processing Loop
Watch for:
- Processing each of 4 documents
- ~12 questions per document
- Some empty warnings are normal
- Takes ~15-20 minutes total

### Cell 14: Empty Response Diagnostic
```
Empty responses: X out of 47 (Y%)
```
✓ Compare to baseline (19 out of 47 = 40.4%)
✓ Should see fewer empty responses!

### Cell 15: Evaluation
```
Exact Match ±1%: Z.Z%
```
✓ Compare to baseline (23.4%)
✓ Should see improvement!

### Cell 16: Save Results
```
Results saved to: results/finhybrid_topk10/finhybrid_topk10_results_*.csv
```
✓ Verify CSV file created

---

## 📊 How to Compare Results

### Quick Comparison

```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark"

# Count empty responses in baseline
grep ',"",' experiments/nemotron-3-ultra-550b/1_without_optimization/finhybrid/results/finhybrid_results_20260629_120808.csv | wc -l

# Count empty responses in optimized (after running)
grep ',"",' experiments/nemotron-3-ultra-550b/2_optimization/results/finhybrid_topk10/finhybrid_topk10_results_*.csv | wc -l
```

### Detailed Comparison

Create a simple comparison:

```python
import pandas as pd

# Load baseline
baseline = pd.read_csv("experiments/nemotron-3-ultra-550b/1_without_optimization/finhybrid/results/finhybrid_results_20260629_120808.csv")

# Load optimized (update filename with actual timestamp)
optimized = pd.read_csv("experiments/nemotron-3-ultra-550b/2_optimization/results/finhybrid_topk10/finhybrid_topk10_results_*.csv")

# Compare empty rates
baseline_empty = (baseline['response'].str.strip() == '').sum()
optimized_empty = (optimized['response'].str.strip() == '').sum()

print(f"Baseline empty:  {baseline_empty}/47 = {baseline_empty/47*100:.1f}%")
print(f"Optimized empty: {optimized_empty}/47 = {optimized_empty/47*100:.1f}%")
print(f"Improvement:     {baseline_empty - optimized_empty} fewer empty ({(baseline_empty - optimized_empty)/47*100:.1f}%)")
```

---

## 💰 Cost & Time Estimate

**Expected:**
- **Runtime:** 15-20 minutes
- **Cost:** ~$3-5
- **API Calls:** ~47 questions × 2 API calls each = ~94 calls
- **Tokens:** Similar to baseline (~2-3k tokens per Q&A)

**Why So Fast?**
- Only 47 Q&A pairs
- Small to medium PDFs
- No complex preprocessing

---

## ⚠️ Troubleshooting

### If Notebook Fails

**Error: "PDF not found"**
- Check Cell 2 project root is correct
- Verify path shows UDA-Benchmark directory

**Error: "Module not found"**
- Restart kernel
- Run Cell 1-4 again to import all modules

**Error: "API rate limit"**
- Wait 1 minute
- Resume from failed question

**Error: "No module named 'uda'"**
- Check Cell 2 executed correctly
- Verify `sys.path.insert(0, project_root)` ran

### If Results Look Wrong

**Empty rate increased:**
- Possible but unlikely with TOP_K=10
- Check if API had issues
- Review empty warnings in output

**Score decreased:**
- Also possible but unlikely
- More context can sometimes confuse model
- Still valuable data point!

**No change at all:**
- Verify TOP_K actually changed to 10
- Check Cell 5 shows TOP_K = 10

---

## ✅ Success Checklist

After running, verify:

- [ ] Notebook ran without errors
- [ ] All 47 Q&A processed
- [ ] Result CSV file created in `results/finhybrid_topk10/`
- [ ] Empty response count documented
- [ ] Evaluation score calculated
- [ ] Results saved successfully

Compare to baseline:
- [ ] Empty rate decreased (ideally by 5-10%)
- [ ] Score improved or stayed same
- [ ] No unexpected errors
- [ ] Results make sense

---

## 🎯 Next Steps After This Experiment

### If It Works Well (Empty rate drops 5-10%+):
1. ✅ Test TOP_K=15 on FinHybrid (even more coverage)
2. ✅ Test TOP_K=10 on NqText (different dataset)
3. ✅ Apply TOP_K=10 to all 6 datasets (full comparison)

### If It Works Moderately (Empty rate drops 3-5%):
1. ✅ Still worth it! Apply to other datasets
2. ✅ Combine with CHUNK_SIZE optimization next
3. ✅ Test TOP_K=15 to see if higher is better

### If It Doesn't Help Much (<3% improvement):
1. ⚠️ Don't worry! This is valuable data
2. ✅ Try CHUNK_SIZE=1500 next (different approach)
3. ✅ Try TEMPERATURE=0.3 (less conservative)
4. ✅ Consider that FinHybrid is just a hard dataset

---

## 📝 Document Your Results

After the experiment, note down:

1. **Final Metrics:**
   - Score: ___%
   - Empty rate: ___%
   - Runtime: ___ minutes
   - Cost: ~$___

2. **Comparison to Baseline:**
   - Score change: ___ (+/- ___%)
   - Empty change: ___ (+/- ___%)
   - Improvement: YES / NO / MIXED

3. **Observations:**
   - Any patterns in which questions improved?
   - Which documents had better results?
   - Any unexpected behavior?

4. **Decision:**
   - [ ] Continue with TOP_K=10 for other datasets
   - [ ] Try TOP_K=15 next
   - [ ] Try different optimization approach
   - [ ] Combine with other optimizations

---

## 🎉 Ready to Run!

Everything is set up. Just run these commands:

```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark/experiments/nemotron-3-ultra-550b/2_optimization"

jupyter notebook finhybrid_topk10_experiment.ipynb
```

Then in Jupyter:
1. **Kernel → Restart & Clear Output**
2. **Cell → Run All**
3. Wait ~15-20 minutes
4. Check results!

**Good luck!** 🚀 You're about to see your first optimization improvement!

---

**Created:** June 29, 2026  
**Experiment:** finhybrid_topk10  
**Expected Runtime:** 15-20 minutes  
**Expected Cost:** $3-5  
**Expected Improvement:** -5 to -10% empty rate, +2 to +5% score
