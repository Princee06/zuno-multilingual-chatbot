from fastapi import FastAPI
from backend.app.routes.chat import router as chat_router

app = FastAPI(
    title="Zuno API",
    description="AI-powered multilingual chatbot for Indian languages",
    version="1.0.0",
)

app.include_router(chat_router)


@app.get("/")
async def root():
    return {
        "project": "Zuno",
        "status": "running",
        "message": "Welcome to the Zuno Multilingual Chatbot API!"
    }