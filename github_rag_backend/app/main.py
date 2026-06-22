from fastapi import FastAPI
from app.api.analyze import router
from app.api.chat import (
    router as chat_router
)
app = FastAPI()

app.include_router(router)

app.include_router(
    chat_router
)

@app.get("/")
def home():
    return {"message": "GitHub RAG backend running"}