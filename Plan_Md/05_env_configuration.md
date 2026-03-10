# 05 – Environment Configuration

## Backend `.env` (`Backend/.env`)

```env
# ── Azure OpenAI ──────────────────────────────────────────────────
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_API_BASE=https://admin-mbkfse6c-eastus2.cognitiveservices.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5-chat
AZURE_OPENAI_API_VERSION=2024-02-01

# ── CORS ──────────────────────────────────────────────────────────
# Comma-separated list of allowed origins (no trailing slash)
CORS_ORIGINS=http://localhost:5173
```

| Variable                      | Description                                               |
|-------------------------------|-----------------------------------------------------------|
| `AZURE_OPENAI_API_KEY`        | API key for Azure Cognitive Services endpoint             |
| `AZURE_OPENAI_API_BASE`       | Full Azure endpoint URL                                    |
| `AZURE_OPENAI_DEPLOYMENT_NAME`| Deployment name (model alias on Azure)                    |
| `AZURE_OPENAI_API_VERSION`    | Azure OpenAI REST API version                             |
| `CORS_ORIGINS`                | Comma-separated allowed frontend origins                  |

---

## Frontend `.env` (`Frontend/.env`)

```env
# ── Backend API ───────────────────────────────────────────────────
VITE_API_BASE_URL=http://localhost:8000
```

| Variable            | Description                              |
|---------------------|------------------------------------------|
| `VITE_API_BASE_URL` | Base URL for the FastAPI backend server  |

> **Important:** All Vite env variables **must** start with `VITE_` to be exposed in the browser bundle. Never put secrets in the frontend `.env`.

---

## Git Security

Add both `.env` files to `.gitignore` (project root):

```gitignore
Backend/.env
Frontend/.env
Backend/venv/
```

---

## How the Backend Reads `.env`

In `main.py` and `services/azure_openai.py`, we use `python-dotenv`:

```python
from dotenv import load_dotenv
import os

load_dotenv()  # reads Backend/.env automatically when run from Backend/

api_key   = os.getenv("AZURE_OPENAI_API_KEY")
api_base  = os.getenv("AZURE_OPENAI_API_BASE")
deployment= os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
api_ver   = os.getenv("AZURE_OPENAI_API_VERSION")
cors_str  = os.getenv("CORS_ORIGINS", "http://localhost:5173")
```

## How the Frontend Reads `.env`

```typescript
const BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
```

Vite injects `VITE_*` variables into `import.meta.env` at build time.
