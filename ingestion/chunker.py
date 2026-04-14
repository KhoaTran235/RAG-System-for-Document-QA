from typing import List
from schemas.chunk import Chunk

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

    def chunk(self, source: str, markdown_text: str) -> List[Chunk]:
        splits = self.header_splitter.split_text(markdown_text)
        # splits = self.text_splitter.split_documents(splits)

        # Format output
        results = []
        for i, doc in enumerate(splits):
            results.append(Chunk(
                source=source,
                id=i,
                content=doc.page_content,
                metadata=doc.metadata
            ))

        return results