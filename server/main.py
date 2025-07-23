from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import traceback
import logging  # Añade esto
from server.rag_chain import ScientificRAG  # Asegúrate de que este import sea correcto

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carga variables de entorno
load_dotenv()

app = FastAPI(
    title="AI Social Content Generator",
    description="API para generar contenido de redes sociales con IA",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialización RAG
try:
    rag = ScientificRAG(os.path.join("server", "vectorstore"))  # Ruta multiplataforma
except Exception as e:
    logger.error(f"❌ Error al inicializar RAG: {str(e)}")
    traceback.print_exc()
    rag = None

# Un solo endpoint /explain
@app.get("/explain")
async def explain_science(topic: str):
    if not rag:
        return {"error": "Sistema RAG no disponible"}, 500
    
    try:
        result = rag.explain_concept(topic)
        return {
            "topic": topic,
            "explanation": result["answer"],
            "sources": result["sources"]
        }
    except Exception as e:
        logger.error(f"Error en /explain: {str(e)}")
        return {"error": str(e)}, 500

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)