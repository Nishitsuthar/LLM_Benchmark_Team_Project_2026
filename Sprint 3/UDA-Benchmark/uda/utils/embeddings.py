"""
FinBERT Embedding Module for UDA-Benchmark
Phase 3B: Financial domain-specific embeddings

This module provides a ChromaDB-compatible embedding function using FinBERT,
a BERT model pre-trained on financial texts for better semantic understanding
of financial terminology, numerical values, and domain-specific concepts.

Model: yiyanghkust/finbert-tone
Source: https://huggingface.co/yiyanghkust/finbert-tone
Embedding dimension: 768
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FinBERTEmbeddingFunction:
    """
    ChromaDB-compatible embedding function using FinBERT.

    FinBERT is specifically trained on financial texts and provides better
    semantic understanding of:
    - Financial terminology (EBITDA, P/E ratio, revenue, etc.)
    - Numerical values and their context
    - Financial statements and reports
    - Market and economic concepts

    Usage:
        embedding_fn = FinBERTEmbeddingFunction()
        embeddings = embedding_fn(["Revenue increased by $45.2M"])
    """

    def __init__(self, model_name: str = "yiyanghkust/finbert-tone"):
        """
        Initialize FinBERT embedding function.

        Args:
            model_name: HuggingFace model identifier for FinBERT
        """
        logger.info(f"Loading FinBERT model: {model_name}")
        self.model = SentenceTransformer(model_name)
        logger.info(f"✅ FinBERT loaded. Embedding dimension: {self.model.get_sentence_embedding_dimension()}")

    def __call__(self, input: Union[str, List[str]]) -> List[np.ndarray]:
        """
        Generate embeddings for input texts.

        Args:
            input: Single text string or list of text strings (ChromaDB v1.5+ uses 'input')

        Returns:
            List of numpy arrays (ChromaDB v1.5+ expects numpy arrays, not lists)
        """
        # Handle single string input
        if isinstance(input, str):
            input = [input]

        # Generate embeddings as numpy arrays
        embeddings = self.model.encode(input, convert_to_numpy=True)

        # Return list of numpy arrays (ChromaDB v1.5+ format)
        if isinstance(embeddings, np.ndarray):
            return [embeddings[i] for i in range(len(embeddings))]

        return embeddings

    def embed_query(self, input: Union[str, List[str]]) -> List[np.ndarray]:
        """
        Generate embedding for query string(s).

        This method is required by ChromaDB for query operations.
        ChromaDB expects the same return type as __call__: List[np.ndarray]

        Args:
            input: Single query text string or list of strings

        Returns:
            List of numpy array embeddings (same format as __call__)
        """
        # Delegate to __call__ for consistent behavior
        return self.__call__(input)


class GenericEmbeddingFunction:
    """
    Generic sentence transformer embedding function for non-financial datasets.

    Uses all-MiniLM-L6-v2 (same as Phase 2 baseline) for consistency.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize generic embedding function.

        Args:
            model_name: HuggingFace model identifier
        """
        logger.info(f"Loading generic model: {model_name}")
        self.model = SentenceTransformer(model_name)
        logger.info(f"✅ Generic model loaded. Embedding dimension: {self.model.get_sentence_embedding_dimension()}")

    def __call__(self, input: Union[str, List[str]]) -> List[np.ndarray]:
        """
        Generate embeddings for input texts.

        Args:
            input: Single text string or list of text strings (ChromaDB v1.5+ uses 'input')

        Returns:
            List of numpy arrays (ChromaDB v1.5+ expects numpy arrays, not lists)
        """
        if isinstance(input, str):
            input = [input]

        embeddings = self.model.encode(input, convert_to_numpy=True)

        # Return list of numpy arrays
        if isinstance(embeddings, np.ndarray):
            return [embeddings[i] for i in range(len(embeddings))]

        return embeddings

    def embed_query(self, input: Union[str, List[str]]) -> List[np.ndarray]:
        """
        Generate embedding for query string(s).

        This method is required by ChromaDB for query operations.
        ChromaDB expects the same return type as __call__: List[np.ndarray]

        Args:
            input: Single query text string or list of strings

        Returns:
            List of numpy array embeddings (same format as __call__)
        """
        # Delegate to __call__ for consistent behavior
        return self.__call__(input)


def get_embedding_function(dataset_name: str = None, use_finbert: bool = False):
    """
    Factory function to get appropriate embedding function for a dataset.

    Args:
        dataset_name: Name of the dataset ('fin', 'tat', etc.)
        use_finbert: Force use of FinBERT embeddings

    Returns:
        Embedding function compatible with ChromaDB

    Usage:
        # For financial datasets
        embedding_fn = get_embedding_function('fin', use_finbert=True)

        # For non-financial datasets
        embedding_fn = get_embedding_function('nq', use_finbert=False)
    """
    # Determine if dataset is financial
    financial_datasets = ['fin', 'tat', 'finhybrid', 'tathybrid']
    is_financial = dataset_name in financial_datasets if dataset_name else False

    # Use FinBERT for financial datasets or if explicitly requested
    if use_finbert or is_financial:
        logger.info(f"🏦 Using FinBERT embeddings for dataset: {dataset_name}")
        return FinBERTEmbeddingFunction()
    else:
        logger.info(f"📄 Using generic embeddings for dataset: {dataset_name}")
        return GenericEmbeddingFunction()


# Convenience function for backward compatibility
def get_finbert_embedding_function():
    """
    Get FinBERT embedding function directly.

    Returns:
        FinBERT embedding function
    """
    return FinBERTEmbeddingFunction()


if __name__ == "__main__":
    # Test the embedding functions
    print("=" * 60)
    print("Testing FinBERT Embedding Function")
    print("=" * 60)

    # Test FinBERT
    finbert_fn = FinBERTEmbeddingFunction()

    test_texts = [
        "Revenue increased by $45.2 million in Q4 2023",
        "EBITDA margin improved from 12.5% to 15.3%",
        "The company reported net income of $2.1B"
    ]

    print("\nTest texts:")
    for i, text in enumerate(test_texts, 1):
        print(f"  {i}. {text}")

    embeddings = finbert_fn(test_texts)
    print(f"\n✅ Generated {len(embeddings)} embeddings")
    print(f"   Embedding dimension: {len(embeddings[0])}")
    print(f"   First embedding (first 5 values): {embeddings[0][:5]}")

    # Test single string
    single_embedding = finbert_fn("Test single string")
    print(f"\n✅ Single string test passed: {len(single_embedding)} embeddings generated")

    # Test generic function
    print("\n" + "=" * 60)
    print("Testing Generic Embedding Function")
    print("=" * 60)

    generic_fn = GenericEmbeddingFunction()
    generic_embeddings = generic_fn(test_texts)
    print(f"\n✅ Generated {len(generic_embeddings)} embeddings")
    print(f"   Embedding dimension: {len(generic_embeddings[0])}")

    # Test factory function
    print("\n" + "=" * 60)
    print("Testing Factory Function")
    print("=" * 60)

    fin_fn = get_embedding_function('fin', use_finbert=True)
    print(f"✅ Financial dataset: {type(fin_fn).__name__}")

    nq_fn = get_embedding_function('nq', use_finbert=False)
    print(f"✅ Non-financial dataset: {type(nq_fn).__name__}")

    print("\n" + "=" * 60)
    print("All tests passed! ✅")
    print("=" * 60)
