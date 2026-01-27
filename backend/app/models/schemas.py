from pydantic import BaseModel
from typing import List, Optional


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    document_id: Optional[str] = None  # Filter queries to specific document


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    sources: Optional[List[str]] = []


class DocumentInfo(BaseModel):
    id: str
    filename: str
    upload_date: str
    status: str


class UploadResponse(BaseModel):
    message: str
    document_id: str
    filename: str

