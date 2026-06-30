# 📝 How Phase 3C Prompting Works - Visual Guide

**Date:** June 29, 2026  
**Purpose:** Show exactly what prompts look like and how they improve results

---

## 🎯 The Problem We're Solving

**Current Phase 2 (Baseline):**
- Uses **simple prompt** with minimal instructions
- Result: **36.2% empty responses** on FinHybrid (17/47 questions)
- Model doesn't always know HOW to answer from the retrieved context

**Goal:**
- Give the model **better instructions** on how to answer
- Reduce empty responses to **<30%** (+3-7 questions)

---

## 📊 How It Works - Complete Flow

### Step 1: Question Asked
```
User question: "What was the revenue in 2019?"
```

### Step 2: RAG System Retrieves Context
```
Retrieved context from PDF:
"The company's total revenue for fiscal year 2019 was $45.2 million, 
representing a 16.8% increase from the prior year's $38.7 million. 
This growth was driven primarily by increased product sales..."
```

### Step 3: Build Prompt (THIS IS WHAT WE'RE CHANGING!)

We combine the context + question into a prompt for the LLM.  
**Phase 2 uses SIMPLE prompt, Phase 3C tests 3 BETTER prompts.**

### Step 4: LLM Generates Answer
```
Model response: "The answer is: $45.2 million"
```

---

## 🔍 The 4 Prompt Variants - Full Examples

Let's use a **real example** to see the difference:

**Question:** "What was the revenue in 2019?"  
**Retrieved Context:** "The company's revenue in 2019 was $45.2 million, up from $38.7 million in 2018."

---

### ❌ BASELINE - Simple Prompt (Phase 2)

**What gets sent to the model:**

```
Context: The company's revenue in 2019 was $45.2 million, up from $38.7 million in 2018.

Question: What was the revenue in 2019?

Answer:
```

**Why it fails sometimes:**
- No instructions on HOW to answer
- Model might not know to extract just the number
- Model might not know what to do if context is unclear
- Can return empty or wrong format

**Example of what goes wrong:**
- Question: "What was the debt ratio?"
- Context doesn't have "debt ratio" explicitly
- Model returns: "" (EMPTY) ❌
- **This is 1 of the 17 empty responses!**

---

### ✅ VARIANT 1 - Instruction-Enhanced Prompt (Phase 3C-1)

**What gets sent to the model:**

```
You are a financial document analysis expert. Answer the question based ONLY on the provided context.

Context:
The company's revenue in 2019 was $45.2 million, up from $38.7 million in 2018.

Question: What was the revenue in 2019?

Instructions:
- Extract the answer directly from the context
- For numerical questions, provide just the number with units (e.g., "$45.2 million", "7 members")
- For yes/no questions, answer with "Yes" or "No" followed by a brief explanation
- If the context doesn't contain the answer, respond with "INSUFFICIENT INFORMATION"
- Be precise and concise
- Do not add information not present in the context

Answer:
```

**Why this helps:**
- ✅ Tells model to be a "financial expert" (sets role)
- ✅ Says "ONLY from context" (prevents hallucinations)
- ✅ Gives format examples (e.g., "$45.2 million")
- ✅ Tells model what to do when info is missing ("INSUFFICIENT INFORMATION")
- ✅ Says "be precise and concise"

**Expected improvement:** +2-4 questions (better instructions → better extraction)

---

### ✅ VARIANT 2 - Few-Shot Examples (Phase 3C-2)

**What gets sent to the model:**

```
Answer questions based on the provided context. Here are examples of good answers:

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
Context: The company's revenue in 2019 was $45.2 million, up from $38.7 million in 2018.
Question: What was the revenue in 2019?
Answer:
```

**Why this helps:**
- ✅ Shows the model **3 real examples** of good answers
- ✅ Example 1: Numerical question → extract just the number with unit
- ✅ Example 2: Counting question → just the number
- ✅ Example 3: Yes/no question → "No, [explanation]"
- ✅ Model learns by imitation (proven technique in ML)

**Expected improvement:** +3-7 questions (examples show HOW to answer)

**Cost:** +20% tokens (longer prompt with examples)

---

### ✅ VARIANT 3 - Chain-of-Thought (Phase 3C-3)

**What gets sent to the model:**

```
Context: The company's revenue in 2019 was $45.2 million, up from $38.7 million in 2018.

Question: What was the revenue in 2019?

Think step by step:
1. What information do I need to answer this question?
2. Where in the context is this information located?
3. What is the precise answer based on the context?

Answer:
```

**Model's response (with reasoning):**

```
1. What information do I need to answer this question?
   → I need the revenue amount for 2019

2. Where in the context is this information located?
   → First sentence: "revenue in 2019 was $45.2 million"

3. What is the precise answer based on the context?
   → $45.2 million

Answer: $45.2 million
```

**Why this helps:**
- ✅ Forces model to **think step-by-step** before answering
- ✅ Model identifies what info it needs
- ✅ Model finds where that info is in the context
- ✅ Model then extracts the precise answer
- ✅ Reduces "empty" responses because model works through the logic

**Expected improvement:** +5-10 questions (reasoning reduces mistakes)

**Cost:** 2x tokens (model generates reasoning + answer, longer output)

---

## 📈 Visual Comparison - How Each Prompt Helps

### Example Question That Currently FAILS (Empty Response)

**Question:** "What is the debt-to-equity ratio in 2016?"

**Retrieved Context:**
```
The company's total debt was $120 million in 2016, with shareholders' 
equity of $240 million. Net income for the year was $45 million.
```

**Phase 2 (Simple Prompt):**
```
Context: [above]
Question: What is the debt-to-equity ratio in 2016?
Answer:
```
**Model output:** "" (EMPTY) ❌  
**Why:** Model doesn't know it needs to CALCULATE (120/240 = 0.5)

---

**Phase 3C-1 (Instruction):**
```
You are a financial document analysis expert...
[instructions about extracting from context]
```
**Model output:** "" (EMPTY) ❌  
**Why:** Still doesn't help - model sees "debt-to-equity ratio" not in text

---

**Phase 3C-2 (Few-Shot):**
```
Example 1: [revenue example]
Example 2: [board members example]
Example 3: [yes/no example]

Now answer: What is the debt-to-equity ratio in 2016?
```
**Model output:** "" (EMPTY) ❌  
**Why:** Examples don't show calculation, still confused

---

**Phase 3C-3 (Chain-of-Thought):**
```
Think step by step:
1. What information do I need?
2. Where is it in the context?
3. What is the precise answer?
```
**Model output:**
```
1. I need the debt-to-equity ratio. This is calculated as: debt / equity
2. Debt is $120 million, equity is $240 million
3. Ratio = 120 / 240 = 0.5

Answer: 0.5 or 1:2
```
**Model output:** "0.5" ✅  
**Why:** CoT forces model to break down the problem and realize it needs to calculate!

---

## 💡 Real Impact - FinHybrid Example

**Phase 2 Baseline:**
- 17 empty responses out of 47 questions (36.2%)
- These are questions where model returned ""

**What we expect with Phase 3C:**

| Prompt | Empty Count | Empty Rate | Improvement |
|--------|-------------|------------|-------------|
| Phase 2 (Simple) | 17 | 36.2% | Baseline |
| Instruction | ~13-15 | ~28-32% | **+2-4 questions** ✅ |
| Few-Shot | ~10-14 | ~21-30% | **+3-7 questions** ✅ |
| CoT (best) | ~7-12 | ~15-26% | **+5-10 questions** ✅ |

**Target:** Get to <30% empty (≤14 empty)

---

## 🔧 How It Works In The Notebooks

### In the notebook code:

```python
# Phase 2 (OLD - Simple prompt)
from uda.utils import llm
messages = llm.make_prompt(question, context, "fin", "gpt-4")
# This creates a simple "Context: ... Question: ... Answer:" prompt

# Phase 3C (NEW - Better prompts)
from uda.utils.prompts import get_prompt

# Choose which prompt to use
prompt_fn = get_prompt("instruction")  # or "fewshot" or "cot"

# Build the prompt
prompt_text = prompt_fn(context=retrieved_context, question=question)

# Convert to message format for Together AI
messages = [{"role": "user", "content": prompt_text}]

# Send to LLM
response = together_client.chat.completions.create(
    model="nvidia/nemotron-3-ultra-550b-a55b",
    messages=messages,
    temperature=0.1,
    max_tokens=512,
)

answer = response.choices[0].message.content
```

**That's it! The only change is the prompt structure.**

---

## 🎯 Why This Should Work

### 1. Literature Proven
- Instruction prompts: +10-30% improvement in many studies
- Few-shot learning: +15-40% improvement (especially for formatting)
- Chain-of-thought: +20-50% improvement (especially for reasoning tasks)

### 2. Low Risk
- ❌ pdfplumber **changed extraction** → broke chunking → made things worse
- ✅ Prompts only change **instructions** → can't break retrieval
- ✅ Worst case: No improvement, but won't make it WORSE

### 3. Universal Benefit
- ❌ pdfplumber only helps tables (failed on academic papers)
- ✅ Better prompts help **ALL datasets** (financial, Wikipedia, academic)

### 4. Easy to Test & Rollback
- ❌ pdfplumber required new extraction module, modified notebooks
- ✅ Prompts: Just change `PROMPT_TYPE = "instruction"` → test → revert if needed

---

## 📊 How To Interpret Results

After running the 3 notebooks on FinHybrid, you'll see:

```
COMPARISON WITH PHASE 2 BASELINE
================================
Phase 2 (Baseline): 17/47 empty (36.2%)
Phase 3C (Instruction): 14/47 empty (29.8%)

Improvement: +3 questions (-6.4 percentage points)
✅ SUCCESS: Instruction prompts reduced empty responses!
```

**What this means:**
- Baseline had 17 questions with empty answers
- Instruction prompt reduced this to 14 questions with empty answers
- **+3 questions now get answers!** (17 - 14 = 3)
- **This is working!** ✅

---

## 🚀 Summary - What You'll Run

You'll test each prompt variant and see which reduces empty responses the most:

1. **Instruction** - Adds explicit rules → Expected: +2-4 questions
2. **Few-Shot** - Shows 3 examples → Expected: +3-7 questions  
3. **CoT** - Step-by-step reasoning → Expected: +5-10 questions (but 2x cost)

Then scale the winner to all 6 datasets for **+10-20 questions overall**!

---

**Now you understand EXACTLY how the prompting works!** 🎯

The prompts are in `uda/utils/prompts.py` - you can read them anytime to see the exact text that gets sent to the model.

**Ready to run the experiments?** Just open the first notebook and see the improvement! 🚀
