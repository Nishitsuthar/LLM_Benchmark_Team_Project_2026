#!/usr/bin/env python3
"""
Master Pipeline: Create Sample + Convert to All Formats
Runs both steps automatically
"""

import subprocess
import sys
from pathlib import Path

def run_script(script_name, step_name):
    """Run a Python script"""
    print("\n" + "="*80)
    print(f"{step_name}")
    print("="*80)

    script_path = Path(__file__).parent / script_name

    try:
        subprocess.run([sys.executable, str(script_path)], check=True)
        print(f"\n✓ {step_name} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {step_name} - FAILED")
        return False

def main():
    print("="*80)
    print("SAMPLED DATASET FORMAT CONVERSION PIPELINE")
    print("="*80)
    print("\nThis will:")
    print("  1. Create balanced sample (~10-15% of data)")
    print("  2. Combine into single CSV (source file)")
    print("  3. Convert to JSON, HTML, XML formats")
    print("\nTarget: Files under 1-2 MB for easy GPT upload")
    print("="*80)

    # Step 1
    if not run_script('create_sample_and_combine.py', 'STEP 1: Sample + Combine'):
        return False

    # Step 2
    if not run_script('convert_to_formats.py', 'STEP 2: Convert Formats'):
        return False

    print("\n" + "="*80)
    print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*80)

    output_dir = Path(__file__).parent.parent.parent / 'dataset_formats'
    print(f"\nAll files ready in: {output_dir}")
    print("\nGenerated files:")
    print("  📄 music_dataset_combined.csv  - Single CSV (source)")
    print("  📄 music_dataset.json          - JSON format")
    print("  📄 music_dataset.html          - HTML format (recommended) ⭐")
    print("  📄 music_dataset.xml           - XML format")

    print("\n⚠️  IMPORTANT: Ground truth answers will be DIFFERENT")
    print("   You'll need to regenerate ground truth for this sample")
    print("\nNext steps:")
    print("  1. Check file sizes (should be under 2 MB)")
    print("  2. Upload to NeonDB (sampled data)")
    print("  3. Re-run 30 SQL queries to get new ground truth")
    print("  4. Then test with GPT 5.2")

    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
