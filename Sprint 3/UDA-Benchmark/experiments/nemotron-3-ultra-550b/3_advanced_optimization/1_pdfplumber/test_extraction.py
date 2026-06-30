"""
Test pdfplumber vs PyPDF2 extraction quality on sample PDFs.

Run this BEFORE creating full notebooks to verify improvement.

Usage:
    python3 test_extraction.py
"""

import sys
from pathlib import Path

# Add project root to path
script_dir = Path(__file__).parent
project_root = script_dir.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

print(f"Project root: {project_root}")
print(f"Looking for uda module at: {project_root / 'uda'}")

from uda.utils.pdf_extraction import extract_text_pdfplumber, extract_text_pypdf2

# Sample PDF paths (relative to project root)
SAMPLE_PDFS = [
    "dataset/src_doc_files_example/fin_docs/JKHY_2015.pdf",
    "dataset/src_doc_files_example/tat_docs/lifeway-foods-inc_2019.pdf",
]


def compare_extraction(pdf_path: str):
    """Compare PyPDF2 vs pdfplumber on one PDF."""
    print(f"\n{'='*80}")
    print(f"TESTING: {Path(pdf_path).name}")
    print(f"{'='*80}\n")

    full_path = project_root / pdf_path

    if not full_path.exists():
        print(f"⚠️  PDF not found: {pdf_path}")
        return

    # PyPDF2 extraction
    print("🔴 PyPDF2 Extraction (First 800 chars)")
    print("-"*80)
    try:
        pypdf2_text = extract_text_pypdf2(str(full_path))
        print(pypdf2_text[:800])
        print(f"\n📊 Total length: {len(pypdf2_text):,} characters")
        print(f"📊 Lines: {len(pypdf2_text.splitlines()):,}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

    print(f"\n{'-'*80}\n")

    # pdfplumber extraction
    print("🟢 pdfplumber Extraction (First 800 chars)")
    print("-"*80)
    try:
        pdfplumber_text = extract_text_pdfplumber(str(full_path))
        print(pdfplumber_text[:800])
        print(f"\n📊 Total length: {len(pdfplumber_text):,} characters")
        print(f"📊 Lines: {len(pdfplumber_text.splitlines()):,}")

        # Show table detection
        table_count = pdfplumber_text.count("[TABLE")
        print(f"📊 Tables detected: {table_count}")

    except Exception as e:
        print(f"❌ ERROR: {e}")

    print(f"\n{'='*80}\n")

    # Quick comparison
    try:
        diff_length = len(pdfplumber_text) - len(pypdf2_text)
        diff_pct = (diff_length / len(pypdf2_text)) * 100 if len(pypdf2_text) > 0 else 0

        print("📈 COMPARISON SUMMARY:")
        print(f"   Length difference: {diff_length:+,} characters ({diff_pct:+.1f}%)")

        if table_count > 0:
            print(f"   ✅ pdfplumber detected {table_count} tables (better structure)")
        else:
            print(f"   ℹ️  No tables detected (text-only document)")

        print()

    except:
        pass


def main():
    print("\n" + "="*80)
    print("📋 PDF EXTRACTION COMPARISON TEST")
    print("="*80)
    print("\nComparing PyPDF2 (Phase 1-2) vs pdfplumber (Phase 3A)")
    print("\n🎯 Look for:")
    print("   ✅ Tables with | separators (pdfplumber)")
    print("   ✅ Better number formatting (pdfplumber)")
    print("   ✅ Clear row/column structure (pdfplumber)")
    print("   ❌ Scrambled numbers (PyPDF2)")
    print("   ❌ Poor spacing (PyPDF2)")

    for pdf_path in SAMPLE_PDFS:
        compare_extraction(pdf_path)

    print("="*80)
    print("✅ TEST COMPLETE!")
    print("\nIf pdfplumber shows better table structure, proceed with Phase 3A.")
    print("Next step: Create test notebook for TatHybrid")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
