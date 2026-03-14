from pathlib import Path

from langchain_community.vectorstores import FAISS


class FAISSVectorStoreManager:
    """Builds, saves, and loads a local FAISS vector index."""

    def __init__(self, embeddings, index_dir: Path):
        self.embeddings = embeddings
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self._store = None

    def _index_exists(self) -> bool:
        return (self.index_dir / "index.faiss").exists() and (self.index_dir / "index.pkl").exists()

    def build_or_load(self, documents):
        if self._index_exists():
            self._store = FAISS.load_local(
                str(self.index_dir),
                self.embeddings,
                allow_dangerous_deserialization=True,
            )
            return self._store

        self._store = FAISS.from_documents(documents, self.embeddings)
        self._store.save_local(str(self.index_dir))
        return self._store

    def get_store(self):
        if self._store is None and self._index_exists():
            self._store = FAISS.load_local(
                str(self.index_dir),
                self.embeddings,
                allow_dangerous_deserialization=True,
            )
        return self._store
