#!/usr/bin/env python3
"""
Generate experiment notebooks for all UDA-Benchmark datasets
"""

import json
import os

# Dataset configurations
DATASETS = {
    "nqtext": {
        "name": "NqText",
        "full_name": "NqText (Wikipedia - Factual Q&A)",
        "dataset_code": "nq",
        "metric": "Span F1",
        "docs": [
            "Supreme Court of the United States",
            "2018 Tour de France",
            "Hannah John-Kamen",
            "Oklahoma"
        ],
        "doc_dir": "wiki_nq_docs/pdfs",
        "qa_file": "nq_qa.csv",
        "description": "Wikipedia articles with factual questions - easier than financial data"
    },
    "fetatab": {
        "name": "FetaTab",
        "full_name": "FetaTab (Wikipedia - Tables)",
        "dataset_code": "feta",
        "metric": "Span F1",
        "docs": [
            "Ben Platt (actor)",
            "Jennifer Jones",
            "List of French monarchs",
            "Smallville"
        ],
        "doc_dir": "wiki_feta_docs/pdfs",
        "qa_file": "feta_qa.csv",
        "description": "Wikipedia articles with table-focused questions"
    },
    "papertab": {
        "name": "PaperTab",
        "full_name": "PaperTab (Academic Papers - Tables)",
        "dataset_code": "paper_tab",
        "metric": "Span F1",
        "docs": [
            "1705.07830",
            "1801.05147",
            "1809.01202",
            "1810.08699",
            "1909.00754",
            "1912.01214",
            "2001.03131"
        ],
        "doc_dir": "paper_docs",
        "qa_file": "paper_qa.csv",
        "description": "Academic papers with table extraction questions"
    },
    "papertext": {
        "name": "PaperText",
        "full_name": "PaperText (Academic Papers - Text)",
        "dataset_code": "paper_text",
        "metric": "Span F1",
        "docs": [
            "1705.07830",
            "1801.05147",
            "1809.01202",
            "1810.08699",
            "1909.00754",
            "1912.01214",
            "2001.03131"
        ],
        "doc_dir": "paper_docs",
        "qa_file": "paper_qa.csv",
        "description": "Academic papers with text-focused questions"
    }
}


def create_notebook(dataset_key, config):
    """Create a Jupyter notebook for the given dataset"""

    docs_list = "\n".join([f"- {doc}" for doc in config["docs"]])

    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"# {config['name']} Dataset Experiment\\n\\n"
                    f"**Dataset:** {config['full_name']}\\n\\n"
                    f"**Model:** NVIDIA Nemotron-3 Ultra 550B (via Together AI)\\n\\n"
                    f"**Metric:** {config['metric']}\\n\\n"
                    f"**Description:** {config['description']}\\n\\n"
                    f"**Documents:** {len(config['docs'])} example PDFs\\n"
                    f"{docs_list}\\n\\n"
                    f"**Parameters:**\\n"
                    f"- Chunk size: 3000 characters\\n"
                    f"- Chunk overlap: 300 characters\\n"
                    f"- Top-K retrieval: 5\\n"
                    f"- Temperature: 0.1\\n"
                    f"- Max tokens: 512"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## Setup and Imports"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import sys\\n"
                    "import os\\n"
                    "sys.path.insert(0, os.path.abspath('../..'))\\n\\n"
                    "import pandas as pd\\n"
                    "import chromadb\\n"
                    "import PyPDF2\\n"
                    "import time\\n"
                    "import importlib.util\\n"
                    "from datetime import datetime\\n"
                    "from together import Together\\n"
                    "from langchain.text_splitter import RecursiveCharacterTextSplitter\\n"
                    "import chromadb.utils.embedding_functions as embedding_functions\\n"
                    "from uda.utils import preprocess, llm\\n"
                    "from uda.eval.my_eval import eval_main\\n\\n"
                    "print(\"✓ All imports successful\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## Configuration"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Load API config\\n"
                    "_spec = importlib.util.spec_from_file_location(\\n"
                    "    \\\"access_config\\\",\\n"
                    "    os.path.join(os.getcwd(), \\\"..\\\", \\\"..\\\", \\\"uda\\\", \\\"utils\\\", \\\"access_config.py\\\")\\n"
                    ")\\n"
                    "access_config = importlib.util.module_from_spec(_spec)\\n"
                    "_spec.loader.exec_module(access_config)\\n\\n"
                    "print(f\\\"Model: {access_config.TOGETHER_MODEL}\\\")\\n"
                    "print(f\\\"API Key: {access_config.TOGETHER_API_KEY[:20]}...\\\")"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    f"# Experiment Parameters\\n"
                    f"DATASET_NAME = \\\"{config['dataset_code']}\\\"\\n"
                    f"CHUNK_SIZE = 3000\\n"
                    f"CHUNK_OVERLAP = 300\\n"
                    f"TOP_K = 5\\n"
                    f"TEMPERATURE = 0.1\\n"
                    f"MAX_TOKENS = 512\\n\\n"
                    f"# Output settings\\n"
                    f"TIMESTAMP = datetime.now().strftime(\\\"%Y%m%d_%H%M%S\\\")\\n"
                    f"OUTPUT_DIR = \\\"./results\\\"\\n"
                    f"os.makedirs(OUTPUT_DIR, exist_ok=True)\\n\\n"
                    f"print(f\\\"Dataset: {{DATASET_NAME}}\\\")\\n"
                    f"print(f\\\"Chunk size: {{CHUNK_SIZE}}\\\")\\n"
                    f"print(f\\\"Top-K: {{TOP_K}}\\\")\\n"
                    f"print(f\\\"Output dir: {{OUTPUT_DIR}}\\\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## Initialize Models"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Together AI client\\n"
                    "together_client = Together(api_key=access_config.TOGETHER_API_KEY)\\n"
                    "print(\\\"✓ Together AI client initialized\\\")\\n\\n"
                    "# Embedding model (local, free)\\n"
                    "ef = embedding_functions.SentenceTransformerEmbeddingFunction(\\n"
                    "    model_name=\\\"all-MiniLM-L6-v2\\\"\\n"
                    ")\\n"
                    "print(\\\"✓ Embedding model loaded: all-MiniLM-L6-v2\\\")\\n\\n"
                    "# Text splitter\\n"
                    "text_splitter = RecursiveCharacterTextSplitter(\\n"
                    "    chunk_size=CHUNK_SIZE,\\n"
                    "    chunk_overlap=CHUNK_OVERLAP,\\n"
                    ")\\n"
                    "print(\\\"✓ Text splitter initialized\\\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## Helper Functions"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "def extract_pdf_text(pdf_path):\\n"
                    "    \\\"\\\"\\\"Extract text from PDF\\\"\\\"\\\"\\n"
                    "    pdf_text = \\\"\\\"\\n"
                    "    with open(pdf_path, \\\"rb\\\") as file:\\n"
                    "        reader = PyPDF2.PdfReader(file, strict=False)\\n"
                    "        for page_num in range(len(reader.pages)):\\n"
                    "            pdf_text += reader.pages[page_num].extract_text()\\n"
                    "    return pdf_text\\n\\n"
                    "def build_index(text_chunks, collection_name=\\\"temp_collection\\\"):\\n"
                    "    \\\"\\\"\\\"Build vector index\\\"\\\"\\\"\\n"
                    "    chroma_client = chromadb.Client()\\n"
                    "    \\n"
                    "    # Delete if exists\\n"
                    "    try:\\n"
                    "        chroma_client.delete_collection(collection_name)\\n"
                    "    except:\\n"
                    "        pass\\n"
                    "    \\n"
                    "    # Create collection\\n"
                    "    collection = chroma_client.create_collection(\\n"
                    "        collection_name,\\n"
                    "        embedding_function=ef,\\n"
                    "        metadata={\\\"hnsw:space\\\": \\\"cosine\\\"}\\n"
                    "    )\\n"
                    "    \\n"
                    "    # Add documents\\n"
                    "    id_list = [str(i) for i in range(len(text_chunks))]\\n"
                    "    collection.add(documents=text_chunks, ids=id_list)\\n"
                    "    \\n"
                    "    return collection\\n\\n"
                    "def answer_question(collection, question):\\n"
                    "    \\\"\\\"\\\"Retrieve context and generate answer\\\"\\\"\\\"\\n"
                    "    # Retrieve\\n"
                    "    fetch_res = collection.query(query_texts=[question], n_results=TOP_K)\\n"
                    "    context = \\\"\\\\n\\\".join(fetch_res[\\\"documents\\\"][0])\\n"
                    "    \\n"
                    "    # Build prompt\\n"
                    "    llm_message = llm.make_prompt(\\n"
                    "        question=question,\\n"
                    "        context=context,\\n"
                    "        task_name=DATASET_NAME,\\n"
                    "        llm_type=\\\"gpt-4\\\"\\n"
                    "    )\\n"
                    "    \\n"
                    "    # Generate\\n"
                    "    response = together_client.chat.completions.create(\\n"
                    "        model=access_config.TOGETHER_MODEL,\\n"
                    "        messages=llm_message,\\n"
                    "        temperature=TEMPERATURE,\\n"
                    "        max_tokens=MAX_TOKENS,\\n"
                    "    )\\n"
                    "    \\n"
                    "    return response.choices[0].message.content\\n\\n"
                    "print(\\\"✓ Helper functions defined\\\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## Load Q&A Data"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    f"# Load {config['name']} Q&A\\n"
                    f"csv_file = \\\"../../dataset/qa/{config['qa_file']}\\\"\\n"
                    f"df = pd.read_csv(csv_file, sep=\\\"|\\\", na_filter=False, dtype={{\\\"doc_name\\\": str}})\\n"
                    f"qas_dict = preprocess.qa_df_to_dict(DATASET_NAME, df)\\n\\n"
                    f"# Count Q&A per document\\n"
                    f"total_qa = 0\\n"
                    f"for doc, qas in qas_dict.items():\\n"
                    f"    count = len(qas)\\n"
                    f"    total_qa += count\\n"
                    f"    print(f\\\"{{doc}}: {{count}} Q&A pairs\\\")\\n\\n"
                    f"print(f\\\"\\\\nTotal: {{total_qa}} Q&A pairs\\\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"## Main Processing Loop\\n\\n"
                    f"**This will process all documents and Q&A pairs**\\n\\n"
                    f"**Expected runtime:** Variable based on Q&A count"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "all_results = []\\n\\n"
                    "for doc_name, doc_qas in qas_dict.items():\\n"
                    "    print(f\\\"\\\\n{{'='*80}}\\\")\\n"
                    "    print(f\\\"Processing: {{doc_name}}\\\")\\n"
                    "    print(f\\\"{{'='*80}}\\\")\\n"
                    "    \\n"
                    "    # Get PDF path\\n"
                    "    pdf_path = preprocess.get_example_pdf_path(DATASET_NAME, doc_name)\\n"
                    "    if not pdf_path:\\n"
                    "        print(f\\\"❌ PDF not found\\\")\\n"
                    "        continue\\n"
                    "    \\n"
                    "    print(f\\\"PDF: {{pdf_path}}\\\")\\n"
                    "    \\n"
                    "    # Extract and chunk\\n"
                    "    print(\\\"Extracting text...\\\")\\n"
                    "    pdf_text = extract_pdf_text(pdf_path)\\n"
                    "    text_chunks = text_splitter.split_text(pdf_text)\\n"
                    "    print(f\\\"Created {{len(text_chunks)}} chunks\\\")\\n"
                    "    \\n"
                    "    # Build index\\n"
                    "    print(\\\"Building vector index...\\\")\\n"
                    "    collection = build_index(text_chunks, collection_name=f\\\"{dataset_key}_{{doc_name}}\\\")\\n"
                    "    print(\\\"✓ Index built\\\")\\n"
                    "    \\n"
                    "    # Process each question\\n"
                    "    print(f\\\"\\\\nAnswering {{len(doc_qas)}} questions...\\\")\\n"
                    "    \\n"
                    "    for idx, qa in enumerate(doc_qas, 1):\\n"
                    "        question = qa[\\\"question\\\"]\\n"
                    "        print(f\\\"\\\\n[{{idx}}/{{len(doc_qas)}}] {{question[:70]}}...\\\")\\n"
                    "        \\n"
                    "        try:\\n"
                    "            answer = answer_question(collection, question)\\n"
                    "            print(f\\\"   Answer: {{answer[:80]}}...\\\")\\n"
                    "            \\n"
                    "            all_results.append({\\n"
                    "                \\\"question\\\": question,\\n"
                    "                \\\"response\\\": answer,\\n"
                    "                \\\"doc\\\": doc_name,\\n"
                    "                \\\"q_uid\\\": qa[\\\"q_uid\\\"],\\n"
                    "                \\\"answers\\\": qa[\\\"answers\\\"],\\n"
                    "                \\\"dataset\\\": DATASET_NAME,\\n"
                    "            })\\n"
                    "            \\n"
                    "            time.sleep(0.5)  # Rate limiting\\n"
                    "            \\n"
                    "        except Exception as e:\\n"
                    "            print(f\\\"   ❌ Error: {{e}}\\\")\\n"
                    "            continue\\n"
                    "    \\n"
                    "    print(f\\\"\\\\n✓ Completed {{doc_name}}: {{len([r for r in all_results if r['doc'] == doc_name])}} questions processed\\\")\\n\\n"
                    "print(f\\\"\\\\n{{'='*80}}\\\")\\n"
                    "print(f\\\"ALL DOCUMENTS PROCESSED\\\")\\n"
                    "print(f\\\"{{'='*80}}\\\")\\n"
                    "print(f\\\"Total Q&A processed: {{len(all_results)}}\\\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## Evaluate Results"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "if all_results:\\n"
                    f"    print(\\\"\\\\nEvaluating {config['name']} results ({config['metric']})...\\\")\\n"
                    "    eval_main(DATASET_NAME, all_results)\\n"
                    "else:\\n"
                    "    print(\\\"❌ No results to evaluate\\\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## Save Results"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "if all_results:\\n"
                    "    # Save to CSV\\n"
                    "    results_df = pd.DataFrame(all_results)\\n"
                    f"    output_file = os.path.join(OUTPUT_DIR, f\\\"{dataset_key}_results_{{TIMESTAMP}}.csv\\\")\\n"
                    "    results_df.to_csv(output_file, index=False)\\n"
                    "    \\n"
                    "    print(f\\\"\\\\n✓ Results saved to: {{output_file}}\\\")\\n"
                    "    print(f\\\"Total Q&A: {{len(results_df)}}\\\")\\n"
                    "    \\n"
                    "    # Summary by document\\n"
                    "    print(\\\"\\\\nResults by document:\\\")\\n"
                    "    for doc in results_df['doc'].unique():\\n"
                    "        count = len(results_df[results_df['doc'] == doc])\\n"
                    "        print(f\\\"  {{doc}}: {{count}} questions\\\")\\n"
                    "else:\\n"
                    "    print(\\\"❌ No results to save\\\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## Summary Statistics"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "if all_results:\\n"
                    "    results_df = pd.DataFrame(all_results)\\n"
                    "    \\n"
                    "    # Count empty responses\\n"
                    "    empty_count = results_df['response'].str.strip().eq('').sum()\\n"
                    "    answered_count = len(results_df) - empty_count\\n"
                    "    \\n"
                    "    print(f\\\"\\\\n{{'='*80}}\\\")\\n"
                    "    print(f\\\"STATISTICS\\\")\\n"
                    "    print(f\\\"{{'='*80}}\\\")\\n"
                    "    print(f\\\"Total questions: {{len(results_df)}}\\\")\\n"
                    "    print(f\\\"Answered: {{answered_count}} ({{answered_count/len(results_df)*100:.1f}}%)\\\")\\n"
                    "    print(f\\\"Empty responses: {{empty_count}} ({{empty_count/len(results_df)*100:.1f}}%)\\\")\\n"
                    "    print(f\\\"Avg response length: {{results_df['response'].str.len().mean():.0f}} characters\\\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "---\\n\\n"
                    "## Done!\\n\\n"
                    f"**Results saved to:** `./results/{dataset_key}_results_[timestamp].csv`\\n\\n"
                    f"**Metric:** {config['metric']}\\n\\n"
                    "**Next steps:**\\n"
                    "1. Review the accuracy score\\n"
                    "2. Compare with other datasets\\n"
                    "3. Try parameter optimization (chunk_size, top_k, temperature)"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.9.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    return notebook


def main():
    """Generate all notebooks"""
    base_dir = "experiments"

    for dataset_key, config in DATASETS.items():
        output_dir = os.path.join(base_dir, dataset_key)
        os.makedirs(output_dir, exist_ok=True)

        # Create results directory
        results_dir = os.path.join(output_dir, "results")
        os.makedirs(results_dir, exist_ok=True)

        # Generate notebook
        notebook = create_notebook(dataset_key, config)
        output_file = os.path.join(output_dir, f"{dataset_key}_experiment.ipynb")

        with open(output_file, 'w') as f:
            json.dump(notebook, f, indent=1)

        print(f"✓ Created: {output_file}")

    print(f"\n✅ All notebooks created successfully!")
    print(f"\nDirectory structure:")
    print(f"experiments/")
    for dataset_key in DATASETS.keys():
        print(f"  ├── {dataset_key}/")
        print(f"  │   ├── {dataset_key}_experiment.ipynb")
        print(f"  │   └── results/")


if __name__ == "__main__":
    main()
