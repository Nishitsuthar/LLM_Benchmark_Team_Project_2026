"""
Sprint 4 — Fixed RAG Configuration

All parameters are locked to UDA paper author defaults (from e2e.ipynb / Phase 1 baseline).
DO NOT change these for Sprint 4. The goal is benchmarking failures, not optimising the system.

Author defaults verified from:
  Sprint 3/UDA-Benchmark/experiment/e2e/e2e.ipynb
  Sprint 3/UDA-Benchmark/experiments/nemotron-3-ultra-550b/1_without_optimization/
"""

# ── RAG parameters (author defaults, frozen) ─────────────────────────────────
CHUNK_SIZE = 3000        # characters (RecursiveCharacterTextSplitter)
CHUNK_OVERLAP = 300      # characters
TOP_K = 5                # chunks retrieved per question
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # local, no API cost
VECTOR_DB = "chromadb"   # in-memory ChromaDB

# ── Generation parameters (frozen) ───────────────────────────────────────────
TEMPERATURE = 0.0        # deterministic — professor's explicit requirement for Sprint 4
MAX_TOKENS = 512

# ── Prompt strategies (Sprint 4 uses exactly 2) ──────────────────────────────
PROMPT_STRATEGIES = ["simple", "cot"]  # zero-shot baseline + chain-of-thought

# ── Models (pending professor approval) ──────────────────────────────────────
MODELS = {
    "llama-3-8b": {
        "together_id": "meta-llama/Llama-3-8b-chat-hf",
        "type": "open",
        "params": "8B",
        "provider": "together",
    },
    "nemotron-550b": {
        "together_id": "nvidia/nemotron-3-ultra-550b-a55b",
        "type": "open",
        "params": "550B",
        "provider": "together",
    },
    "gpt4-turbo": {
        "together_id": None,
        "openai_id": "gpt-4-turbo",
        "type": "proprietary",
        "params": "~1T+",
        "provider": "openai",
    },
    "gemini-3.1-flash-lite": {
        "gemini_id": "gemini-3.1-flash-lite",
        "type": "proprietary",
        "params": "unknown",
        "provider": "gemini",
    },
    "nemotron-nvidia": {
        "nvidia_id": "nvidia/nemotron-3-ultra-550b-a55b",
        "type": "open",
        "params": "550B",
        "provider": "nvidia",
    },
    "deepseek-v3": {
        "deepseek_id": "deepseek-chat",
        "type": "open",
        "params": "671B",
        "provider": "deepseek",
    },
}

# ── Dataset → metric mapping (from UDA paper) ────────────────────────────────
DATASET_METRICS = {
    "nqtext":    "f1",
    "fetatab":   "f1",
    "papertab":  "f1",
    "papertext": "f1",
    "finhybrid": "exact_match",
    "tathybrid": "numeracy_f1",
}

# ── UDA dataset name aliases (Sprint 3 code uses these) ──────────────────────
DATASET_UDA_NAMES = {
    "nqtext":    "nq",
    "fetatab":   "feta",
    "papertab":  "paper_tab",
    "papertext": "paper_text",
    "finhybrid": "fin",
    "tathybrid": "tat",
}
