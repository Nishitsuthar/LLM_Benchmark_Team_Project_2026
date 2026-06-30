#!/usr/bin/env python3
"""
Update Phase 3C notebooks with correct Phase 2 document lists.
"""

import json
import sys

def update_notebook_cell(notebook_path, cell_id_pattern, new_docs_list, dataset_name):
    """Update AVAILABLE_DOCS in a notebook cell"""

    with open(notebook_path, 'r') as f:
        nb = json.load(f)

    updated = False
    for cell in nb['cells']:
        cell_id = cell.get('id', '')
        source = ''.join(cell.get('source', []))

        # Look for cell with AVAILABLE_DOCS
        if 'AVAILABLE_DOCS' in source and dataset_name in source.lower():
            print(f"  Found AVAILABLE_DOCS in cell {cell_id}")

            # Build new source
            new_source = f"""# Load Q&A
csv_file = "./dataset/qa/{dataset_name}_qa.csv"
df = pd.read_csv(csv_file, sep="|", na_filter=False, dtype={{"doc_name": str}})
qas_dict_all = preprocess.qa_df_to_dict(DATASET_NAME, df)

# Filter to documents with available PDFs - PHASE 2 DOCUMENT LIST
AVAILABLE_DOCS = [
{new_docs_list}
]

qas_dict = {{doc: qas for doc, qas in qas_dict_all.items() if doc in AVAILABLE_DOCS}}

print(f"Total documents in CSV: {{len(qas_dict_all)}}")
print(f"Available PDFs: {{len(AVAILABLE_DOCS)}}")
print(f"\\nFiltered to documents with PDFs:\\n")

total_qa = 0
for doc in AVAILABLE_DOCS:
    if doc in qas_dict:
        count = len(qas_dict[doc])
        total_qa += count
        print(f"  {{doc}}: {{count}} Q&A pairs")

print(f"\\nTotal Q&A to process: {{total_qa}}")"""

            cell['source'] = [new_source + '\n']
            updated = True
            break

    if updated:
        with open(notebook_path, 'w') as f:
            json.dump(nb, f, indent=1)
        return True
    return False

# NqText notebooks (2)
nqtext_docs = '''    "2018 Tour de France",
    "Hannah John-Kamen",
    "Oklahoma",  # ADDED: Phase 2 included this (7 Q&A)
    "Supreme Court of the United States"'''

for notebook in ['nqtext_cot_experiment.ipynb', 'nqtext_fewshot_experiment.ipynb']:
    path = f'experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/{notebook}'
    print(f"\nUpdating {notebook}...")
    if update_notebook_cell(path, 'AVAILABLE_DOCS', nqtext_docs, 'nq'):
        print(f"  ✅ Updated successfully")
    else:
        print(f"  ❌ Failed to update")

# FetaTab notebooks (2)
fetatab_docs = '''    "Ben Platt (actor)",
    "Jennifer Jones",  # ADDED: Phase 2 included this (1 Q&A)
    "List of French monarchs",
    "Smallville"  # ADDED: Phase 2 included this (1 Q&A)'''

for notebook in ['fetatab_cot_experiment.ipynb', 'fetatab_fewshot_experiment.ipynb']:
    path = f'experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/{notebook}'
    print(f"\nUpdating {notebook}...")
    if update_notebook_cell(path, 'AVAILABLE_DOCS', fetatab_docs, 'feta'):
        print(f"  ✅ Updated successfully")
    else:
        print(f"  ❌ Failed to update")

# PaperText notebooks (2)
papertext_docs = '''    "1705.07830",
    "1801.05147",
    "1809.01202",
    "1810.08699",
    "1909.00754",
    "1912.01214",
    "2001.03131"'''

for notebook in ['papertext_cot_experiment.ipynb', 'papertext_fewshot_experiment.ipynb']:
    path = f'experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/{notebook}'
    print(f"\nUpdating {notebook}...")
    if update_notebook_cell(path, 'AVAILABLE_DOCS', papertext_docs, 'paper_text'):
        print(f"  ✅ Updated successfully")
    else:
        print(f"  ❌ Failed to update")

# PaperTab notebooks (2)
papertab_docs = '''    "1705.07830",
    "1801.05147",
    "1809.01202",
    "1810.08699",
    "1909.00754",
    "1912.01214",
    "2001.03131"'''

for notebook in ['papertab_cot_experiment.ipynb', 'papertab_fewshot_experiment.ipynb']:
    path = f'experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/{notebook}'
    print(f"\nUpdating {notebook}...")
    if update_notebook_cell(path, 'AVAILABLE_DOCS', papertab_docs, 'paper_tab'):
        print(f"  ✅ Updated successfully")
    else:
        print(f"  ❌ Failed to update")

print("\n" + "="*80)
print("All notebooks updated!")
print("="*80)
