from ingestion.docling_loader import DoclingLoader
from ingestion.chunker import StructureChunker
from schemas.chunk import Chunk


class IngestionPipeline:
    def __init__(self):
        self.loader = DoclingLoader()
        self.chunker = StructureChunker()

    def run(self, source: str) -> list[Chunk]:
        # Step 1: Convert document to markdown
        markdown = self.loader.load(source)

        # Step 2: Chunk
        chunks = self.chunker.chunk(source=source, markdown_text=markdown)

        return chunks
    
if __name__ == "__main__":
    pipeline = IngestionPipeline()
    pipeline.loader.__init__()
    document_url_list = [
        "https://arxiv.org/pdf/2604.07236.pdf",
        # "https://arxiv.org/pdf/2511.02645v1.pdf",
        # Add more document URLs or local file paths as needed
    ]
    print("Ingesting documents...")
    results = []
    for i, url in enumerate(document_url_list):
        print(f"Processing document {i + 1}/{len(document_url_list)}: {url}")
        result = pipeline.run(url)
        results.extend(result)
    
    for chunk in results[0:3]:
        print(f"Source: {chunk.source}")
        print(f"Chunk ID: {chunk.id}")
        print("Content:", chunk.content)
        print("Metadata:", chunk.metadata)
        print("-" * 100)