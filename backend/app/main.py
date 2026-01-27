import os
from pathlib import Path
from dotenv import load_dotenv

# 1. FORCE LOAD .ENV BEFORE ANYTHING ELSE
# This prevents "API Key Missing" errors in services imported later
env_found = False
possible_paths = [
    Path(".env"),
    Path("backend/.env"),
    Path("../.env")
]

for p in possible_paths:
    if p.exists():
        print(f"LOADING ENV FROM: {p.absolute()}")
        load_dotenv(p)
        env_found = True
        break

if not env_found:
    print("WARNING: No .env file found! API features may fail.")

# Distinguish imports to ensure env is ready
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.routers import chat, documents

app = FastAPI(title="Document Chatbot API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for development simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])

@app.get("/")
async def root():
    return {
        "message": "Document Chatbot API", 
        "gemini_status": "Active" if os.getenv("GOOGLE_API_KEY") else "Inactive"
    }

@app.get("/api/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
