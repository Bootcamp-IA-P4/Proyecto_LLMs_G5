from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import traceback
import logging  # Añade esto
from server.RAG.rag_chain import ScientificRAG  # Asegúrate de que este import sea correcto
from server.routes.auth import router as auth_router
from server.routes.content import router as content_router
from server.config.settings import settings
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

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
    rag = ScientificRAG(os.path.join("server", "RAG"  ,"server", "vectorstore"))  # Ruta multiplataforma
except Exception as e:
    logger.error(f"❌ Error al inicializar RAG: {str(e)}")
    traceback.print_exc()
    rag = None

# Un solo endpoint /explain
@app.get("/explain")
async def explain_science(social_network: str, topic: str, company_info: str, voice: str, language: str):
    if not rag:
        return {"error": "Sistema RAG no disponible"}, 500
    try:
        rag.initialize_prompt(social_network, topic, company_info, voice, language)
        result = rag.explain_concept(topic)
        return {
            "topic": topic,
            "social_network": social_network,
            "explanation": result["answer"],
            "sources": result["sources"]
        }
    except Exception as e:
        logger.error(f"Error en /explain: {str(e)}")
        return {"error": str(e)}, 500
# Static files (CSS, JS, images)
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "client"))
app.mount("/static", StaticFiles(directory=os.path.join(frontend_path, "static")), name="static")

# Templates
templates = Jinja2Templates(directory=os.path.join(frontend_path, "templates"))


# Routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(content_router, prefix="/api/content", tags=["content"])

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/langsmith")
async def langsmit_page(request: Request):
    return templates.TemplateResponse("langsmith.html", {"request": request})