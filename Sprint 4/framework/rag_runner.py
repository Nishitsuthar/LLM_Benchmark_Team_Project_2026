"""
Sprint 4 RAG Runner

Thin wrapper around the Sprint 3 UDA pipeline, locked to author-default parameters.
Supports Together AI (Llama-3-8B, Nemotron-550B), OpenAI (GPT-4-Turbo),
and Google Gemini (Gemini 3.1 Flash-Lite).

Usage (from a notebook):
    from framework.rag_runner import RAGRunner
    runner = RAGRunner(model_key="gemini-3.1-flash-lite", dataset="tathybrid", prompt="simple")
    results = runner.run(questions_csv="benchmark/questions/tathybrid_hard_cases.csv")
"""

import os
import sys
import time
import pandas as pd
import chromadb
import PyPDF2
from datetime import datetime
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb.utils.embedding_functions as embedding_functions
from together import Together
from openai import OpenAI
from google import genai as google_genai

from framework.config import (
    CHUNK_SIZE, CHUNK_OVERLAP, TOP_K, EMBEDDING_MODEL,
    TEMPERATURE, MAX_TOKENS, MODELS, DATASET_UDA_NAMES,
)
import framework.api_keys as api_keys


class RAGRunner:
    """
    Fixed-config RAG pipeline for Sprint 4 benchmarking.

    Parameters are frozen to UDA paper author defaults.
    Switch model and prompt strategy; everything else stays constant.
    """

    def __init__(self, model_key: str, dataset: str, prompt: str = "simple"):
        """
        Args:
            model_key:  One of "llama-3-8b", "nemotron-550b", "gpt4-turbo"
            dataset:    One of "tathybrid", "finhybrid", "nqtext", "fetatab",
                        "papertab", "papertext"
            prompt:     "simple" (zero-shot) or "cot" (chain-of-thought)
        """
        if model_key not in MODELS:
            raise ValueError(f"Unknown model '{model_key}'. Valid: {list(MODELS)}")
        if prompt not in ("simple", "cot"):
            raise ValueError("prompt must be 'simple' or 'cot'")

        self.model_key = model_key
        self.model_cfg = MODELS[model_key]
        self.dataset = dataset
        self.uda_dataset = DATASET_UDA_NAMES[dataset]
        self.prompt = prompt

        # Embedding function (shared, no API cost)
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL
        )

        # Text splitter (author defaults)
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )

        # LLM client
        provider = self.model_cfg.get("provider", "together")
        if provider == "together":
            self._client = Together(api_key=api_keys.TOGETHER_API_KEY)
            self._model_id = self.model_cfg["together_id"]
        elif provider == "gemini":
            self._client = google_genai.Client(api_key=api_keys.GEMINI_API_KEY)
            self._model_id = self.model_cfg["gemini_id"]
        elif provider == "nvidia":
            self._client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=api_keys.NVIDIA_API_KEY,
            )
            self._model_id = self.model_cfg["nvidia_id"]
        elif provider == "deepseek":
            self._client = OpenAI(
                base_url="https://api.deepseek.com/v1",
                api_key=api_keys.DEEPSEEK_API_KEY,
            )
            self._model_id = self.model_cfg["deepseek_id"]
        else:
            self._client = OpenAI(api_key=api_keys.OPENAI_API_KEY)
            self._model_id = self.model_cfg["openai_id"]

        print(f"RAGRunner ready: model={model_key}, dataset={dataset}, prompt={prompt}")
        print(f"  CHUNK_SIZE={CHUNK_SIZE}, CHUNK_OVERLAP={CHUNK_OVERLAP}, "
              f"TOP_K={TOP_K}, TEMP={TEMPERATURE}")

    # ── PDF helpers ──────────────────────────────────────────────────────────

    def _extract_pdf(self, pdf_path: str) -> str:
        text = ""
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f, strict=False)
            for page in reader.pages:
                text += page.extract_text()
        return text

    def _build_index(self, text: str, collection_name: str):
        chroma = chromadb.Client()
        try:
            chroma.delete_collection(collection_name)
        except Exception:
            pass
        collection = chroma.create_collection(
            collection_name,
            embedding_function=self.ef,
            metadata={"hnsw:space": "cosine"},
        )
        chunks = self.splitter.split_text(text)
        collection.add(documents=chunks, ids=[str(i) for i in range(len(chunks))])
        return collection, chunks

    # ── Prompt building ──────────────────────────────────────────────────────

    def _make_messages(self, context: str, question: str) -> list:
        """Build the message list for the LLM using UDA author's prompt templates."""
        # Import here to avoid circular dependency issues in notebooks
        sys.path.insert(0, os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../Sprint 3/UDA-Benchmark")
        ))
        from uda.utils.llm import make_prompt

        if self.prompt == "simple":
            # Author's standard prompt (same as Phase 1 baseline)
            return make_prompt(question, context, self.uda_dataset, llm_type="gpt-4")
        else:
            # CoT: wrap the author's prompt with step-by-step instruction
            base_msgs = make_prompt(question, context, self.uda_dataset, llm_type="gpt-4")
            # Append CoT instruction to the last user message
            last = base_msgs[-1]
            base_msgs[-1] = {
                "role": last["role"],
                "content": last["content"] + "\n\nThink step by step before giving the final answer.",
            }
            return base_msgs

    # ── Generation ───────────────────────────────────────────────────────────

    def _generate(self, messages: list, max_retries: int = 3) -> str:
        provider = self.model_cfg.get("provider", "together")
        for attempt in range(max_retries):
            try:
                if provider == "gemini":
                    prompt_parts = []
                    for m in messages:
                        role = m.get("role", "")
                        content = m.get("content", "")
                        if role == "system":
                            prompt_parts.append(f"[System]: {content}")
                        elif role == "user":
                            prompt_parts.append(content)
                        elif role == "assistant":
                            prompt_parts.append(f"[Assistant]: {content}")
                    prompt_text = "\n\n".join(prompt_parts)
                    resp = self._client.models.generate_content(
                        model=self._model_id,
                        contents=prompt_text,
                        config={"temperature": TEMPERATURE, "max_output_tokens": MAX_TOKENS},
                    )
                    return resp.text or ""
                elif provider == "nvidia":
                    # Streaming response — collect only answer tokens, skip reasoning_content
                    stream = self._client.chat.completions.create(
                        model=self._model_id,
                        messages=messages,
                        temperature=TEMPERATURE,
                        max_tokens=MAX_TOKENS,
                        extra_body={
                            "chat_template_kwargs": {"enable_thinking": True},
                            "reasoning_budget": MAX_TOKENS,
                        },
                        stream=True,
                    )
                    answer_parts = []
                    for chunk in stream:
                        if not chunk.choices:
                            continue
                        delta = chunk.choices[0].delta
                        if delta.content:
                            answer_parts.append(delta.content)
                    return "".join(answer_parts)
                elif provider == "together":
                    resp = self._client.chat.completions.create(
                        model=self._model_id,
                        messages=messages,
                        temperature=TEMPERATURE,
                        max_tokens=MAX_TOKENS,
                    )
                else:
                    resp = self._client.chat.completions.create(
                        model=self._model_id,
                        messages=messages,
                        temperature=TEMPERATURE,
                        max_tokens=MAX_TOKENS,
                    )
                return resp.choices[0].message.content or ""
            except Exception as e:
                err = str(e)
                if "429" in err or "RESOURCE_EXHAUSTED" in err:
                    import re as _re
                    m = _re.search(r'retry[^\d]*(\d+)', err, _re.IGNORECASE)
                    wait = int(m.group(1)) + 5 if m else 60
                    print(f"  [RATE LIMIT] attempt {attempt+1}/{max_retries} — waiting {wait}s...", flush=True)
                    time.sleep(wait)
                else:
                    print(f"  [LLM ERROR] {e}")
                    return ""
        print(f"  [LLM ERROR] max retries exhausted")
        return ""

    # ── Main runner ──────────────────────────────────────────────────────────

    def run_on_pdf(self, pdf_path: str, questions: list) -> list:
        """
        Run all questions against a single PDF document.

        Args:
            pdf_path:  Path to the source PDF
            questions: List of dicts with keys: question_id, question, ground_truth,
                       and any other metadata columns

        Returns:
            List of result dicts (input row + 'response' + 'context' columns)
        """
        print(f"\n  PDF: {os.path.basename(pdf_path)}")
        text = self._extract_pdf(pdf_path)
        collection_name = f"sprint4_{self.dataset}_{int(time.time())}"
        collection, chunks = self._build_index(text, collection_name)
        print(f"  {len(chunks)} chunks indexed")

        results = []
        for i, qa in enumerate(questions, 1):
            q = qa["question"]
            print(f"  [{i}/{len(questions)}] {q[:70]}...")

            # Retrieve
            fetch = collection.query(query_texts=[q], n_results=TOP_K)
            context = "\n".join(fetch["documents"][0])

            # Generate
            messages = self._make_messages(context, q)
            response = self._generate(messages)
            print(f"    → {response[:80]}")

            result = dict(qa)
            result["response"] = response
            result["context_snippet"] = context[:300]
            result["model"] = self.model_key
            result["prompt_strategy"] = self.prompt
            results.append(result)

            time.sleep(0.3)  # rate limiting

        return results

    def run(
        self,
        questions_csv: str,
        pdf_dir: str,
        doc_col: str = "doc_name",
        output_dir: str = None,
    ) -> pd.DataFrame:
        """
        Run the full benchmark for this model × dataset × prompt combination.

        Args:
            questions_csv: Path to hard-cases CSV
                           (must have columns: question_id, question, ground_truth,
                            doc_name, and any extra metadata)
            pdf_dir:       Directory containing the source PDFs
            doc_col:       Column in the CSV that identifies the PDF filename
                           (without .pdf extension)
            output_dir:    Where to save the scored CSV. Defaults to Sprint 4 results/

        Returns:
            DataFrame with all results
        """
        df = pd.read_csv(questions_csv)
        df[doc_col] = df[doc_col].astype(str).str.strip()  # ensure string, handles numeric doc names like 1909.00754
        all_results = []

        for doc_name, group in df.groupby(doc_col):
            pdf_path = os.path.join(pdf_dir, str(doc_name) + ".pdf")
            if not os.path.exists(pdf_path):
                print(f"  WARNING: PDF not found — {pdf_path}")
                continue
            questions = group.to_dict("records")
            results = self.run_on_pdf(pdf_path, questions)
            all_results.extend(results)

        results_df = pd.DataFrame(all_results)

        # Save
        if output_dir is None:
            output_dir = os.path.join(
                os.path.dirname(__file__), "../results"
            )
        os.makedirs(output_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"{self.dataset}_{self.model_key}_{self.prompt}_{ts}.csv"
        out_path = os.path.join(output_dir, fname)
        results_df.to_csv(out_path, index=False)
        print(f"\n  Saved → {out_path}")

        return results_df
