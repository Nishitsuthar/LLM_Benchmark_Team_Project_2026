# Sprint 2: LLM Format Comparison Benchmark

**Duration:** May 2026  
**Status:** Complete  
**Team Member:** Nishit Suthar

---

## Objective

Benchmark Google Gemini 3.1 Pro Extended performance across different tabular data formats (CSV, HTML, JSON, XML) to determine optimal format for LLM data analysis tasks.

---

## Goals

1. Format Comparison: Test 4 formats (CSV, HTML, JSON, XML)
2. Question Complexity: Evaluate across difficulty levels (Medium, Hard, Extremely Hard)
3. Performance Metrics: Measure accuracy, error types, format preferences
4. Baseline Establishment: Create benchmark for future LLM comparisons

---

## Test Configuration

### Dataset
- Domain: Music industry (synthetic data)
- Size: 567 records (sampled with referential integrity)
- Tables: 12 interconnected tables
- Database: NeonDB (PostgreSQL)

### LLM Model
- Model: Google Gemini 3.1 Pro Extended
- Mode: Zero-shot (no examples provided)
- Temperature: 0 (deterministic)

### Test Questions
- Total: 20 questions
- Medium: 6 questions (30%)
- Hard: 7 questions (35%)
- Extremely Hard: 7 questions (35%)

---

## Results Summary

### Phase 1: Batch Mode (All 20 Questions at Once)

| Format | Accuracy | Medium | Hard | Ext. Hard | Empty | Wrong |
|--------|----------|--------|------|-----------|-------|-------|
| JSON | 80% | 100% | 86% | 57% | 0% | 20% |
| HTML | 70% | 83% | 71% | 57% | 0% | 30% |
| XML | 65% | 83% | 71% | 43% | 0% | 35% |
| CSV | 55% | 67% | 57% | 43% | 5% | 40% |

Winner: JSON (80% accuracy)

### Phase 2: Individual Mode (One Question at a Time)

| Format | Accuracy | Improvement |
|--------|----------|-------------|
| All Formats | 80% | +25% (CSV) |
| JSON | 80% | 0% |
| HTML | 80% | +10% |
| XML | 80% | +15% |
| CSV | 80% | +25% |

Result: All formats achieved 80% when tested individually.

---

## Methodology

### Phase 1: Batch Mode Testing
1. Load all 567 records in single format
2. Ask all 20 questions in one conversation
3. Evaluate responses against NeonDB ground truth
4. Repeat for all 4 formats

### Phase 2: Individual Mode Testing
1. Load all 567 records in single format
2. Ask ONE question per conversation
3. Evaluate response against NeonDB ground truth
4. Repeat for all 20 questions × 4 formats = 80 tests

### Evaluation Criteria
- Correct: Exact match with ground truth
- Wrong: Incorrect answer provided
- Empty: No answer returned
- Accuracy: Correct / Total questions

---

## Key Results

### Batch Mode Results
- JSON: 80% accuracy (Best)
- HTML: 70% accuracy
- XML: 65% accuracy
- CSV: 55% accuracy

### Individual Mode Results
- All Formats: 80% accuracy (format-agnostic)

### Key Findings
- JSON 45% better than CSV in batch mode
- Individual mode eliminates format differences
- 80% accuracy ceiling for zero-shot prompting
- Context window size critical for performance

---

## Key Learnings
1. Format matters in batch mode - JSON 45% better than CSV
2. Individual mode eliminates format bias - All formats converge to 80%
3. Context window size is critical - Smaller contexts benefit all formats
4. Ground truth validation essential - NeonDB critical for accuracy verification
5. Multiple test modes needed - Batch vs individual reveals different patterns

---

## Next Steps

1. Test RAG (Retrieval Augmented Generation) on unstructured documents
2. Try few-shot prompting to break 80% ceiling
3. Test different LLM models (GPT-4, Claude, Nemotron)
4. Focus on complex financial documents
