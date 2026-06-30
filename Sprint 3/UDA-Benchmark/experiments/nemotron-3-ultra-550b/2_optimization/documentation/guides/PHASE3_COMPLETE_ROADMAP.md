# 🚀 Phase 3 Optimization Plan - Complete Roadmap

**Date:** June 29, 2026  
**Current Status:** Phase 2 Complete - Winning Config Found (TOP_K=10 + CHUNK_SIZE=1500)  
**Next Steps:** Apply to remaining datasets + Phase 3 advanced optimizations

---

## 📋 **EXECUTION PLAN**

### **Step 1: Apply Winning Config to Remaining Table Datasets ⏳**

**Status:** Notebooks created, ready to run

| Dataset | Notebook | Q&A | Expected Time | Expected Cost | Expected Improvement |
|---------|----------|-----|---------------|---------------|---------------------|
| **FetaTab** | `fetatab_topk10_chunk1500_experiment.ipynb` | 8 | 5-10 min | $2-3 | +1-2 questions |
| **PaperTab** | `papertab_topk10_chunk1500_experiment.ipynb` | 4 | 3-5 min | $1-2 | +0-1 questions |

**Total:** ~8-15 min, ~$3-5, expected +1-3 questions

**Run these first:**
```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark/experiments/nemotron-3-ultra-550b/2_optimization"

jupyter notebook fetatab_topk10_chunk1500_experiment.ipynb
jupyter notebook papertab_topk10_chunk1500_experiment.ipynb
```

---

### **Step 2: Better PDF Parsing (pdfplumber) 🔧**

**Goal:** Fix PyPDF2's poor table extraction

#### **Why This Matters:**
- PyPDF2 mangles tables (numbers get scrambled)
- Financial reports have complex table structures
- **Current bottleneck:** Even with best params, still 16-36% empty

#### **Implementation Plan:**

**A. Install pdfplumber:**
```bash
pip install pdfplumber
```

**B. Create new extraction function:**

```python
# File: uda/utils/pdf_extraction.py (NEW FILE)

import pdfplumber

def extract_text_pdfplumber(pdf_path):
    """
    Extract text from PDF using pdfplumber for better table handling.
    
    Returns structured text with tables properly formatted.
    """
    text_parts = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            # Extract text
            page_text = page.extract_text() or ""
            
            # Extract tables
            tables = page.extract_tables()
            
            if tables:
                # Add text before tables
                text_parts.append(f"[Page {page_num} - Text]\n{page_text}\n")
                
                # Add formatted tables
                for table_idx, table in enumerate(tables, 1):
                    text_parts.append(f"\n[Page {page_num} - Table {table_idx}]\n")
                    
                    # Convert table to formatted text
                    for row in table:
                        # Clean and join cells
                        clean_row = [str(cell or "").strip() for cell in row]
                        text_parts.append(" | ".join(clean_row) + "\n")
                    
                    text_parts.append("\n")
            else:
                # No tables, just add text
                text_parts.append(f"[Page {page_num}]\n{page_text}\n\n")
    
    return "".join(text_parts)


def extract_text_hybrid(pdf_path):
    """
    Hybrid approach: Use pdfplumber for tables, PyPDF2 as fallback.
    """
    try:
        return extract_text_pdfplumber(pdf_path)
    except Exception as e:
        print(f"Warning: pdfplumber failed ({e}), falling back to PyPDF2")
        # Fall back to PyPDF2
        import PyPDF2
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f, strict=False)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
```

**C. Update notebooks to use new extractor:**

Replace in notebooks:
```python
# OLD
def extract_pdf_text(pdf_path):
    pdf_text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file, strict=False)
        for page_num in range(len(reader.pages)):
            pdf_text += reader.pages[page_num].extract_text()
    return pdf_text

# NEW
from uda.utils.pdf_extraction import extract_text_pdfplumber as extract_pdf_text
```

#### **Testing Plan:**

1. Create test notebook for TatHybrid with pdfplumber
2. Compare extraction quality manually (pick 1-2 tables)
3. Run full experiment
4. Compare results vs current best (TOP_K=10 + CHUNK=1500)

**Expected Impact:**
- TatHybrid: 16.0% → 10-12% empty (+6-10 questions)
- FinHybrid: 36.2% → 25-30% empty (+3-5 questions)
- Total: +9-15 questions across table datasets

**Cost:** ~$20-35, ~2-3 hours implementation + testing

---

### **Step 3: Domain-Specific Embeddings 🧠**

**Goal:** Better semantic understanding for financial data

#### **Why This Matters:**
- Current: all-MiniLM-L6-v2 (generic, free, local)
- Problem: Doesn't understand financial terminology
- Numbers treated as text, not quantities

#### **Implementation Options:**

**Option A: FinBERT (Free, Local) - RECOMMENDED**

```python
from sentence_transformers import SentenceTransformer

# Load FinBERT embedding model
finbert_model = SentenceTransformer('yiyanghkust/finbert-tone')

# Create ChromaDB embedding function wrapper
class FinBERTEmbeddingFunction:
    def __call__(self, texts):
        return finbert_model.encode(texts).tolist()

# Use in notebook
ef = FinBERTEmbeddingFunction()
```

**Pros:**
- Free and local
- Trained on financial texts
- Better understanding of financial terminology

**Cons:**
- Slower than MiniLM
- Larger model size (~500MB)

---

**Option B: Together AI Embeddings (Paid, Better)**

```python
from together import Together

client = Together(api_key=TOGETHER_API_KEY)

class TogetherEmbeddingFunction:
    def __call__(self, texts):
        response = client.embeddings.create(
            model="togethercomputer/m2-bert-80M-8k-retrieval",
            input=texts
        )
        return [item.embedding for item in response.data]

ef = TogetherEmbeddingFunction()
```

**Pros:**
- Better quality embeddings
- Longer context window (8k tokens)
- Already have Together AI account

**Cons:**
- Costs money (~$0.0001 per 1k tokens)
- ~$2-5 additional per experiment
- Slower (API calls)

---

#### **Testing Plan:**

1. Create test notebook with FinBERT embeddings
2. Test on FinHybrid (finance-specific)
3. Compare retrieval quality
4. Run full experiment
5. If successful, apply to TatHybrid

**Expected Impact:**
- FinHybrid: +2-4 questions (better financial semantics)
- TatHybrid: +3-5 questions (better numerical understanding)
- Total: +5-9 questions

**Cost:** 
- FinBERT: $0 (free), ~30-60 min slower runtime
- Together AI: ~$10-20 additional cost

**Recommendation:** Start with FinBERT (free), test Together AI if results are promising

---

### **Step 4: Prompt Engineering 📝**

**Goal:** Better instruction following and answer extraction

#### **Current Prompt (Simple):**
```python
prompt = f"""Context: {context}

Question: {question}

Answer:"""
```

#### **Improvement Options:**

**Option A: Instruction-Enhanced Prompt**

```python
prompt = f"""You are a financial document analysis expert. Answer the question based ONLY on the provided context.

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
```

**Expected Impact:** +2-4 questions (clearer instructions)

---

**Option B: Few-Shot Examples**

```python
prompt = f"""Answer questions based on the provided context.

Example 1:
Context: The company's revenue in 2019 was $45.2 million, up from $38.7 million in 2018.
Question: What was the revenue in 2019?
Answer: $45.2 million

Example 2:
Context: The board consists of 7 members, 3 of whom are independent directors.
Question: How many board members are there?
Answer: 7

Now answer this question:
Context: {context}
Question: {question}
Answer:"""
```

**Expected Impact:** +3-7 questions (better answer format)

---

**Option C: Chain-of-Thought (for Hard Questions)**

```python
prompt = f"""Context: {context}

Question: {question}

Think step by step:
1. What information do I need from the context?
2. Where in the context is this information?
3. What is the answer?

Answer:"""
```

**Expected Impact:** +5-10 questions on hard questions
**Cost Trade-off:** ~2x output tokens (higher cost)

---

#### **Testing Plan:**

1. Test on FinHybrid (worst performer, 36.2% empty)
2. Try Instruction-Enhanced first (lowest cost)
3. If good, try Few-Shot
4. Compare all variants
5. Choose best and apply to all datasets

**Expected Impact:**
- Instruction-Enhanced: +2-4 questions
- Few-Shot: +3-7 questions
- Chain-of-Thought: +5-10 questions (but 2x cost)

**Cost:** ~$5-15 per variant test

---

## 📊 **EXPECTED CUMULATIVE RESULTS**

### **Current Best (Phase 2):**
| Dataset | Empty % | Config |
|---------|---------|--------|
| TatHybrid | 16.0% | TOP_K=10 + CHUNK=1500 |
| FinHybrid | 36.2% | TOP_K=10 + CHUNK=1500 |

### **After Step 1 (Apply to others):**
| Dataset | Current | Expected | Improvement |
|---------|---------|----------|-------------|
| FetaTab | 25.0% | 20-22% | +1-2 questions |
| PaperTab | 25.0% | 15-20% | +0-1 questions |

### **After Step 2 (pdfplumber):**
| Dataset | Current | Expected | Improvement |
|---------|---------|----------|-------------|
| TatHybrid | 16.0% | 10-12% | +6-10 questions |
| FinHybrid | 36.2% | 25-30% | +3-5 questions |
| FetaTab | 20-22% | 15-18% | +1-2 questions |
| PaperTab | 15-20% | 10-15% | +0-1 questions |

### **After Step 3 (FinBERT):**
| Dataset | Current | Expected | Improvement |
|---------|---------|----------|-------------|
| TatHybrid | 10-12% | 7-10% | +3-5 questions |
| FinHybrid | 25-30% | 20-25% | +2-4 questions |

### **After Step 4 (Prompt Engineering):**
| Dataset | Current | Expected | Improvement |
|---------|---------|----------|-------------|
| All datasets | - | - | +2-7 questions each |

### **🎯 Final Expected Results (All Phases):**

| Dataset | Baseline | Phase 2 | Phase 3 Final | Total Improvement |
|---------|----------|---------|---------------|-------------------|
| TatHybrid | 22.8% | 16.0% | **5-8%** | **+20-30 questions** ✅✅✅ |
| FinHybrid | 44.7% | 36.2% | **18-23%** | **+10-13 questions** ✅✅✅ |
| FetaTab | 25.0% | 25.0% | **12-15%** | **+1-2 questions** ✅ |
| PaperTab | 75.0% | 25.0% | **8-12%** | **+2-3 questions** ✅ |

**Overall Target:** <15% average empty rate, 45-50% average score

---

## 💰 **INVESTMENT ESTIMATE**

### **Step 1: Apply Winning Config**
- Time: 10-15 min
- Cost: $3-5
- Return: +1-3 questions

### **Step 2: pdfplumber**
- Time: 2-3 hours (implementation + testing)
- Cost: $20-35
- Return: +9-15 questions

### **Step 3: FinBERT**
- Time: 1-2 hours (implementation + testing)
- Cost: $0 (free) + slower runtime
- Return: +5-9 questions

### **Step 4: Prompt Engineering**
- Time: 2-3 hours (multiple variants)
- Cost: $15-30
- Return: +10-20 questions

**Total Phase 3:**
- Time: 5-8 hours
- Cost: $38-70
- Return: +25-45 questions
- ROI: $0.85-$2.80 per question ✅ EXCELLENT!

---

## 📅 **RECOMMENDED TIMELINE**

### **Day 1: Quick Wins**
- ☐ Run FetaTab + PaperTab with winning config (15 min)
- ☐ Analyze results
- ☐ Install pdfplumber

### **Day 2-3: Better PDF Parsing**
- ☐ Implement pdfplumber extraction function
- ☐ Test on 1-2 sample PDFs (visual inspection)
- ☐ Create test notebook for TatHybrid
- ☐ Run full TatHybrid test
- ☐ If successful, apply to FinHybrid, FetaTab, PaperTab

### **Day 4: Domain Embeddings**
- ☐ Install FinBERT
- ☐ Create test notebook for FinHybrid
- ☐ Run experiment
- ☐ Compare vs current best
- ☐ If successful, apply to TatHybrid

### **Day 5-6: Prompt Engineering**
- ☐ Test Instruction-Enhanced prompt
- ☐ Test Few-Shot prompt
- ☐ Compare all variants
- ☐ Choose best
- ☐ Apply to all datasets

### **Day 7: Final Analysis**
- ☐ Compile all results
- ☐ Create comprehensive comparison
- ☐ Document final best configuration
- ☐ Celebrate! 🎉

---

## ✅ **IMMEDIATE NEXT STEPS**

**RIGHT NOW - Run these 2 notebooks:**
```bash
cd "/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark/experiments/nemotron-3-ultra-550b/2_optimization"

jupyter notebook fetatab_topk10_chunk1500_experiment.ipynb
jupyter notebook papertab_topk10_chunk1500_experiment.ipynb
```

**After that completes:**
1. Install pdfplumber: `pip install pdfplumber`
2. I'll help you create the extraction function
3. We'll test it on sample PDFs first
4. Then run full experiments

---

## 📁 **FILES CREATED**

- ✅ `fetatab_topk10_chunk1500_experiment.ipynb` - Ready to run
- ✅ `papertab_topk10_chunk1500_experiment.ipynb` - Ready to run
- ✅ `THIS FILE` - Complete Phase 3 roadmap

---

**🚀 Ready to execute! Let's start with the quick wins (FetaTab + PaperTab), then move to the big improvements (pdfplumber, FinBERT, prompts)!**
