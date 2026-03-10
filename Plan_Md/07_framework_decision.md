# 07 – Framework Decision: Why Not LangChain / LangGraph / LangSmith?

## The Question
Should we use **LangChain**, **LangGraph**, or **LangSmith** for the backend?

**Short answer: NO for LangChain/LangGraph, OPTIONAL for LangSmith.**

---

## What Each Framework Does

| Framework    | Purpose                                               | When to use                            |
|--------------|-------------------------------------------------------|----------------------------------------|
| **LangChain**  | High-level abstractions for LLM pipelines: chains, memory, agents, tools | Complex multi-tool agents, RAG pipelines, document QA |
| **LangGraph**  | Graph-based state machine for multi-actor agent flows | Multi-step agents with branching logic, loops, parallel nodes |
| **LangSmith**  | Observability: trace, debug, and monitor LLM calls   | Production monitoring, debugging slow/bad responses |

---

## Why We Are NOT Using LangChain

### 1. Our pipeline is simple and linear
```
LangChain is built for THIS kind of complexity:
  Tool 1 → Tool 2 (if condition A) → Tool 3 (if condition B) → Memory → output
  Web search → Calculator → code executor → human review ...

Our pipeline is just THREE sequential API calls:
  Stage 1: Topic Guard API call
  Stage 2: Main Chat API call
  Stage 3: Summary Update API call

LangChain would wrap these 3 calls in 500+ lines of abstraction
for no benefit. We can write them in 60 lines directly. ✅
```

### 2. LangChain adds token overhead
```
LangChain's built-in prompts and chains inject extra text into
every call. For a demo project, this wastes tokens and makes
prompts harder to inspect and control.

With raw openai SDK, our prompts are EXACTLY what we write. ✅
```

### 3. LangChain memory != our smart history strategy
```
LangChain's ConversationBufferWindowMemory keeps last N messages.
LangChain's ConversationSummaryMemory auto-summarizes.

BUT: neither combines both (recent exact + old summarized) the way
our custom strategy does. And neither has the Topic Guard filter
that prevents off-topic content from polluting the summary.

Building it ourselves = better control + shows deeper understanding. ✅
```

### 4. Azure OpenAI SDK is directly supported
```
from openai import AzureOpenAI     ← works perfectly with Azure

client = AzureOpenAI(
    api_key=...,
    azure_endpoint=...,
    api_version="2024-02-01"
)

response = client.chat.completions.create(
    model="gpt-5-chat",
    messages=[...]
)

No adapter layers needed. No LangChain custom Azure provider. ✅
```

### 5. For an internship evaluation demo — raw SDK impresses more
```
Evaluators who understand AI know that:
  LangChain user  → "good with tools"
  Raw SDK user    → "understands how LLMs actually work"

Building a smart pipeline (topic guard + summary) from scratch
demonstrates far deeper understanding than calling
  chain = ConversationChain(llm=llm, memory=memory)
```

---

## Why We Are NOT Using LangGraph

```
LangGraph is designed for:
  • Multi-actor agent networks (Agent A calls Agent B, Agent C, ...)
  • Stateful workflows with loops and retries
  • Human-in-the-loop approval flows
  • Parallel agent execution

Our app is a single chatbot with 3 sequential API calls.
LangGraph would be enormous overkill — like using a 40-ton crane
to lift a coffee cup.

IF the project later needs:
  • A "claims agent" that calls different specialist sub-agents
  • A document extraction agent + QA agent working in parallel
  → THEN LangGraph makes sense.
```

---

## LangSmith — Optional, Recommended for Demo Video

```
LangSmith is ONLY for observability (not for logic or chain building).
It can be added later WITHOUT changing any code logic.

If we add it:
  • Every GPT call gets traced with timing, tokens, inputs, outputs
  • The 3 stages show up as separate spans in the LangSmith dashboard
  • Great screenshot/recording material for the demo video
  • Helps debug if Topic Guard mis-classifies a question

How to add (just 2 env vars + 1 import):
  LANGCHAIN_TRACING_V2=true
  LANGCHAIN_API_KEY=<your key>
  import langsmith   # auto-wraps openai calls

Decision: SKIP for now, can add in 10 minutes before recording demo. ✅
```

---

## Final Decision Table

| Framework    | Use?            | Reason                                                |
|--------------|-----------------|-------------------------------------------------------|
| LangChain    | ❌ No           | Overkill, adds complexity and token overhead          |
| LangGraph    | ❌ No           | Designed for multi-agent graphs, not a single chatbot |
| LangSmith    | ⚠️ Optional    | Great for demo video tracing — add before recording   |
| `openai` SDK | ✅ Yes (direct) | Simple, full control, native Azure support            |

---

## Our Backend Stack (Final)

```
requirements.txt:
  fastapi          ← web framework
  uvicorn          ← ASGI server
  openai           ← Azure OpenAI SDK (v1.x, native Azure support)
  python-dotenv    ← read .env file
  pydantic         ← request/response validation
  httpx            ← HTTP client (used by openai SDK internally)
  pytest           ← testing

Optional (add later):
  langsmith        ← observability traces for demo video
```
