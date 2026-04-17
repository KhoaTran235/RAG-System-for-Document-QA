# retrieval/retrievers/vector_retriever.py
from typing import List
from schemas.chunk import Chunk


class VectorRetriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(self, query: str, k: int = 5) -> List[Chunk]:
        results = self.vector_store.similarity_search(query, k)

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        ids = results["ids"][0]
        print(ids)

        chunks = []
        for doc, meta, _id in zip(documents, metadatas, ids):
            chunks.append(
                Chunk(
                    id=_id,
                    content=doc,
                    source=meta.get("source", ""),
                    metadata=meta
                )
            )
        return chunks