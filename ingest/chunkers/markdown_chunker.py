from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from .base_chunker import BaseChunker

class MarkdownChunker(BaseChunker):

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.MARKDOWN, 
            chunk_size=800, chunk_overlap=100
            )

    def chunk(self, document: Document) -> list[Document]:

        chunks = []
        split_texts = self.splitter.split_text(document.page_content)
        for _, text in enumerate(split_texts):

            metadata = document.metadata.copy()
            chunks.append(Document(page_content=text, metadata=metadata))

        return chunks