const BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export interface ChatMessage {
    role: "user" | "assistant";
    content: string;
}

export interface ChatUsage {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
}

export interface ChatResponse {
    reply: string;
    on_topic: boolean;
    new_summary: string | null;
    usage?: ChatUsage;
}

export async function sendChat(
    message: string,
    history: ChatMessage[],
    summary: string
): Promise<ChatResponse> {
    const res = await fetch(`${BASE}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, history, summary }),
    });

    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail ?? `HTTP ${res.status}`);
    }

    return res.json();
}
