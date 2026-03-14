# Resume RAG Chatbot (Streamlit)

A clean, modular RAG-based chatbot that analyzes a resume PDF and answers questions using only resume content.

## Project Structure

- `config/config.py` - settings and environment-backed constants
- `models/llm.py` - OpenAI/Ollama LLM wrapper
- `models/embeddings.py` - sentence-transformers embedding wrapper
- `utils/loader.py` - upload persistence + PyPDF loading
- `utils/chunker.py` - recursive chunking
- `utils/vector_store.py` - FAISS build/save/load manager
- `utils/retriever.py` - top-k retriever wrapper
- `utils/rag_pipeline.py` - end-to-end RAG orchestration
- `app.py` - Streamlit UI

## Tech Stack

- Python 3.11
- Streamlit
- LangChain
- FAISS
- sentence-transformers
- PyPDF
- python-dotenv
- OpenAI or Ollama compatible LLM

## Installation

1. Create and activate a virtual environment.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

## Configuration

Create a local `.env` file in the project root (do not commit secrets):

```bash
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama3-8b-8192
```

You can also export variables in your shell if preferred.

### Groq example

```bash
export LLM_PROVIDER=groq
export GROQ_API_KEY=your_groq_api_key
export GROQ_MODEL=llama3-8b-8192
```

### Ollama example

```bash
export LLM_PROVIDER=ollama
export OLLAMA_MODEL=llama3.1:8b
export OLLAMA_BASE_URL=http://localhost:11434
```

### OpenAI example

```bash
export LLM_PROVIDER=openai
export OPENAI_API_KEY=your_openai_api_key
export OPENAI_MODEL=gpt-4o-mini
```

Optional tuning:

```bash
export CHUNK_SIZE=500
export CHUNK_OVERLAP=100
export TOP_K=3
export EMBEDDING_MODEL=all-MiniLM-L6-v2
```

## Run the App

```bash
streamlit run app.py
```

Open: `http://localhost:8501`

## Usage

1. Upload a resume PDF from the app.
2. Click **Build Vector DB**.
3. Ask questions in the input box.
4. Review answers and chat history.

Answers are constrained to retrieved resume context.

## Docker

Build:

```bash
docker build -t resume-rag-chatbot .
```

Run:

```bash
docker run -p 8501:8501 resume-rag-chatbot
```
