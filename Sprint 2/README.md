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

## Key Findings

### 1. Context Window Impact
- Batch Mode: Format structure affects performance (JSON > HTML > XML > CSV)
- Individual Mode: Format differences disappear (all reach 80%)
- Insight: Large context windows (all data + 20 questions) favor structured formats

### 2. Format Characteristics

JSON (Best in Batch):
- Self-documenting (key-value pairs)
- Hierarchical structure natural for LLMs
- Easy to parse relationships

HTML:
- Visual structure hints (tables, headers)
- More verbose than JSON

XML:
- Hierarchical like JSON
- More verbose, harder to parse

CSV (Worst in Batch):
- Minimal structure (just commas)
- No relationship hints
- Most compact format

### 3. Question Difficulty

Medium Questions: 67-100% accuracy (easier)
- Simple filtering, counting
- Single table queries

Hard Questions: 57-86% accuracy
- Multi-table joins
- Aggregations with conditions

Extremely Hard: 43-57% accuracy (hardest)
- Complex multi-hop reasoning
- Multiple aggregations
- Edge case handling

### 4. Error Analysis

Common Errors:
- Stale metadata (old column values)
- Complex filtering mistakes
- Multi-table join errors
- Calculation errors

Empty Responses:
- Only 1/80 tests (CSV batch mode)
- 99% response rate overall

---

## File Structure

```
Sprint 2/
├── README.md (this file)
│
├── synthetic_data_from_LLM/
│   ├── albums.csv
│   ├── artists.csv
│   ├── tracks.csv
│   ├── streams.csv
│   ├── playlists.csv
│   ├── royalties.csv
│   ├── awards.csv
│   ├── collaborations.csv
│   ├── charts.csv
│   ├── track_features.csv
│   ├── record_labels.csv
│   └── anomalies.json
│
├── synthetic_data_from_script/
│   └── (alternative data generation approach)
│
├── Visualizations/
│   ├── benchmark_comparison_graph.png
│   ├── comprehensive_benchmark_analysis.png
│   ├── difficulty_distribution.png
│   ├── create_benchmark_visualization.py
│   ├── create_comprehensive_visualization.py
│   └── create_difficulty_visualization.py
│
├── Sprint2_Presentation_Nishit_Suthar.pptx
└── Individual_Work_Report_Nishit_Suthar_Sprint 2.docx
```

---

## Lessons Learned

### Technical Insights
1. Format matters in batch mode - JSON 45% better than CSV
2. Individual mode eliminates format bias - All formats converge to 80%
3. Context window size is critical - Smaller contexts benefit all formats
4. Gemini handles tabular data well - 80% baseline without training

### Methodological Insights
1. Ground truth essential - NeonDB validation critical
2. Question difficulty calibration - Need balanced distribution
3. Stale metadata issue - Data sampling must preserve currency
4. Multiple test modes needed - Batch vs individual reveals different patterns

### Practical Recommendations
1. For batch processing: Use JSON
2. For individual queries: Any format works (80% ceiling)
3. For production: Balance format choice with existing infrastructure
4. For future work: Test with examples (few-shot) to break 80% ceiling

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

## Impact & Next Steps

### Impact on Project
- Established 80% baseline for Gemini on tabular data
- Proved JSON best for batch processing
- Showed format-agnostic performance in individual mode
- Identified 80% ceiling for zero-shot prompting

### Recommendations for Sprint 3
1. Test RAG (Retrieval Augmented Generation) on unstructured documents
2. Try few-shot prompting to break 80% ceiling
3. Test different LLM models (GPT-4, Claude, Nemotron)
4. Focus on complex financial documents

---

## Key Achievements

- Comprehensive 4-format benchmark (80 total tests)  
- Identified JSON as optimal batch format  
- Discovered format-agnostic 80% ceiling  
- Established baseline for future comparisons  
- Created reusable test methodology
