#!/bin/bash
# Skill: sprint3-experiment
# Description: Explain Sprint 3 experiment phases and what was tested
# Usage: /sprint3-experiment [phase]

You are helping the user understand the Sprint 3 experiment timeline and what each phase tested.

## Your Task:

### If user specifies a phase (1, 2, 3a, 3b, 3c):

Provide detailed information about that specific phase:

**Phase 1: Baseline Evaluation**
- Goal: Establish baseline performance
- Scope: 27 Q&A on 2 documents (initial), then expanded to 312 Q&A
- Method: Zero-shot prompts, default parameters
- Results: 11-34% accuracy on 2 docs, 35% empty rate on full set
- Files: Sprint 3/PHASE1_BASELINE_RESULTS.md
- Status: Complete (historical baseline)

**Phase 2: Hyperparameter Optimization**
- Goal: Optimize RAG retrieval parameters
- Variables tested:
  - TOP_K: 3, 5, 10 chunks
  - CHUNK_SIZE: 500, 1000, 1500 characters
- Results: 16.7% empty rate (improved from 35%)
- Optimal: TOP_K=10, CHUNK_SIZE=1500
- Files: experiments/nemotron-3-ultra-550b/2_optimization/
- Status: Complete, configuration adopted for Phase 3

**Phase 3A: PDFPlumber (ABANDONED)**
- Goal: Better PDF text extraction
- Method: Replace PyPDF2 with pdfplumber
- Results: No significant improvement, added complexity
- Decision: Abandoned, stuck with PyPDF2
- Files: experiments/.../3_advanced_optimization/1_pdfplumber/
- Status: Abandoned

**Phase 3B: FinBERT Embeddings (FAILED)**
- Goal: Domain-specific embeddings for financial docs
- Method: Replace generic embeddings with FinBERT
- Results: REGRESSION - 14.4% empty (worse than 12.2%)
- Root cause: FinBERT is sentiment model, not retrieval model
- Files: UDA-Benchmark/PHASE3B_ABANDONED.md
- Status: Failed experiment, lessons learned

**Phase 3C: Prompt Optimization (FINAL)**
- Goal: Optimize prompts per dataset
- Methods tested:
  - Zero-shot baseline
  - Chain-of-Thought (CoT)
  - Few-shot with examples
  - Instruction prompting
  - Self-consistency
- Results: 12.2% empty rate (TARGET: <12%)
- Best prompts:
  - NqText: CoT (4.2% empty)
  - FetaTab: CoT (6.2% empty)
  - TatHybrid: Few-shot (12.3% empty)
  - FinHybrid: CoT (27.7% empty)
- Files: UDA-Benchmark/FINAL_RESULTS_PHASE3C.md
- Status: ✅ FINAL - Project complete

### If no phase specified:

Show the complete experiment timeline:

```
Sprint 3 Experiment Timeline
════════════════════════════════════════════════════════════

Phase 1: Baseline (June 28)
├── Initial test: 27 Q&A, 2 docs
├── Result: 11-34% accuracy
└── Expanded: 312 Q&A, 17 docs → 35% empty

        ↓ [10% improvement]

Phase 2: Hyperparameter Tuning (June 29)
├── Optimized: TOP_K, CHUNK_SIZE
├── Result: 16.7% empty rate
└── Adopted: TOP_K=10, CHUNK_SIZE=1500

        ↓ [4.5% improvement]

Phase 3A: PDFPlumber Test (June 29)
├── Tested: Better PDF extraction
└── Result: ❌ Abandoned (no improvement)

        ↓ [attempt failed]

Phase 3B: FinBERT Embeddings (June 30)
├── Tested: Domain-specific embeddings
├── Result: 14.4% empty (REGRESSION!)
└── Decision: ❌ Stick with generic embeddings

        ↓ [back to Phase 2 config]

Phase 3C: Prompt Optimization (June 30)
├── Tested: 5 prompt types per dataset
├── Result: 12.2% empty rate ✅
├── Success: 274/312 answered (87.8%)
└── Status: FINAL - Project complete

════════════════════════════════════════════════════════════

Total Improvement: 35% → 12.2% (65% reduction in failures)
Total Cost: ~$138
Total Time: 15 hours
Final Gap to Target: +0.2% (just 2 questions away)
```

### Key Lessons Learned:

1. **Hyperparameters matter** - Phase 2 gained 18.3% improvement
2. **Dataset-specific prompts** - No one-size-fits-all solution
3. **CoT works for reasoning** - Best for financial and complex questions
4. **Few-shot works for extraction** - Best for table and factual data
5. **Domain models ≠ Always better** - FinBERT failed (wrong use case)
6. **Diminishing returns** - Phase 3C only improved 4.5% for significant effort

### Where to Find More:

- **Phase 1 details:** Sprint 3/PHASE1_BASELINE_RESULTS.md
- **Phase 2 reports:** experiments/.../2_optimization/documentation/reports/
- **Phase 3A verdict:** experiments/.../1_pdfplumber/FINAL_VERDICT_ABANDON.md
- **Phase 3B analysis:** UDA-Benchmark/PHASE3B_ABANDONED.md
- **Phase 3C final:** UDA-Benchmark/FINAL_RESULTS_PHASE3C.md (⭐ THE MAIN RESULTS)

## Provide Context:

**Why these experiments mattered:**
- Started at 35% empty rate (barely usable)
- Ended at 12.2% empty rate (production-ready)
- Learned what works (and doesn't) for RAG on financial docs
- Created reusable methodology for future LLM benchmarking

Make the explanation clear and show the progression story.
