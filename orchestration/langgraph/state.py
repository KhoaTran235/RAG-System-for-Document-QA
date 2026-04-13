from typing import TypedDict, List, Optional
from schemas.chunk import Chunk


class RAGState(TypedDict, total=False):
    query: str
    rewritten_query: Optional[str]
    documents: List[Chunk]
    answer: str