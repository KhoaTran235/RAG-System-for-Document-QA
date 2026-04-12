import pytest
from schemas.message import Message
from typing import List

from query.rewrite import QueryRewriter
from generation.prompt.prompt_builder import PromptBuilder
from generation.llm.clients.gemini_client import GeminiClient




# ===== LLM =====
llm = GeminiClient(model_name="gemma-3-1b-it")
promt_builder = PromptBuilder()
rewriter = QueryRewriter(llm=llm, prompt_builder=promt_builder)

# =========================================
# 1. Basic functionality
# =========================================

def test_basic_rewrite():
    expected = "What is the capital of Germany?"
    history = [
        Message(role="user", content="What is the capital of France?"),
        Message(role="assistant", content="The capital of France is Paris.")
    ]
    query = Message(role="user", content="What about Germany?")

    result = rewriter.rewrite(query=query, chat_history=history)

    assert result.content == expected


# =========================================
# 2. Empty history
# =========================================

def test_empty_history():
    expected = "Explain Germany."
    query = Message(role="user", content="Germany?")
    result = rewriter.rewrite(query=query, chat_history=[])

    assert result.content == expected