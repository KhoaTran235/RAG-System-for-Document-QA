from typing import List
from schemas.message import Message
from schemas.summary import Summary

from generation.prompt.templates.rag import (
    RAG_SYSTEM_PROMPT,
    RAG_USER_TEMPLATE
)
from generation.prompt.templates.rewrite import (
    REWRITE_SYSTEM_PROMPT,
    REWRITE_USER_TEMPLATE
)
from generation.prompt.templates.summary import (
    SUMMARY_SYSTEM_PROMPT,
    SUMMARY_USER_TEMPLATE
)





# ========================
# Helper
# ========================

def format_history(messages: List[Message], max_turns: int = 5) -> str:
    """
    Convert message list → plain text history
    """
    if not messages:
        return ""

    selected = messages[-max_turns:]

    lines = []
    for m in selected:
        role = m.role.capitalize()
        lines.append(f"{role}: {m.content}")

    return "\n".join(lines)


# ========================
# Prompt Builder
# ========================

class PromptBuilder:

    # ---------- RAG ----------
    def build_rag_prompt(
        self,
        query: Message,
        context: str,
        chat_history: List[Message]
    ) -> List[Message]:

        history = chat_history[-5:] if chat_history else []

        user_content = RAG_USER_TEMPLATE.format(
            context=context,
            query=query.content
        )

        return [
            Message(role="system", content=RAG_SYSTEM_PROMPT.strip()),
            *history,
            Message(role="user", content=user_content.strip())
        ]

    # ---------- REWRITE ----------
    def build_rewrite_prompt(
        self,
        query: Message,
        chat_history: List[Message]
    ) -> List[Message]:

        history_text = format_history(chat_history, max_turns=5)

        user_content = REWRITE_USER_TEMPLATE.format(
            history=history_text,
            query=query.content
        )

        return [
            Message(role="system", content=REWRITE_SYSTEM_PROMPT.strip()),
            Message(role="user", content=user_content.strip())
        ]

    # ---------- SUMMARY ----------
    def build_summary_prompt(
        self,
        chat_history: List[Message],
        prev_summary: Summary = None
    ) -> List[Message]:

        history_text = format_history(chat_history, max_turns=20)

        user_content = SUMMARY_USER_TEMPLATE.format(
            history=history_text,
            prev_summary=prev_summary.content if prev_summary else ""
        )

        return [
            Message(role="system", content=SUMMARY_SYSTEM_PROMPT.strip()),
            Message(role="user", content=user_content.strip())
        ]