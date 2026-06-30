# PaperText vs PaperTab - What's the Difference?

**Date:** 2026-06-29  
**Question:** Why do papertext and papertab show different results if they use the same PDFs?

---

## TL;DR - They Test Different Skills

**Same PDFs, Different Questions!**

- **PaperText** = Reading comprehension (understanding text)
- **PaperTab** = Table extraction (reading tables/numbers)

---

## The Facts

### Same Source PDFs ✓
Both notebooks use the **same 7 academic paper PDFs**:
- 1705.07830.pdf
- 1801.05147.pdf
- 1809.01202.pdf
- 1810.08699.pdf
- 1909.00754.pdf
- 1912.01214.pdf
- 2001.03131.pdf

### Identical Pipeline ✓
Both notebooks use the **exact same RAG pipeline**:
- CHUNK_SIZE: 3000 characters
- CHUNK_OVERLAP: 300 characters  
- TOP_K: 5 chunks retrieved
- TEMPERATURE: 0.1
- MAX_TOKENS: 512
- Model: Nemotron-3 Ultra 550B
- Embeddings: all-MiniLM-L6-v2

### Different Questions! ✓
They load **different CSV files** with **different questions**:

| Notebook | CSV File | Total Q&A | Available Q&A |
|----------|----------|-----------|---------------|
| PaperText | paper_text_qa.csv | 2,804 | 13 |
| PaperTab | paper_tab_qa.csv | 393 | 4 |

---

## Example: Same PDF, Different Questions

### Document: 1912.01214.pdf

**PaperText Questions (text comprehension):**
1. "which multilingual approaches do they compare with?"
2. "what are the pivot-based baselines?"
3. "which datasets did they experiment with?"

**PaperTab Questions (table extraction):**
1. "what language pairs are explored?"

**See the difference?**
- PaperText asks about the **methodology described in text**
- PaperTab asks about **data shown in tables**

---

## Why Results Differ

### Reason 1: Different Question Types
- **Text questions** = Find information in paragraphs
- **Table questions** = Extract data from structured tables

### Reason 2: Different Difficulty
- PaperText: 13 questions across 7 docs (some docs have multiple questions)
- PaperTab: 4 questions across 4 docs (3 docs have no table questions)

### Reason 3: Different Skills Required
- **Text comprehension** = Understanding narrative, concepts, methods
- **Table extraction** = Parsing structure, reading numbers, understanding column headers

---

## Results Comparison

From your runs:

| Metric | PaperText | PaperTab |
|--------|-----------|----------|
| **Q&A Pairs** | 13 | 4 |
| **Documents** | 7 | 4 |
| **Span F1** | ~38% | ~38% |
| **Empty Rate** | ~23% | ~23% |
| **Avg Response** | 87 chars | Similar |

**Interpretation:**
- Similar F1 scores suggest the model handles both tasks equally (moderately)
- Similar empty rates suggest retrieval works about the same
- Fewer PaperTab questions means less data to evaluate

---

## What's Actually Different in the Notebooks?

### ONLY These 4 Things:

```python
# 1. Dataset Name
PaperText: DATASET_NAME = "paper_text"
PaperTab:  DATASET_NAME = "paper_tab"

# 2. CSV File  
PaperText: csv_file = "./dataset/qa/paper_text_qa.csv"
PaperTab:  csv_file = "./dataset/qa/paper_tab_qa.csv"

# 3. Output Directory
PaperText: OUTPUT_DIR = "./experiments/papertext/results"
PaperTab:  OUTPUT_DIR = "./experiments/papertab/results"

# 4. Collection Name
PaperText: collection_name=f"papertext_{doc_name}"
PaperTab:  collection_name=f"papertab_{doc_name}"
```

**Everything else is 100% identical!**

---

## Why This Design Makes Sense

### It's A/B Testing for AI Skills

The UDA-Benchmark authors want to test:
1. **Can the model read text?** → PaperText
2. **Can the model read tables?** → PaperTab

By using the **same PDFs** but **different question types**, they isolate the skill being tested.

### Real-World Example

Imagine a student reading a research paper:

**Text Question (PaperText):**
"What methodology does the paper propose?"
→ Requires reading the introduction/methods section

**Table Question (PaperTab):**
"What was the accuracy on the German-English task?"
→ Requires finding Table 2 and reading the correct row/column

Both use the same paper, but test different abilities!

---

## Common Confusion Resolved

### ❌ Misconception
"PaperText and PaperTab are the same, so results should be identical"

### ✅ Reality
"PaperText and PaperTab use the **same PDFs** but ask **different questions** testing **different skills**"

---

## Analogy

Think of it like testing a student with:

| Test | Same Textbook? | Different Questions? |
|------|----------------|----------------------|
| Reading Comprehension | ✓ Yes | ✓ Yes - about the text |
| Math Problems | ✓ Yes | ✓ Yes - about the tables/graphs |

The textbook is the same, but you're testing different skills!

---

## What You Should Expect

### If results are similar (like yours):
✓ Model handles text and tables about equally well
✓ Both tasks have similar difficulty for this model

### If results were very different:
- Large gap → Model is better at one skill than the other
- Example: 60% text, 20% tables → Model struggles with structured data

### Your Results (~38% both):
→ Model is **moderately competent** at both text and table tasks
→ Neither is significantly easier/harder for this model
→ Lots of room for improvement (empty responses ~23%)

---

## Bottom Line

**Same PDFs + Same Pipeline + Different Questions = Different Tests**

PaperText and PaperTab are **complementary experiments** that together paint a picture of the model's ability to understand academic papers - both the narrative (text) and the data (tables).

Your results show the model performs **consistently but moderately** on both types of comprehension tasks, suggesting the bottleneck is likely in the **retrieval** (finding the right chunks) rather than the **task type** (text vs table).

---

## Next Steps

Since both got ~38% with ~23% empty:

1. **Try increasing TOP_K** (5 → 10) to improve retrieval
2. **Try smaller CHUNK_SIZE** (3000 → 1500) for more precise chunks
3. **Compare with other datasets** (FinHybrid, TatHybrid, NqText)
4. **Focus on reducing empty responses** - that's the main issue

The pipeline is identical, so any optimization will benefit both!
