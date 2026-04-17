# retrieval/retrievers/bm25_retriever.py
from typing import List
from rank_bm25 import BM25Okapi
from schemas.chunk import Chunk


class BM25Retriever:
    def __init__(self, chunks: List[Chunk]):
        self.chunks = chunks
        self.tokenized_corpus = [self._tokenize(chunk.content) for chunk in chunks]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def _tokenize(self, text: str):
        return text.lower().split()

    def retrieve(self, query: str, k: int = 5) -> List[Chunk]:
        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:k]

        return [self.chunks[i] for i in ranked_indices]