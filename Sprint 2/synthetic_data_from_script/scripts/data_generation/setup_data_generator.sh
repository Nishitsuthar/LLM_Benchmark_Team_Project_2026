#!/bin/bash
# Setup script for synthetic data generation

echo "======================================================================"
echo "SYNTHETIC DATA GENERATOR - SETUP"
echo "======================================================================"

echo ""
echo "[1/3] Checking Python version..."
python3 --version

echo ""
echo "[2/3] Installing required packages..."
echo "This will install: pandas, faker, numpy, scipy"

pip3 install pandas faker numpy scipy

echo ""
echo "[3/3] Verifying installation..."
python3 -c "import pandas, faker, numpy, scipy; print('✓ All packages installed successfully')"

echo ""
echo "======================================================================"
echo "SETUP COMPLETE!"
echo "======================================================================"
echo ""
echo "You can now run:"
echo "  python3 data_gen_script_enhanced.py    # High-quality version"
echo "  python3 data_gen_advanced.py            # Demo of advanced techniques"
echo "  python3 data_gen_script.py              # Original version"
echo ""
echo "======================================================================"
