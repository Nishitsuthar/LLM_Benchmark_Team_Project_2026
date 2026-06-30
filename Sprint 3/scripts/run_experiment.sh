#!/bin/bash
# Quick Start Script for UDA-Benchmark Experiments
# Run this to open any experiment notebook

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     UDA-Benchmark Experiments - Quick Start              ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "Available experiments:"
echo ""
echo "  1. FinHybrid     - Financial reports (Exact Match)"
echo "  2. TatHybrid     - Financial reports (Numeracy F1)"
echo "  3. NqText        - Wikipedia factual Q&A"
echo "  4. FetaTab       - Wikipedia tables"
echo "  5. PaperTab      - Academic papers - tables"
echo "  6. PaperText     - Academic papers - text"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if argument provided
if [ $# -eq 0 ]; then
    echo "Usage: ./run_experiment.sh <dataset>"
    echo ""
    echo "Examples:"
    echo "  ./run_experiment.sh finhybrid"
    echo "  ./run_experiment.sh nqtext"
    echo "  ./run_experiment.sh tathybrid"
    echo ""
    exit 1
fi

DATASET=$1
NOTEBOOK_DIR="experiments/${DATASET}"
NOTEBOOK_FILE="${NOTEBOOK_DIR}/${DATASET}_experiment.ipynb"

# Check if experiment exists
if [ ! -d "$NOTEBOOK_DIR" ]; then
    echo "❌ Error: Dataset '${DATASET}' not found!"
    echo ""
    echo "Available datasets:"
    echo "  - finhybrid"
    echo "  - tathybrid"
    echo "  - nqtext"
    echo "  - fetatab"
    echo "  - papertab"
    echo "  - papertext"
    echo ""
    exit 1
fi

if [ ! -f "$NOTEBOOK_FILE" ]; then
    echo "❌ Error: Notebook not found: ${NOTEBOOK_FILE}"
    exit 1
fi

echo "✓ Starting experiment: ${DATASET}"
echo "✓ Notebook: ${NOTEBOOK_FILE}"
echo ""
echo "Opening Jupyter notebook..."
echo ""

cd "$NOTEBOOK_DIR" && jupyter notebook "${DATASET}_experiment.ipynb"
