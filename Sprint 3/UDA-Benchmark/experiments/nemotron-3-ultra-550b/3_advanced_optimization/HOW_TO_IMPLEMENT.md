# 🚀 Phase 3 Implementation Guide - How To Execute

**Date:** June 29, 2026  
**Status:** Ready to implement  
**Location:** `experiments/nemotron-3-ultra-550b/3_advanced_optimization/`

---

## 📋 TABLE OF CONTENTS

1. [Overview](#overview)
2. [Phase 3A: pdfplumber Implementation](#phase-3a-pdfplumber)
3. [Phase 3B: FinBERT Implementation](#phase-3b-finbert)
4. [Phase 3C: Prompt Engineering](#phase-3c-prompts)
5. [Testing Strategy](#testing-strategy)
6. [How to Run Experiments](#how-to-run)
7. [Results Analysis](#results-analysis)

---

## 🎯 OVERVIEW

### **Current State (Phase 2):**
- **Empty Rate:** 16.7% (52/312 questions)
- **Best Config:** TOP_K=10 + CHUNK_SIZE=1500 (tables) / 3000 (text)
- **Star Achievement:** PaperTab = 100% answer rate

### **Phase 3 Goal:**
- **Target Empty Rate:** <12% overall
- **Expected Gain:** +25-45 questions
- **Investment:** 5-8 hours, $35-65

### **3 Optimization Strategies:**
1. **pdfplumber** - Better PDF table extraction (+10-15 questions)
2. **FinBERT** - Domain embeddings (+5-9 questions)
3. **Prompts** - Better instructions (+10-20 questions)

---

## 🔧 PHASE 3A: pdfplumber Implementation

### **Step 1: Install pdfplumber**

```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark"

# Install pdfplumber
pip install pdfplumber

# Verify installation
python -c "import pdfplumber; print('pdfplumber version:', pdfplumber.__version__)"
```

---

### **Step 2: Create PDF Extraction Module**

**File:** `uda/utils/pdf_extraction.py`

```python
"""
PDF extraction utilities using pdfplumber for better table handling.

Created: June 29, 2026
Purpose: Replace PyPDF2 to fix table extraction issues
"""

import pdfplumber
import PyPDF2
from pathlib import Path


def extract_text_pdfplumber(pdf_path: str) -> str:
    """
    Extract text from PDF using pdfplumber for better table handling.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Extracted text with tables properly formatted
        
    Improvements over PyPDF2:
        - Tables are preserved with proper structure
        - Numbers are not scrambled
        - Better spacing and formatting
        - Explicit page and table markers for better chunking
    """
    text_parts = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                # Extract regular text
                page_text = page.extract_text() or ""
                
                # Extract tables
                tables = page.extract_tables()
                
                if tables:
                    # Add page header
                    text_parts.append(f"\n{'='*80}\n")
                    text_parts.append(f"PAGE {page_num}\n")
                    text_parts.append(f"{'='*80}\n\n")
                    
                    # Add text content before tables
                    if page_text.strip():
                        text_parts.append(f"[TEXT CONTENT]\n{page_text}\n\n")
                    
                    # Add formatted tables
                    for table_idx, table in enumerate(tables, 1):
                        text_parts.append(f"[TABLE {table_idx}]\n")
                        
                        # Convert table to formatted text
                        for row_idx, row in enumerate(table):
                            # Clean cells and join with separator
                            clean_row = [str(cell or "").strip() for cell in row]
                            
                            # Use | separator for better parsing
                            row_text = " | ".join(clean_row)
                            text_parts.append(f"{row_text}\n")
                            
                            # Add separator after header row (first row)
                            if row_idx == 0:
                                separator = "-" * len(row_text)
                                text_parts.append(f"{separator}\n")
                        
                        text_parts.append("\n")
                else:
                    # No tables, just add text with page marker
                    text_parts.append(f"\n{'='*80}\n")
                    text_parts.append(f"PAGE {page_num}\n")
                    text_parts.append(f"{'='*80}\n\n")
                    text_parts.append(f"{page_text}\n\n")
        
        return "".join(text_parts)
    
    except Exception as e:
        raise RuntimeError(f"pdfplumber extraction failed for {pdf_path}: {e}")


def extract_text_pypdf2(pdf_path: str) -> str:
    """
    Extract text using PyPDF2 (fallback method).
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Extracted text (basic)
    """
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f, strict=False)
            text_parts = []
            
            for page_num, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                text_parts.append(f"\n{'='*80}\n")
                text_parts.append(f"PAGE {page_num}\n")
                text_parts.append(f"{'='*80}\n\n")
                text_parts.append(f"{page_text}\n\n")
            
            return "".join(text_parts)
    
    except Exception as e:
        raise RuntimeError(f"PyPDF2 extraction failed for {pdf_path}: {e}")


def extract_text_hybrid(pdf_path: str, prefer_pdfplumber: bool = True) -> str:
    """
    Hybrid extraction: Try pdfplumber first, fall back to PyPDF2.
    
    Args:
        pdf_path: Path to PDF file
        prefer_pdfplumber: If True, use pdfplumber; if False, use PyPDF2
        
    Returns:
        Extracted text
        
    Usage in notebooks:
        # For table-heavy PDFs (recommended)
        text = extract_text_hybrid(pdf_path, prefer_pdfplumber=True)
        
        # For text-only PDFs (faster)
        text = extract_text_hybrid(pdf_path, prefer_pdfplumber=False)
    """
    if not Path(pdf_path).exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    if prefer_pdfplumber:
        try:
            print(f"Extracting with pdfplumber: {Path(pdf_path).name}")
            return extract_text_pdfplumber(pdf_path)
        except Exception as e:
            print(f"⚠️ pdfplumber failed ({e}), falling back to PyPDF2")
            return extract_text_pypdf2(pdf_path)
    else:
        try:
            print(f"Extracting with PyPDF2: {Path(pdf_path).name}")
            return extract_text_pypdf2(pdf_path)
        except Exception as e:
            print(f"⚠️ PyPDF2 failed ({e}), trying pdfplumber")
            return extract_text_pdfplumber(pdf_path)


# Convenience function - default to pdfplumber
def extract_pdf_text(pdf_path: str) -> str:
    """
    Main extraction function - uses pdfplumber by default.
    
    Drop-in replacement for old extract_pdf_text function.
    """
    return extract_text_hybrid(pdf_path, prefer_pdfplumber=True)
```

**Create this file:**
```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark"

# File will be created by Claude
```

---

### **Step 3: Test on Sample PDF**

Create test script to compare extraction quality:

**File:** `3_advanced_optimization/1_pdfplumber/test_extraction.py`

```python
"""
Test pdfplumber vs PyPDF2 extraction quality on sample PDFs.

Run this BEFORE creating full notebooks to verify improvement.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from uda.utils.pdf_extraction import extract_text_pdfplumber, extract_text_pypdf2

# Sample PDF paths
SAMPLE_PDFS = [
    "dataset/src_doc_files_example/tatdqa/FinTabNet_1.0.0_table_example_0.pdf",
    "dataset/src_doc_files_example/finhybrid/finhybrid_sample_1.pdf",
]

def compare_extraction(pdf_path: str):
    """Compare PyPDF2 vs pdfplumber on one PDF."""
    print(f"\n{'='*80}")
    print(f"TESTING: {Path(pdf_path).name}")
    print(f"{'='*80}\n")
    
    # PyPDF2 extraction
    print("--- PyPDF2 Extraction (First 500 chars) ---")
    try:
        pypdf2_text = extract_text_pypdf2(pdf_path)
        print(pypdf2_text[:500])
        print(f"\nTotal length: {len(pypdf2_text)} characters")
    except Exception as e:
        print(f"ERROR: {e}")
    
    print(f"\n{'-'*80}\n")
    
    # pdfplumber extraction
    print("--- pdfplumber Extraction (First 500 chars) ---")
    try:
        pdfplumber_text = extract_text_pdfplumber(pdf_path)
        print(pdfplumber_text[:500])
        print(f"\nTotal length: {len(pdfplumber_text)} characters")
    except Exception as e:
        print(f"ERROR: {e}")
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    for pdf_path in SAMPLE_PDFS:
        if Path(project_root / pdf_path).exists():
            compare_extraction(str(project_root / pdf_path))
        else:
            print(f"⚠️ PDF not found: {pdf_path}")
```

**Run test:**
```bash
cd experiments/nemotron-3-ultra-550b/3_advanced_optimization/1_pdfplumber
python test_extraction.py
```

**What to look for:**
- ✅ Tables are properly formatted (rows/columns aligned)
- ✅ Numbers are correct (not scrambled)
- ✅ Better spacing between sections
- ✅ Page markers are clear

---

### **Step 4: Create Test Notebook**

**File:** `3_advanced_optimization/1_pdfplumber/notebooks/tathybrid_pdfplumber_experiment.ipynb`

**Key changes in notebook:**

```python
# OLD (Phase 2)
def extract_pdf_text(pdf_path):
    pdf_text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file, strict=False)
        for page_num in range(len(reader.pages)):
            pdf_text += reader.pages[page_num].extract_text()
    return pdf_text

# NEW (Phase 3A - pdfplumber)
from uda.utils.pdf_extraction import extract_pdf_text

# That's it! Drop-in replacement
```

**Parameters (keep same as Phase 2 best):**
```python
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 150
TOP_K = 10
TEMPERATURE = 0.1
MAX_TOKENS = 512
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Will change in Phase 3B
```

**Output path:**
```python
OUTPUT_DIR = "./experiments/nemotron-3-ultra-550b/3_advanced_optimization/1_pdfplumber/results/tathybrid_pdfplumber"
```

---

### **Step 5: Run Experiments**

**Priority order:**
1. TatHybrid (162 Q&A, biggest dataset, 16% empty)
2. FinHybrid (47 Q&A, worst performer, 36% empty)
3. FetaTab (8 Q&A, small sample)
4. PaperTab (4 Q&A, already perfect but verify)

**Expected runtime:**
- TatHybrid: 45-65 min
- FinHybrid: 15-25 min
- FetaTab: 5-10 min
- PaperTab: 3-5 min

---

## 🧠 PHASE 3B: FinBERT Implementation

### **Step 1: Install FinBERT**

```bash
pip install sentence-transformers

# Verify
python -c "from sentence_transformers import SentenceTransformer; print('OK')"
```

---

### **Step 2: Create Embedding Wrapper**

**File:** `uda/utils/embeddings.py` (NEW)

```python
"""
Custom embedding functions for ChromaDB.

Supports:
- Default: all-MiniLM-L6-v2 (generic, fast)
- FinBERT: yiyanghkust/finbert-tone (financial domain)
- Together AI: m2-bert-80M-8k-retrieval (paid, best)
"""

from sentence_transformers import SentenceTransformer
from typing import List


class FinBERTEmbeddingFunction:
    """
    FinBERT embedding function for financial domain.
    
    Model: yiyanghkust/finbert-tone
    Dimensions: 768
    Training: Financial reports, news, documents
    
    Use for: FinHybrid, TatHybrid (financial datasets)
    """
    
    def __init__(self):
        print("Loading FinBERT model (first time downloads ~500MB)...")
        self.model = SentenceTransformer('yiyanghkust/finbert-tone')
        print("FinBERT loaded successfully!")
    
    def __call__(self, texts: List[str]) -> List[List[float]]:
        """Embed texts using FinBERT."""
        embeddings = self.model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()


class MiniLMEmbeddingFunction:
    """
    Default MiniLM embedding function (Phase 1-2).
    
    Model: all-MiniLM-L6-v2
    Dimensions: 384
    Training: General web text
    
    Use for: NqText, PaperText, PaperTab, FetaTab (general datasets)
    """
    
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def __call__(self, texts: List[str]) -> List[List[float]]:
        """Embed texts using MiniLM."""
        embeddings = self.model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()


# Factory function for easy switching
def get_embedding_function(model_name: str = "minilm"):
    """
    Get embedding function by name.
    
    Args:
        model_name: "minilm" or "finbert"
        
    Returns:
        Embedding function instance
    """
    if model_name.lower() == "finbert":
        return FinBERTEmbeddingFunction()
    elif model_name.lower() == "minilm":
        return MiniLMEmbeddingFunction()
    else:
        raise ValueError(f"Unknown model: {model_name}. Use 'minilm' or 'finbert'")
```

---

### **Step 3: Create Test Notebook**

**File:** `3_advanced_optimization/2_finbert/notebooks/finhybrid_finbert_experiment.ipynb`

**Key changes:**

```python
# Import custom embeddings
from uda.utils.embeddings import get_embedding_function

# OLD (Phase 2)
from langchain.embeddings import HuggingFaceEmbeddings
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# NEW (Phase 3B - FinBERT)
embedding_function = get_embedding_function("finbert")

# Use in ChromaDB
collection = chroma_client.create_collection(
    name=f"uda_benchmark_{dataset_name}",
    embedding_function=embedding_function
)
```

**Test on FinHybrid first (financial domain), then TatHybrid if successful.**

---

## 📝 PHASE 3C: Prompt Engineering

### **Step 1: Design Prompts**

**Create:** `uda/utils/prompts.py` (NEW)

```python
"""
Prompt templates for UDA benchmark experiments.

Contains:
- Simple prompt (Phase 1-2 baseline)
- Instruction-enhanced prompt (Phase 3C-1)
- Few-shot prompt (Phase 3C-2)
- Chain-of-thought prompt (Phase 3C-3)
"""


def simple_prompt(context: str, question: str) -> str:
    """Simple prompt (Phase 1-2 baseline)."""
    return f"""Context: {context}

Question: {question}

Answer:"""


def instruction_prompt(context: str, question: str) -> str:
    """Instruction-enhanced prompt (Phase 3C-1)."""
    return f"""You are a financial document analysis expert. Answer the question based ONLY on the provided context.

Context:
{context}

Question: {question}

Instructions:
- Extract the answer directly from the context
- For numerical questions, provide just the number with units
- For yes/no questions, answer with "Yes" or "No" followed by a brief explanation
- If the context doesn't contain the answer, respond with "INSUFFICIENT INFORMATION"
- Be precise and concise

Answer:"""


def fewshot_prompt(context: str, question: str) -> str:
    """Few-shot prompt with examples (Phase 3C-2)."""
    return f"""Answer questions based on the provided context.

Example 1:
Context: The company's revenue in 2019 was $45.2 million, up from $38.7 million in 2018.
Question: What was the revenue in 2019?
Answer: $45.2 million

Example 2:
Context: The board consists of 7 members, 3 of whom are independent directors.
Question: How many board members are there?
Answer: 7

Example 3:
Context: The merger was completed in Q3 2020, combining two major industry players.
Question: Did the merger happen in 2019?
Answer: No, it happened in Q3 2020.

Now answer this question:
Context: {context}
Question: {question}
Answer:"""


def cot_prompt(context: str, question: str) -> str:
    """Chain-of-thought prompt (Phase 3C-3 - expensive but effective)."""
    return f"""Context: {context}

Question: {question}

Think step by step:
1. What information do I need to answer this question?
2. Where in the context is this information?
3. What is the precise answer?

Answer:"""


# Prompt registry for easy switching
PROMPTS = {
    "simple": simple_prompt,
    "instruction": instruction_prompt,
    "fewshot": fewshot_prompt,
    "cot": cot_prompt,
}


def get_prompt(prompt_type: str = "simple"):
    """
    Get prompt function by type.
    
    Args:
        prompt_type: "simple", "instruction", "fewshot", or "cot"
        
    Returns:
        Prompt function(context, question) -> str
    """
    if prompt_type not in PROMPTS:
        raise ValueError(f"Unknown prompt type: {prompt_type}. Choose from {list(PROMPTS.keys())}")
    
    return PROMPTS[prompt_type]
```

---

### **Step 2: Create Test Notebooks**

Create 3 test notebooks for FinHybrid (worst performer):

1. `3_prompts/notebooks/finhybrid_instruction_experiment.ipynb`
2. `3_prompts/notebooks/finhybrid_fewshot_experiment.ipynb`
3. `3_prompts/notebooks/finhybrid_cot_experiment.ipynb`

**Key changes:**

```python
# Import prompts
from uda.utils.prompts import get_prompt

# Choose prompt type
prompt_fn = get_prompt("instruction")  # or "fewshot" or "cot"

# Use in QA
prompt = prompt_fn(context=retrieved_context, question=question)
answer = llm.generate(prompt)
```

---

### **Step 3: Test and Compare**

**Testing order:**
1. Test "instruction" on FinHybrid (cheapest)
2. Test "fewshot" on FinHybrid (medium cost)
3. Test "cot" on FinHybrid (expensive)
4. Compare results
5. Choose best
6. Apply to all datasets

**Expected costs:**
- Instruction: Similar to baseline
- Few-shot: +20% tokens (longer prompt)
- CoT: +100% tokens (2x longer output)

---

## 🧪 TESTING STRATEGY

### **For Each Optimization:**

1. **Create Test Notebook**
   - Copy best Phase 2 notebook
   - Apply ONE change (pdfplumber OR finbert OR prompt)
   - Update output directory

2. **Run on Small Dataset First**
   - FetaTab (8 Q&A) or PaperTab (4 Q&A) for quick validation
   - Or: Take 10-20 questions from TatHybrid for sample

3. **Compare Results**
   - Empty rate: Did it improve?
   - Accuracy scores: Better or worse?
   - Visual inspection: Are answers better quality?

4. **Scale Up if Successful**
   - Apply to larger datasets
   - Document results
   - Move to next optimization

---

## 🏃 HOW TO RUN EXPERIMENTS

### **Step-by-Step Process:**

```bash
# 1. Navigate to project
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark"

# 2. Activate environment (if needed)
# conda activate your_env

# 3. Navigate to Phase 3 directory
cd experiments/nemotron-3-ultra-550b/3_advanced_optimization

# 4. Open notebook
cd 1_pdfplumber/notebooks
jupyter notebook tathybrid_pdfplumber_experiment.ipynb

# 5. Run notebook (Shift+Enter through cells or Kernel > Restart & Run All)

# 6. Wait for completion (~45-65 min for TatHybrid)

# 7. Check results
cd ../results/tathybrid_pdfplumber
ls -lh *.csv
head -20 *.csv
```

---

## 📊 RESULTS ANALYSIS

### **After Each Experiment:**

1. **Check Empty Rate**
   ```python
   import pandas as pd
   df = pd.read_csv('results.csv')
   empty_count = (df['pred'].str.strip() == "").sum()
   empty_rate = empty_count / len(df) * 100
   print(f"Empty rate: {empty_rate:.1f}% ({empty_count}/{len(df)})")
   ```

2. **Compare vs Phase 2**
   ```python
   phase2_empty_rate = 16.0  # TatHybrid Phase 2
   improvement = phase2_empty_rate - empty_rate
   print(f"Improvement: {improvement:.1f} percentage points")
   ```

3. **Visual Inspection**
   - Look at first 10-20 predictions
   - Are tables better extracted?
   - Are answers more accurate?
   - Any new failure patterns?

4. **Create Comparison CSV**
   - Phase 1, Phase 2, Phase 3 side by side
   - Track empty rate, scores, improvements

---

## 🎯 SUCCESS CRITERIA

**Phase 3A (pdfplumber) Successful If:**
- [ ] TatHybrid: Empty rate < 12% (vs 16% Phase 2) = +6+ questions
- [ ] FinHybrid: Empty rate < 30% (vs 36% Phase 2) = +3+ questions
- [ ] Tables are visually better formatted
- [ ] No regressions on text datasets

**Phase 3B (FinBERT) Successful If:**
- [ ] FinHybrid: +2+ questions vs Phase 3A
- [ ] TatHybrid: +3+ questions vs Phase 3A
- [ ] Financial terms better understood
- [ ] Runtime impact acceptable (<2x slower)

**Phase 3C (Prompts) Successful If:**
- [ ] Any dataset: +2+ questions with instruction prompt
- [ ] Any dataset: +3+ questions with few-shot prompt
- [ ] Cost increase justified by improvements
- [ ] Universal benefit (helps all datasets)

---

## ✅ CHECKLIST FOR EACH OPTIMIZATION

**Before Running:**
- [ ] Install dependencies
- [ ] Create helper module (pdf_extraction.py / embeddings.py / prompts.py)
- [ ] Test module import works
- [ ] Create test notebook
- [ ] Update output directory paths
- [ ] Verify API keys and config

**During Running:**
- [ ] Monitor progress (should see progress bars)
- [ ] Check for errors
- [ ] Watch empty rate in real-time (if possible)
- [ ] Note runtime

**After Running:**
- [ ] Results CSV exists
- [ ] Empty rate calculated
- [ ] Compared vs Phase 2
- [ ] Document findings
- [ ] Decide: continue or pivot?

---

## 📁 FILE STRUCTURE REFERENCE

```
3_advanced_optimization/
├── 1_pdfplumber/
│   ├── notebooks/
│   │   ├── tathybrid_pdfplumber_experiment.ipynb
│   │   ├── finhybrid_pdfplumber_experiment.ipynb
│   │   ├── fetatab_pdfplumber_experiment.ipynb
│   │   └── papertab_pdfplumber_experiment.ipynb
│   ├── results/
│   │   ├── tathybrid_pdfplumber/
│   │   ├── finhybrid_pdfplumber/
│   │   ├── fetatab_pdfplumber/
│   │   └── papertab_pdfplumber/
│   ├── analysis/
│   │   └── pdfplumber_comparison.ipynb
│   └── test_extraction.py
│
├── 2_finbert/
│   ├── notebooks/
│   │   ├── finhybrid_finbert_experiment.ipynb
│   │   └── tathybrid_finbert_experiment.ipynb
│   ├── results/
│   │   ├── finhybrid_finbert/
│   │   └── tathybrid_finbert/
│   └── analysis/
│       └── finbert_comparison.ipynb
│
└── 3_prompts/
    ├── notebooks/
    │   ├── finhybrid_instruction_experiment.ipynb
    │   ├── finhybrid_fewshot_experiment.ipynb
    │   └── finhybrid_cot_experiment.ipynb
    ├── results/
    │   ├── finhybrid_instruction/
    │   ├── finhybrid_fewshot/
    │   └── finhybrid_cot/
    └── analysis/
        └── prompt_comparison.ipynb
```

---

## 🚀 READY TO START!

**Recommended order:**
1. Start with **pdfplumber** (biggest impact, clear benefit)
2. Then **FinBERT** (free, easy to test)
3. Finally **prompts** (universal benefit, test multiple variants)

**First command:**
```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark"
pip install pdfplumber
```

**Let's do this!** 🎯
