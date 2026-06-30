"""
Prompt templates for UDA benchmark experiments.

Created: June 29, 2026
Purpose: Phase 3C - Improve QA performance through better prompting

Contains:
- simple_prompt: Phase 1-2 baseline (current)
- instruction_prompt: Phase 3C-1 (instruction-enhanced)
- fewshot_prompt: Phase 3C-2 (few-shot examples)
- cot_prompt: Phase 3C-3 (chain-of-thought, expensive)

Usage:
    from uda.utils.prompts import get_prompt

    prompt_fn = get_prompt("instruction")
    prompt = prompt_fn(context=retrieved_context, question=question)
    answer = llm.generate(prompt)
"""


def simple_prompt(context: str, question: str) -> str:
    """
    Simple prompt (Phase 1-2 baseline).

    This is the current prompt used in Phase 2.
    Minimal instructions, just context + question.

    Args:
        context: Retrieved document context
        question: Question to answer

    Returns:
        Formatted prompt string
    """
    return f"""Context: {context}

Question: {question}

Answer:"""


def instruction_prompt(context: str, question: str) -> str:
    """
    Instruction-enhanced prompt (Phase 3C-1).

    Adds explicit instructions to guide the model:
    - Answer only from context
    - Format guidelines (numerical, yes/no)
    - Insufficient information handling
    - Precision requirements

    Expected improvement: +2-4 questions
    Cost: Similar to baseline

    Args:
        context: Retrieved document context
        question: Question to answer

    Returns:
        Formatted prompt string with instructions
    """
    return f"""You are a financial document analysis expert. Answer the question based ONLY on the provided context.

Context:
{context}

Question: {question}

Instructions:
- Extract the answer directly from the context
- For numerical questions, provide just the number with units (e.g., "$45.2 million", "7 members")
- For yes/no questions, answer with "Yes" or "No" followed by a brief explanation
- If the context doesn't contain the answer, respond with "INSUFFICIENT INFORMATION"
- Be precise and concise
- Do not add information not present in the context

Answer:"""


def fewshot_prompt(context: str, question: str) -> str:
    """
    Few-shot prompt with examples (Phase 3C-2).

    Provides 3 examples of good question-answering:
    1. Numerical question (revenue)
    2. Counting question (board members)
    3. Yes/no with context (merger timing)

    Expected improvement: +3-7 questions
    Cost: +20% tokens (longer prompt)

    Args:
        context: Retrieved document context
        question: Question to answer

    Returns:
        Formatted prompt string with examples
    """
    return f"""Answer questions based on the provided context. Here are examples of good answers:

Example 1:
Context: The company's revenue in 2019 was $45.2 million, up from $38.7 million in 2018.
Question: What was the revenue in 2019?
Answer: $45.2 million

Example 2:
Context: The board consists of 7 members, 3 of whom are independent directors.
Question: How many board members are there?
Answer: 7

Example 3:
Context: The merger was completed in Q3 2020, combining two major industry players.
Question: Did the merger happen in 2019?
Answer: No, it happened in Q3 2020.

Now answer this question:
Context: {context}
Question: {question}
Answer:"""


def cot_prompt(context: str, question: str) -> str:
    """
    Chain-of-thought prompt (Phase 3C-3).

    Encourages step-by-step reasoning:
    1. What information is needed?
    2. Where is it in the context?
    3. What is the answer?

    Expected improvement: +5-10 questions
    Cost: +100% tokens (model generates reasoning + answer)

    NOTE: This is the most expensive option but potentially most effective.
    Test on small dataset first to validate cost/benefit.

    Args:
        context: Retrieved document context
        question: Question to answer

    Returns:
        Formatted prompt string with CoT instructions
    """
    return f"""Context: {context}

Question: {question}

Think step by step:
1. What information do I need to answer this question?
2. Where in the context is this information located?
3. What is the precise answer based on the context?

Answer:"""


# Prompt registry for easy switching
PROMPTS = {
    "simple": simple_prompt,
    "instruction": instruction_prompt,
    "fewshot": fewshot_prompt,
    "cot": cot_prompt,
}


def get_prompt(prompt_type: str = "simple"):
    """
    Get prompt function by type.

    Args:
        prompt_type: One of "simple", "instruction", "fewshot", "cot"

    Returns:
        Prompt function with signature: (context: str, question: str) -> str

    Raises:
        ValueError: If prompt_type is not recognized

    Example:
        >>> prompt_fn = get_prompt("instruction")
        >>> prompt = prompt_fn(context="...", question="...")
        >>> # Use prompt with LLM
    """
    if prompt_type not in PROMPTS:
        valid_types = list(PROMPTS.keys())
        raise ValueError(
            f"Unknown prompt type: '{prompt_type}'. "
            f"Valid options: {valid_types}"
        )

    return PROMPTS[prompt_type]


def list_prompts():
    """
    List all available prompt types with descriptions.

    Returns:
        Dictionary mapping prompt type to description
    """
    return {
        "simple": "Phase 1-2 baseline - minimal instructions",
        "instruction": "Phase 3C-1 - explicit instructions (+2-4 Q expected)",
        "fewshot": "Phase 3C-2 - few-shot examples (+3-7 Q expected, +20% cost)",
        "cot": "Phase 3C-3 - chain-of-thought (+5-10 Q expected, 2x cost)",
    }


if __name__ == "__main__":
    # Test the module
    print("Available prompts:")
    for name, desc in list_prompts().items():
        print(f"  - {name}: {desc}")

    # Test each prompt with sample data
    sample_context = "The company's revenue in 2019 was $45.2 million."
    sample_question = "What was the revenue in 2019?"

    print("\n" + "="*80)
    print("Sample prompts:")
    print("="*80)

    for prompt_type in ["simple", "instruction", "fewshot", "cot"]:
        print(f"\n--- {prompt_type.upper()} PROMPT ---")
        prompt_fn = get_prompt(prompt_type)
        prompt = prompt_fn(sample_context, sample_question)
        print(prompt[:300] + "..." if len(prompt) > 300 else prompt)
