#!/usr/bin/env python3
import sys
print("Python executable:", sys.executable)
print("Python version:", sys.version)
print("\nTrying imports...")

try:
    import pandas as pd
    print("✓ pandas:", pd.__version__)
    import chromadb
    print("✓ chromadb:", chromadb.__version__)
    import PyPDF2
    print("✓ PyPDF2:", PyPDF2.__version__)
    from together import Together
    print("✓ together: OK")
    print("\n✅ All imports successful!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
