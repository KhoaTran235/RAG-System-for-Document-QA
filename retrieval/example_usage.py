from retrieval.vectorstores.chroma_store import ChromaStore
from embedding.gemini_embedder import GeminiEmbedder

from schemas.chunk import Chunk

from retrieval.retrievers.bm25_retriever import BM25Retriever
from retrieval.retrievers.vector_retriever import VectorRetriever
from retrieval.retrievers.hybrid_retriever import HybridRetriever


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

    # # Perform a similarity search
    # query = "Tell me about cities of Vietnam?"
    # results = chroma_store.similarity_search(query, k=3)
    # print(results)

    # bm25 = BM25Retriever(chunks)
    vector = VectorRetriever(chroma_store)

    # hybrid = HybridRetriever(bm25, vector, alpha=0.6)

    results = vector.retrieve("Tell me about cities of Vietnam?", k=2)

    for r in results:
        print(r)