from config.config import settings


class ResumeRetriever:
    """Thin wrapper around the vector store retriever API."""

    def __init__(self, vector_store, top_k: int | None = None):
        self.vector_store = vector_store
        self.top_k = top_k or settings.TOP_K

    def retrieve(self, query: str):
        retriever = self.vector_store.as_retriever(search_kwargs={"k": self.top_k})
        return retriever.invoke(query)
