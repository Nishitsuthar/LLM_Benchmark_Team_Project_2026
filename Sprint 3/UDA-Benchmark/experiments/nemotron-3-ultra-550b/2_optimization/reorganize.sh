#!/bin/bash
# Reorganize 2_optimization directory for better organization

BASE="/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark/experiments/nemotron-3-ultra-550b/2_optimization"

cd "$BASE"

echo "================================"
echo "REORGANIZING 2_OPTIMIZATION/"
echo "================================"
echo ""

# Create new directory structure
echo "Creating organized directory structure..."
mkdir -p notebooks/topk10_only
mkdir -p notebooks/topk10_chunk1500
mkdir -p notebooks/topk10_temp03
mkdir -p documentation/guides
mkdir -p documentation/reports
mkdir -p documentation/archived
mkdir -p analysis_scripts
mkdir -p summaries

echo "✓ Directories created"
echo ""

# Move notebooks
echo "Moving notebooks..."
mv fetatab_topk10_experiment.ipynb notebooks/topk10_only/
mv finhybrid_topk10_experiment.ipynb notebooks/topk10_only/
mv nqtext_topk10_experiment.ipynb notebooks/topk10_only/
mv papertab_topk10_experiment.ipynb notebooks/topk10_only/
mv papertext_topk10_experiment.ipynb notebooks/topk10_only/
mv tathybrid_topk10_experiment.ipynb notebooks/topk10_only/

mv fetatab_topk10_chunk1500_experiment.ipynb notebooks/topk10_chunk1500/
mv finhybrid_topk10_chunk1500_experiment.ipynb notebooks/topk10_chunk1500/
mv papertab_topk10_chunk1500_experiment.ipynb notebooks/topk10_chunk1500/
mv tathybrid_topk10_chunk1500_experiment.ipynb notebooks/topk10_chunk1500/

mv finhybrid_topk10_temp03_experiment.ipynb notebooks/topk10_temp03/

echo "✓ Notebooks moved"
echo ""

# Move analysis scripts
echo "Moving analysis scripts..."
mv analyze_all_topk10_results.py analysis_scripts/
mv analyze_combined_optimizations.py analysis_scripts/
mv analyze_complete_results.py analysis_scripts/
mv create_combined_optimizations.py analysis_scripts/

echo "✓ Analysis scripts moved"
echo ""

# Move summaries
echo "Moving summary CSVs..."
mv TOPK10_COMPLETE_SUMMARY.csv summaries/
mv COMBINED_OPTIMIZATION_SUMMARY.csv summaries/
mv COMPLETE_OPTIMIZATION_SUMMARY_ALL_6_DATASETS.csv summaries/

echo "✓ Summaries moved"
echo ""

# Move reports
echo "Moving final reports..."
mv COMPLETE_FINAL_REPORT_ALL_DATASETS.md documentation/reports/
mv COMPLETE_TOPK10_FINAL_REPORT.md documentation/reports/
mv COMBINED_OPTIMIZATION_FINAL_REPORT.md documentation/reports/
mv COMPREHENSIVE_RESULTS_TOPK10.md documentation/reports/
mv RESULTS_ANALYSIS_TOPK10.md documentation/reports/

echo "✓ Reports moved"
echo ""

# Move guides
echo "Moving guides..."
mv PHASE3_COMPLETE_ROADMAP.md documentation/guides/
mv COMBINED_OPTIMIZATION_GUIDE.md documentation/guides/

echo "✓ Guides moved"
echo ""

# Move archived documentation
echo "Moving archived documentation..."
mv ISSUE_FIXED.md documentation/archived/
mv OPTION2_GUIDE.md documentation/archived/
mv READY_TO_RUN.md documentation/archived/
mv READY_TO_RUN_REMAINING.md documentation/archived/
mv RUN_TOPK10_REMAINING.md documentation/archived/
mv WHICH_CELL_OPTIMIZES.md documentation/archived/

echo "✓ Archived docs moved"
echo ""

echo "================================"
echo "REORGANIZATION COMPLETE!"
echo "================================"
