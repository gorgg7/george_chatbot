from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
import logging
from chatbot import rag_chat_bot  
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
load_dotenv(override=True)

app = FastAPI(title="RAG Chatbot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str
@app.post("/rag-chaat")
async def rag_chat_post(request: ChatRequest):
    try:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="API key not found")

        response = rag_chat_bot(api_key=api_key, question=request.question)
        return {
            "success": True,
            "question": request.question,
            "response": response
            
        }

    except Exception as e:
        logging.error(f"RAG Chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/healthz")
def health():
    return {"status": "ok"}
@app.get("/")
def read_root():
    return {"message": "API is running!"}
