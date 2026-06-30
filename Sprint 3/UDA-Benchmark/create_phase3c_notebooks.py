"""
Create Phase 3C notebooks for remaining 4 datasets (both CoT and Few-Shot)
"""
import json
import os
from datetime import datetime

# Dataset configurations from Phase 2 baselines
DATASETS = {
    "nqtext": {
        "name": "nq",
        "display_name": "NqText",
        "description": "Wikipedia Factual Q&A",
        "qa_count": 78,
        "empty_baseline": 6,
        "empty_pct": 7.7,
        "chunk_size": 3000,
        "top_k": 10,
        "metric": "Span F1",
        "available_docs": [
            "Supreme Court of the United States",
            "2018 Tour de France",
            "Hannah John-Kamen"
        ],
        "task_name": "nq"
    },
    "fetatab": {
        "name": "feta",
        "display_name": "FetaTab",
        "description": "Wikipedia Tables",
        "qa_count": 8,
        "empty_baseline": 2,
        "empty_pct": 25.0,
        "chunk_size": 1500,
        "top_k": 10,
        "metric": "Span F1",
        "available_docs": [
            "Ben Platt (actor)",
            "List of French monarchs"
        ],
        "task_name": "feta"
    },
    "papertext": {
        "name": "paper",
        "display_name": "PaperText",
        "description": "Scientific Papers - Text Q&A",
        "qa_count": 13,
        "empty_baseline": 1,
        "empty_pct": 7.7,
        "chunk_size": 3000,
        "top_k": 10,
        "metric": "Span F1",
        "available_docs": [
            "1705.07830",
            "1801.05147"
        ],
        "task_name": "paper"
    },
    "papertab": {
        "name": "paper",
        "display_name": "PaperTab",
        "description": "Scientific Papers - Table Q&A",
        "qa_count": 4,
        "empty_baseline": 0,
        "empty_pct": 0.0,
        "chunk_size": 1500,
        "top_k": 10,
        "metric": "Span F1",
        "available_docs": [
            "1705.07830",
            "1801.05147"
        ],
        "task_name": "paper",
        "csv_file": "./dataset/qa/paper_tab_qa.csv"
    }
}

PROMPT_TYPES = {
    "cot": {
        "display": "Chain-of-Thought",
        "desc": "step-by-step reasoning",
        "cost": "2x tokens"
    },
    "fewshot": {
        "display": "Few-Shot",
        "desc": "2-3 domain examples",
        "cost": "1.2x tokens"
    }
}

def create_notebook(dataset_key, prompt_type):
    """Create a notebook for dataset and prompt type"""

    dataset = DATASETS[dataset_key]
    prompt = PROMPT_TYPES[prompt_type]

    # Build notebook structure
    notebook = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    # Cell IDs
    cell_num = 0

    def add_markdown(content):
        nonlocal cell_num
        notebook["cells"].append({
            "cell_type": "markdown",
            "id": f"cell-{cell_num}",
            "metadata": {},
            "source": content
        })
        cell_num += 1

    def add_code(content):
        nonlocal cell_num
        notebook["cells"].append({
            "cell_type": "code",
            "id": f"cell-{cell_num}",
            "metadata": {},
            "source": content,
            "outputs": [],
            "execution_count": None
        })
        cell_num += 1

    # Header
    add_markdown(f"""# {dataset['display_name']} - Phase 3C: {prompt['display']} Prompt

**Optimization:** Phase 3C - {prompt['display']} prompting

**Dataset:** {dataset['display_name']} ({dataset['description']})

**Model:** NVIDIA Nemotron-3 Ultra 550B (via Together AI)

**Metric:** {dataset['metric']}

**Documents:** {len(dataset['available_docs'])} example PDFs

**Q&A Count:** {dataset['qa_count']} pairs

**What changed:**
- ✅ {prompt['display']} prompt ({prompt['desc']})
- ✅ Keep all Phase 2 parameters (TOP_K={dataset['top_k']}, CHUNK_SIZE={dataset['chunk_size']})

**Baseline (Phase 2):**
- Empty rate: {dataset['empty_pct']:.1f}% ({dataset['empty_baseline']}/{dataset['qa_count']} questions)

**Target:**
- Empty rate: <{dataset['empty_pct']:.1f}% (any improvement)

**Expected runtime:** {int(dataset['qa_count'] * 0.5)}-{int(dataset['qa_count'] * 0.75)} minutes
**Expected cost:** {prompt['cost']}""")

    # Setup
    add_markdown("## Setup and Imports")

    add_code("""import sys
import os

# Navigate to project root
project_root = os.path.abspath('../../../../..')
os.chdir(project_root)
sys.path.insert(0, project_root)

print(f"Working directory: {os.getcwd()}")""")

    add_code("""import pandas as pd
import chromadb
import PyPDF2
import time
import importlib.util
from datetime import datetime
from together import Together
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb.utils.embedding_functions as embedding_functions
from uda.utils import preprocess
from uda.utils.prompts import get_prompt
from uda.eval.my_eval import eval_main

print("✓ All imports successful")""")

    # Configuration
    add_markdown("## Configuration")

    add_code("""# Load API config
_spec = importlib.util.spec_from_file_location(
    "access_config",
    os.path.join(os.getcwd(), "uda", "utils", "access_config.py")
)
access_config = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(access_config)

print(f"Model: {access_config.TOGETHER_MODEL}")
print(f"API Key: {access_config.TOGETHER_API_KEY[:20]}...")""")

    csv_file = dataset.get('csv_file', f"./dataset/qa/{dataset['name']}_qa.csv")

    add_code(f"""# Experiment Parameters
DATASET_NAME = "{dataset['name']}"
CHUNK_SIZE = {dataset['chunk_size']}
CHUNK_OVERLAP = {int(dataset['chunk_size'] / 10)}
TOP_K = {dataset['top_k']}
TEMPERATURE = 0.1
MAX_TOKENS = 512

# Prompt type
PROMPT_TYPE = "{prompt_type}"

# Output settings
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_DIR = "./experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/results/{dataset_key}_{prompt_type}"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Dataset: {{DATASET_NAME}}")
print(f"Chunk size: {{CHUNK_SIZE}}")
print(f"Top-K: {{TOP_K}}")
print(f"Prompt type: {{PROMPT_TYPE}}")
print(f"Output dir: {{OUTPUT_DIR}}")""")

    # Initialize models
    add_markdown("## Initialize Models")

    add_code("""# Together AI client
together_client = Together(api_key=access_config.TOGETHER_API_KEY)
print("✓ Together AI client initialized")

# Embedding model
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
print("✓ Embedding model loaded: all-MiniLM-L6-v2")

# Text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)
print("✓ Text splitter initialized")

# Load prompt function
prompt_fn = get_prompt(PROMPT_TYPE)
print(f"✓ Prompt function loaded: {PROMPT_TYPE}")""")

    # Helper functions
    add_markdown("## Helper Functions")

    add_code(f"""def extract_pdf_text(pdf_path):
    \"\"\"Extract text from PDF using PyPDF2\"\"\"
    pdf_text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file, strict=False)
        for page_num in range(len(reader.pages)):
            pdf_text += reader.pages[page_num].extract_text()
    return pdf_text

def build_index(text_chunks, collection_name="temp_collection"):
    \"\"\"Build vector index\"\"\"
    chroma_client = chromadb.Client()

    try:
        chroma_client.delete_collection(collection_name)
    except:
        pass

    collection = chroma_client.create_collection(
        collection_name,
        embedding_function=ef,
        metadata={{"hnsw:space": "cosine"}}
    )

    id_list = [str(i) for i in range(len(text_chunks))]
    collection.add(documents=text_chunks, ids=id_list)

    return collection

def answer_question(collection, question):
    \"\"\"
    Retrieve context and generate answer.

    CHANGED: Uses {prompt['display']} prompt
    \"\"\"
    # Retrieve
    fetch_res = collection.query(query_texts=[question], n_results=TOP_K)
    context = "\\n".join(fetch_res["documents"][0])

    # Build prompt using prompts module
    prompt_text = prompt_fn(context=context, question=question)

    # Convert to message format
    messages = [
        {{"role": "user", "content": prompt_text}}
    ]

    # Generate
    response = together_client.chat.completions.create(
        model=access_config.TOGETHER_MODEL,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    return response.choices[0].message.content

print("✓ Helper functions defined")""")

    # Load Q&A
    add_markdown("## Load Q&A Data")

    docs_list = ", ".join([f'"{doc}"' for doc in dataset['available_docs']])

    add_code(f"""# Load Q&A
csv_file = "{csv_file}"
df = pd.read_csv(csv_file, sep="|", na_filter=False, dtype={{"doc_name": str}})
qas_dict_all = preprocess.qa_df_to_dict(DATASET_NAME, df)

# Filter to documents with available PDFs
AVAILABLE_DOCS = [{docs_list}]

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

print(f"\\nTotal Q&A to process: {{total_qa}}")""")

    # Processing loop
    add_markdown(f"""## Main Processing Loop

**Expected runtime:** {int(dataset['qa_count'] * 0.5)}-{int(dataset['qa_count'] * 0.75)} minutes""")

    add_code("""all_results = []

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
    collection = build_index(text_chunks, collection_name=f"{DATASET_NAME}_{doc_name.replace(' ', '_').replace('.', '_')}")
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
print(f"Total Q&A processed: {len(all_results)}")""")

    # Diagnostics
    add_markdown("## Diagnostic: Check Empty Responses")

    add_code(f"""if all_results:
    results_df = pd.DataFrame(all_results)

    # Count empty responses
    results_df['is_empty'] = results_df['response'].fillna('').str.strip() == ''
    empty_count = results_df['is_empty'].sum()
    total_count = len(results_df)

    print(f"\\n{{'='*80}}")
    print(f"DIAGNOSTIC: Empty Response Analysis")
    print(f"{{'='*80}}")
    print(f"Total Q&A processed: {{total_count}}")
    print(f"Empty responses: {{empty_count}} ({{empty_count/total_count*100:.1f}}%)")
    print(f"Answered: {{total_count - empty_count}} ({{(total_count-empty_count)/total_count*100:.1f}}%)")

    # Comparison with Phase 2
    phase2_empty = {dataset['empty_baseline']}
    phase2_total = {dataset['qa_count']}
    phase2_empty_pct = {dataset['empty_pct']}

    improvement = phase2_empty - empty_count
    improvement_pct = phase2_empty_pct - (empty_count/total_count*100)

    print(f"\\n{{'='*80}}")
    print(f"COMPARISON WITH PHASE 2 BASELINE")
    print(f"{{'='*80}}")
    print(f"Phase 2 (Baseline): {{phase2_empty}}/{{phase2_total}} empty ({{phase2_empty_pct:.1f}}%)")
    print(f"Phase 3C ({prompt['display']}): {{empty_count}}/{{total_count}} empty ({{empty_count/total_count*100:.1f}}%)")
    print(f"\\nImprovement: {{improvement:+d}} questions ({{improvement_pct:+.1f}} percentage points)")

    if improvement > 0:
        print(f"✅ SUCCESS: {prompt['display']} reduced empty responses!")
    elif improvement == 0:
        print(f"⚠️  NEUTRAL: No change")
    else:
        print(f"❌ REGRESSION: Empty responses increased")

    if empty_count > 0:
        print(f"\\nEmpty responses by document:")
        for doc in results_df['doc'].unique():
            doc_df = results_df[results_df['doc'] == doc]
            doc_empty = doc_df['is_empty'].sum()
            doc_total = len(doc_df)
            print(f"  {{doc}}: {{doc_empty}}/{{doc_total}} empty ({{doc_empty/doc_total*100:.1f}}%)")
else:
    print("❌ No results to analyze")""")

    # Evaluate
    add_markdown("## Evaluate Results")

    add_code("""if all_results:
    print(f"\\nEvaluating {DATASET_NAME} results...")
    eval_main(DATASET_NAME, all_results)
else:
    print("❌ No results to evaluate")""")

    # Save
    add_markdown("## Save Results")

    add_code(f"""if all_results:
    results_df = pd.DataFrame(all_results)
    output_file = os.path.join(OUTPUT_DIR, f"{dataset_key}_{prompt_type}_{{TIMESTAMP}}.csv")
    results_df.to_csv(output_file, index=False)

    print(f"\\n✓ Results saved to: {{output_file}}")
    print(f"Total Q&A: {{len(results_df)}}")

    print("\\nResults by document:")
    for doc in results_df['doc'].unique():
        count = len(results_df[results_df['doc'] == doc])
        print(f"  {{doc}}: {{count}} questions")
else:
    print("❌ No results to save")""")

    # Final summary
    add_markdown("## Final Summary")

    add_code(f"""if all_results:
    results_df = pd.DataFrame(all_results)

    empty_count = results_df['response'].fillna('').str.strip().eq('').sum()
    answered_count = len(results_df) - empty_count

    phase2_empty = {dataset['empty_baseline']}
    improvement = phase2_empty - empty_count

    print(f"\\n{{'='*80}}")
    print(f"FINAL SUMMARY - {prompt['display'].upper()} ({dataset['display_name']})")
    print(f"{{'='*80}}")
    print(f"Dataset: {dataset['display_name']} ({{len(results_df)}} Q&A)")
    print(f"Prompt type: {{PROMPT_TYPE}}")
    print(f"\\nResults:")
    print(f"  Answered: {{answered_count}}/{{len(results_df)}} ({{answered_count/len(results_df)*100:.1f}}%)")
    print(f"  Empty: {{empty_count}}/{{len(results_df)}} ({{empty_count/len(results_df)*100:.1f}}%)")
    print(f"\\nVs Phase 2 Baseline:")
    print(f"  Change: {{improvement:+d}} questions")
    print(f"  Cost: {prompt['cost']}")

    if improvement >= 2:
        print(f"\\n✅ EXCELLENT: {prompt['display']} significantly improved!")
    elif improvement >= 1:
        print(f"\\n✅ GOOD: {prompt['display']} helped")
    elif improvement == 0:
        print(f"\\n⚠️  NEUTRAL: No change")
    else:
        print(f"\\n❌ REGRESSION: Made things worse")
else:
    print("\\n❌ No results to summarize")""")

    add_markdown(f"""---

## Done!

**Results saved to:** `./results/{dataset_key}_{prompt_type}/`

Compare with other prompt types to find the best approach for {dataset['display_name']}.""")

    return notebook

def main():
    """Generate all notebooks"""
    output_dir = "experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/notebooks"
    os.makedirs(output_dir, exist_ok=True)

    created = []

    for dataset_key in DATASETS.keys():
        for prompt_type in PROMPT_TYPES.keys():
            filename = f"{dataset_key}_{prompt_type}_experiment.ipynb"
            filepath = os.path.join(output_dir, filename)

            print(f"Creating {filename}...")
            notebook = create_notebook(dataset_key, prompt_type)

            with open(filepath, 'w') as f:
                json.dump(notebook, f, indent=2)

            created.append(filename)

            # Create output directory
            result_dir = f"experiments/nemotron-3-ultra-550b/3_advanced_optimization/3_prompts/results/{dataset_key}_{prompt_type}"
            os.makedirs(result_dir, exist_ok=True)

    print(f"\n✅ Created {len(created)} notebooks:")
    for filename in created:
        print(f"  - {filename}")

    print(f"\n📁 Location: {output_dir}/")
    print(f"\n🚀 Ready to run experiments!")

if __name__ == "__main__":
    main()
