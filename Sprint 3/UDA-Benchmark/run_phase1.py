#!/usr/bin/env python3
"""
Sprint 3 - Phase 1: NVIDIA Nemotron Baseline Evaluation
Run directly with Python (alternative to Jupyter notebook)
"""

import pandas as pd
import chromadb
import PyPDF2
import time
import importlib.util
import os
from datetime import datetime
from tqdm import tqdm
from together import Together
from langchain.text_splitter import RecursiveCharacterTextSplitter
import sys

# Add current directory to path for imports
sys.path.insert(0, os.getcwd())
from uda.utils import preprocess, llm
from uda.eval.my_eval import eval_main

print("="*80)
print("SPRINT 3 - PHASE 1: NEMOTRON BASELINE EVALUATION")
print("="*80)

# Load access_config
_spec = importlib.util.spec_from_file_location(
    "access_config",
    os.path.join(os.getcwd(), "uda", "utils", "access_config.py")
)
access_config = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(access_config)

print(f"\n✓ Model: {access_config.TOGETHER_MODEL}")
print(f"✓ API Key: {access_config.TOGETHER_API_KEY[:20]}...")

# Configuration
CHUNK_SIZE = 3000
CHUNK_OVERLAP = 300
TOP_K = 5
TEMPERATURE = 0.1
MAX_TOKENS = 512

DATASETS = ["fin", "tat", "paper_tab", "paper_text", "feta", "nq"]

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
RESULTS_CSV = f"../phase1_results_{TIMESTAMP}.csv"
SUMMARY_CSV = f"../phase1_summary_{TIMESTAMP}.csv"

print(f"\nParameters:")
print(f"  - chunk_size: {CHUNK_SIZE}")
print(f"  - chunk_overlap: {CHUNK_OVERLAP}")
print(f"  - top_k: {TOP_K}")
print(f"  - temperature: {TEMPERATURE}")
print(f"  - datasets: {DATASETS}")

# Initialize clients
together_client = Together(api_key=access_config.TOGETHER_API_KEY)

# Use SentenceTransformer for local embeddings (free, no API calls)
from sentence_transformers import SentenceTransformer
import chromadb.utils.embedding_functions as embedding_functions

# Use ChromaDB's built-in SentenceTransformer wrapper
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
print(f"✓ Loaded embedding model: all-MiniLM-L6-v2")

# Text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)

print("\n✓ Helper functions initialized")

# Pipeline functions
def extract_pdf_text(pdf_path):
    """Extract text from PDF file"""
    pdf_text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file, strict=False)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()
    return pdf_text

def build_vector_index(text_chunks, collection_name="temp_vdb"):
    """Build ChromaDB vector index from text chunks"""
    chroma_client = chromadb.Client()

    # Delete if exists
    try:
        chroma_client.delete_collection(collection_name)
    except:
        pass

    # Create collection with global embedding function
    collection = chroma_client.create_collection(
        collection_name,
        embedding_function=ef,  # Use global ef defined above
        metadata={"hnsw:space": "cosine"},
    )

    # Add documents
    id_list = [str(i) for i in range(len(text_chunks))]
    collection.add(documents=text_chunks, ids=id_list)

    return collection

def retrieve_context(collection, question, top_k=TOP_K):
    """Retrieve top-k relevant chunks for a question"""
    fetch_res = collection.query(query_texts=[question], n_results=top_k)
    contexts = fetch_res["documents"][0]
    return "\n".join(contexts)

def generate_answer(question, context, dataset_name):
    """Generate answer using Nemotron"""
    # Build prompt
    llm_message = llm.make_prompt(
        question=question,
        context=context,
        task_name=dataset_name,
        llm_type="gpt-4",
    )

    # Call Together AI
    raw_response = together_client.chat.completions.create(
        model=access_config.TOGETHER_MODEL,
        messages=llm_message,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    return raw_response.choices[0].message.content

# Main experiment function
def run_experiment_on_dataset(dataset_name):
    """Run experiment on one dataset"""
    print(f"\n{'='*80}")
    print(f"Starting experiment: {dataset_name.upper()}")
    print(f"{'='*80}\n")

    # Load Q&A pairs
    csv_file_path = f"./dataset/qa/{dataset_name}_qa.csv"
    df = pd.read_csv(csv_file_path, sep="|", na_filter=False, dtype={"doc_name": str})
    qas_dict = preprocess.qa_df_to_dict(dataset_name, df)

    print(f"Loaded {len(qas_dict)} documents with Q&A pairs")

    all_results = []
    doc_count = 0

    # Process each document
    for doc_name in qas_dict.keys():
        doc_count += 1

        # Get PDF path (example documents only)
        pdf_path = preprocess.get_example_pdf_path(dataset_name, doc_name)

        if pdf_path is None:
            print(f"  ⚠️  Skipping {doc_name}: No example PDF found")
            continue

        print(f"\n[{doc_count}] Processing: {doc_name}")
        print(f"    PDF: {pdf_path}")

        # Extract and chunk text
        pdf_text = extract_pdf_text(pdf_path)
        text_chunks = text_splitter.split_text(pdf_text)
        print(f"    Chunks: {len(text_chunks)} (avg {sum(len(c.split()) for c in text_chunks) / len(text_chunks):.0f} words/chunk)")

        # Build vector index
        collection = build_vector_index(text_chunks, collection_name=f"{dataset_name}_{doc_count}")
        print(f"    Indexed: ✓")

        # Process each Q&A pair
        doc_qas = qas_dict[doc_name]
        print(f"    Questions: {len(doc_qas)}")

        for qa_idx, qa in enumerate(tqdm(doc_qas, desc="    Answering")):
            question = qa["question"]

            try:
                # Retrieve context
                context = retrieve_context(collection, question, top_k=TOP_K)

                # Generate answer
                answer = generate_answer(question, context, dataset_name)

                # Store result
                all_results.append({
                    "question": question,
                    "response": answer,
                    "doc": doc_name,
                    "q_uid": qa["q_uid"],
                    "answers": qa["answers"],
                    "dataset": dataset_name,
                })

                # Rate limiting
                time.sleep(0.3)

            except Exception as e:
                print(f"\n    ❌ Error on question {qa_idx+1}: {e}")
                continue

    print(f"\n✓ Completed {dataset_name}: {len(all_results)} Q&A pairs processed\n")
    return all_results

# Run all datasets
print(f"\n{'#'*80}")
print(f"# STARTING PHASE 1 EXPERIMENTS")
print(f"# Timestamp: {TIMESTAMP}")
print(f"{'#'*80}\n")

all_dataset_results = {}

for dataset in DATASETS:
    results = run_experiment_on_dataset(dataset)
    all_dataset_results[dataset] = results

    # Evaluate immediately
    if results:
        print(f"\nEvaluating {dataset}...")
        eval_main(dataset, results)

    print(f"\n{'-'*80}\n")

print("\n✓ All datasets completed!")

# Save results
all_results_list = []
for dataset, results in all_dataset_results.items():
    all_results_list.extend(results)

results_df = pd.DataFrame(all_results_list)

# Save raw results
results_df.to_csv(RESULTS_CSV, index=False)
print(f"\n✓ Saved raw results to: {RESULTS_CSV}")
print(f"  Total Q&A pairs: {len(results_df)}")

# Create summary
summary_data = []
for dataset, results in all_dataset_results.items():
    summary_data.append({
        "Dataset": dataset,
        "Total_QA": len(results),
        "Documents": len(set(r["doc"] for r in results)),
        "Avg_Response_Length": sum(len(r["response"]) for r in results) / len(results) if results else 0,
    })

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv(SUMMARY_CSV, index=False)
print(f"✓ Saved summary to: {SUMMARY_CSV}\n")
print(summary_df.to_string(index=False))

print(f"\n{'='*80}")
print(f"EXPERIMENT COMPLETE")
print(f"{'='*80}")
print(f"\nResults saved to:")
print(f"  - {RESULTS_CSV}")
print(f"  - {SUMMARY_CSV}")
print(f"\n{'='*80}\n")
