# server/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Importa ScientificRAG (asegúrate de que el path sea correcto)
from server.rag_chain import ScientificRAG

# --- ¡IMPORTANTE! Cargar variables de entorno al inicio ---
load_dotenv()

# --- ¡IMPORTANTE! Definir la instancia de FastAPI una ÚNICA VEZ ---
app = FastAPI(
    title="AI Social Content Generator",
    description="API para generar contenido de redes sociales con IA",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers adicionales (COMENTA/DESCOMENTA según los tengas definidos) ---
# Si tienes los archivos server/routes/auth.py y server/routes/content.py
# y exportan una instancia de APIRouter llamada 'router', descomenta estas líneas.
# Si no los tienes, déjalos comentados para evitar errores de importación.
# from server.routes.auth import router as auth_router
# from server.routes.content import router as content_router
# app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
# app.include_router(content_router, prefix="/api/content", tags=["content"])


# --- Inicialización de la cadena RAG ---
# Asegúrate de que "server/vectorstore" sea la ruta correcta a tu base de datos FAISS.
# Si la DB no existe, el constructor de ScientificRAG lanzará un error.
try:
    rag = ScientificRAG("server/vectorstore")
except Exception as e:
    print(f"❌ ERROR CRÍTICO al inicializar ScientificRAG: {e}")
    # Considera una forma de manejar esto en producción, quizás deshabilitando el endpoint.
    # Por ahora, simplemente lo imprimimos y la app podría no funcionar correctamente.
    rag = None # Establece a None para que el endpoint pueda verificar si se inicializó correctamente.


# --- Endpoint raíz ---
@app.get("/")
async def root():
    return {"message": "AI Social Content Generator API"}

# --- Endpoint para el RAG ---
@app.post("/explain")
async def explain_science(topic: str):
    if rag is None:
        return {"error": "El sistema RAG no se pudo inicializar. Consulta los logs del servidor para más detalles."}, 500

    try:
        # rag_response ahora es el diccionario con 'content' y 'metadata'
        rag_response = rag.explain_concept(topic)

        return {
            "topic": topic,
            "explanation": rag_response["content"], # Acceso correcto al contenido
            "sources": [doc.metadata for doc in rag_response["metadata"]["source_docs"]] # Acceso correcto a las fuentes
        }
    except Exception as e:
        print(f"🚨 Error en /explain al procesar la solicitud: {e}") # Imprime el error para depuración
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)