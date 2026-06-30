# Phase 2 Document Lists - Verified Reference

**Created:** June 30, 2026  
**Source:** Phase 2 baseline notebooks in `experiments/nemotron-3-ultra-550b/1_without_optimization/`  
**Purpose:** Exact document lists to ensure Phase 3C results are comparable to Phase 2

---

## ✅ Valid Datasets (Already Match)

### **FinHybrid (47 Q&A)**
```python
AVAILABLE_DOCS = [
    "ADI_2009",
    "ADI_2010",
    "ADI_2011",
    "ADI_2012"
]
```
Status: ✅ Phase 3C already uses correct docs

### **TatHybrid (162 Q&A)**
```python
AVAILABLE_DOCS = [
    "AMR_2009",
    "AMR_2010"
]
```
Status: ✅ Phase 3C already uses correct docs

---

## ❌ Invalid Datasets (Need Correction)

### **NqText (78 Q&A) - NEEDS FIX**

**Phase 2 used (CORRECT):**
```python
AVAILABLE_DOCS = [
    "2018 Tour de France",
    "Hannah John-Kamen",
    "Oklahoma",
    "Supreme Court of the United States"
]
```

**Q&A counts:**
- 2018 Tour de France: 13 Q&A
- Hannah John-Kamen: 1 Q&A
- Oklahoma: 7 Q&A
- Supreme Court of the United States: 57 Q&A
- **Total: 78 Q&A**

**Phase 3C used (WRONG):**
```python
NQ_DOCS = [
    "Supreme Court of the United States",  # 57 Q&A
    "2018 Tour de France",                  # 13 Q&A
    "Hannah John-Kamen"                     # 1 Q&A
]
# Missing: Oklahoma (7 Q&A)
# Total: 71 Q&A (should be 78)
```

**Fix:** Add "Oklahoma" to AVAILABLE_DOCS

---

### **FetaTab (8 Q&A) - NEEDS FIX**

**Phase 2 used (CORRECT):**
```python
AVAILABLE_DOCS = [
    "Ben Platt (actor)",
    "Jennifer Jones",
    "List of French monarchs",
    "Smallville"
]
```

**Q&A counts:**
- Ben Platt (actor): 2 Q&A
- Jennifer Jones: 1 Q&A
- List of French monarchs: 4 Q&A
- Smallville: 1 Q&A
- **Total: 8 Q&A**

**Phase 3C used (WRONG):**
```python
AVAILABLE_DOCS = [
    "Ben Platt (actor)",      # 2 Q&A
    "List of French monarchs"  # 4 Q&A
]
# Missing: Jennifer Jones (1 Q&A), Smallville (1 Q&A)
# Total: 6 Q&A (should be 8)
```

**Fix:** Add "Jennifer Jones" and "Smallville" to AVAILABLE_DOCS

---

### **PaperText (12 Q&A) - NEEDS FIX** ⚠️

**NOTE:** Phase 2 tested 13 Q&A, but current dataset only has 12 Q&A for these documents (1705.07830 has 0 Q&A in current CSV but had 1 Q&A in Phase 2). Using current dataset count of 12 Q&A.

**Phase 2 used (CORRECT):**
```python
AVAILABLE_DOCS = [
    "1705.07830",
    "1801.05147",
    "1809.01202",
    "1810.08699",
    "1909.00754",
    "1912.01214",
    "2001.03131"
]
```

**Q&A counts (current dataset):**
- 1705.07830: 0 Q&A (had 1 Q&A in Phase 2)
- 1801.05147: 1 Q&A
- 1809.01202: 1 Q&A
- 1810.08699: 3 Q&A
- 1909.00754: 2 Q&A
- 1912.01214: 3 Q&A
- 2001.03131: 2 Q&A
- **Total: 12 Q&A** (Phase 2 had 13)

**Phase 3C used (WRONG):**
```python
AVAILABLE_DOCS = [
    "1801.05147",  # 1 Q&A
    "1705.0783"    # 1 Q&A (note: typo "0783" instead of "07830")
]
# Missing: 1809.01202, 1810.08699, 1909.00754, 1912.01214, 2001.03131
# Total: 2 Q&A (should be 13)
```

**Fix:** Use complete list of 7 documents

---

### **PaperTab (4 Q&A) - NEEDS FIX**

**Phase 2 used (CORRECT):**
```python
AVAILABLE_DOCS = [
    "1705.07830",
    "1801.05147",
    "1809.01202",
    "1810.08699",
    "1909.00754",
    "1912.01214",
    "2001.03131"
]
```

**Q&A counts:**
- 1801.05147: 1 Q&A
- 1809.01202: 1 Q&A
- 1909.00754: 1 Q&A
- 1912.01214: 1 Q&A
- **Total: 4 Q&A** (only 4 of the 7 docs have PaperTab questions)

**Phase 3C used (WRONG):**
```python
AVAILABLE_DOCS = [
    "1912.01214"  # 1 Q&A
]
# Missing: 1801.05147, 1809.01202, 1909.00754
# Total: 1 Q&A (should be 4)
```

**Fix:** Use complete list of 7 documents (same as PaperText)

---

## 📊 Summary

| Dataset | Phase 2 Q&A | Phase 3C Q&A | Missing Q&A | Status |
|---------|-------------|--------------|-------------|--------|
| FinHybrid | 47 | 47 | 0 | ✅ Valid |
| TatHybrid | 162 | 162 | 0 | ✅ Valid |
| **NqText** | **78** | **71** | **7** | ❌ **Invalid** |
| **FetaTab** | **8** | **6** | **2** | ❌ **Invalid** |
| **PaperText** | **12** | **2** | **10** | ❌ **Invalid** |
| **PaperTab** | **4** | **1** | **3** | ❌ **Invalid** |
| **TOTAL** | **311** | **289** | **22** | ❌ **22 Q&A missing** |

---

## 🔍 Verification Commands

Use these to verify Q&A counts after updating notebooks:

```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark"

# NqText - should be 78
python3 << 'EOF'
import pandas as pd
from uda.utils import preprocess
df = pd.read_csv("./dataset/qa/nq_qa.csv", sep="|", na_filter=False)
qas_dict = preprocess.qa_df_to_dict("nq", df)
docs = ["2018 Tour de France", "Hannah John-Kamen", "Oklahoma", "Supreme Court of the United States"]
total = sum(len(qas_dict.get(doc, [])) for doc in docs)
print(f"NqText: {total} Q&A (expected: 78)")
EOF

# FetaTab - should be 8
python3 << 'EOF'
import pandas as pd
from uda.utils import preprocess
df = pd.read_csv("./dataset/qa/feta_qa.csv", sep="|", na_filter=False)
qas_dict = preprocess.qa_df_to_dict("feta", df)
docs = ["Ben Platt (actor)", "Jennifer Jones", "List of French monarchs", "Smallville"]
total = sum(len(qas_dict.get(doc, [])) for doc in docs)
print(f"FetaTab: {total} Q&A (expected: 8)")
EOF

# PaperText - should be 12 (Phase 2 had 13 but current dataset has 12)
python3 << 'EOF'
import pandas as pd
from uda.utils import preprocess
df = pd.read_csv("./dataset/qa/paper_text_qa.csv", sep="|", na_filter=False)
qas_dict = preprocess.qa_df_to_dict("paper_text", df)
docs = ["1705.07830", "1801.05147", "1809.01202", "1810.08699", "1909.00754", "1912.01214", "2001.03131"]
total = sum(len(qas_dict.get(doc, [])) for doc in docs)
print(f"PaperText: {total} Q&A (expected: 12)")
EOF

# PaperTab - should be 4
python3 << 'EOF'
import pandas as pd
from uda.utils import preprocess
df = pd.read_csv("./dataset/qa/paper_tab_qa.csv", sep="|", na_filter=False)
qas_dict = preprocess.qa_df_to_dict("paper_tab", df)
docs = ["1705.07830", "1801.05147", "1809.01202", "1810.08699", "1909.00754", "1912.01214", "2001.03131"]
total = sum(len(qas_dict.get(doc, [])) for doc in docs)
print(f"PaperTab: {total} Q&A (expected: 4)")
EOF
```

---

## ✅ Ready for Step 2

This document contains the **verified Phase 2 document lists** needed to update Phase 3C notebooks.

**Next:** Update the 8 Phase 3C notebooks with correct AVAILABLE_DOCS lists.
