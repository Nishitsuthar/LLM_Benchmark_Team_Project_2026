#!/usr/bin/env python3
"""
Fix ChromaDB collection name sanitization in all Phase 3C notebooks.
"""

import json
import os

# The new sanitize function to add
SANITIZE_FUNCTION = '''def sanitize_collection_name(doc_name, dataset_name):
    """
    Sanitize document name for ChromaDB collection.

    ChromaDB requires: 3-512 chars from [a-zA-Z0-9._-],
    starting and ending with alphanumeric.
    """
    # Replace invalid chars with underscore
    safe_name = re.sub(r'[^a-zA-Z0-9._-]', '_', doc_name)
    # Remove consecutive underscores
    safe_name = re.sub(r'_+', '_', safe_name)
    # Remove leading/trailing underscores
    safe_name = safe_name.strip('_')
    # Prepend dataset name
    collection_name = f"{dataset_name}_{safe_name}"
    return collection_name

'''

notebooks_dir = 'experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/'

# All notebooks to fix
notebooks = [
    'fetatab_cot_experiment.ipynb',
    'fetatab_fewshot_experiment.ipynb',
    'nqtext_cot_experiment.ipynb',
    'nqtext_fewshot_experiment.ipynb',
    'papertext_cot_experiment.ipynb',
    'papertext_fewshot_experiment.ipynb',
    'papertab_cot_experiment.ipynb',
    'papertab_fewshot_experiment.ipynb',
]

for notebook_name in notebooks:
    notebook_path = os.path.join(notebooks_dir, notebook_name)
    print(f"\nFixing {notebook_name}...")

    with open(notebook_path, 'r') as f:
        nb = json.load(f)

    fixed = False

    for cell in nb['cells']:
        source = ''.join(cell.get('source', []))

        # Find helper functions cell
        if 'def build_index' in source and 'def extract_pdf_text' in source:
            # Check if sanitize function already exists
            if 'def sanitize_collection_name' in source:
                print(f"  ✓ Already has sanitize function")
                continue

            # Add sanitize function after extract_pdf_text
            lines = source.split('\n')
            new_lines = []
            for i, line in enumerate(lines):
                new_lines.append(line)
                # After extract_pdf_text function ends, add sanitize function
                if line.startswith('def build_index'):
                    # Insert sanitize function before build_index
                    new_lines.insert(-1, SANITIZE_FUNCTION)
                    break
            else:
                # If we didn't find build_index, just append
                new_lines = lines[:]
                # Find where to insert (after extract_pdf_text)
                for i, line in enumerate(lines):
                    if 'return pdf_text' in line:
                        # Insert after this function
                        new_lines = lines[:i+1] + ['\n', SANITIZE_FUNCTION] + lines[i+1:]
                        break

            cell['source'] = ['\n'.join(new_lines) + '\n']
            fixed = True
            print(f"  ✓ Added sanitize function")

        # Find main processing loop cell and update it
        if 'for doc_name, doc_qas in qas_dict.items():' in source:
            # Replace the old collection name generation
            old_pattern = 'collection_name=f"{DATASET_NAME}_{re.sub(r\'[^a-zA-Z0-9._-]\', \'_\', doc_name)}"'
            new_pattern = 'collection_name = sanitize_collection_name(doc_name, DATASET_NAME)\n    collection = build_index(text_chunks, collection_name=collection_name)'

            if old_pattern in source:
                new_source = source.replace(
                    'collection = build_index(text_chunks, collection_name=f"{DATASET_NAME}_{re.sub(r\'[^a-zA-Z0-9._-]\', \'_\', doc_name)}")',
                    new_pattern
                )
                cell['source'] = [new_source + '\n']
                fixed = True
                print(f"  ✓ Updated collection name generation")

    if fixed:
        with open(notebook_path, 'w') as f:
            json.dump(nb, f, indent=1)
        print(f"  ✅ Saved {notebook_name}")
    else:
        print(f"  ⚠️  No changes needed or pattern not found")

print("\n" + "="*80)
print("All notebooks fixed!")
print("="*80)
print("\nYou can now restart the notebook from the beginning:")
print("  Kernel → Restart & Run All")
