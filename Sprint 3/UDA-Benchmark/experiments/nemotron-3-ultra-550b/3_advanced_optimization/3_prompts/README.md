# Phase 3C: Prompt Engineering

**Date Created:** June 29, 2026  
**Status:** Ready to run  
**Priority:** HIGH (after Phase 3A pdfplumber abandonment)

---

## 📍 Overview

**Goal:** Improve QA performance through better prompting strategies

**Approach:** Test 3 prompt variants on FinHybrid, choose best, scale to all datasets

**Expected Impact:** +10-20 questions overall (vs Phase 2 baseline)

**Investment:** 3-4 hours, ~$40-60

---

## 🎯 Current Baseline (Phase 2)

| Dataset | Empty Rate | Score | Config |
|---------|------------|-------|--------|
| **FinHybrid** | 36.2% (17/47) | 34.04% EM | TOP_K=10, CHUNK=1500 |
| **TatHybrid** | 16.0% (26/162) | 57.91 F1 | TOP_K=10, CHUNK=1500 |
| **NqText** | 7.7% (6/78) | 27.6% F1 | TOP_K=10, CHUNK=3000 |
| **FetaTab** | 25.0% (2/8) | 31.3% F1 | TOP_K=10, CHUNK=1500 |
| **PaperText** | 7.7% (1/13) | 43.0% F1 | TOP_K=10, CHUNK=3000 |
| **PaperTab** | 0.0% (0/4) | 38.0% F1 | TOP_K=10, CHUNK=1500 |
| **OVERALL** | **16.7% (52/312)** | **34.3% avg** | Mixed |

**Target:** <12% empty overall

---

## 📝 3 Prompt Variants

### 1. Instruction-Enhanced (Phase 3C-1)

**File:** `notebooks/finhybrid_instruction_experiment.ipynb`

**Description:** Adds explicit instructions for answering:
- Extract from context only
- Format guidelines (numerical, yes/no)
- Insufficient information handling
- Precision requirements

**Expected:** +2-4 questions  
**Cost:** Same as baseline  
**Priority:** Test first (easiest, proven approach)

### 2. Few-Shot Examples (Phase 3C-2)

**File:** `notebooks/finhybrid_fewshot_experiment.ipynb`

**Description:** Provides 3 example Q&A pairs:
1. Numerical question (revenue)
2. Counting question (board members)
3. Yes/no with context (merger timing)

**Expected:** +3-7 questions  
**Cost:** +20% tokens (longer prompt)  
**Priority:** Test second

### 3. Chain-of-Thought (Phase 3C-3)

**File:** `notebooks/finhybrid_cot_experiment.ipynb`

**Description:** Encourages step-by-step reasoning:
1. What information is needed?
2. Where is it in the context?
3. What is the precise answer?

**Expected:** +5-10 questions  
**Cost:** 2x tokens (model generates reasoning + answer)  
**Priority:** Test last (expensive, only if needed)

---

## 🚀 How to Run

### Step 1: Test on FinHybrid (Worst Performer)

**Why FinHybrid first:**
- Worst performer (36.2% empty)
- Quick validation (47 Q&A, ~20-30 min)
- Best indicator of improvement potential

**Run all 3 variants:**

```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark"

# Test 1: Instruction-enhanced
jupyter notebook experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/finhybrid_instruction_experiment.ipynb

# Test 2: Few-shot (after instruction completes)
jupyter notebook experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/finhybrid_fewshot_experiment.ipynb

# Test 3: Chain-of-thought (optional, if first 2 disappointing)
jupyter notebook experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/finhybrid_cot_experiment.ipynb
```

**Runtime:** ~20-30 min each

### Step 2: Compare Results

After running all 3, compare:

| Variant | Empty Count | Empty Rate | Change vs Phase 2 | Cost |
|---------|-------------|------------|-------------------|------|
| Phase 2 Baseline | 17 | 36.2% | - | Baseline |
| Instruction | ? | ?% | ? | Same |
| Few-Shot | ? | ?% | ? | +20% |
| CoT | ? | ?% | ? | 2x |

**Choose best:** Highest improvement OR best improvement/cost ratio

### Step 3: Scale to All Datasets

Create 6 notebooks using winning prompt:
- TatHybrid (162 Q&A) - ~45-65 min
- NqText (78 Q&A) - ~25-35 min
- FetaTab (8 Q&A) - ~5-10 min
- PaperText (13 Q&A) - ~8-12 min
- PaperTab (4 Q&A) - ~3-5 min
- FinHybrid (already done)

**Total runtime:** ~2-3 hours  
**Expected:** +10-20 questions overall

---

## 📊 Success Criteria

**Phase 3C Successful If:**
- [ ] FinHybrid: < 30% empty (from 36.2%, gain +3+ questions)
- [ ] TatHybrid: < 14% empty (from 16.0%, gain +3+ questions)
- [ ] Overall: < 12% empty (from 16.7%, gain +10-15 questions)
- [ ] No regressions on any dataset

**If Achieved:**
- Document winning prompt
- Update default prompts in `uda/utils/llm.py` (optional)
- Consider Phase 3B (FinBERT) to stack optimizations
- Target: <10% empty combined

---

## 📁 Directory Structure

```
3_prompts/
├── notebooks/
│   ├── finhybrid_instruction_experiment.ipynb   ✅ Ready
│   ├── finhybrid_fewshot_experiment.ipynb       ✅ Ready
│   └── finhybrid_cot_experiment.ipynb           ✅ Ready
│
├── results/
│   ├── finhybrid_instruction/   (results CSVs here)
│   ├── finhybrid_fewshot/       (results CSVs here)
│   └── finhybrid_cot/           (results CSVs here)
│
├── analysis/
│   └── (comparison notebooks after testing)
│
└── README.md                    ← You are here
```

---

## 🔧 Technical Details

**What Changed:**
- ✅ New module: `uda/utils/prompts.py` with 4 prompt variants
- ✅ Notebooks use `get_prompt(prompt_type)` function
- ✅ All Phase 2 parameters preserved (TOP_K=10, CHUNK_SIZE=1500/3000)
- ✅ Only prompt changes, no retrieval or model changes

**Prompt Module:**
```python
from uda.utils.prompts import get_prompt

# Get prompt function
prompt_fn = get_prompt("instruction")  # or "fewshot" or "cot"

# Use in QA pipeline
prompt = prompt_fn(context=retrieved_context, question=question)
answer = llm.generate(prompt)
```

**Available prompts:**
- `simple` - Phase 1-2 baseline
- `instruction` - Phase 3C-1 (explicit instructions)
- `fewshot` - Phase 3C-2 (3 examples)
- `cot` - Phase 3C-3 (step-by-step reasoning)

---

## 💡 Key Decisions

### Why Skip Phase 3A (pdfplumber)?

Phase 3A tested pdfplumber on 3 datasets:
- **Result:** -6 questions overall (WORSE)
- **Failure rate:** 2/3 datasets regressed
- **Decision:** ABANDONED completely

See: `../1_pdfplumber/FINAL_VERDICT_ABANDON.md`

### Why Prompt Engineering Next?

1. **Literature-proven:** Prompting consistently works
2. **Universal benefit:** Helps ALL datasets, not domain-specific
3. **Low risk:** Can't make things worse, only better
4. **Easy rollback:** Just revert to Phase 2 prompts
5. **High ROI:** Expected +10-20 vs pdfplumber's -6

### Why FinHybrid First?

1. **Worst performer:** 36.2% empty (highest improvement potential)
2. **Fast validation:** 47 Q&A (~20-30 min per variant)
3. **Best signal:** If prompts help here, they'll help everywhere
4. **Risk mitigation:** Test on hardest case before scaling

---

## 📈 Expected Results

### Conservative Estimate:
- **Instruction:** +2 questions (32.0% empty)
- **Few-Shot:** +3 questions (29.8% empty)
- **CoT:** +5 questions (25.5% empty)
- **Overall:** +10-12 questions (13-14% empty rate)

### Optimistic Estimate:
- **Instruction:** +4 questions (27.7% empty)
- **Few-Shot:** +7 questions (21.3% empty)
- **CoT:** +10 questions (14.9% empty)
- **Overall:** +15-20 questions (11-12% empty rate)

**Target achieved:** <12% empty overall ✅

---

## 🔄 Next Steps After Phase 3C

### If Successful:
1. Document results in comparison table
2. Consider Phase 3B (FinBERT) to stack optimizations
3. Expected combined: <10% empty overall
4. Final goal: +25-45 questions total (Phase 3B + 3C)

### If Unsuccessful:
1. Investigate why prompts didn't help
2. Review prompt design
3. Test on different dataset
4. Consider alternative approaches

---

## ⚠️ Important Notes

**Don't:**
- ❌ Change TOP_K or CHUNK_SIZE (Phase 2 optimal)
- ❌ Use pdfplumber (proven negative in Phase 3A)
- ❌ Test PyPDF2 alternatives (Phase 2 optimal)
- ❌ Skip FinHybrid testing (critical validation step)

**Do:**
- ✅ Test all 3 prompts on FinHybrid first
- ✅ Compare results objectively
- ✅ Choose best improvement/cost ratio
- ✅ Document everything thoroughly
- ✅ Scale winner to all datasets

---

## 📞 Quick Reference

**Project Root:**
```
/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark
```

**First Command:**
```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark"
jupyter notebook experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/finhybrid_instruction_experiment.ipynb
```

**Prompt Module:**
```bash
cat uda/utils/prompts.py
```

---

**Ready to start Phase 3C! Expected: +10-20 questions improvement!** 🚀

**Date:** June 29, 2026  
**Status:** ✅ Setup complete, ready to run  
**Next:** Execute instruction notebook on FinHybrid
