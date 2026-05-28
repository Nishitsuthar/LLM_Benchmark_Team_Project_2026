# LLM Benchmark Questions for Music Industry Dataset

## 📋 Overview

This benchmark suite contains **30 carefully crafted questions** designed to evaluate LLM performance on complex database queries and analytical reasoning tasks using a realistic music industry dataset.

## 📊 Dataset Composition

| Category | Count | Description |
|----------|-------|-------------|
| **Medium** | 15 questions | Basic aggregations, simple JOINs (2-3 tables), percentage calculations |
| **Hard** | 7 questions | Complex JOINs (4+ tables), CTEs, window functions, statistical analysis |
| **Extremely Hard** | 8 questions | Advanced analytics, nested CTEs, business intelligence metrics, network analysis |
| **TOTAL** | **30 questions** | Progressive difficulty scaling |

---

## 🎯 Question Categories by Difficulty

### 📗 MEDIUM (Q001-Q015)
**Focus:** Foundational SQL skills and basic analytical thinking

**Skills Tested:**
- Single/two-table queries
- Basic aggregations: `COUNT()`, `SUM()`, `AVG()`, `MAX()`, `MIN()`
- Simple JOINs (2-3 tables)
- Percentage calculations
- WHERE clause filtering
- GROUP BY operations

**Example Questions:**
- Which artist has the highest popularity score?
- What is the total revenue in Q4-2024?
- Which genre has the most tracks?
- What percentage of tracks have explicit content?

---

### 📘 HARD (Q016-Q022)
**Focus:** Multi-step reasoning and advanced SQL techniques

**Skills Tested:**
- Complex multi-table JOINs (4+ tables)
- Common Table Expressions (CTEs)
- Window functions: `LAG()`, `RANK()`, `ROW_NUMBER()`
- Conditional aggregations with `CASE WHEN`
- Subqueries in SELECT, FROM, and WHERE clauses
- Statistical binning and grouping
- Month-over-month calculations

**Example Questions:**
- Calculate streams-to-awards ratio for top artists
- Analyze correlation between danceability and stream count
- Month-over-month streaming growth rate in 2024
- Identify artists with diverse album types

---

### 📕 EXTREMELY HARD (Q023-Q030)
**Focus:** Complex business logic, advanced analytics, and creative problem-solving

**Skills Tested:**
- Multiple nested CTEs (3+ levels)
- Advanced window functions with partitioning
- Complex mathematical formulas and custom metrics
- Network analysis (collaboration graphs)
- Temporal evolution analysis
- Business intelligence KPIs
- Multi-step data transformations
- String aggregation and dynamic grouping

**Example Questions:**
- Calculate "virality coefficient" across genres
- Find "hidden gem" tracks using multiple criteria
- Analyze "collaboration network effect" for artists
- Create "genre evolution timeline" across decades
- Calculate "revenue efficiency ratio" by label type
- Identify "Midas touch" producers
- Compute "playlist power index" by platform

---

## 📁 File Structure

```
llm_benchmark_questions.csv
├── question_id     : Unique identifier (Q001-Q030)
├── category        : Difficulty level (Medium/Hard/Extremely Hard)
├── question        : Natural language question for LLM
├── sql_query       : PostgreSQL query for ground truth
└── answer          : Empty field for storing ground truth results
```

---

## 🚀 Usage Instructions

### Step 1: Generate Ground Truth
```bash
# Connect to your NeonDB instance
psql "postgresql://user:password@host/database?sslmode=require"

# Execute queries from sql_query column
# Store results in answer column
```

### Step 2: Python Script Example
```python
import pandas as pd
import psycopg2

# Load questions
df = pd.read_csv('llm_benchmark_questions.csv')

# Connect to NeonDB
conn = psycopg2.connect("your_connection_string")
cursor = conn.cursor()

# Generate ground truth
for idx, row in df.iterrows():
    cursor.execute(row['sql_query'])
    result = cursor.fetchall()
    df.at[idx, 'answer'] = str(result)

# Save with answers
df.to_csv('llm_benchmark_questions_with_answers.csv', index=False)
```

### Step 3: Benchmark LLMs
```python
# Present question to LLM (without sql_query)
llm_response = query_llm(df.loc[0, 'question'])

# Compare with ground truth
ground_truth = df.loc[0, 'answer']
score = evaluate_response(llm_response, ground_truth)
```

---

## 🎓 Evaluation Criteria

### 1. **Correctness (50 points)**
- Exact match: 50/50
- Close match (±5% for numeric): 40/50
- Partially correct: 20/50
- Incorrect: 0/50

### 2. **SQL Quality (30 points)** *(if LLM generates SQL)*
- Optimal query structure: 30/30
- Suboptimal but correct: 20/30
- Inefficient but functional: 10/30
- Incorrect syntax/logic: 0/30

### 3. **Reasoning (20 points)**
- Clear explanation: 20/20
- Partial explanation: 10/20
- No explanation: 0/20

**Total Score: 100 points per question**

---

## 🔍 Query Complexity Breakdown

### Medium Queries (Q001-Q015)
- **Average Tables Joined:** 2-3
- **Average Lines of SQL:** 5-8
- **Key Concepts:** Basic JOINs, aggregations, filtering

### Hard Queries (Q016-Q022)
- **Average Tables Joined:** 4-6
- **Average Lines of SQL:** 10-20
- **Key Concepts:** CTEs, window functions, conditional logic

### Extremely Hard Queries (Q023-Q030)
- **Average Tables Joined:** 5-8
- **Average Lines of SQL:** 20-40
- **Key Concepts:** Nested CTEs, complex calculations, advanced analytics

---

## 📊 Schema Coverage

All 11 tables are covered across the 30 questions:

| Table | Questions Using It | Coverage |
|-------|-------------------|----------|
| artists | 28 questions | 93% |
| tracks | 25 questions | 83% |
| streams | 20 questions | 67% |
| albums | 15 questions | 50% |
| track_features | 12 questions | 40% |
| royalties | 10 questions | 33% |
| awards | 10 questions | 33% |
| charts | 9 questions | 30% |
| collaborations | 8 questions | 27% |
| playlists | 5 questions | 17% |
| record_labels | 5 questions | 17% |

---

## 💡 Advanced Metrics Explained

### Virality Coefficient (Q023)
```
(avg_peak_position × avg_weeks_on_chart × total_awards) / avg_completion_rate
```
Measures genre-level success combining chart performance, longevity, and industry recognition.

### Collaboration Network Effect (Q025)
```
artist_popularity - avg_collaborator_popularity
```
Identifies artists who "punch above their weight" by collaborating with less popular artists.

### Revenue Efficiency Ratio (Q026)
```
total_artist_payout / (artist_count × avg_years_active)
```
Measures label efficiency in artist development and monetization.

### Playlist Power Index (Q029)
```
(public_playlist_count × avg_position) / unique_users
```
Indicates platform curation quality and user engagement.

---

## 🎯 Benchmark Goals

This question set evaluates LLM capabilities across multiple dimensions:

1. **SQL Proficiency** - Can the LLM generate correct, efficient queries?
2. **Analytical Reasoning** - Can it understand complex business questions?
3. **Multi-step Logic** - Can it break down complex problems?
4. **Domain Knowledge** - Does it understand music industry concepts?
5. **Data Interpretation** - Can it explain results meaningfully?

---

## 🔧 Customization

### Adding Questions
```python
new_question = {
    'question_id': 'Q031',
    'category': 'Hard',
    'question': 'Your question here?',
    'sql_query': 'SELECT ... FROM ... WHERE ...',
    'answer': ''
}
```

### Adjusting Difficulty
- **Easier:** Reduce number of JOINs, remove CTEs, simplify conditions
- **Harder:** Add more tables, require nested subqueries, introduce edge cases

---

## 📈 Expected Performance

### GPT-4 / Claude 3.5 Sonnet (Estimated)
- **Medium:** 90-95% accuracy
- **Hard:** 70-80% accuracy
- **Extremely Hard:** 40-60% accuracy

### GPT-3.5 / Claude 3 Haiku (Estimated)
- **Medium:** 70-80% accuracy
- **Hard:** 40-50% accuracy
- **Extremely Hard:** 10-20% accuracy

### Smaller Models (<7B parameters)
- **Medium:** 30-50% accuracy
- **Hard:** 10-20% accuracy
- **Extremely Hard:** 0-5% accuracy

---

## 🐛 Common Pitfalls for LLMs

1. **Incorrect JOIN types** - Using INNER when LEFT is needed
2. **Missing HAVING clauses** - Using WHERE on aggregated columns
3. **Incorrect date functions** - Timezone issues, date arithmetic errors
4. **Division by zero** - Not using NULLIF() in denominators
5. **String aggregation** - Forgetting ORDER BY in STRING_AGG()
6. **Window function confusion** - Misusing PARTITION BY vs GROUP BY
7. **CTE dependency** - Referencing CTEs in wrong order

---

## 📚 References

- **Dataset:** Music Industry Synthetic Data (32,550 records, 11 tables)
- **Database:** NeonDB (PostgreSQL-compatible)
- **SQL Dialect:** PostgreSQL 15+
- **Date Range:** 2001-2026 (25 years)

---

## ✅ Validation Checklist

Before running benchmark:
- [ ] Data imported into NeonDB
- [ ] All 11 tables present and populated
- [ ] Foreign key relationships intact
- [ ] Test query execution on sample questions
- [ ] Ground truth answers generated
- [ ] Evaluation criteria defined
- [ ] LLM API configured and tested

---

## 🎉 Quick Start

```bash
# 1. Import data to NeonDB
python scripts/data_import_neonDB/import_to_neon.py

# 2. Generate ground truth
python generate_ground_truth.py

# 3. Run benchmark
python run_llm_benchmark.py --model gpt-4 --questions llm_benchmark_questions.csv

# 4. View results
python analyze_benchmark_results.py
```

---

## 📞 Support

For questions or issues with the benchmark dataset:
1. Check data integrity with validation queries
2. Verify NeonDB connection and permissions
3. Review SQL syntax for PostgreSQL compatibility
4. Ensure all tables are properly indexed

---

## 🏆 Success Metrics

A well-performing LLM should achieve:
- **>85% on Medium questions** - Demonstrates basic SQL competency
- **>60% on Hard questions** - Shows advanced analytical capability
- **>30% on Extremely Hard questions** - Indicates expert-level reasoning

**Overall Target:** 70%+ average across all 30 questions for production-ready LLMs.

---

Generated: 2026-05-27
Version: 1.0
Status: Production-Ready ✅
