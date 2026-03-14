from utils.job_search import search_jobs
from utils.web_search import search_tutorials, search_web


def resume_tool(pipeline, question: str) -> str:
    """Answer from the uploaded resume using the RAG pipeline."""
    return pipeline.ask(question)


def web_tool(question: str) -> str:
    """Answer using general web search results."""
    return search_web(question)


def tutorial_tool(question: str) -> str:
    """Answer using tutorial-focused web search results."""
    return search_tutorials(question)


def job_tool(question: str) -> str:
    """Answer using job-focused search results."""
    return search_jobs(question)
