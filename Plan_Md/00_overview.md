# 🏥 Healthcare AI Assistant – Project Overview (v2)

## Project Name
**Volo Health AI** – Agentic AI assistant that helps patients prepare for hospitalisation.

## Goal
Build a complete AI-powered chat application that answers patient questions about:
- Hospital admission documents
- Surgery preparation checklists
- Discharge procedures
- Post-hospitalisation follow-ups

---

## Stack

| Layer       | Technology                                                    |
|-------------|---------------------------------------------------------------|
| Frontend    | React 18 + Vite + TypeScript + Tailwind CSS + ShadCN UI       |
| Backend     | Python 3.11+ · FastAPI · Uvicorn                              |
| AI Engine   | Azure OpenAI SDK (v1.x) · GPT-5-chat deployment              |
| AI Pipeline | Raw `openai` SDK – NO LangChain (see `07_framework_decision.md`) |
| Dev Tools   | Python venv · npm/Node · batch scripts                        |

---

## Folder Layout

```
intern/
├── Backend/                  ← FastAPI application
│   ├── venv/                 ← Python virtual environment (gitignore)
│   ├── routers/
│   │   ├── chat.py           ← POST /api/chat (3-stage pipeline)
│   │   └── health.py         ← GET /health
│   ├── services/
│   │   ├── azure_openai.py   ← AzureOpenAI client wrapper
│   │   ├── topic_guard.py    ← Stage 1: topic relevance check (NEW)
│   │   └── summarizer.py     ← Stage 3: rolling summary update (NEW)
│   ├── models/
│   │   └── chat.py           ← Pydantic schemas (updated for summary field)
│   ├── main.py               ← FastAPI entry point + CORS
│   ├── requirements.txt
│   └── .env                  ← secrets (gitignore)
│
├── Frontend/                 ← React/Vite application
│   ├── src/
│   │   ├── lib/api.ts        ← API client (NEW – replaces hardcoded answers)
│   │   └── ...               ← existing components unchanged except Index.tsx
│   ├── .env                  ← VITE_API_BASE_URL (NEW)
│   └── vite.config.ts        ← port changed to 5173
│
├── Plan_Md/                  ← All planning docs & test scripts
│   ├── 00_overview.md        ← this file
│   ├── 01_backend_setup.md
│   ├── 02_api_endpoints.md
│   ├── 03_frontend_changes.md
│   ├── 04_batch_scripts.md
│   ├── 05_env_configuration.md
│   ├── 06_test_plan.md
│   ├── 07_framework_decision.md   ← Why NOT LangChain (NEW)
│   ├── test_chat_api.py
│   └── test_health.py
│
├── backend.bat               ← launches backend (port 8000)
└── frontend.bat              ← launches frontend (port 5173)
```

---

## How It Works – Full Pipeline (v2)

```
Patient types question
        │
        ▼
  React Frontend (port 5173)
  State: { messages[], history[], summary: string }
        │
        │  POST /api/chat
        │  { message, history (last 6), summary }
        ▼
  FastAPI Backend (port 8000)
        │
        ├─── STAGE 1: TOPIC GUARD ──────────────────────┐
        │    GPT mini-call: "Is this healthcare?"        │
        │    YES → continue                              │
        │    NO  → return polite redirect (stop) ──────→ Frontend shows redirect bubble
        │
        ├─── STAGE 2: MAIN CHAT ────────────────────────┐
        │    messages = [                                │
        │      system: HEALTHCARE_PROMPT,               │
        │      system: "Summary: <summary>",  (if any)  │
        │      ...last 6 turns verbatim...,             │
        │      user: <current message>                  │
        │    ]                                          │
        │    GPT-5-chat → detailed healthcare answer    │
        │
        └─── STAGE 3: SUMMARY UPDATE ───────────────────┐
             GPT mini-call: update rolling summary       │
             (max 100 words, skip off-topic queries)     │
             new_summary → returned in response          │
                   │
                   ▼
  Frontend stores new_summary in state
  Appends AI reply to messages[]
  Slides history window (keeps last 6 turns)
  Renders answer in chat bubble ✅
```

---

## Key Design Decisions (v2)

1. **Azure OpenAI direct SDK** – no LangChain overhead; raw `openai` v1.x gives full control. See `07_framework_decision.md`.
2. **3-stage AI pipeline** – Topic Guard → Main Chat → Summary Update; each stage is one focused GPT call.
3. **Smart history: 6 recent + rolling summary** – best context quality at lowest token cost; handles infinite-length conversations.
4. **Off-topic filter** – rejected queries are NEVER stored in history or summary; keeps the AI context clean.
5. **Summary trigger at turn 7+** – before turn 7, all history fits in 6 slots; summary only activates when needed.
6. **CORS via env variable** – `CORS_ORIGINS=http://localhost:5173` in `Backend/.env`; easy to change for deployment.
7. **Stateless backend** – all state lives in the React frontend; backend is a pure function (input → output).
