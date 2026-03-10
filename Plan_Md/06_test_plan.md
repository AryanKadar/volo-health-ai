# 06 – Test Plan

## Test Location
All test files live in `Plan_Md/` (as required by the project organisation).

---

## 1. Unit / Integration Tests – Python (pytest)

### File: `test_health.py`
Tests the `/health` GET endpoint.

**Run command (from `Backend/` with venv active):**
```bash
cd c:\Users\aryan\OneDrive\Desktop\intern\Backend
venv\Scripts\activate.bat
pip install httpx pytest -q
pytest ../Plan_Md/test_health.py -v
```

**What it covers:**
- Status code is `200`
- Response body has `status: "ok"`
- Response body has `service` key

---

### File: `test_chat_api.py`
Tests the `/api/chat` POST endpoint.

**Run command:**
```bash
pytest ../Plan_Md/test_chat_api.py -v
```

**What it covers:**
- Valid request returns `200` with a `reply` field
- Empty message returns `422` validation error
- History is properly forwarded (checked via response coherence)
- Server error scenario (mocked Azure failure) returns `500`

---

## 2. Manual Browser Tests

### Test A – Basic Chat Flow
1. Run `backend.bat` and `frontend.bat`
2. Open `http://localhost:5173`
3. Click the sidebar question: **"What documents are required for hospital admission?"**
4. ✅ Expected: A detailed AI-generated answer appears in the chat bubble (NOT the old hardcoded text from `chatData.ts`)

### Test B – Free-form Question
1. Type a custom question: **"Is surgery in a non-network hospital covered?"**
2. ✅ Expected: AI gives a real response relevant to Indian health insurance

### Test C – Backend Down Gracefully
1. Stop `backend.bat`
2. Send any message in the frontend
3. ✅ Expected: Error message "Sorry, I couldn't connect to the server. Please try again."

### Test D – CORS Check
1. Open browser DevTools → Network tab
2. Send a chat message
3. ✅ Expected: No CORS errors in the console; `Access-Control-Allow-Origin: http://localhost:5173` header present in response

### Test E – Port Verification
1. ✅ Backend accessible at `http://localhost:8000/health`
2. ✅ Frontend accessible at `http://localhost:5173`

---

## 3. Swagger UI Test
1. Open `http://localhost:8000/docs`
2. Click **POST /api/chat** → **Try it out**
3. Send:
```json
{
  "message": "What happens during discharge?",
  "history": []
}
```
4. ✅ Expected: `200` response with a `reply` string from Azure OpenAI

---

## Test Coverage Matrix

| Test                  | File/Tool           | Automated? |
|-----------------------|---------------------|------------|
| Health endpoint       | `test_health.py`    | ✅ pytest   |
| Chat endpoint (valid) | `test_chat_api.py`  | ✅ pytest   |
| Chat endpoint (422)   | `test_chat_api.py`  | ✅ pytest   |
| Basic chat flow       | Browser manual      | Manual      |
| Free-form question    | Browser manual      | Manual      |
| Backend-down error    | Browser manual      | Manual      |
| CORS headers          | Browser DevTools    | Manual      |
| Port verification     | Browser manual      | Manual      |
| Swagger UI            | Browser manual      | Manual      |
