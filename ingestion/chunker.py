from typing import List

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)


class StructureChunker:
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ):
        # Step 1: Split by markdown header
        self.header_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "h1"),
                ("##", "h2"),
                ("###", "h3"),
            ],
            strip_headers=False,  # Retain headers in the content
        )

        # Step 2: Further split into smaller chunks
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def chunk(self, markdown_text: str) -> List[dict]:
        splits = self.header_splitter.split_text(markdown_text)
        # splits = self.text_splitter.split_documents(splits)

        # Format output
        results = []
        for doc in splits:
            results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
            })

        return results