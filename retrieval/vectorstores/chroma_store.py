# retrieval/vectorstores/chroma_store.py
import chromadb
from typing import List
from schemas.chunk import Chunk
from retrieval.vectorstores.base import BaseVectorStore



class ChromaStore(BaseVectorStore):
    def __init__(self, collection_name="rag_collection", persist_dir="./chroma_db", embedding_function=None):
        self.client = chromadb.Client(
            settings=chromadb.config.Settings(
                persist_directory=persist_dir
            )
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

        self.embedding_function = embedding_function

    def add_documents(self, chunks: List[Chunk]):
        ids = [str(chunk.id) for chunk in chunks]
        documents = [chunk.content for chunk in chunks]
        metadatas = [
            {
                "source": chunk.source,
                **chunk.metadata
            }
            for chunk in chunks
        ]

        embeddings = self.embedding_function.embed_documents(documents)
        

        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )

    def similarity_search(self, query: str, k: int = 5):
        query_embedding = self.embedding_function.embed_query(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )

        return results
    
if __name__ == "__main__":
    # Example usage
    from embedding.gemini_embedder import GeminiEmbedder

    embedding_function = GeminiEmbedder(model_name="gemini-embedding-2-preview")
    chroma_store = ChromaStore(embedding_function=embedding_function)

    # Add some documents
    chunks = [
        Chunk(id=1, content="This is the first document. The first document talks about the capital of France.", source="doc1", metadata={"author": "Alice"}),
        Chunk(id=2, content="This is the second document. The second document talks about the population of HoChiMinh City.", source="doc2", metadata={"author": "Bob"}),
        Chunk(id=3, content="This is the third document. The third document talks about the capital of Vietnam.", source="doc3", metadata={"author": "Charlie"})
    ]
    chroma_store.add_documents(chunks)
    # print("Retrieved documents from chroma store by id:")
    # for chunk in chunks:
    #     retrieved = chroma_store.collection.get(ids=[str(chunk.id)], include=["embeddings"])
    #     print(retrieved)

    # Perform a similarity search
    query = "Tell me about cities of Vietnam?"
    results = chroma_store.similarity_search(query, k=2)
    print(results)