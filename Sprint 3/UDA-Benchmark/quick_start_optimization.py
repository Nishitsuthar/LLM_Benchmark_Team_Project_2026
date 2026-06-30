#!/usr/bin/env python3
"""
Quick Start: Create your first optimization experiment
This script copies a baseline notebook and modifies it for parameter testing
"""

import json
import sys
import os
from pathlib import Path
import shutil

# Paths
BASE_DIR = Path("/Users/I772947/personal work/LLM Benchmark Team Project/LLM_Benchmark_Team_Project_2026/Sprint 3/UDA-Benchmark")
BASELINE_DIR = BASE_DIR / "experiments/nemotron-3-ultra-550b/1_without_optimization"
OPTIMIZATION_DIR = BASE_DIR / "experiments/nemotron-3-ultra-550b/2_optimization"

# Available datasets
DATASETS = ["tathybrid", "finhybrid", "nqtext", "fetatab", "papertext", "papertab"]

# Optimization presets
OPTIMIZATIONS = {
    "topk10": {"TOP_K": 10, "description": "Increase retrieval to 10 chunks (from 5)"},
    "topk15": {"TOP_K": 15, "description": "Increase retrieval to 15 chunks (from 5)"},
    "chunk1500": {"CHUNK_SIZE": 1500, "CHUNK_OVERLAP": 150, "description": "Smaller chunks for precision (from 3000)"},
    "chunk4500": {"CHUNK_SIZE": 4500, "CHUNK_OVERLAP": 450, "description": "Larger chunks for context (from 3000)"},
    "temp03": {"TEMPERATURE": 0.3, "description": "Higher temperature for less conservatism (from 0.1)"},
    "temp00": {"TEMPERATURE": 0.0, "description": "Zero temperature for maximum determinism (from 0.1)"},
}


def create_optimization_notebook(dataset, optimization_name):
    """
    Copy baseline notebook and modify parameters for optimization.

    Args:
        dataset: Dataset name (e.g., 'finhybrid')
        optimization_name: Optimization preset (e.g., 'topk10')
    """

    # Validate inputs
    if dataset not in DATASETS:
        print(f"❌ Error: Dataset '{dataset}' not found.")
        print(f"   Available: {', '.join(DATASETS)}")
        return False

    if optimization_name not in OPTIMIZATIONS:
        print(f"❌ Error: Optimization '{optimization_name}' not found.")
        print(f"   Available: {', '.join(OPTIMIZATIONS.keys())}")
        return False

    # Paths
    source_nb = BASELINE_DIR / dataset / f"{dataset}_experiment.ipynb"
    target_nb = OPTIMIZATION_DIR / f"{dataset}_{optimization_name}_experiment.ipynb"

    if not source_nb.exists():
        print(f"❌ Error: Source notebook not found: {source_nb}")
        return False

    # Create optimization directory if needed
    OPTIMIZATION_DIR.mkdir(parents=True, exist_ok=True)

    # Load optimization config
    opt_config = OPTIMIZATIONS[optimization_name]

    print(f"\n{'='*70}")
    print(f"📓 Creating Optimization Notebook")
    print(f"{'='*70}")
    print(f"Dataset:      {dataset}")
    print(f"Optimization: {optimization_name}")
    print(f"Description:  {opt_config['description']}")
    print(f"Source:       {source_nb.name}")
    print(f"Target:       {target_nb.name}")
    print()

    # Load source notebook
    with open(source_nb, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    # Modify parameters cell
    changes_made = 0
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') != 'code':
            continue

        source = cell.get('source', [])
        if not source:
            continue

        source_text = ''.join(source)
        original_text = source_text

        # Update parameters
        for param, value in opt_config.items():
            if param == "description":
                continue

            # Find and replace parameter
            if f"{param} = " in source_text:
                import re
                pattern = rf"{param}\s*=\s*\d+\.?\d*"
                replacement = f"{param} = {value}"
                source_text = re.sub(pattern, replacement, source_text)

                if source_text != original_text:
                    print(f"  ✓ Updated {param}: {value}")
                    changes_made += 1
                    original_text = source_text

        # Update OUTPUT_DIR to optimization directory
        old_output_pattern = f"./experiments/nemotron-3-ultra-550b/1_without_optimization/{dataset}/results"
        new_output_pattern = f"./experiments/nemotron-3-ultra-550b/2_optimization/results/{dataset}_{optimization_name}"

        if old_output_pattern in source_text:
            source_text = source_text.replace(old_output_pattern, new_output_pattern)
            print(f"  ✓ Updated OUTPUT_DIR to optimization folder")
            changes_made += 1

        # Update cell if changed
        if source_text != ''.join(source):
            cell['source'] = source_text.splitlines(keepends=True)

    # Save modified notebook
    with open(target_nb, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)

    print()
    print(f"{'='*70}")
    print(f"✅ Notebook created successfully!")
    print(f"{'='*70}")
    print(f"Changes made: {changes_made}")
    print(f"Saved to:     {target_nb}")
    print()
    print(f"🚀 To run the experiment:")
    print(f"   cd {OPTIMIZATION_DIR}")
    print(f"   jupyter notebook {target_nb.name}")
    print()
    print(f"📊 Compare results:")
    print(f"   Baseline:  {BASELINE_DIR}/{dataset}/results/")
    print(f"   Optimized: {OPTIMIZATION_DIR}/results/{dataset}_{optimization_name}/")
    print()

    return True


def show_menu():
    """Interactive menu for creating optimization notebooks."""

    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║                                                                      ║")
    print("║  🚀 Quick Start: Phase 2 Optimization Experiment Generator           ║")
    print("║                                                                      ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()

    # Step 1: Choose dataset
    print("📁 Step 1: Choose a dataset")
    print()
    recommended = {
        "finhybrid": "Worst empty rate (40.4%) - best for testing TOP_K",
        "tathybrid": "Good performance (43.5%) - best for testing CHUNK_SIZE",
        "nqtext": "Moderate (27.6%) - good for general testing"
    }

    for i, dataset in enumerate(DATASETS, 1):
        marker = "⭐" if dataset in recommended else "  "
        rec_text = f" - {recommended[dataset]}" if dataset in recommended else ""
        print(f"{marker} {i}. {dataset}{rec_text}")

    print()
    dataset_choice = input("Enter dataset number or name: ").strip().lower()

    # Parse choice
    if dataset_choice.isdigit():
        idx = int(dataset_choice) - 1
        if 0 <= idx < len(DATASETS):
            dataset = DATASETS[idx]
        else:
            print("❌ Invalid number")
            return
    elif dataset_choice in DATASETS:
        dataset = dataset_choice
    else:
        print("❌ Invalid dataset")
        return

    print(f"✓ Selected: {dataset}")
    print()

    # Step 2: Choose optimization
    print("🔧 Step 2: Choose optimization")
    print()

    recommended_opts = {
        "finhybrid": ["topk10", "topk15"],
        "tathybrid": ["chunk1500", "topk10"],
        "nqtext": ["topk10", "temp03"]
    }

    opts_list = list(OPTIMIZATIONS.keys())
    for i, opt_name in enumerate(opts_list, 1):
        opt_config = OPTIMIZATIONS[opt_name]
        marker = "⭐" if opt_name in recommended_opts.get(dataset, []) else "  "
        print(f"{marker} {i}. {opt_name:12} - {opt_config['description']}")

    print()
    opt_choice = input("Enter optimization number or name: ").strip().lower()

    # Parse choice
    if opt_choice.isdigit():
        idx = int(opt_choice) - 1
        if 0 <= idx < len(opts_list):
            optimization = opts_list[idx]
        else:
            print("❌ Invalid number")
            return
    elif opt_choice in OPTIMIZATIONS:
        optimization = opt_choice
    else:
        print("❌ Invalid optimization")
        return

    print(f"✓ Selected: {optimization}")
    print()

    # Confirm and create
    print("=" * 70)
    print(f"Ready to create: {dataset}_{optimization}_experiment.ipynb")
    print("=" * 70)
    confirm = input("Create notebook? [Y/n]: ").strip().lower()

    if confirm in ['', 'y', 'yes']:
        create_optimization_notebook(dataset, optimization)
    else:
        print("Cancelled.")


def show_recommendations():
    """Show recommended first experiments."""

    print("\n" + "="*70)
    print("💡 RECOMMENDED FIRST EXPERIMENTS")
    print("="*70)
    print()

    print("🎯 Best First Experiment (Highest Impact, Lowest Cost):")
    print("   Dataset:      finhybrid")
    print("   Optimization: topk10")
    print("   Why:          Worst empty rate (40.4%), likely to show big improvement")
    print("   Expected:     Empty rate drops from 40% → ~30%, score +2-5%")
    print("   Time:         15-20 minutes")
    print("   Cost:         $3-5")
    print()
    print("   Run:")
    print("   python3 quick_start_optimization.py finhybrid topk10")
    print()

    print("🎯 Second Experiment (Table Extraction):")
    print("   Dataset:      tathybrid")
    print("   Optimization: chunk1500")
    print("   Why:          Better table extraction with smaller chunks")
    print("   Expected:     Score improves from 43.5% → ~47%, empty ~20%")
    print("   Time:         60-90 minutes")
    print("   Cost:         $13-20")
    print()
    print("   Run:")
    print("   python3 quick_start_optimization.py tathybrid chunk1500")
    print()

    print("🎯 Third Experiment (Combined):")
    print("   Dataset:      finhybrid")
    print("   Optimization: topk15")
    print("   Why:          Even better retrieval coverage")
    print("   Expected:     Further improvement on already optimized TOP_K=10")
    print("   Time:         15-20 minutes")
    print("   Cost:         $3-5")
    print()
    print("   Run:")
    print("   python3 quick_start_optimization.py finhybrid topk15")
    print()


def main():
    """Main entry point."""

    # Parse command line
    if len(sys.argv) == 1:
        # Interactive mode
        show_menu()
    elif len(sys.argv) == 2 and sys.argv[1] in ['--help', '-h', 'help']:
        # Help
        print("\n📖 Usage:")
        print("   python3 quick_start_optimization.py                    # Interactive mode")
        print("   python3 quick_start_optimization.py <dataset> <opt>    # Direct mode")
        print("   python3 quick_start_optimization.py --recommendations  # Show recommended experiments")
        print()
        print("Examples:")
        print("   python3 quick_start_optimization.py finhybrid topk10")
        print("   python3 quick_start_optimization.py tathybrid chunk1500")
        print()
    elif len(sys.argv) == 2 and sys.argv[1] in ['--recommendations', '-r', 'rec']:
        # Show recommendations
        show_recommendations()
    elif len(sys.argv) == 3:
        # Direct mode
        dataset = sys.argv[1]
        optimization = sys.argv[2]
        create_optimization_notebook(dataset, optimization)
    else:
        print("❌ Invalid arguments. Use --help for usage.")


if __name__ == "__main__":
    main()
