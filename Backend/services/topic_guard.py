import os
from .azure_openai import call_gpt

PROMPT = """
You are a strict topic classifier for a healthcare assistant.
Classify if the user's question relates to ANY of these topics:
- Hospitalisation
- Surgery
- Discharge
- Follow-up care
- Medical documents (claims, records)
- Health insurance / TPA processes

Reply ONLY with the exact word YES (if related) or NO (if completely unrelated).
Do not explain your reasoning.
"""

def is_healthcare_related(message: str) -> tuple[bool, dict]:
    """
    Returns (True/False, usage_dict)
    """
    messages = [
        {"role": "system", "content": PROMPT.strip()},
        {"role": "user", "content": message.strip()}
    ]
    
    max_tokens = int(os.getenv("AZURE_OPENAI_TOPIC_GUARD_MAX_TOKENS", "5"))
    temp = float(os.getenv("AZURE_OPENAI_TOPIC_GUARD_TEMPERATURE", "0.0"))
    
    reply, usage = call_gpt(messages, max_tokens=max_tokens, temperature=temp)
    
    verdict = reply.strip().upper()
    return (verdict == "YES" or "YES" in verdict), usage
