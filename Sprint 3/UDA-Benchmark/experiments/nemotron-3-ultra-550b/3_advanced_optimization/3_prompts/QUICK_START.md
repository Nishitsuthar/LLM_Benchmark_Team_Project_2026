# ⚡ QUICK START - Phase 3C Prompt Engineering

**Read this first to run the experiments immediately!**

---

## 🎯 What We're Doing

Testing 3 prompt variants on FinHybrid (worst performer) to find which one improves empty response rate.

**Current baseline:** 36.2% empty (17/47 questions)  
**Target:** <30% empty (+3-7 questions)  
**Time:** ~60-90 minutes total (3 variants × 20-30 min each)

---

## 🚀 Step-by-Step Instructions

### 1. Open First Notebook (Instruction Prompt)

```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark"

jupyter notebook experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/finhybrid_instruction_experiment.ipynb
```

### 2. Run the Notebook

In Jupyter:
1. Click **Kernel → Restart & Run All**
2. Wait ~20-30 minutes
3. Check results at the end

### 3. Record Results

At the end of the notebook, you'll see:

```
Phase 2 (Baseline): 17/47 empty (36.2%)
Phase 3C (Instruction): ?/47 empty (?%)

Improvement: +? questions
```

**Write down:**
- Empty count: `?`
- Empty rate: `?%`
- Improvement: `+?`

### 4. Repeat for Few-Shot

```bash
jupyter notebook experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/finhybrid_fewshot_experiment.ipynb
```

Run and record results.

### 5. Repeat for CoT (Optional)

Only if first 2 results are disappointing.

```bash
jupyter notebook experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/finhybrid_cot_experiment.ipynb
```

Run and record results (this one costs 2x tokens).

---

## 📊 Comparison Table

After running all 3, fill this in:

| Variant | Empty Count | Empty Rate | Change | Cost |
|---------|-------------|------------|--------|------|
| **Phase 2** | 17 | 36.2% | - | Baseline |
| **Instruction** | ? | ?% | +? | Same |
| **Few-Shot** | ? | ?% | +? | +20% |
| **CoT** | ? | ?% | +? | 2x |

---

## ✅ Decision Matrix

**Choose instruction if:**
- It improved by +2-4 questions
- Similar or better than few-shot
- Best improvement/cost ratio

**Choose few-shot if:**
- It improved by +3+ questions
- Better than instruction
- Worth the +20% cost

**Choose CoT if:**
- It improved by +5+ questions significantly more than others
- Worth the 2x cost increase

---

## 🎯 Next Step After Choosing

If you chose **instruction**, create notebooks for all 6 datasets:
- `tathybrid_instruction_experiment.ipynb`
- `nqtext_instruction_experiment.ipynb`
- `fetatab_instruction_experiment.ipynb`
- `papertext_instruction_experiment.ipynb`
- `papertab_instruction_experiment.ipynb`
- `finhybrid_instruction_experiment.ipynb` (already done ✅)

Copy the finhybrid notebook and change:
- Dataset name (e.g., `DATASET_NAME = "tat"`)
- Output directory (e.g., `tathybrid_instruction`)
- Document list (check Phase 2 notebooks for correct doc names)

---

## 💡 Tips

1. **Run in order:** Instruction → Few-Shot → (CoT if needed)
2. **Don't skip:** Test all variants to make informed decision
3. **Record everything:** You'll need to compare later
4. **Check empty rate:** Primary metric (not just scores)
5. **Consider cost:** Improvement vs token cost tradeoff

---

## ⏱️ Timeline

- **Instruction test:** 20-30 min
- **Few-shot test:** 20-30 min
- **CoT test (optional):** 25-35 min
- **Total:** 60-90 minutes for all 3

---

## 🆘 If Something Goes Wrong

**Import error:**
```python
ModuleNotFoundError: No module named 'uda.utils.prompts'
```
**Fix:** Check you ran `cd` to project root first

**Wrong directory error:**
```
FileNotFoundError: dataset/qa/fin_qa.csv
```
**Fix:** Cell 2 should show correct working directory

**API error:**
```
AuthenticationError: Invalid API key
```
**Fix:** Check `uda/utils/access_config.py` has valid Together AI key

---

## 📁 Where Results Are Saved

```
experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/results/
├── finhybrid_instruction/
│   └── finhybrid_instruction_YYYYMMDD_HHMMSS.csv
├── finhybrid_fewshot/
│   └── finhybrid_fewshot_YYYYMMDD_HHMMSS.csv
└── finhybrid_cot/
    └── finhybrid_cot_YYYYMMDD_HHMMSS.csv
```

---

## 🎉 Expected Outcome

After testing all 3 variants:

**Best case:** One variant reduces empty rate to ~25-30% (+5-7 questions)
**Good case:** One variant reduces empty rate to ~30-32% (+3-5 questions)
**Acceptable:** Any variant improves by +2+ questions

Then scale winning variant to all 6 datasets for overall <12% empty target!

---

**Ready to start! Open the first notebook and run it!** 🚀

**First command:**
```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark"
jupyter notebook experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/finhybrid_instruction_experiment.ipynb
```
