import os
from fastapi import APIRouter, HTTPException
from models.chat import ChatRequest, ChatResponse, ChatUsage
from services import topic_guard, summarizer, azure_openai

router = APIRouter()

HEALTHCARE_PROMPT = """
You are a helpful healthcare assistant for Volo Health Insurance TPA.
Your role is to help patients prepare for hospitalisation, understand
discharge procedures, and navigate insurance processes.

Guidelines:
- Be empathetic, clear, and professional.
- Focus on Indian healthcare context (CGHS, ECHS, TPA processes).
- For documents, always mention government IDs, insurance cards, and medical reports.
- Always advise patients to consult their treating doctor for medical decisions.
- Keep answers concise (3-5 sentences) unless detail is needed.
- If unsure, say so and recommend contacting the hospital/insurer directly.
"""

@router.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    try:
        # ── STAGE 1: TOPIC GUARD ──────────────────────────────────────────────
        is_relevant, tg_usage = topic_guard.is_healthcare_related(req.message)
        
        if not is_relevant:
            # Off-topic: return redirect, do not update summary
            return ChatResponse(
                reply="I'm here to help with healthcare and hospitalisation topics. Could you ask something related to hospital admission, surgery, discharge, or follow-up care?",
                on_topic=False,
                new_summary=None,
                usage=ChatUsage(**tg_usage)
            )
            
        # ── STAGE 2: MAIN CHAT ────────────────────────────────────────────────
        messages = [{"role": "system", "content": HEALTHCARE_PROMPT.strip()}]
        
        if req.summary:
            messages.append({
                "role": "system", 
                "content": f"Context from earlier conversation:\n{req.summary}"
            })
            
        # Append up to last 6 turns
        for m in req.history[-6:]:
            messages.append({"role": m.role, "content": m.content})
            
        # Append current user message
        messages.append({"role": "user", "content": req.message})
        
        max_tokens = int(os.getenv("AZURE_OPENAI_MAX_COMPLETION_TOKENS", "512"))
        temp = float(os.getenv("AZURE_OPENAI_TEMPERATURE", "0.7"))
        
        ai_reply, main_usage = azure_openai.call_gpt(messages, max_tokens, temp)
        
        # ── STAGE 3: SUMMARY UPDATE ───────────────────────────────────────────
        new_sum_text, sum_usage = summarizer.update_summary(
            current_summary=req.summary,
            user_message=req.message,
            ai_reply=ai_reply
        )
        
        # Combine token usage from all 3 stages for accurate cost tracking
        total_usage = ChatUsage(
            prompt_tokens = tg_usage["prompt_tokens"] + main_usage["prompt_tokens"] + sum_usage["prompt_tokens"],
            completion_tokens = tg_usage["completion_tokens"] + main_usage["completion_tokens"] + sum_usage["completion_tokens"],
            total_tokens = tg_usage["total_tokens"] + main_usage["total_tokens"] + sum_usage["total_tokens"],
        )
        
        return ChatResponse(
            reply=ai_reply,
            on_topic=True,
            new_summary=new_sum_text,
            usage=total_usage
        )
        
    except Exception as e:
        print(f"Error in /api/chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))
