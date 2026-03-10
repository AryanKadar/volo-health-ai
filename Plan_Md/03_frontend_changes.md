# 03 – Frontend Changes

## What Already Exists (Do NOT Break)
- React 18 + Vite + TypeScript + Tailwind CSS + ShadCN UI
- Components: `ChatBubble`, `ChatInput`, `Sidebar`, `TopBar`, `MobileSuggestions`, `TypingIndicator`
- Pages: `Index.tsx` (main chat), `NotFound.tsx`
- Data: `src/lib/chatData.ts` – hardcoded `suggestions` and `answers`

---

## Changes Required

### 1. `vite.config.ts` – Change Port to 5173

```diff
 server: {
   host: "::",
-  port: 8080,
+  port: 5173,
```

### 2. `Frontend/.env` – Add API Base URL (NEW FILE)

```env
VITE_API_BASE_URL=http://localhost:8000
```

> Vite exposes only variables prefixed with `VITE_` to the browser.

### 3. `src/lib/api.ts` – New API Client (NEW FILE)

```typescript
const BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface ChatResponse {
  reply: string;
  usage?: { prompt_tokens: number; completion_tokens: number; total_tokens: number };
}

export async function sendChat(
  message: string,
  history: ChatMessage[]
): Promise<ChatResponse> {
  const res = await fetch(`${BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, history }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ?? `HTTP ${res.status}`);
  }
  return res.json();
}
```

### 4. `src/pages/Index.tsx` – Replace Hardcoded Answers with API call

**Old flow:**
```typescript
const answer = answers[text] || "Thank you for your question...";
addAssistantReply(answer);
```

**New flow:**
```typescript
const handleSend = useCallback(async (text: string) => {
  const userMsg = { id: crypto.randomUUID(), role: "user" as const, content: text };
  setMessages(prev => [...prev, userMsg]);
  setTyping(true);
  try {
    const history = messages.map(m => ({ role: m.role, content: m.content }));
    const { reply } = await sendChat(text, history);
    setMessages(prev => [...prev, { id: crypto.randomUUID(), role: "assistant", content: reply }]);
  } catch (e) {
    setMessages(prev => [...prev, {
      id: crypto.randomUUID(),
      role: "assistant",
      content: "Sorry, I couldn't connect to the server. Please try again."
    }]);
  } finally {
    setTyping(false);
  }
}, [messages]);
```

> **Note:** `handleSend` becomes `async`. The `addAssistantReply` helper and the `setTimeout` simulation are removed. `chatData.ts` `answers` import is removed (suggestions stay).

### 5. `src/lib/chatData.ts` – Keep Suggestions, Remove Answers

The `answers` export is no longer needed. Remove it to keep the file clean.  
The `suggestions` array and `Message` interface remain unchanged.

---

## Files Changed Summary

| File                      | Change Type | Description                               |
|---------------------------|-------------|-------------------------------------------|
| `Frontend/.env`           | NEW         | `VITE_API_BASE_URL`                       |
| `src/lib/api.ts`          | NEW         | Fetch wrapper for `/api/chat`             |
| `src/pages/Index.tsx`     | MODIFY      | Async API call, remove hardcoded lookup   |
| `src/lib/chatData.ts`     | MODIFY      | Remove `answers` export                   |
| `vite.config.ts`          | MODIFY      | Port 8080 → 5173                          |

---

## No Visual Changes
All visual components remain identical. The only behavioural change is that answers now come from the Azure OpenAI API via the FastAPI backend instead of from a local dictionary.
