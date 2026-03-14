import hashlib
from pathlib import Path

from config.config import settings
from models.embeddings import EmbeddingModel
from models.llm import LLMClient
from utils.chunker import ResumeChunker
from utils.loader import ResumeLoader
from utils.retriever import ResumeRetriever
from utils.vector_store import FAISSVectorStoreManager
from utils.router import route_query
from utils.tools import job_tool, resume_tool, tutorial_tool, web_tool


class ResumeRAGPipeline:
    """End-to-end RAG workflow for resume-based question answering."""

    PROMPT_TEMPLATE = """You are an AI resume assistant.
Answer only from the context.
If the answer is not present in the context, say: I cannot find that in the uploaded resume.

Context:
{context}

Question:
{question}
"""

    CAREER_ASSISTANT_PROMPT = """You are an AI career assistant.
Use the information provided to answer clearly and helpfully.

Resume context:
{resume_context}

External info:
{external_info}

Question:
{question}
"""

    def __init__(self):
        self.loader = ResumeLoader()
        self.chunker = ResumeChunker()
        self.embeddings = EmbeddingModel().get_embeddings()
        self.llm = LLMClient()
        self.vector_store_manager = None
        self.retriever = None

    def _index_dir_for_file(self, file_path: Path) -> Path:
        file_hash = hashlib.md5(file_path.read_bytes()).hexdigest()[:10]
        return settings.VECTOR_DB_PATH / f"resume_{file_hash}"

    def build_from_upload(self, uploaded_file):
        file_path = self.loader.save_uploaded_file(uploaded_file)
        documents = self.loader.load_pdf(file_path)
        chunks = self.chunker.split_documents(documents)

        index_dir = self._index_dir_for_file(file_path)
        self.vector_store_manager = FAISSVectorStoreManager(self.embeddings, index_dir)
        vector_store = self.vector_store_manager.build_or_load(chunks)
        self.retriever = ResumeRetriever(vector_store, top_k=settings.TOP_K)

        return {
            "file_path": str(file_path),
            "documents": len(documents),
            "chunks": len(chunks),
            "index_dir": str(index_dir),
        }

    def build_from_file_path(self, file_path: Path):
        """Build or load a vector index from a PDF file path."""
        documents = self.loader.load_pdf(file_path)
        chunks = self.chunker.split_documents(documents)

        index_dir = self._index_dir_for_file(file_path)
        self.vector_store_manager = FAISSVectorStoreManager(self.embeddings, index_dir)
        vector_store = self.vector_store_manager.build_or_load(chunks)
        self.retriever = ResumeRetriever(vector_store, top_k=settings.TOP_K)

        return {
            "file_path": str(file_path),
            "documents": len(documents),
            "chunks": len(chunks),
            "index_dir": str(index_dir),
        }

    def ask(self, question: str) -> str:
        if not self.retriever:
            return "Please upload and index a resume first."

        retrieved_docs = self.retriever.retrieve(question)
        context = "\n\n".join(doc.page_content for doc in retrieved_docs)
        prompt = self.PROMPT_TEMPLATE.format(context=context, question=question)
        return self.llm.invoke(prompt)

    def _get_resume_context(self, question: str) -> str:
        if not self.retriever:
            return ""
        retrieved_docs = self.retriever.retrieve(question)
        return "\n\n".join(doc.page_content for doc in retrieved_docs)

    def answer_question(self, question: str) -> str:
        route = route_query(question)

        if route == "resume":
            return resume_tool(self, question)

        if route == "job":
            external_info = job_tool(question)
            prompt = self.CAREER_ASSISTANT_PROMPT.format(
                resume_context="",
                external_info=external_info,
                question=question,
            )
            return self.llm.generate(prompt)

        if route == "web":
            external_info = web_tool(question)
            prompt = self.CAREER_ASSISTANT_PROMPT.format(
                resume_context="",
                external_info=external_info,
                question=question,
            )
            return self.llm.generate(prompt)

        if route == "tutorial":
            external_info = tutorial_tool(question)
            prompt = self.CAREER_ASSISTANT_PROMPT.format(
                resume_context="",
                external_info=external_info,
                question=question,
            )
            return self.llm.generate(prompt)

        if route == "hybrid":
            resume_context = self._get_resume_context(question)
            external_info = web_tool(question)
            prompt = self.CAREER_ASSISTANT_PROMPT.format(
                resume_context=resume_context,
                external_info=external_info,
                question=question,
            )
            return self.llm.generate(prompt)

        return "Could not route the question."
