from dotenv import load_dotenv
import os

from google import genai
from typing import List, Optional

load_dotenv()

class GeminiEmbedder():
    # Gemini embedding 2
    def __init__(self, model_name):
        self.model_name = model_name
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )
    
    # ======================
    # Internal helpers
    # ======================
    def _format_query(self, query: str, task_type: str = "search") -> str:
        if task_type == "search":
            return f"task: search result | query: {query}"
        elif task_type == "qa":
            return f"task: question answering | query: {query}"
        elif task_type == "fact_check":
            return f"task: fact checking | query: {query}"
        elif task_type == "classification":
            return f"task: classification | query: {query}"
        elif task_type == "similarity":
            return f"task: sentence similarity | query: {query}"
        else:
            return query  # fallback

    def _format_document(self, content: str, title: Optional[str] = None, task_type: str = "search") -> str:
        if task_type in ["search", "qa", "fact_check"]:
            title = title or "none"
            return f"title: {title} | text: {content}"
        else:
            # symmetric tasks
            return self._format_query(content, task_type)

    def embed_documents(self, docs: List[str], titles: Optional[List[str]] = None, task_type: str = "search", **kwargs) -> List[List[float]]:
        if titles is not None and len(titles) != len(docs):
            raise ValueError("titles length must match docs length")
        formatted_docs = []
        for i, doc in enumerate(docs):
            title = titles[i] if titles is not None else None
            formatted_doc = self._format_document(doc, title, task_type)
            formatted_docs.append(formatted_doc)

        result = self.client.models.embed_content(
            model=self.model_name,
            contents=formatted_docs
        )

        return [embedding.values for embedding in result.embeddings]

    def embed_query(self, query: str, task_type: str = "search", **kwargs) -> List[float]:
        formatted_query = self._format_query(query, task_type)
        result = self.client.models.embed_content(
            model=self.model_name,
            contents=formatted_query
        )
        return result.embeddings[0].values
    
if __name__ == "__main__":    
    # Example usage
    model_name = "gemini-embedding-2-preview"
    embedder = GeminiEmbedder(model_name)
    contents= [
            "What is the meaning of life?",
            "What is the purpose of existence?",
            "How do I bake a cake?"
        ]
    result = embedder.embed_documents(contents)
    print(result)