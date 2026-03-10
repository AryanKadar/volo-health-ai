# 01 – Backend Setup (v2 – FastAPI + venv + 3-Stage Pipeline)

## Prerequisites
- Python 3.11 or 3.12 installed and on PATH
- Node.js 18+ for frontend (frontend setup handled by `frontend.bat`)

---

## Step 1 – Create Python Virtual Environment

Open a terminal inside `Backend/`:

```bash
cd c:\Users\aryan\OneDrive\Desktop\intern\Backend
python -m venv venv
```

Activate:
```powershell
.\venv\Scripts\Activate.ps1   # PowerShell
.\venv\Scripts\activate.bat   # CMD
```

---

## Step 2 – Install Dependencies

```bash
pip install -r requirements.txt
```

### `requirements.txt` (final v2)

```
fastapi==0.111.0
uvicorn[standard]==0.30.1
openai==1.40.0
python-dotenv==1.0.1
pydantic==2.8.2
httpx==0.27.0
pytest==8.2.2

# Optional – add before recording demo video for tracing
# langsmith==0.1.83
```

> **Why no LangChain/LangGraph?** See `07_framework_decision.md` for the full reasoning.  
> Short: our 3-stage pipeline is clean, simple, and more impressive without abstraction layers.

---

## Step 3 – Project Structure (v2)

```
Backend/
├── venv/                        ← virtual environment (do NOT commit)
│
├── routers/
│   ├── __init__.py
│   ├── chat.py                  ← POST /api/chat – orchestrates 3 stages
│   └── health.py                ← GET /health
│
├── services/
│   ├── __init__.py
│   ├── azure_openai.py          ← AzureOpenAI client + base call function
│   ├── topic_guard.py           ← Stage 1: GPT topic relevance classifier
│   └── summarizer.py            ← Stage 3: GPT rolling summary updater
│
├── models/
│   ├── __init__.py
│   └── chat.py                  ← Pydantic models (updated with summary field)
│
├── main.py                      ← FastAPI app + CORS + router registration
├── requirements.txt
└── .env                         ← secrets (gitignore)
```

---

## Step 4 – Service Responsibilities

### `services/azure_openai.py`
- Loads `.env` via `python-dotenv`
- Creates one shared `AzureOpenAI(...)` client (singleton)
- Exposes `call_gpt(messages: list, max_tokens: int) → str`
- Used by all 3 stages

### `services/topic_guard.py`
```
Input:  user's raw message (string)
Output: bool (True = on-topic, False = off-topic)

Internally:
  messages = [
    { system: "Classify if related to healthcare/hospitalisation/TPA.
               Reply ONLY: YES or NO" },
    { user: <message> }
  ]
  GPT reply → strip → "YES" → True, else False
```

### `services/summarizer.py`
```
Input:  current_summary (str), user_message (str), ai_reply (str)
Output: updated_summary (str, max 100 words)

Internally:
  messages = [
    { system: "Update the summary with the new Q&A. Max 100 words.
               Omit off-topic content." },
    { user: "Summary so far: <current_summary>
             New Q: <user_message>
             New A: <ai_reply>
             Updated summary:" }
  ]
```

### `routers/chat.py` – 3-Stage Orchestration
```python
# Pseudocode (not final – see implementation)

@router.post("/api/chat")
async def chat(req: ChatRequest):

    # STAGE 1 – Topic Guard
    is_relevant = topic_guard.check(req.message)
    if not is_relevant:
        return ChatResponse(
            reply="I'm here to help with healthcare topics. Please ask about...",
            on_topic=False,
            new_summary=None
        )

    # STAGE 2 – Build messages and call GPT
    messages = build_messages(
        summary=req.summary,
        history=req.history,       # last 6 turns only
        user_message=req.message
    )
    reply = azure_openai.call_gpt(messages)

    # STAGE 3 – Update summary
    new_summary = summarizer.update(
        current=req.summary,
        user_message=req.message,
        ai_reply=reply
    )

    return ChatResponse(reply=reply, on_topic=True, new_summary=new_summary)
```

---

## Step 5 – Environment Variables

The `.env` already has the Azure keys. Add one line for CORS:
```
CORS_ORIGINS=http://localhost:5173
```

See `05_env_configuration.md` for full details.

---

## Step 6 – Run the Backend

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The `backend.bat` script at the root automates all steps.

---

## Step 7 – Verify

| URL | Expected |
|-----|----------|
| `http://localhost:8000/health` | `{"status": "ok", ...}` |
| `http://localhost:8000/docs`   | Swagger UI with `/api/chat` |

---

## Frontend State Management (for reference)

The React frontend manages this state to support the 3-stage pipeline:

```typescript
// In Index.tsx
const [messages, setMessages]     = useState<Message[]>([]);   // full display list
const [history, setHistory]       = useState<ChatMessage[]>([]); // last 6 turns
const [summary, setSummary]       = useState<string>("");        // rolling summary

// Logic:
// After turn 6+: slide history window (keep last 6)
// After each on-topic reply: setSummary(response.new_summary)
// Off-topic reply: don't update history or summary
```
