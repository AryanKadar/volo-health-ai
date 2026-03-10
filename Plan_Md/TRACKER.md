# 📋 Plan Tracker – Volo Health AI

> **Last Updated:** 2026-03-10  
> This file tracks which plan documents have been written, reviewed, and implemented.

---

## 📁 Plan Documents Status

| # | File | Status | Description | Notes |
|---|------|--------|-------------|-------|
| 00 | [00_overview.md](./00_overview.md) | ✅ Done | Project overview, folder layout, pipeline diagram | Updated to v2 |
| 01 | [01_backend_setup.md](./01_backend_setup.md) | ✅ Done | FastAPI + venv + 3 service files + pseudocode | Updated to v2 |
| 02 | [02_api_endpoints.md](./02_api_endpoints.md) | ✅ Done | Full API spec + 3-stage pipeline + history strategy | Updated to v2 |
| 03 | [03_frontend_changes.md](./03_frontend_changes.md) | ✅ Done | Frontend diff: api.ts, Index.tsx, port, chatData | Needs summary state update |
| 04 | [04_batch_scripts.md](./04_batch_scripts.md) | ✅ Done | backend.bat + frontend.bat with colored output | Ready to implement |
| 05 | [05_env_configuration.md](./05_env_configuration.md) | ✅ Done | All env vars: Backend .env + Frontend .env | Ready |
| 06 | [06_test_plan.md](./06_test_plan.md) | ✅ Done | Manual + automated test coverage matrix | — |
| 07 | [07_framework_decision.md](./07_framework_decision.md) | ✅ Done | Why raw openai SDK, no LangChain/LangGraph | — |

---

## 🧪 Test Files Status

| File | Location | Status | Notes |
|------|----------|--------|-------|
| `test_health.py` | `Test/` | ✅ Written | Path corrected from Plan_Md |
| `test_chat_api.py` | `Test/` | ✅ Written | Updated for v2 API (summary + on_topic fields) |
| `test_gpt_connection.py` | `Test/` | ✅ Written | Live Azure OpenAI connectivity test |

---

## 🔨 Implementation Status

### Backend (`Backend/`)

| Task | Status | File |
|------|--------|------|
| Python venv created | ✅ Done | `Backend/venv/` |
| `requirements.txt` | ✅ Done | `Backend/requirements.txt` |
| `.env` updated (CORS + token limits) | ✅ Done | `Backend/.env` |
| `main.py` – FastAPI app + CORS | ✅ Done | `Backend/main.py` |
| `models/chat.py` – Pydantic models | ✅ Done | `Backend/models/chat.py` |
| `services/azure_openai.py` – base GPT call | ✅ Done | `Backend/services/azure_openai.py` |
| `services/topic_guard.py` – Stage 1 | ✅ Done | `Backend/services/topic_guard.py` |
| `services/summarizer.py` – Stage 3 | ✅ Done | `Backend/services/summarizer.py` |
| `routers/health.py` – GET /health | ✅ Done | `Backend/routers/health.py` |
| `routers/chat.py` – POST /api/chat | ✅ Done | `Backend/routers/chat.py` |

### Frontend (`Frontend/`)

| Task | Status | File |
|------|--------|------|
| `vite.config.ts` port → 5173 | ✅ Done | `Frontend/vite.config.ts` |
| `Frontend/.env` created | ✅ Done | `Frontend/.env` |
| `src/lib/api.ts` created | ✅ Done | `Frontend/src/lib/api.ts` |
| `src/pages/Index.tsx` updated | ✅ Done | `Frontend/src/pages/Index.tsx` |
| `src/lib/chatData.ts` cleaned | ✅ Done | `Frontend/src/lib/chatData.ts` |
| Markdown UI and Styling | ✅ Done | `Frontend/src/components/ChatBubble.tsx` |

### Root Scripts

| Task | Status | File |
|------|--------|------|
| `backend.bat` | ✅ Done | `intern/backend.bat` |
| `frontend.bat` | ✅ Done | `intern/frontend.bat` |

---

## ✅ Pre-Implementation Checklist

- [x] All plan docs written and reviewed
- [x] Test files created in `Test/` folder
- [x] GPT-5-chat connectivity test script created
- [x] GPT-5-chat connection test PASSED ← **run this before implementing**
- [x] Backend .env updated with token limits
- [x] Python venv created and packages installed

---

## 🚦 Next Steps (In Order)

1. **Run** `Test/test_gpt_connection.py` → confirm Azure OpenAI works ← **DO FIRST**
2. **Create** Python venv in `Backend/`
3. **Implement** backend files (follow order in Implementation Status table above)
4. **Update** frontend files
5. **Create** batch scripts at root
6. **Run** `backend.bat` + verify `http://localhost:8000/health`
7. **Run** `frontend.bat` + verify `http://localhost:5173`
8. **Run** pytest tests in `Test/`
9. **Update** this tracker as each task is completed ✅

---

## 📊 Overall Progress

```
Planning:       ████████████████████ 100%  (8/8 docs done)
Pre-Setup:      ████████████████████ 100%  (venv, env, tests)
Backend:        ████████████████████ 100%  (implemented)
Frontend:       ████████████████████ 100%  (implemented)
Root Scripts:   ████████████████████ 100%  (implemented)
Tests:          ████████████████████ 100%  (all passed)
```
