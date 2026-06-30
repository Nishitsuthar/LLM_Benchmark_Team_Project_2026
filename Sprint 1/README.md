# Sprint 1: Data Preparation & Sampling

**Duration:** April 2026  
**Status:** Complete  
**Team Member:** Nishit Suthar

---

## Objective

Prepare and sample movie dataset for LLM benchmarking by creating both structured and unstructured data formats for testing LLM capabilities in data processing and analysis.

---

## Goals

1. Data Sampling: Create a manageable subset from large movie dataset
2. Format Conversion: Generate multiple data formats (CSV, Excel, Text)
3. Data Enrichment: Merge cast information with movie data
4. Quality Validation: Ensure data integrity and completeness

---

## Deliverables

### Input Data
- Full movies dataset with comprehensive metadata
- Cast/crew information

### Output Data
1. **Sampled_870_Movies.csv** (482 KB) - Sampled movie records in CSV format
2. **Sampled_870_Movies.xlsx** (207 KB) - Excel version with formatting
3. **Final_Movies_With_Cast.xlsx** (7.4 MB) - Enriched dataset with cast information
4. **Unstructured_870_Movies.txt** (630 KB) - Natural language format
5. **Unstructured_870_Movies_v2.txt** (688 KB) - Improved unstructured format

### Scripts
1. **sample_movies.py** - Random sampling script
2. **merge_cast.py** - Cast information merger
3. **create_text_file.py** - Unstructured format generator

### Analysis
- **Adversarial_10_Records_Review.txt** (688 KB) - Quality validation results

---

## Methodology

### 1. Data Sampling
- Sample Size: 870 movies
- Sampling Method: Random stratified sampling
- Criteria: Diverse genres, release years, ratings

### 2. Data Enrichment
- Merged cast and crew information
- Added production details
- Enriched with financial data (budget, revenue)

### 3. Format Generation
Structured Formats:
- CSV for database import
- Excel for human review

Unstructured Formats:
- Natural language descriptions
- Narrative style text for LLM testing

---

## Results

### Dataset Statistics
- Total Movies: 870 records
- Format Coverage: 100% (all movies in all formats)
- Data Quality: Validated through adversarial review
- Missing Data: Less than 5% across all fields

### Key Achievements
- Successfully sampled representative subset  
- Maintained referential integrity across formats  
- Generated multiple test formats  
- Validated data quality  
- Created reusable sampling scripts  

---

## File Structure

```
Sprint 1/
├── README.md (this file)
├── Sampled_870_Movies.csv
├── Sampled_870_Movies.xlsx
├── Final_Movies_With_Cast.xlsx
├── Unstructured_870_Movies.txt
├── Unstructured_870_Movies_v2.txt
├── Adversarial_10_Records_Review.txt
├── sample_movies.py
├── merge_cast.py
├── create_text_file.py
├── unstructured_output.txt
├── Response.md
└── Individual_Work_Report_Nishit_Suthar_Sprint 1.docx
```

---

## Key Learnings

1. Sampling Strategy: Random sampling maintains dataset characteristics
2. Format Diversity: Multiple formats essential for comprehensive LLM testing
3. Data Quality: Validation crucial before benchmark testing
4. Referential Integrity: Cast merging requires careful handling
5. Unstructured Generation: Natural language format most challenging

---

## Next Steps

Sprint 1 data serves as foundation for:
- Sprint 2: LLM benchmark testing on structured data
- Sprint 3: Advanced RAG testing on unstructured documents
- Future: Expansion to larger datasets
