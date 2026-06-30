# 🔍 Which Cell Optimizes the Process?

**Quick Answer:** The optimization happens in **TWO places**:
1. **Cell 6** - Where you SET the parameter value
2. **Cell 10** - Where the parameter is USED in retrieval

---

## 📋 The Two Key Cells

### Cell 6: Parameter Definition ⚙️

**What it does:** Sets TOP_K = 10

```python
# Experiment Parameters
DATASET_NAME = "fin"
CHUNK_SIZE = 3000
CHUNK_OVERLAP = 300
TOP_K = 10              ← THIS IS THE OPTIMIZATION! Changed from 5 to 10
TEMPERATURE = 0.1
MAX_TOKENS = 512

# Output settings
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_DIR = "./experiments/nemotron-3-ultra-550b/2_optimization/results/finhybrid_topk10"
```

**Why it matters:** This is where you control the optimization parameter

---

### Cell 10: Retrieval Function 🎯 ⭐ CRITICAL!

**What it does:** Uses TOP_K to retrieve chunks

```python
def answer_question(collection, question):
    """Retrieve context and generate answer"""
    
    # Retrieve TOP_K chunks from vector database
    fetch_res = collection.query(
        query_texts=[question], 
        n_results=TOP_K        ← THIS LINE USES YOUR OPTIMIZATION!
    )
    
    # Combine retrieved chunks into context
    context = "\n".join(fetch_res["documents"][0])
    
    # Build prompt with question + context
    llm_message = llm.make_prompt(
        question=question,
        context=context,
        task_name=DATASET_NAME,
        llm_type="gpt-4"
    )
    
    # Generate answer using LLM
    response = client.chat.completions.create(
        model=TOGETHER_MODEL,
        messages=llm_message,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )
    
    return response.choices[0].message.content
```

**Why it matters:** This is the actual retrieval step where optimization takes effect!

---

## 🔄 How the Optimization Works - Step by Step

### Baseline (TOP_K=5):
```
Question: "What was the revenue in 2019?"
    ↓
1. Convert question to vector (embedding)
    ↓
2. Search vector database for similar chunks
    ↓
3. Retrieve TOP 5 most similar chunks     ← Baseline: only 5 chunks
    ↓
4. Combine chunks into context
    ↓
5. Send to LLM: "Context: <5 chunks>\nQuestion: What was the revenue?"
    ↓
6. Get answer
```

**Problem:** If the answer is in chunk #6, #7, or #8, we miss it! → Empty response

---

### Optimized (TOP_K=10):
```
Question: "What was the revenue in 2019?"
    ↓
1. Convert question to vector (embedding)
    ↓
2. Search vector database for similar chunks
    ↓
3. Retrieve TOP 10 most similar chunks    ← Optimized: 10 chunks!
    ↓
4. Combine chunks into context
    ↓
5. Send to LLM: "Context: <10 chunks>\nQuestion: What was the revenue?"
    ↓
6. Get answer
```

**Benefit:** More chances to find the answer! → Fewer empty responses

---

## 📊 Visual Comparison

### Baseline Retrieval (TOP_K=5):
```
Document: [Chunk1] [Chunk2] [Chunk3] [Chunk4] [Chunk5] [Chunk6] [Chunk7] [Chunk8] [Chunk9] [Chunk10]
                                                         ^
Question: "What was revenue?"                            |
                                                    Answer is here!
Retrieved: [Chunk1] [Chunk2] [Chunk4] [Chunk8] [Chunk10]
           ↑ Most  ↑        ↑        ↑        ↑ 5th most
           similar                            similar

Result: MISS! Chunk6 has the answer but wasn't retrieved.
Model Response: "" (empty)
```

### Optimized Retrieval (TOP_K=10):
```
Document: [Chunk1] [Chunk2] [Chunk3] [Chunk4] [Chunk5] [Chunk6] [Chunk7] [Chunk8] [Chunk9] [Chunk10]
                                                         ^
Question: "What was revenue?"                            |
                                                    Answer is here!
Retrieved: [Chunk1] [Chunk2] [Chunk3] [Chunk4] [Chunk5] [Chunk6] [Chunk7] [Chunk8] [Chunk9] [Chunk10]
           ↑ Most                                 ↑                                 ↑ 10th most
           similar                           FOUND IT!                              similar

Result: HIT! Chunk6 retrieved!
Model Response: "$45.2 million"
```

---

## 🎯 The Optimization Logic

### Why Increasing TOP_K Helps:

**1. Better Coverage**
- More chunks = more context
- Higher chance of finding relevant information
- Reduces "needle in haystack" problem

**2. Redundancy**
- Even if one chunk is incomplete, others might help
- Multiple perspectives on same topic
- Better for complex questions

**3. Handles Imperfect Embeddings**
- Embeddings aren't perfect
- Sometimes answer is in 6th or 7th most similar chunk
- TOP_K=10 gives us a buffer

### Trade-offs:

**Pros:**
- ✅ Fewer empty responses
- ✅ More context for complex questions
- ✅ Better recall

**Cons:**
- ⚠️ More tokens used (10 chunks vs 5)
- ⚠️ Slightly higher cost (~$0.50-1 extra per run)
- ⚠️ More noise in context (less relevant chunks)
- ⚠️ Slightly slower retrieval

---

## 📝 Other Cells in the Pipeline

For completeness, here's what other cells do:

### Cell 1-4: Setup
- Import libraries
- Load modules
- No optimization here

### Cell 5: Load API Config
- Loads Together AI credentials
- No optimization here

### Cell 6: **OPTIMIZATION PARAMETER** ⚙️
- **Sets TOP_K = 10**
- This is where you control it!

### Cell 7-9: Initialize Models
- Load embedding model
- Create text splitter
- No optimization here

### Cell 10: **OPTIMIZATION USAGE** 🎯
- **Uses TOP_K in retrieval**
- This is where it takes effect!

### Cell 11: Load Q&A Data
- Reads CSV file
- Filters to available PDFs
- No optimization here

### Cell 12: Main Processing Loop
- For each document:
  - Extract text from PDF
  - Split into chunks
  - Build vector index
  - For each question:
    - **Call answer_question() which uses TOP_K** ← Optimization happens here!
    - Save response

### Cell 13: Empty Response Diagnostic
- Analyzes empty responses
- This is where you'll see improvement!

### Cell 14: Evaluation
- Calculates accuracy score
- This is where you'll see score improvement!

### Cell 15: Save Results
- Saves to CSV
- No optimization here

---

## 🔍 How to Verify Optimization is Working

### Before Running:
Check Cell 6 shows:
```python
TOP_K = 10  ✓
```

### While Running:
Watch Cell 12 output - you should see:
- Processing questions
- Fewer "Empty response" warnings (hopefully!)

### After Running:
Check Cell 13 diagnostic:
```
Empty responses: X out of 47 (Y%)
```
Compare to baseline: 19 out of 47 (40.4%)
Target: ~14-17 out of 47 (30-35%)

---

## 💡 Summary

**The optimization happens in TWO cells:**

1. **Cell 6** - You SET the parameter
   ```python
   TOP_K = 10  # Changed from 5
   ```

2. **Cell 10** - The parameter is USED
   ```python
   fetch_res = collection.query(query_texts=[question], n_results=TOP_K)
   ```

**The effect:**
- Baseline: Retrieves 5 chunks per question
- Optimized: Retrieves 10 chunks per question
- Impact: More context → fewer empty responses → better scores

**To verify it's working:**
- Check Cell 6 shows TOP_K = 10
- Watch for fewer empty responses in Cell 12
- Compare empty rate in Cell 13 to baseline

---

**That's it!** The optimization is simple but effective. You're just retrieving more context chunks to give the model a better chance of finding the answer.

Ready to run? Open the notebook and watch Cell 13 to see the improvement! 🚀
