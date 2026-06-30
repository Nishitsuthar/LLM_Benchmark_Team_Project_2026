"""
Fix corrupted processing loop cell in all Phase 3C notebooks
"""
import json
import glob

CORRECT_CELL_SOURCE = """all_results = []

for doc_name, doc_qas in qas_dict.items():
    print(f"\\n{'='*80}")
    print(f"Processing: {doc_name}")
    print(f"{'='*80}")

    # Get PDF path
    pdf_path = preprocess.get_example_pdf_path(DATASET_NAME, doc_name)
    if not pdf_path:
        print(f"❌ PDF not found - skipping")
        continue

    print(f"PDF: {pdf_path}")

    # Extract and chunk
    print("Extracting text...")
    pdf_text = extract_pdf_text(pdf_path)
    text_chunks = text_splitter.split_text(pdf_text)
    print(f"Created {len(text_chunks)} chunks")

    # Build index
    print("Building vector index...")
    collection = build_index(text_chunks, collection_name=f"{DATASET_NAME}_{re.sub(r'[^a-zA-Z0-9._-]', '_', doc_name)}")
    print("✓ Index built")

    # Process questions
    print(f"\\nAnswering {len(doc_qas)} questions...")

    for idx, qa in enumerate(doc_qas, 1):
        question = qa["question"]
        print(f"\\n[{idx}/{len(doc_qas)}] {question[:70]}...")

        try:
            answer = answer_question(collection, question)
            print(f"   Answer: {answer[:80]}...")

            all_results.append({
                "question": question,
                "response": answer,
                "doc": doc_name,
                "q_uid": qa["q_uid"],
                "answers": qa["answers"],
                "dataset": DATASET_NAME,
                "prompt_type": PROMPT_TYPE,
            })

            time.sleep(0.5)

        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue

    print(f"\\n✓ Completed {doc_name}")

print(f"\\n{'='*80}")
print(f"ALL DOCUMENTS PROCESSED")
print(f"{'='*80}")
print(f"Total Q&A processed: {len(all_results)}")"""

# Find notebooks that need fixing
notebooks = [
    "experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/nqtext_cot_experiment.ipynb",
    "experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/nqtext_fewshot_experiment.ipynb",
    "experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/fetatab_fewshot_experiment.ipynb",
    "experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/papertab_cot_experiment.ipynb",
    "experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/papertab_fewshot_experiment.ipynb",
    "experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/papertext_cot_experiment.ipynb",
    "experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks/papertext_fewshot_experiment.ipynb",
]

print(f"Fixing {len(notebooks)} notebooks...")

for nb_path in notebooks:
    print(f"\nProcessing: {nb_path}")

    try:
        with open(nb_path, 'r') as f:
            nb = json.load(f)

        fixed = False

        for cell in nb['cells']:
            if cell['cell_type'] == 'code' and cell.get('id') == 'cell-14':
                # Check if it's corrupted (all on one line)
                source = cell['source'] if isinstance(cell['source'], str) else ''.join(cell['source'])

                if 'all_results = []for doc_name' in source or len(source.split('\n')) < 10:
                    print(f"  Found corrupted cell-14, fixing...")
                    cell['source'] = CORRECT_CELL_SOURCE
                    fixed = True
                    break

        if fixed:
            with open(nb_path, 'w') as f:
                json.dump(nb, f, indent=2)
            print(f"  ✅ Fixed and saved")
        else:
            print(f"  ⏭️  Already OK or not found")

    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n✅ All notebooks processed!")
