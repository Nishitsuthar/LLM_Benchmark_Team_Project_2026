#!/bin/bash
# Quick start script - generates data and validates it

echo "======================================================================"
echo "SYNTHETIC DATA GENERATOR - QUICK START"
echo "======================================================================"
echo ""

# Check if dependencies are installed
echo "[Step 1/3] Checking dependencies..."
python3 -c "import pandas, faker, numpy" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "⚠ Dependencies not found. Installing..."
    pip3 install pandas faker numpy scipy
else
    echo "✓ All dependencies installed"
fi

echo ""
echo "[Step 2/3] Generating high-quality synthetic data..."
python3 data_gen_script_enhanced.py

if [ $? -eq 0 ]; then
    echo "✓ Data generation successful!"
else
    echo "✗ Data generation failed. Check errors above."
    exit 1
fi

echo ""
echo "[Step 3/3] Validating data quality..."
python3 compare_data_quality.py --validate

echo ""
echo "======================================================================"
echo "✓ COMPLETE! Your synthetic data is ready."
echo "======================================================================"
echo ""
echo "Generated files:"
ls -lh *.csv 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'
echo ""
echo "Next steps:"
echo "  - Load data into your database"
echo "  - Run analytics queries"
echo "  - Use for development/testing"
echo ""
echo "======================================================================"
