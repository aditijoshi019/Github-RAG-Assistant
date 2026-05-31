from fastapi import FastAPI
from app.api.analyze import router

app = FastAPI()

app.include_router(router)

@app.get("/")
def home():
    return {"message": "GitHub RAG backend running"}