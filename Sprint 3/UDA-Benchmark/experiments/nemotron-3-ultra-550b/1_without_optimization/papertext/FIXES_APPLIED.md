# PaperText Notebook - Fixes Applied

**Date:** 2026-06-29  
**Based on:** TatHybrid experiment (working reference)

---

## Issues Fixed

### 1. Missing Project Root Directory Change (Cell 2) ✅
**Problem:** Notebook was running from subdirectory, causing PDF path resolution to fail.

**Fix:** Added working directory change to project root:
```python
# CRITICAL: Change to project root directory
# The preprocess module uses relative paths from project root
project_root = os.path.abspath('../..')
os.chdir(project_root)
sys.path.insert(0, project_root)

print(f"Working directory: {os.getcwd()}")
```

---

### 2. Wrong Config Path (Cell 4) ✅
**Problem:** Config path was using `../..` relative path instead of project root.

**Fix:** Changed to use `os.getcwd()` (now at project root):
```python
_spec = importlib.util.spec_from_file_location(
    "access_config",
    os.path.join(os.getcwd(), "uda", "utils", "access_config.py")
)
```

---

### 3. Wrong Output Directory Path (Cell 5) ✅
**Problem:** OUTPUT_DIR was `./results` instead of `./experiments/papertext/results`.

**Fix:** Updated to correct path:
```python
OUTPUT_DIR = "./experiments/papertext/results"
os.makedirs(OUTPUT_DIR, exist_ok=True)
```

---

### 4. Wrong CSV File Path (Cell 11) ✅
**Problem:** CSV path was using `../..` relative path instead of project root path.

**Fix:** Changed to use project root path:
```python
csv_file = "./dataset/qa/paper_qa.csv"
```

---

### 5. Undefined Variable `dataset_key` (Cell 13) ✅
**Problem:** Collection name used undefined variable `dataset_key` instead of hardcoded string.

**Fix:** Changed to use hardcoded collection name:
```python
collection = build_index(text_chunks, collection_name=f"papertext_{doc_name}")
```

---

### 6. F-String Formatting Issues (Cell 13) ✅
**Problem:** Print statements had broken f-string formatting with `{{` instead of `{`.

**Fix:** Corrected all f-strings:
```python
print(f"\n{'='*80}")
print(f"Processing: {doc_name}")
print(f"Created {len(text_chunks)} chunks")
# ... etc
```

---

### 7. Missing Diagnostic Cell ✅
**Problem:** No cell to check empty responses (critical for debugging).

**Fix:** Added new Cell 15 with diagnostic code:
```python
if all_results:
    import pandas as pd
    
    # Create DataFrame for analysis
    results_df = pd.DataFrame(all_results)
    
    # Count empty responses
    results_df['is_empty'] = results_df['response'].fillna('').str.strip() == ''
    empty_count = results_df['is_empty'].sum()
    total_count = len(results_df)
    
    print(f"\n{'='*80}")
    print(f"DIAGNOSTIC: Empty Response Analysis")
    print(f"{'='*80}")
    # ... detailed analysis
```

---

### 8. F-String Issues in Save/Stats Cells (Cells 18, 20) ✅
**Problem:** Used `{{` instead of `{` in f-strings.

**Fix:** Corrected all f-strings:

**Cell 18:**
```python
print(f"\n✓ Results saved to: {output_file}")
print(f"Total Q&A: {len(results_df)}")
print(f"  {doc}: {count} questions")
```

**Cell 20:**
```python
print(f"\n{'='*80}")
print(f"Total questions: {len(results_df)}")
print(f"Answered: {answered_count} ({answered_count/len(results_df)*100:.1f}%)")
```

---

## Summary of Changes

| Cell | Issue | Status |
|------|-------|--------|
| Cell 2 | Missing project root change | ✅ Fixed |
| Cell 4 | Wrong config path | ✅ Fixed |
| Cell 5 | Wrong OUTPUT_DIR | ✅ Fixed |
| Cell 11 | Wrong CSV path | ✅ Fixed |
| Cell 13 | Undefined `dataset_key` | ✅ Fixed |
| Cell 13 | F-string formatting | ✅ Fixed |
| Cell 14 | Added diagnostic header | ✅ Added |
| Cell 15 | Missing diagnostic code | ✅ Added |
| Cell 16 | Added evaluate header | ✅ Added |
| Cell 18 | F-string formatting | ✅ Fixed |
| Cell 20 | F-string formatting | ✅ Fixed |

---

## Key Differences from Original

### Before (Broken)
- Ran from subdirectory `experiments/papertext/`
- Used relative paths `../../` throughout
- Missing diagnostic cell
- Had f-string formatting bugs
- Would fail on PDF path resolution

### After (Fixed)
- Changes to project root first (`os.chdir(project_root)`)
- Uses project root paths `./dataset/...`, `./experiments/...`
- Has diagnostic cell for empty response analysis
- All f-strings properly formatted
- PDF paths resolve correctly

---

## How to Run

1. **Open notebook in Jupyter:**
   ```bash
   cd ~/personal\ work/LLM\ Benchmark\ Team\ Project/LLM_Benchmark_Team_Project_2026/Sprint\ 3/UDA-Benchmark/experiments/papertext
   jupyter notebook papertext_experiment.ipynb
   ```

2. **Restart kernel** (Important!)
   - Kernel → Restart & Clear Output

3. **Run all cells:**
   - Cell → Run All

4. **Monitor progress:**
   - Should see: "Working directory: .../Sprint 3/UDA-Benchmark"
   - PDFs should be found for all 7 documents
   - Each question will show progress

5. **Check results:**
   - Results saved to: `./experiments/papertext/results/papertext_results_[timestamp].csv`
   - Diagnostic cell shows empty response rate
   - Evaluation cell shows Span F1 score

---

## Expected Behavior

✅ **Cell 2:** Should print working directory as project root  
✅ **Cell 4:** Should load config successfully  
✅ **Cell 11:** Should load paper_qa.csv and show Q&A counts  
✅ **Cell 13:** Should find all 7 PDFs and process questions  
✅ **Cell 15:** Should show empty response diagnostics  
✅ **Cell 17:** Should evaluate with Span F1 metric  
✅ **Cell 19:** Should save results CSV  
✅ **Cell 21:** Should show statistics summary

---

## Reference: TatHybrid Working Code

All fixes were based on the successful TatHybrid implementation:
- File: `experiments/tathybrid/tathybrid_experiment.ipynb`
- Status: ✅ Working (43.5% Numeracy F1, 77.2% answered)
- Key pattern: Change to project root → use `./` paths → proper f-strings

---

## Notebook Now Ready! 🚀

All issues have been fixed. The notebook should now run without errors, following the same pattern as the successful TatHybrid experiment.
