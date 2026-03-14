from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader

from config.config import settings


class ResumeLoader:
    """Handles upload persistence and PDF loading as LangChain documents."""

    def __init__(self, data_dir: Path | None = None):
        self.data_dir = data_dir or settings.DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def save_uploaded_file(self, uploaded_file) -> Path:
        file_path = self.data_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path

    def load_pdf(self, file_path: Path):
        loader = PyPDFLoader(str(file_path))
        return loader.load()
