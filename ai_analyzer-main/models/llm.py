from config.config import settings


class LLMClient:
    """Provider-agnostic LLM wrapper (Groq, OpenAI, or Ollama)."""

    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.llm = self._build_client()

    def _build_client(self):
        if self.provider == "groq":
            if not settings.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY is required when LLM_PROVIDER=groq")
            from langchain_groq import ChatGroq

            return ChatGroq(
                api_key=settings.GROQ_API_KEY,
                model=settings.GROQ_MODEL,
                temperature=0,
            )

        if self.provider == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                api_key=settings.OPENAI_API_KEY,
                model=settings.OPENAI_MODEL,
                temperature=0,
            )

        if self.provider == "ollama":
            from langchain_ollama import ChatOllama

            return ChatOllama(
                model=settings.OLLAMA_MODEL,
                base_url=settings.OLLAMA_BASE_URL,
                temperature=0,
            )

        raise ValueError("Unsupported LLM_PROVIDER. Use 'groq', 'openai', or 'ollama'.")

    def invoke(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)
        return response.content if hasattr(response, "content") else str(response)

    def generate(self, prompt: str) -> str:
        return self.invoke(prompt)