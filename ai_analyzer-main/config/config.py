import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


class Settings:
    """Centralized app settings read from environment variables."""

    PROJECT_ROOT = PROJECT_ROOT
    DATA_DIR = PROJECT_ROOT / "data"
    VECTOR_DB_PATH = DATA_DIR / "faiss_index"

    DB_PATH = PROJECT_ROOT / "app.db"

    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))
    TOP_K = int(os.getenv("TOP_K", "3"))

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").strip().lower()

    # ---------- SEARCH ----------
    SEARCH_PROVIDER = os.getenv("SEARCH_PROVIDER", "duckduckgo").strip().lower()
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
    SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")

    # ---------- GROQ ----------
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = os.getenv(
        "GROQ_MODEL",
        "llama-3.1-8b-instant"
    )

    # ---------- AUTH ----------
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@gmail.com")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")


settings = Settings()
DB_PATH = settings.DB_PATH


# Ensure required local folders exist at startup.
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)