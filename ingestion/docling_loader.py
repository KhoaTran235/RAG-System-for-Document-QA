from docling.document_converter import DocumentConverter


class DoclingLoader:
    def __init__(self):
        self.converter = DocumentConverter()

    def load(self, source: str) -> str:
        """
        Load document and directly return markdown
        """
        result = self.converter.convert(source)
        document = result.document

        # export luôn ở đây
        markdown = document.export_to_markdown()
        return markdown
    
if __name__ == "__main__":
    # Example usage
    loader = DoclingLoader()
    markdown = loader.load("https://arxiv.org/pdf/2604.07236.pdf") # Either a local file path or a URL
    print(markdown)