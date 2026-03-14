from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader

from config.config import settings


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


class ResumeLoader:
    """Save uploaded resume files and load them as LangChain documents."""

    def __init__(self, data_dir: Path | None = None):
        self.data_dir = data_dir or settings.DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def save_uploaded_file(self, uploaded_file) -> Path:
        file_path = self.data_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path

    def load_documents(self, file_path: Path):
        suffix = file_path.suffix.lower()
        if suffix not in SUPPORTED_EXTENSIONS:
            raise ValueError("Unsupported file type. Use PDF, DOCX, or TXT.")

        if suffix == ".pdf":
            return PyPDFLoader(str(file_path)).load()

        if suffix == ".txt":
            return TextLoader(str(file_path), encoding="utf-8").load()

        # DOCX
        try:
            from langchain_community.document_loaders import Docx2txtLoader
        except Exception as exc:
            raise RuntimeError(
                "DOCX support requires docx2txt. Add it to requirements and install dependencies."
            ) from exc

        return Docx2txtLoader(str(file_path)).load()
