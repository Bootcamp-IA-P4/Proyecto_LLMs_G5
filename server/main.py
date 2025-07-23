from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routes.auth import router as auth_router
from server.routes.content import router as content_router
from server.config.settings import settings

app = FastAPI(
    title="AI Social Content Generator",
    description="API para generar contenido de redes sociales con IA",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(content_router, prefix="/api/content", tags=["content"])

@app.get("/")
async def root():
    return {"message": "AI Social Content Generator API"}

from fastapi import FastAPI
from .rag_chain import ScientificRAG

app = FastAPI()
rag = ScientificRAG("server/vectorstore") # Ruta al vector store


@app.post("/explain")
async def explain_science(topic: str):
    try:
        response = rag.explain_concept(topic)
        return {
            "topic": topic,
            "explanation": response.content,
            "sources": [doc.metadata for doc in response.metadata.get("source_docs", [])]
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)