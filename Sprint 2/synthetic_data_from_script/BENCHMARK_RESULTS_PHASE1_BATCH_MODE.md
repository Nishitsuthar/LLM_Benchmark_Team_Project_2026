# LLM Benchmark Results - Phase 1: Batch Mode Testing

**Date:** 2026-05-27  
**Model:** Gemini 3.1 Pro Extended  
**Dataset:** Music Industry (Sampled - 567 records)  
**Mode:** Batch (All 20 questions at once)  
**Prompting:** Zero-shot, baseline (no special techniques)

---

## Executive Summary

**Overall Performance Ranking:**
1. **JSON: 80.0%** (16/20 correct)
2. **HTML: 70.0%** (14/20 correct)
3. **XML: 65.0%** (13/20 correct)
4. **CSV: 55.0%** (11/20 correct)

**Key Findings:**
- JSON format significantly outperforms other formats (+10-25% higher accuracy)
- All formats perfect on Medium difficulty questions (except CSV on Q006)
- Hard questions are the weakest category across all formats (28.6-57.1%)
- Extremely Hard questions paradoxically perform better than Hard questions
- Consistent error pattern: Q007 stale metadata issue affects all formats

---

## Detailed Results by Format

### 📊 CSV Format - 55% Accuracy (11/20)

| Question | Difficulty | Correct? | Notes |
|----------|-----------|----------|-------|
| Q001 | Medium | ✓ | The Ortegas, 1.0, 10 albums |
| Q002 | Medium | ✓ | 4.74 minutes |
| Q003 | Medium | ✓ | Hip-Hop, 42 artists |
| Q004 | Medium | ✓ | 84.69% active |
| Q005 | Medium | ✓ | 6 explicit tracks |
| Q006 | Medium | ✗ | Said "Gray-Mayo Entertainment" (correct but 1 of 4 tied) |
| Q007 | Hard | ✗ | Jazz 13.67 (should be 2.00) - stale metadata |
| Q008 | Hard | ✗ | Found 4 artists, ground truth is 6 |
| Q009 | Hard | ✓ | All 10 distributions correct |
| Q010 | Hard | ✓ | Top 5 tracks correct |
| Q011 | Hard | ✓ | Countries by popularity (truncated) |
| Q012 | Hard | ✗ | Found 18 artists, ground truth is 3 |
| Q013 | Hard | ✗ | Wrong speechiness values |
| Q014 | Extremely Hard | ✓ | David Davis, 0.126 |
| Q015 | Extremely Hard | ✗ | Wrong ranking/calculation |
| Q016 | Extremely Hard | ✓ | All 4 mood quadrants match |
| Q017 | Extremely Hard | ✓ | Rock, 0.9127 |
| Q018 | Extremely Hard | ✓ | Top 3 prolific years |
| Q019 | Extremely Hard | ✗ | Partial answer |
| Q020 | Extremely Hard | ✓ | No results (correct) |

**By Difficulty:**
- Medium (6): 5/6 = 83.3%
- Hard (7): 2/7 = 28.6%
- Extremely Hard (7): 4/7 = 57.1%

---

### 📊 HTML Format - 70% Accuracy (14/20)

| Question | Difficulty | Correct? | Notes |
|----------|-----------|----------|-------|
| Q001 | Medium | ✓ | The Ortegas, 1.0, 10 albums |
| Q002 | Medium | ✓ | 4.74 minutes |
| Q003 | Medium | ✓ | Hip-Hop, 42 artists |
| Q004 | Medium | ✓ | 84.69% active |
| Q005 | Medium | ✓ | 6 explicit tracks |
| Q006 | Medium | ✓ | Gray-Mayo Entertainment (1 of 4 tied) |
| Q007 | Hard | ✗ | Jazz 13.67 (should be 2.00) - stale metadata |
| Q008 | Hard | ✗ | Found 4 artists, ground truth is 6 |
| Q009 | Hard | ✓ | All 10 distributions correct |
| Q010 | Hard | ✓ | Top 5 tracks correct |
| Q011 | Hard | ✓ | Countries by popularity (truncated) |
| Q012 | Hard | ✗ | Found 18 artists, ground truth is 3 |
| Q013 | Hard | ✗ | Wrong speechiness values |
| Q014 | Extremely Hard | ✓ | David Davis, 0.126 |
| Q015 | Extremely Hard | ✗ | Wrong calculation method |
| Q016 | Extremely Hard | ✓ | All 4 mood quadrants match |
| Q017 | Extremely Hard | ✓ | Rock, 0.9127 |
| Q018 | Extremely Hard | ✓ | Top 3 prolific years |
| Q019 | Extremely Hard | ✓ | Full spectrum for 10 genres |
| Q020 | Extremely Hard | ✓ | No results (correct) |

**By Difficulty:**
- Medium (6): 6/6 = 100%
- Hard (7): 3/7 = 42.9%
- Extremely Hard (7): 5/7 = 71.4%

**Key Observations:**
- Generated Python code to parse HTML tables
- Perfect on Medium questions
- Struggled with Hard questions (filtering, aggregations)

---

### 📊 JSON Format - 80% Accuracy (16/20) ⭐ BEST

| Question | Difficulty | Correct? | Notes |
|----------|-----------|----------|-------|
| Q001 | Medium | ✓ | The Ortegas, 1.0, 10 albums |
| Q002 | Medium | ✓ | 4.74 minutes |
| Q003 | Medium | ✓ | Hip-Hop, 42 artists |
| Q004 | Medium | ✓ | 84.69% active |
| Q005 | Medium | ✓ | 6 explicit tracks |
| Q006 | Medium | ✓ | Gray-Mayo Entertainment (1 of 4 tied) |
| Q007 | Hard | ✗ | Jazz 13.67 (should be 2.00) - stale metadata |
| Q008 | Hard | ✗ | Found 4 artists, ground truth is 6 |
| Q009 | Hard | ✓ | All 10 distributions correct |
| Q010 | Hard | ✓ | Top 5 tracks correct |
| Q011 | Hard | ✓ | Countries by popularity (truncated) |
| Q012 | Hard | ✗ | Found 18 artists, ground truth is 3 |
| Q013 | Hard | ✓ | Explicit vs non-explicit speechiness |
| Q014 | Extremely Hard | ✓ | David Davis, 0.126 |
| Q015 | Extremely Hard | ✗ | Calculation error: 1.2 vs 12.00 |
| Q016 | Extremely Hard | ✓ | All 4 mood quadrants match |
| Q017 | Extremely Hard | ✓ | Rock, 0.9127 |
| Q018 | Extremely Hard | ✓ | Top 3 prolific years |
| Q019 | Extremely Hard | ✓ | Full spectrum for 10 genres |
| Q020 | Extremely Hard | ✓ | No results (correct) |

**By Difficulty:**
- Medium (6): 6/6 = 100%
- Hard (7): 4/7 = 57.1%
- Extremely Hard (7): 6/7 = 85.7%

**Key Observations:**
- Best overall performance
- Generated Python code to parse JSON
- Excellent on Extremely Hard questions (85.7%)
- Still struggled with Q007 (stale metadata), Q008 (missing artists), Q012 (wrong filtering)

---

### 📊 XML Format - 65% Accuracy (13/20)

| Question | Difficulty | Correct? | Notes |
|----------|-----------|----------|-------|
| Q001 | Medium | ✓ | The Ortegas, 1.0, 10 albums |
| Q002 | Medium | ✓ | 4.74 minutes |
| Q003 | Medium | ✓ | Hip-Hop, 42 artists |
| Q004 | Medium | ✓ | 84.69% active |
| Q005 | Medium | ✓ | 6 explicit tracks |
| Q006 | Medium | ✓ | Mcclure, Ward and Lee Entertainment (1 of 4 tied) |
| Q007 | Hard | ✗ | Jazz 13.67 (should be 2.00) - stale metadata |
| Q008 | Hard | ✗ | Found 4 artists (The Ortegas=11), ground truth is 6 (The Ortegas=12) |
| Q009 | Hard | ✓ | All 10 distributions correct |
| Q010 | Hard | ✗ | Only returned 3 tracks instead of 5 |
| Q011 | Hard | ✓ | Countries by popularity (truncated) |
| Q012 | Hard | ✗ | Found 18 artists, ground truth is 3 |
| Q013 | Hard | ✓ | Explicit vs non-explicit speechiness |
| Q014 | Extremely Hard | ✓ | David Davis, 0.378 |
| Q015 | Extremely Hard | ✗ | Used different formula |
| Q016 | Extremely Hard | ✓ | All 4 mood quadrants match |
| Q017 | Extremely Hard | ✗ | Rock with score 2.74 (ground truth: 0.9127) |
| Q018 | Extremely Hard | ✓ | Top 3 prolific years |
| Q019 | Extremely Hard | ✗ | Only returned most acoustic/electronic, not full spectrum |
| Q020 | Extremely Hard | ✓ | No results (correct) |

**By Difficulty:**
- Medium (6): 6/6 = 100%
- Hard (7): 3/7 = 42.9%
- Extremely Hard (7): 5/7 = 71.4%

**Key Observations:**
- Generated Python code with ElementTree for XML parsing
- Q010: Only returned top 3 instead of top 5
- Q015: Used custom overperformance formula
- Q017: Different normalization approach (2.74 vs 0.9127)
- Q019: Partial answer (only extremes, not full spectrum)

---

## Cross-Format Analysis

### Performance by Difficulty Level

| Difficulty | CSV | HTML | JSON | XML | Average |
|------------|-----|------|------|-----|---------|
| **Medium (6)** | 83.3% | 100% | 100% | 100% | **95.8%** |
| **Hard (7)** | 28.6% | 42.9% | 57.1% | 42.9% | **42.9%** |
| **Extremely Hard (7)** | 57.1% | 71.4% | 85.7% | 71.4% | **71.4%** |

**Key Insight:** Hard questions are actually harder than Extremely Hard questions across all formats!

---

### Common Errors Across All Formats

#### ✗ Q007 - Stale Metadata Issue (All 4 formats failed)
- **Question:** Average tracks per album by genre
- **Ground Truth:** Jazz = 2.00 tracks/album (counting actual tracks)
- **All Formats Said:** Jazz = 13.67 tracks/album (using `albums.total_tracks` metadata column)
- **Root Cause:** LLM trusts pre-calculated metadata instead of counting from tracks table
- **Impact:** Reveals LLM behavior - takes shortcuts with metadata columns

#### ✗ Q008 - Missing Artists (All 4 formats failed)
- **Question:** Artists with at least 1 award won
- **Ground Truth:** 6 artists (The Ortegas=12, James Brooks=1, The Bryants=1, Susan Murray MD=1, The Knights=1, The Haydens=1)
- **All Formats Found:** 4 artists (missing 2-3 artists)
- **Root Cause:** Incomplete joins or filtering issue

#### ✗ Q012 - Wrong Filtering (All 4 formats failed)
- **Question:** Artists with tracks in multiple albums (album_count > 1)
- **Ground Truth:** 3 artists
- **All Formats Found:** 18+ artists
- **Root Cause:** Likely returned artists with 1 album but multiple tracks per album

---

### Format-Specific Strengths

**JSON Strengths:**
- Best overall accuracy (80%)
- Excellent on Extremely Hard questions (85.7%)
- Clean Python pandas parsing
- Native data structure for programming

**HTML Strengths:**
- Second-best accuracy (70%)
- Perfect on Medium questions (100%)
- Good on Extremely Hard (71.4%)
- BeautifulSoup parsing worked well

**XML Strengths:**
- Third place (65%)
- Perfect on Medium questions (100%)
- ElementTree parsing functional
- Structured hierarchical data

**CSV Strengths:**
- Simplest format, easiest to parse
- Still competitive on Extremely Hard (57.1%)
- Direct pandas.read_csv()

**CSV Weaknesses:**
- Lowest overall accuracy (55%)
- Worst on Hard questions (28.6%)
- Struggled with Q006 tie-breaking

---

## Question-Level Insights

### Easiest Questions (100% across all formats)
- Q001: Highest popularity artist + album count
- Q002: Average track duration
- Q003: Genre with most artists
- Q004: Percentage active artists
- Q005: Count explicit tracks

### Hardest Questions (0-25% across formats)
- Q007: Average tracks per album by genre (0% - stale metadata)
- Q008: Artists with awards (0% - missing records)
- Q012: Artists in multiple albums (0% - wrong filtering)
- Q015: Overperforming artists (0-25% - calculation errors)

### Most Reliable Questions (75-100% across formats)
- Q016: Track mood profile (100%)
- Q018: Prolific years (100%)
- Q020: Hidden gem tracks (100%)
- Q009: Album distribution by label type (100%)
- Q017: Genre dominance score (75%)

---

## Gemini Model Behavior Observations

### Code Generation Approach
All formats except CSV triggered Python code generation:
- **HTML:** Used BeautifulSoup + pandas
- **JSON:** Used json module + pandas
- **XML:** Used xml.etree.ElementTree + pandas

### Common Patterns
1. **Metadata Trust:** Model consistently trusts pre-calculated columns over actual counts
2. **Incomplete Aggregations:** Misses records in complex JOIN operations
3. **Formula Interpretation:** Sometimes invents own formulas for ambiguous questions
4. **Truncation:** Appropriately truncates long lists (Q011 countries)
5. **NULL Handling:** Generally handles missing data well

### Error Categories
1. **Data Quality Issues:** Stale metadata (Q007)
2. **Logic Errors:** Wrong filtering conditions (Q012)
3. **Incomplete Results:** Missing records (Q008, Q010)
4. **Calculation Errors:** Wrong formulas (Q015, Q017)
5. **Partial Answers:** Only returning extremes (Q019 in XML)

---

## Statistical Summary

| Metric | CSV | HTML | JSON | XML |
|--------|-----|------|------|-----|
| **Total Correct** | 11 | 14 | 16 | 13 |
| **Total Wrong** | 9 | 6 | 4 | 7 |
| **Accuracy** | 55.0% | 70.0% | 80.0% | 65.0% |
| **Medium Accuracy** | 83.3% | 100% | 100% | 100% |
| **Hard Accuracy** | 28.6% | 42.9% | 57.1% | 42.9% |
| **Extremely Hard Accuracy** | 57.1% | 71.4% | 85.7% | 71.4% |

**Confidence Intervals (assuming binomial distribution):**
- CSV: 55% ± 22% (95% CI: 33-77%)
- HTML: 70% ± 20% (95% CI: 50-90%)
- JSON: 80% ± 18% (95% CI: 62-98%)
- XML: 65% ± 21% (95% CI: 44-86%)

---

## Conclusions

1. **JSON is the best format** for tabular data analysis with Gemini 3.1 Pro Extended (80% accuracy)

2. **Hard questions are harder than Extremely Hard** - Possible reasons:
   - Extremely Hard questions more explicit in requirements
   - Hard questions more ambiguous
   - Complex JOINs in Hard questions trip up the model

3. **Stale metadata is a critical issue** - Models trust pre-calculated columns without validation

4. **All formats struggle with the same questions** - Suggests model logic issues, not format parsing issues

5. **Medium questions are nearly perfect** (95.8% average) - Basic aggregations work well

6. **Format matters significantly** - 25% difference between best (JSON 80%) and worst (CSV 55%)

---

## Next Steps: Phase 2

### Individual Question Mode Testing
Test each question separately to see if batch mode creates context pollution:
- 20 questions × 4 formats = 80 individual tests
- Compare individual vs batch performance
- Hypothesis: Individual mode may reduce accumulating errors

### Advanced Prompting Techniques
Apply research paper findings:
1. **Self-Augmented Prompting:** Let model generate intermediate steps
2. **Few-Shot Learning:** Provide 2-3 example questions with solutions
3. **Chain-of-Thought:** Ask model to explain reasoning step-by-step
4. **Schema Awareness:** Provide explicit schema definitions

### Expected Improvements
- Target: 90%+ accuracy with advanced techniques
- Focus on Hard questions (currently weakest at 42.9%)
- Fix stale metadata issue with explicit instructions

---

## Data Verification Status

✅ **All ground truth answers verified against NeonDB**
- Confirmed Q007 stale metadata issue (metadata: 13.67 vs actual: 2.00)
- Confirmed Q006 has 4-way tie (all acceptable answers)
- Confirmed Q008 ground truth is correct (6 artists with awards)
- Verified all 20 ground truth answers are accurate

---

## Appendices

### Appendix A: Ground Truth Answers
See: `llm_benchmark_questions_sampled.csv`

### Appendix B: Raw Gemini Responses
- CSV Batch: [User provided in conversation]
- HTML Batch: [User provided in conversation]
- JSON Batch: [User provided in conversation]
- XML Batch: [User provided in conversation]

### Appendix C: Verification Queries
See: `verify_answers.sql`

### Appendix D: Dataset Information
- **Original Dataset:** 32,550 records
- **Sampled Dataset:** 567 records (2.1% sample)
- **Sampling Method:** Balanced stratified sampling with referential integrity
- **Format Files:**
  - CSV: 41 KB
  - HTML: 168 KB
  - JSON: 173 KB
  - XML: 211 KB

---

**Report Generated:** 2026-05-27  
**Phase:** 1 - Batch Mode Testing (Complete)  
**Next Phase:** Individual Question Mode Testing  
**Future Phase:** Advanced Prompting Techniques
