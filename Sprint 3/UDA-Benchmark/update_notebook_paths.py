#!/usr/bin/env python3
"""
Update all notebook paths to reflect new directory structure:
experiments/{dataset}/ -> experiments/nemotron-3-ultra-550b/1_without_optimization/{dataset}/

This updates:
1. project_root path (../..) -> (../../../../)
2. OUTPUT_DIR paths
3. CSV file paths in results_analysis notebook
"""

import json
import os
import re
from pathlib import Path

# Base directory
BASE_DIR = Path("/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark")
EXPERIMENTS_DIR = BASE_DIR / "experiments/nemotron-3-ultra-550b/1_without_optimization"

# Dataset notebooks
DATASET_NOTEBOOKS = {
    "tathybrid": EXPERIMENTS_DIR / "tathybrid/tathybrid_experiment.ipynb",
    "finhybrid": EXPERIMENTS_DIR / "finhybrid/finhybrid_experiment.ipynb",
    "nqtext": EXPERIMENTS_DIR / "nqtext/nqtext_experiment.ipynb",
    "fetatab": EXPERIMENTS_DIR / "fetatab/fetatab_experiment.ipynb",
    "papertext": EXPERIMENTS_DIR / "papertext/papertext_experiment.ipynb",
    "papertab": EXPERIMENTS_DIR / "papertab/papertab_experiment.ipynb",
}

# Results analysis notebook
RESULTS_NOTEBOOK = EXPERIMENTS_DIR / "results_analysis/sprint3_results_visualization.ipynb"


def update_dataset_notebook(notebook_path, dataset_name):
    """Update paths in a dataset experiment notebook."""
    print(f"\n📓 Updating {dataset_name} notebook...")

    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    changes = 0

    for cell in notebook.get('cells', []):
        if cell.get('cell_type') != 'code':
            continue

        source = cell.get('source', [])
        if not source:
            continue

        # Join source lines
        source_text = ''.join(source)
        original_text = source_text

        # Update 1: project_root path from ../.. to ../../../..
        if "project_root = os.path.abspath(" in source_text:
            source_text = re.sub(
                r"project_root = os\.path\.abspath\(['\"]\.\.\/\.\.['\"]",
                "project_root = os.path.abspath('../../../..'",
                source_text
            )
            if source_text != original_text:
                print(f"  ✓ Updated project_root path")
                changes += 1
                original_text = source_text

        # Update 2: OUTPUT_DIR path
        old_output_path = f"./experiments/{dataset_name}/results"
        new_output_path = f"./experiments/nemotron-3-ultra-550b/1_without_optimization/{dataset_name}/results"

        if old_output_path in source_text:
            source_text = source_text.replace(old_output_path, new_output_path)
            if source_text != original_text:
                print(f"  ✓ Updated OUTPUT_DIR path")
                changes += 1
                original_text = source_text

        # Update cell source if changed
        if source_text != ''.join(source):
            cell['source'] = source_text.splitlines(keepends=True)

    # Save updated notebook
    if changes > 0:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)
        print(f"  ✅ Saved {changes} changes")
    else:
        print(f"  ℹ️  No changes needed")

    return changes


def update_results_notebook(notebook_path):
    """Update paths in the results analysis notebook."""
    print(f"\n📊 Updating results_analysis notebook...")

    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    changes = 0

    for cell in notebook.get('cells', []):
        if cell.get('cell_type') != 'code':
            continue

        source = cell.get('source', [])
        if not source:
            continue

        source_text = ''.join(source)
        original_text = source_text

        # Update result file paths
        # Old: "../{dataset}/results/{dataset}_results_*.csv"
        # New: "../{dataset}/results/{dataset}_results_*.csv" (relative paths stay same since we're in same structure)

        # Actually, the relative paths from results_analysis to dataset folders remain the same!
        # results_analysis/../tathybrid/results/ still works

        # But if there are any absolute references, we should check
        if "experiments/" in source_text and "results_analysis" not in source_text:
            # Check for patterns like: experiments/tathybrid/results/
            pattern = r'experiments/([a-z]+)/results/'
            if re.search(pattern, source_text):
                source_text = re.sub(
                    pattern,
                    r'experiments/nemotron-3-ultra-550b/1_without_optimization/\1/results/',
                    source_text
                )
                if source_text != original_text:
                    print(f"  ✓ Updated result file paths")
                    changes += 1

        # Update cell source if changed
        if source_text != ''.join(source):
            cell['source'] = source_text.splitlines(keepends=True)

    # Save updated notebook
    if changes > 0:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)
        print(f"  ✅ Saved {changes} changes")
    else:
        print(f"  ℹ️  No changes needed (relative paths still work)")

    return changes


def main():
    print("=" * 70)
    print("🔧 Updating Notebook Paths for New Directory Structure")
    print("=" * 70)

    total_changes = 0

    # Update dataset notebooks
    print("\n📁 Dataset Experiment Notebooks:")
    for dataset_name, notebook_path in DATASET_NOTEBOOKS.items():
        if notebook_path.exists():
            changes = update_dataset_notebook(notebook_path, dataset_name)
            total_changes += changes
        else:
            print(f"\n⚠️  {dataset_name} notebook not found: {notebook_path}")

    # Update results notebook
    print("\n📁 Results Analysis Notebook:")
    if RESULTS_NOTEBOOK.exists():
        changes = update_results_notebook(RESULTS_NOTEBOOK)
        total_changes += changes
    else:
        print(f"\n⚠️  Results notebook not found: {RESULTS_NOTEBOOK}")

    # Summary
    print("\n" + "=" * 70)
    print(f"✅ Complete! Total changes: {total_changes}")
    print("=" * 70)

    print("\n📋 New Directory Structure:")
    print("experiments/")
    print("└── nemotron-3-ultra-550b/")
    print("    ├── 1_without_optimization/  ← All current work moved here")
    print("    │   ├── tathybrid/")
    print("    │   ├── finhybrid/")
    print("    │   ├── nqtext/")
    print("    │   ├── fetatab/")
    print("    │   ├── papertext/")
    print("    │   ├── papertab/")
    print("    │   └── results_analysis/")
    print("    └── 2_optimization/          ← Ready for Phase 2 work")
    print()


if __name__ == "__main__":
    main()
