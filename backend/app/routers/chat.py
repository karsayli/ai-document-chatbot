from fastapi import APIRouter, HTTPException
import uuid

from app.models.schemas import ChatRequest, ChatResponse
from app.services.rag_service import rag_service

router = APIRouter()

# Simple in-memory conversation storage (use a proper DB in production)
conversations = {}


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle chat messages with RAG"""
    try:
        # Get or create conversation ID
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        # Add user message BEFORE querying to include it in history (optional, or pass current separately)
        # Here we pass the history UP TO this point (excluding current if we want, or including)
        # Let's include current message in history so RAG sees it as "latest"
        current_history = conversations[conversation_id] + [{"role": "user", "content": request.message}]
        
        # Get RAG response with History and Document ID
        response, sources = rag_service.query(
            request.message, 
            history=current_history,
            document_id=request.document_id
        )
        
        # Now Append to storage
        conversations[conversation_id].append({
            "role": "user",
            "content": request.message
        })
        conversations[conversation_id].append({
            "role": "assistant",
            "content": response
        })
        
        return ChatResponse(
            response=response,
            conversation_id=conversation_id,
            sources=sources
        )
    except Exception as e:
        print(f"Chat Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@router.get("/conversation/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history"""
    if conversation_id not in conversations:
        return {"messages": []}
    return {"messages": conversations[conversation_id]}

