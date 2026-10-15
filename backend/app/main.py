import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.routes.chat import router as chat_router
from backend.app.routes.upload import router as upload_router


app = FastAPI(
    title="Zuno API",
    description="AI-powered multilingual chatbot for Indian languages",
    version="1.0.0",
)

origins = [
    o.strip()
    for o in os.getenv(
        "ALLOWED_ORIGINS",
        "http://127.0.0.1:8000,http://localhost:8000",
    ).split(",")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(upload_router)


@app.get("/")
async def root():
    return {
        "project": "Zuno",
        "status": "running",
        "message": "Welcome to the Zuno Multilingual Chatbot API!"
    }


if os.path.isdir("frontend"):
    app.mount(
        "/app",
        StaticFiles(directory="frontend", html=True),
        name="frontend",
    )