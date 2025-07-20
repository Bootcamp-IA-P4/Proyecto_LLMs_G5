from fastapi import FastAPI
from server.api.routes.groq import router 

app = FastAPI(title="LLM Content Generator")

# Rutas disponibles
app.include_router(router, prefix="/api/v1", tags=["ollama"])

@app.get("/")
async def root():
    return {"message": "Content Generator API - Proyecto LLMs"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "content-generator-api"}