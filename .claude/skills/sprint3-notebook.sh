#!/bin/bash
# Skill: sprint3-notebook
# Description: Find and run the right notebook for Sprint 3 experiments
# Usage: /sprint3-notebook [dataset]

You are helping the user find and run Sprint 3 experiment notebooks.

## Your Task:

### If user provides a dataset name (finhybrid, tathybrid, nqtext, fetatab, papertab, papertext):

1. Show the optimal Phase 3C notebook for that dataset:
   - Full path to notebook
   - Optimal prompt type (CoT, Few-shot, etc.)
   - Expected results (% empty, success rate)
   - Expected runtime and cost
   - How to run it (Jupyter command)

2. Also list historical notebooks for that dataset:
   - Phase 1 baseline (if exists)
   - Phase 2 optimization variations
   - Phase 3 other prompt types
   - Where they're archived

3. Show the expected output:
   - Where results CSV will be saved
   - What metrics to look for
   - How to compare with Phase 3C finals

### If no dataset specified:

1. List all available notebooks organized by:
   - **Phase 3C Finals (Optimal)** - 4 notebooks
   - **Demos** - 2 notebooks
   - **Phase 1 Archive** - historical baselines
   - **Phase 2 Archive** - optimization experiments
   - **Phase 3 Archive** - other prompt variations

2. For each notebook show:
   - Path
   - Purpose
   - Dataset
   - Status (Final/Demo/Archive)
   - Quick description

3. Provide quick commands:
   ```bash
   # Run a specific notebook
   cd "Sprint 3/UDA-Benchmark"
   jupyter notebook [path/to/notebook.ipynb]
   ```

## Key Information to Include:

### Phase 3C Final Notebooks (THE OPTIMAL ONES):
```
experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/
├── nqtext_cot_experiment.ipynb          → CoT prompt, 4.2% empty
├── fetatab_cot_experiment.ipynb         → CoT prompt, 6.2% empty
├── tathybrid_fewshot_experiment.ipynb   → Few-shot, 12.3% empty
└── finhybrid_cot_experiment.ipynb       → CoT prompt, 27.7% empty
```

### Demo Notebooks:
```
UDA-Benchmark/
├── basic_demo.ipynb                     → Original UDA benchmark demo
└── basic_demo_together.ipynb            → Together API integration demo
```

### Archived Notebooks:
```
UDA-Benchmark/notebooks/archive/
├── phase1/
│   └── nemotron_phase1_experiment.ipynb  → Initial baseline (27 Q&A)
└── complete_tests/
    ├── finhybrid_complete_test.ipynb     → All FinHybrid docs test
    └── nqtext_complete_test.ipynb        → All NqText docs test
```

## Configuration Info to Share:

**Optimal Configuration (used in Phase 3C):**
```python
TOP_K = 10                    # Number of chunks to retrieve
CHUNK_SIZE = 1500             # Characters per chunk
CHUNK_OVERLAP = 100           # Overlap between chunks
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TEMPERATURE = 0.0             # Deterministic
MAX_TOKENS = 2000             # Answer length
```

**Cost Estimates:**
- Per question: ~$0.048
- Full dataset run: $15-75 depending on size
- Demo notebooks: $1-2

**Runtime Estimates:**
- Phase 3C notebooks: 30-90 minutes each
- Demo notebooks: 5-10 minutes
- Phase 1 baseline: 1-2 hours

## Troubleshooting Tips:
- If ModuleNotFoundError: `pip install together langchain chromadb sentence-transformers PyPDF2 pandas tqdm`
- If API key error: Check `uda/utils/access_config.py`
- If rate limiting: Increase sleep time between calls
- If ChromaDB error: Delete `chroma_db/` folder and rerun

Make the response actionable - user should be able to copy-paste commands and run immediately.
