from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str
    content: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"role": "user", "content": "What documents do I need?"}
        }
    )

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    history: List[ChatMessage]
    summary: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "What about surgery?",
                "history": [],
                "summary": "Patient asked about admission documents."
            }
        }
    )

class ChatUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatResponse(BaseModel):
    reply: str
    on_topic: bool
    new_summary: Optional[str] = None
    usage: Optional[ChatUsage] = None
