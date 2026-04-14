# retrieval/vectorstores/base.py
from abc import ABC, abstractmethod
from typing import List
from schemas.chunk import Chunk


class BaseVectorStore(ABC):

    @abstractmethod
    def add_documents(self, chunks: List[Chunk], embeddings: List[List[float]]):
        pass

    @abstractmethod
    def similarity_search(self, query_embedding: List[float], k: int):
        pass