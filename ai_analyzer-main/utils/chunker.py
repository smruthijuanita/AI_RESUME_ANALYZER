from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.config import settings


class ResumeChunker:
    """Splits documents into RAG-friendly chunks."""

    def __init__(self, chunk_size: int | None = None, chunk_overlap: int | None = None):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )

    def split_documents(self, documents):
        return self.splitter.split_documents(documents)
