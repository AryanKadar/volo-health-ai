import os
from .azure_openai import call_gpt

PROMPT = """
You are a summarizer. Your job is to update a running summary of a healthcare conversation.
You will be given the CURRENT SUMMARY, and the NEW Q&A pair.
Output an updated summary incorporating the new Q&A. 

Rules:
1. Maximum length: 100 words. Keep it strictly concise.
2. Omit conversational filler (hello, thank you, ok).
3. If the new Q&A contains off-topic content, ignore it.
4. Output ONLY the new summary text. No intro/outro formatting.
"""

def update_summary(current_summary: str, user_message: str, ai_reply: str) -> tuple[str, dict]:
    """
    Returns (new_summary_text, usage_dict)
    """
    user_content = (
        f"CURRENT SUMMARY: {current_summary or 'None'}\n\n"
        f"NEW QUESTION: {user_message}\n"
        f"NEW ANSWER: {ai_reply}\n\n"
        "UPDATED SUMMARY:"
    )
    
    messages = [
        {"role": "system", "content": PROMPT.strip()},
        {"role": "user", "content": user_content}
    ]
    
    max_tokens = int(os.getenv("AZURE_OPENAI_SUMMARY_MAX_TOKENS", "150"))
    # Can use same deterministic temp as topic guard for summaries
    temp = float(os.getenv("AZURE_OPENAI_TOPIC_GUARD_TEMPERATURE", "0.0"))
    
    reply, usage = call_gpt(messages, max_tokens=max_tokens, temperature=temp)
    return reply.strip(), usage
