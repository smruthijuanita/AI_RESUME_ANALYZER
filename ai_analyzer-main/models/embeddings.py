from langchain_community.embeddings import HuggingFaceEmbeddings

from config.config import settings


class EmbeddingModel:
    """Creates sentence-transformers embeddings for local RAG indexing."""

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL

    def get_embeddings(self):
        return HuggingFaceEmbeddings(model_name=self.model_name)