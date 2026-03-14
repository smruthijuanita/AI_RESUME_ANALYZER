import hashlib
from pathlib import Path

from config.config import settings
from resume_loader import ResumeLoader
from utils.chunker import ResumeChunker
from utils.retriever import ResumeRetriever
from utils.vector_store import FAISSVectorStoreManager


loader = ResumeLoader()
chunker = ResumeChunker()


def _index_dir_for_file(file_path: Path) -> Path:
    file_hash = hashlib.md5(file_path.read_bytes()).hexdigest()[:10]
    return settings.VECTOR_DB_PATH / f"resume_{file_hash}"


def build_vector_db_from_upload(pipeline, uploaded_file, user_id=None):
    """Save uploaded resume and build/load FAISS index automatically."""
    file_path = loader.save_uploaded_file(uploaded_file)
    documents = loader.load_documents(file_path)
    chunks = chunker.split_documents(documents)

    index_dir = _index_dir_for_file(file_path)
    embedding_id = str(index_dir)
    pipeline.vector_store_manager = FAISSVectorStoreManager(pipeline.embeddings, index_dir)
    vector_store = pipeline.vector_store_manager.build_or_load(chunks)
    pipeline.retriever = ResumeRetriever(vector_store, top_k=settings.TOP_K)

    if user_id is not None and user_id > 0:
        try:
            from db.database import save_resume, set_resume_uploaded
            save_resume(user_id, str(file_path), embedding_id)
            set_resume_uploaded(user_id, True)
        except Exception:
            pass

    return {
        "file_path": str(file_path),
        "documents": len(documents),
        "chunks": len(chunks),
        "index_dir": embedding_id,
    }
