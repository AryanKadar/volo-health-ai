# 02 – API Endpoints Specification (v2 – Smart History + Topic Guard)

Base URL: `http://localhost:8000`

---

## 1. Health Check

| Field  | Value     |
|--------|-----------|
| Method | `GET`     |
| Path   | `/health` |
| Auth   | None      |

### Response `200 OK`
```json
{ "status": "ok", "service": "Volo Health AI Backend" }
```

---

## 2. Chat – Send Message (with Topic Guard + Smart History)

| Field  | Value              |
|--------|--------------------|
| Method | `POST`             |
| Path   | `/api/chat`        |
| Auth   | None (CORS-gated)  |

### Request Body
```json
{
  "message": "What documents are required for hospital admission?",
  "history": [
    {"role": "user",      "content": "Hello"},
    {"role": "assistant", "content": "Hi! How can I help?"}
  ],
  "summary": "Patient asked about surgery prep. AI explained fasting rules and consent forms."
}
```

| Field     | Type             | Required | Description                                              |
|-----------|------------------|----------|----------------------------------------------------------|
| `message` | `string`         | ✅        | The user's latest message (min length 1)                 |
| `history` | `array[Message]` | ✅        | Last 6 conversation turns only (can be `[]`)             |
| `summary` | `string`         | ✅        | GPT-generated summary of all turns before the last 6    |

> `summary` can be `""` (empty string) when the conversation has ≤ 6 turns.

### Response `200 OK` – On-topic answer
```json
{
  "reply": "For hospital admission, you'll need ...",
  "on_topic": true,
  "new_summary": "Patient asked about admission docs. AI listed Aadhaar, insurance card, medical reports.",
  "usage": { "prompt_tokens": 412, "completion_tokens": 156, "total_tokens": 568 }
}
```

### Response `200 OK` – Off-topic rejection
```json
{
  "reply": "I'm here to help with healthcare and hospitalisation topics. Could you ask something related to hospital admission, surgery, discharge, or follow-up care?",
  "on_topic": false,
  "new_summary": null,
  "usage": { "prompt_tokens": 80, "completion_tokens": 28, "total_tokens": 108 }
}
```

| Response Field | Description                                              |
|----------------|----------------------------------------------------------|
| `reply`        | Message to show to the user                             |
| `on_topic`     | `true` = AI answered; `false` = topic guard rejected    |
| `new_summary`  | Updated summary (only on `on_topic: true`)              |
| `usage`        | Token usage for cost tracking                           |

### Response `422 Unprocessable Entity`
Input validation failed (empty message, wrong types).

### Response `500 Internal Server Error`
```json
{"detail": "Azure OpenAI call failed: <error message>"}
```

---

## 3. Processing Pipeline (Internal – inside Backend)

Every `/api/chat` call follows this exact pipeline:

```
STAGE 1 – TOPIC GUARD (GPT-5-chat mini-call)
─────────────────────────────────────────────
messages = [
  { system: "You are a topic classifier for a healthcare assistant.
             Classify if the user's question is related to:
             hospitalisation, surgery, discharge, follow-up care,
             medical documents, health insurance, or TPA processes.
             Reply ONLY with: YES or NO" },
  { user: <user's message> }
]

GPT replies "YES" → proceed to Stage 2
GPT replies "NO"  → return rejection message immediately
                    do NOT add to history or summary
                    stop here ✋

─────────────────────────────────────────────
STAGE 2 – MAIN CHAT (GPT-5-chat full call)
─────────────────────────────────────────────
messages = [
  { system: HEALTHCARE_SYSTEM_PROMPT },
  { user: "Summary of earlier conversation: <summary>" },  ← injected if summary exists
  ... last 6 history turns (verbatim) ...,
  { user: <user's current message> }
]

GPT replies with detailed healthcare answer

─────────────────────────────────────────────
STAGE 3 – SUMMARY UPDATE (GPT-5-chat mini-call)
─────────────────────────────────────────────
Only triggered on-topic answers.

messages = [
  { system: "You are a summarizer. Given an existing summary and a new
             Q&A pair from a healthcare chat, produce an updated concise
             summary. Keep it under 100 words. Omit off-topic content." },
  { user: "Existing summary: <current_summary>
           New Q: <user message>
           New A: <AI reply>
           Updated summary:" }
]

Returns: new_summary string → sent back to frontend to store in state
```

---

## 4. Smart History Strategy (Frontend State)

```
Conversation grows over time:

Turn 1   User: "What docs for admission?"
         AI:   "Aadhaar, insurance card..."

Turn 2   User: "What about surgery prep?"
         AI:   "Fast for 8-12 hours..."

Turn 3   User: "What is discharge like?"
         AI:   "You get a discharge summary..."

Turn 4   User: "What follow-ups are needed?"
         AI:   "Revisit in 7-14 days..."

...

Turn 7   ← summary kicks in here (total > 6)
         Frontend state:
         {
           summary: "Patient asked about admission docs, surgery prep,
                     discharge process, follow-up schedule. [~40 words]",
           history: [last 6 turns verbatim]
         }

Turn 8   summary is updated by backend after each on-topic reply
         history slides forward (oldest of the 6 is dropped)
```

**Why this is better than just sending all messages:**

| Approach            | Tokens Used | Context Quality | Handles Long Chats |
|---------------------|-------------|-----------------|---------------------|
| All messages raw    | High (grows unbounded) | Good        | ❌ Hits token limit |
| Last 10 raw (old)  | Medium      | Good for recent | ❌ Loses early context |
| 6 recent + summary ✅ | Low-Medium | Best of both    | ✅ Infinite history |

---

## 5. Off-topic Query Handling

```
Off-topic queries:
  ❌ NOT added to history array
  ❌ NOT included in summary
  ❌ NOT forwarded to the main healthcare AI
  ✅ Get a polite redirect message
  ✅ Topic guard uses only a tiny token count (~80 tokens)
```

**Examples of what gets blocked:**
- "Write me a Python script"
- "What is the population of India?"
- "Tell me a joke"
- "What is the stock price of Reliance?"

**Examples of what passes through:**
- "What documents do I need for admission?"
- "Is my surgery covered under CGHS?"
- "How long is the discharge process?"
- "Can my family member accompany me?"

---

## 6. Future Endpoints (not in this sprint)

| Endpoint               | Purpose                             |
|------------------------|-------------------------------------|
| `GET /api/suggestions` | Return dynamic quick questions      |
| `POST /api/feedback`   | Thumbs up/down on a response        |
| `POST /api/documents`  | Upload and extract from medical PDF |
