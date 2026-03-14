# Deploying to Streamlit Community Cloud

## Prerequisites

1. Push your code to a **GitHub** repository.
2. Create a [Streamlit Cloud](https://share.streamlit.io/) account (free).

## Step 1: Prepare the Repository

Ensure your project has:

- `app.py` as the main entry point (Streamlit runs this by default)
- `requirements.txt` with all dependencies
- A `.streamlit/config.toml` (optional, for theme/settings)

## Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
2. Click **"New app"**.
3. Fill in:
   - **Repository**: `your-username/ai_resume_skill_analyzer` (or your repo name)
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `app.py`
   - **App URL**: optional custom subdomain
4. Click **"Advanced settings"** and add **Secrets** (environment variables).

## Step 3: Set Secrets (Environment Variables)

In Streamlit Cloud, go to your app → **Settings** → **Secrets**, or add them when creating the app.

Create a `.streamlit/secrets.toml` file locally (and add it to `.gitignore` so it is not committed), or use the Cloud UI to paste:

```toml
# .streamlit/secrets.toml (for local testing; use Cloud Secrets UI for production)

ADMIN_EMAIL = "admin@yourdomain.com"
ADMIN_PASSWORD = "your_secure_admin_password"

GROQ_API_KEY = "your_groq_api_key"
TAVILY_API_KEY = "your_tavily_api_key"  # if using Tavily search
```

**In Streamlit Cloud**, use the Secrets editor (Settings → Secrets) and add in TOML format:

```toml
ADMIN_EMAIL = "admin@yourdomain.com"
ADMIN_PASSWORD = "your_secure_admin_password"
GROQ_API_KEY = "gsk_xxxxx"
TAVILY_API_KEY = "tvly_xxxxx"
```

Streamlit Cloud also supports setting these as environment variables in your deployment platform if you deploy elsewhere.

## Step 4: Database and File Storage

- **SQLite** (`app.db`) is created in the app’s working directory.
- On Streamlit Cloud, the filesystem is **ephemeral**: data is lost when the app restarts or is redeployed.
- For persistent data, use an external database (e.g. PostgreSQL on Supabase, Neon, or Railway) and switch from SQLite to that backend.

## Step 5: Vector DB and Data Directory

- FAISS indices and uploaded resumes are stored under `data/` and `data/faiss_index/`.
- On Streamlit Cloud, these are also ephemeral.
- For production, consider:
  - Cloud object storage (S3, GCS) for resume files
  - A hosted vector DB (Pinecone, Weaviate, etc.) instead of local FAISS

## Step 6: Deploy

1. Click **"Deploy"**.
2. Wait for the build to finish (first run can take a few minutes).
3. Open the app URL (e.g. `https://your-app-name.streamlit.app`).

## Troubleshooting

| Issue | Fix |
|------|-----|
| Build fails | Check `requirements.txt` and Python version (Streamlit uses 3.11 by default) |
| "Pipeline initialization failed" | Ensure `GROQ_API_KEY` (and other API keys) are set in Secrets |
| Admin login fails | Verify `ADMIN_EMAIL` and `ADMIN_PASSWORD` in Secrets |
| App is slow | First load downloads models (e.g. sentence-transformers); consider a smaller embedding model |

## Optional: Python Version

To pin Python, add a `runtime.txt` in the project root:

```
python-3.11
```

## Optional: `.streamlit/config.toml`

```toml
[theme]
primaryColor = "#4a90d9"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#262730"

[server]
headless = true
```
