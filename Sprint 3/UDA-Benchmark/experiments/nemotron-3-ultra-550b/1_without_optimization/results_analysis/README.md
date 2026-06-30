# Sprint 3 Results Analysis

**Model:** NVIDIA Nemotron-3 Ultra 550B (via Together AI)  
**Date:** 2026-06-29  
**Purpose:** Comprehensive visualization and comparison of all 6 UDA-Benchmark datasets

---

## 📊 Quick Access

### Main Notebook:
- **`sprint3_results_visualization.ipynb`** - Complete analysis with all visualizations

### Generated Outputs:
After running the notebook, you'll get:
1. **`performance_comparison.png`** - Side-by-side score and empty rate comparison
2. **`domain_comparison.png`** - Domain-level statistics (Finance, Wikipedia, Academic)
3. **`score_vs_empty_scatter.png`** - Correlation analysis
4. **`document_level_analysis.png`** - Per-document breakdown for all datasets
5. **`sprint3_results_summary.csv`** - Complete dataset statistics table
6. **`sprint3_domain_summary.csv`** - Domain-aggregated statistics

---

## 📁 Results Files Used

The notebook loads results from all 6 experiments:

| Dataset | Result File | Q&A | Domain | Metric |
|---------|-------------|-----|--------|--------|
| TatHybrid | `../tathybrid/results/tathybrid_results_20260629_094232.csv` | 162 | Finance | Numeracy F1 |
| FinHybrid | `../finhybrid/results/finhybrid_results_20260629_120808.csv` | 47 | Finance | Exact Match ±1% |
| NqText | `../nqtext/results/nqtext_results_20260629_112238.csv` | 78 | Wikipedia | Span F1 |
| FetaTab | `../fetatab/results/fetatab_results_20260629_120656.csv` | 8 | Wikipedia | Span F1 |
| PaperText | `../papertext/results/papertext_results_20260629_104112.csv` | 13 | Academic | Span F1 |
| PaperTab | `../papertab/results/papertab_results_20260629_103921.csv` | 4 | Academic | Span F1 |

**Total:** 312 Q&A pairs across 6 datasets

---

## 🎯 What This Notebook Analyzes

### 1. Dataset-Level Analysis
- Performance scores (accuracy/F1) for each dataset
- Empty response rates (main bottleneck)
- Q&A coverage and sample sizes
- Response length statistics

### 2. Domain-Level Analysis
- **Finance** (TatHybrid, FinHybrid)
- **Wikipedia** (NqText, FetaTab)
- **Academic** (PaperText, PaperTab)
- Average performance by domain
- Domain-specific challenges

### 3. Correlation Analysis
- Relationship between score and empty rate
- Impact of Q&A count on performance
- Identification of outliers

### 4. Document-Level Breakdown
- Per-document empty rates
- Best and worst performing documents
- Document-specific insights

---

## 🚀 How to Run

### Option 1: Jupyter Notebook
```bash
cd ~/personal\ work/LLM\ Benchmark\ Team\ Project/LLM_Benchmark_Team_Project_2026/Sprint\ 3/UDA-Benchmark/experiments/results_analysis
jupyter notebook sprint3_results_visualization.ipynb
```

Then: **Cell → Run All**

### Option 2: Command Line
```bash
cd ~/personal\ work/LLM\ Benchmark\ Team\ Project/LLM_Benchmark_Team_Project_2026/Sprint\ 3/UDA-Benchmark/experiments/results_analysis
jupyter nbconvert --to notebook --execute sprint3_results_visualization.ipynb
```

---

## 📈 Visualizations Generated

### 1. Performance Comparison (Horizontal Bar Charts)
- **Chart A:** Performance scores by dataset
- **Chart B:** Empty response rates by dataset
- Color-coded: Green (good), Yellow (moderate), Red (poor)

### 2. Domain Comparison (3-Panel Bar Chart)
- **Panel A:** Average score by domain
- **Panel B:** Average empty rate by domain
- **Panel C:** Q&A count by domain

### 3. Score vs Empty Rate (Scatter Plot)
- X-axis: Empty response rate (lower is better)
- Y-axis: Performance score (higher is better)
- Bubble size: Q&A count
- Color: Domain
- Quadrant analysis with best/worst regions marked

### 4. Document-Level Analysis (6-Panel Grid)
- One panel per dataset
- Empty rate for each document within dataset
- Identifies problematic documents

---

## 📊 Key Metrics Explained

### Performance Scores:
- **Numeracy F1** (TatHybrid): Numeracy-aware F1 score, handles numerical values
- **Exact Match ±1%** (FinHybrid): Answer within 1% of ground truth
- **Span F1** (Others): Token-level overlap between prediction and answer

### Empty Response Rate:
- **Definition:** Percentage of questions where model returned empty string
- **Cause:** Retrieval failure, model conservatism, poor PDF extraction
- **Impact:** Empty = 0% accuracy for that question
- **Main Bottleneck:** 10-40% empty rate across datasets

### Response Length:
- Average characters in model responses
- Longer ≠ better (can indicate verbosity)
- Useful for understanding model behavior

---

## 🎓 Expected Findings

Based on completed experiments:

### Best Performers:
1. **TatHybrid** (43.5% Numeracy F1) - Finance with specialized metric
2. **PaperText** (~43% Span F1) - Academic text comprehension
3. **PaperTab** (~38% Span F1) - Academic table extraction

### Challenging Datasets:
1. **FinHybrid** (23.4% Exact Match) - Strict financial calculations
2. **NqText** (27.6% Span F1) - General Wikipedia knowledge

### Empty Rate Patterns:
- **Best:** PaperText (7.7%) - Clean structured PDFs
- **Good:** NqText (14.1%) - Well-written articles
- **Moderate:** TatHybrid (22.8%) - Financial tables
- **Challenging:** FinHybrid (40.4%) - Complex financial documents

### Domain Insights:
- **Finance:** Numeracy-aware metrics help significantly
- **Academic:** Best retrieval quality (structured PDFs)
- **Wikipedia:** Variable performance by topic

---

## 💡 Use Cases

### For Research:
- Compare RAG performance across domains
- Analyze impact of PDF quality on retrieval
- Understand relationship between empty rate and accuracy
- Identify which document types work best

### For Development:
- Identify datasets that need optimization
- Guide parameter tuning (prioritize high-empty datasets)
- Understand which domains to focus on
- Compare different metrics and their applicability

### For Reporting:
- Publication-ready visualizations
- Comprehensive statistics tables
- Domain-level aggregations
- Easy-to-understand charts

---

## 🔧 Customization

### To Update Result Files:
1. Edit the `result_files` dictionary in Cell 3
2. Update timestamps to latest results
3. Re-run notebook

### To Add New Metrics:
1. Update the `metrics` dictionary in Cell 4
2. Add manual scores from evaluation output
3. Re-run summary calculations

### To Change Visualizations:
- Modify matplotlib/seaborn code in visualization cells
- Adjust colors, sizes, layouts as needed
- Update labels and titles

### To Export Additional Formats:
```python
# Add to export cell
summary_df.to_excel('sprint3_results.xlsx', index=False)
summary_df.to_json('sprint3_results.json', orient='records')
```

---

## 📦 Dependencies

Required packages (already in environment):
- `pandas` - Data manipulation
- `matplotlib` - Plotting
- `seaborn` - Statistical visualizations
- `numpy` - Numerical operations

Install if needed:
```bash
pip install pandas matplotlib seaborn numpy
```

---

## 🎯 Next Steps After Running

1. **Review Visualizations** - Understand performance patterns
2. **Identify Bottlenecks** - Focus on high-empty datasets
3. **Plan Optimizations** - Parameter tuning, better PDF parsing
4. **Compare with Baselines** - Check paper results (if available)
5. **Document Findings** - Update project documentation

### Potential Optimizations:
- **High Empty Rate?** → Increase TOP_K, reduce CHUNK_SIZE
- **Poor Table Extraction?** → Use pdfplumber instead of PyPDF2
- **Domain-Specific Issues?** → Try domain-specific embeddings
- **Low Overall Score?** → Experiment with prompt engineering

---

## 📝 Example Insights

After running, you might discover:

✅ **"Academic papers have 3x lower empty rate than financial documents"**  
→ Insight: PDF quality matters more than domain complexity

✅ **"TatHybrid with Numeracy F1 scores 43% vs FinHybrid with Exact Match at 23%"**  
→ Insight: Metric choice significantly impacts perceived performance

✅ **"Empty rate correlates inversely with performance (r = -0.65)"**  
→ Insight: Improving retrieval is more important than improving generation

---

## 🔗 Related Files

- **`RESULTS_COMPARISON.md`** - Written summary of first 4 datasets
- **`NEXT_SESSION_HANDOFF.md`** - Session context and findings
- **`../*/results/*.csv`** - Individual experiment results

---

## ✅ Checklist Before Running

- [x] All 6 datasets have result CSV files
- [x] Result file paths in notebook are correct
- [x] Required packages are installed
- [x] Jupyter environment is set up

---

**Created:** 2026-06-29  
**Purpose:** Comprehensive Sprint 3 results visualization and analysis  
**Status:** Ready to run  
**Output:** 6 visualizations + 2 CSV exports
