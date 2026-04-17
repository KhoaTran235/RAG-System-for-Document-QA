# retrieval/retrievers/hybrid_retriever.py
from typing import List, Dict
from schemas.chunk import Chunk


class HybridRetriever:
    def __init__(self, bm25_retriever, vector_retriever, alpha=0.5):
        """
        alpha: weight for vector score
        (1 - alpha): weight for BM25
        """
        self.bm25 = bm25_retriever
        self.vector = vector_retriever
        self.alpha = alpha

    def _normalize(self, scores: List[float]):
        # if not scores:
        #     return scores
        min_s, max_s = min(scores), max(scores)
        if max_s - min_s == 0:
            return [1.0] * len(scores)
        return [(s - min_s) / (max_s - min_s) for s in scores]

    def retrieve(self, query: str, k: int = 5) -> List[Chunk]:
        # --- BM25 ---
        bm25_chunks = self.bm25.chunks
        bm25_scores = self.bm25.bm25.get_scores(query.lower().split())

        # --- Vector ---
        vec_results = self.vector.vector_store.similarity_search(query, k=20)
        vec_docs = vec_results["documents"][0]
        vec_metas = vec_results["metadatas"][0]
        vec_ids = vec_results["ids"][0]
        vec_scores = vec_results["distances"][0] if "distances" in vec_results else [1.0]*len(vec_ids)

        # normalize
        bm25_scores_norm = self._normalize(bm25_scores)
        vec_scores_norm = self._normalize(vec_scores)

        # map id -> score
        score_map: Dict[str, float] = {}

        # BM25 scores
        for chunk, score in zip(bm25_chunks, bm25_scores_norm):
            score_map[str(chunk.id)] = (1 - self.alpha) * score

        # Vector scores
        for _id, score in zip(vec_ids, vec_scores_norm):
            score_map[_id] = score_map.get(_id, 0) + self.alpha * score

        # build chunk map
        chunk_map = {str(c.id): c for c in bm25_chunks}

        # add vector-only chunks
        for doc, meta, _id in zip(vec_docs, vec_metas, vec_ids):
            if _id not in chunk_map:
                chunk_map[_id] = Chunk(
                    id=_id,
                    content=doc,
                    source=meta.get("source", ""),
                    metadata=meta
                )

        # rank
        ranked = sorted(score_map.items(), key=lambda x: x[1], reverse=True)[:k]

        return [chunk_map[_id] for _id, _ in ranked]