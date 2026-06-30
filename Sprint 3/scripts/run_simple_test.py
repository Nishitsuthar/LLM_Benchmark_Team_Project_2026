#!/usr/bin/env python3
"""
Sprint 3 - Phase 1: Simple Nemotron Test
Based on the working basic_demo_together.ipynb
Tests a few questions from each dataset to verify Nemotron performance
"""

import pandas as pd
import chromadb
import PyPDF2
import time
import importlib.util
import os
from datetime import datetime
from together import Together
from langchain.text_splitter import RecursiveCharacterTextSplitter
import sys
import chromadb.utils.embedding_functions as embedding_functions

# Add current directory to path
sys.path.insert(0, os.getcwd())
from uda.utils import preprocess, llm
from uda.eval.my_eval import eval_main

print("="*80)
print("SPRINT 3 - PHASE 1: SIMPLE NEMOTRON TEST")
print("Testing on example documents only")
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

# Test on financial datasets (where Nemotron should excel)
DATASETS_TO_TEST = {
    "fin": ["ADI_2009"],  # 9 questions
    "tat": ["inpixon_2019"],  # 18 questions
}

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# Initialize
together_client = Together(api_key=access_config.TOGETHER_API_KEY)

# Use ChromaDB's built-in embedding function
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
print(f"✓ Loaded embedding model: all-MiniLM-L6-v2")

# Text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)

def extract_pdf_text(pdf_path):
    """Extract text from PDF"""
    pdf_text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file, strict=False)
        for page_num in range(len(reader.pages)):
            pdf_text += reader.pages[page_num].extract_text()
    return pdf_text

def process_document(dataset_name, doc_name):
    """Process one document and return results"""
    print(f"\n{'='*80}")
    print(f"Processing: {doc_name} ({dataset_name})")
    print(f"{'='*80}")

    # Load Q&A
    csv_file = f"./dataset/qa/{dataset_name}_qa.csv"
    df = pd.read_csv(csv_file, sep="|", na_filter=False, dtype={"doc_name": str})
    qas_dict = preprocess.qa_df_to_dict(dataset_name, df)

    if doc_name not in qas_dict:
        print(f"❌ Document {doc_name} not found in Q&A file")
        return []

    doc_qas = qas_dict[doc_name]
    print(f"Questions: {len(doc_qas)}")

    # Get PDF
    pdf_path = preprocess.get_example_pdf_path(dataset_name, doc_name)
    if not pdf_path:
        print(f"❌ PDF not found")
        return []

    print(f"PDF: {pdf_path}")

    # Extract and chunk
    print("Extracting text...")
    pdf_text = extract_pdf_text(pdf_path)
    text_chunks = text_splitter.split_text(pdf_text)
    print(f"Created {len(text_chunks)} chunks")

    # Build index
    print("Building vector index...")
    chroma_client = chromadb.Client()
    try:
        chroma_client.delete_collection("temp_collection")
    except:
        pass

    collection = chroma_client.create_collection(
        "temp_collection",
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"}
    )

    id_list = [str(i) for i in range(len(text_chunks))]
    collection.add(documents=text_chunks, ids=id_list)
    print("✓ Index built")

    # Process questions
    results = []
    print(f"\nAnswering {len(doc_qas)} questions...")

    for idx, qa in enumerate(doc_qas, 1):
        question = qa["question"]
        print(f"\n[{idx}/{len(doc_qas)}] {question[:80]}...")

        try:
            # Retrieve context
            fetch_res = collection.query(query_texts=[question], n_results=TOP_K)
            context = "\n".join(fetch_res["documents"][0])

            # Build prompt
            llm_message = llm.make_prompt(
                question=question,
                context=context,
                task_name=dataset_name,
                llm_type="gpt-4"
            )

            # Generate answer
            response = together_client.chat.completions.create(
                model=access_config.TOGETHER_MODEL,
                messages=llm_message,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
            )

            answer = response.choices[0].message.content
            print(f"   Answer: {answer[:100]}...")

            results.append({
                "question": question,
                "response": answer,
                "doc": doc_name,
                "q_uid": qa["q_uid"],
                "answers": qa["answers"],
                "dataset": dataset_name,
            })

            time.sleep(0.5)  # Rate limiting

        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue

    print(f"\n✓ Processed {len(results)}/{len(doc_qas)} questions")
    return results

# Run tests
all_results = []

for dataset, docs in DATASETS_TO_TEST.items():
    for doc in docs:
        results = process_document(dataset, doc)
        all_results.extend(results)

        # Evaluate
        if results:
            print(f"\nEvaluating {dataset}...")
            eval_main(dataset, results)

# Save results
if all_results:
    results_df = pd.DataFrame(all_results)
    output_file = f"../phase1_simple_results_{TIMESTAMP}.csv"
    results_df.to_csv(output_file, index=False)

    print(f"\n{'='*80}")
    print(f"COMPLETE!")
    print(f"{'='*80}")
    print(f"\nTotal Q&A processed: {len(all_results)}")
    print(f"Results saved to: {output_file}")
    print(f"\nDatasets tested:")
    for dataset, docs in DATASETS_TO_TEST.items():
        count = len([r for r in all_results if r['dataset'] == dataset])
        print(f"  - {dataset}: {count} questions")
else:
    print("\n❌ No results generated")
