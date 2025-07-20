from fastapi import APIRouter
from pydantic import BaseModel
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

router = APIRouter()

# Modelos disponibles en Groq (puedes añadir más)
AVAILABLE_MODELS = [
    "llama3-8b-8192",
    "mixtral-8x7b-32768",
    "gemma-7b-it"
]

class PromptRequest(BaseModel):
    prompt: str
    model: str = "llama3-8b-8192"

@router.post("/generate")
async def generate_text(request: PromptRequest):
    if not os.getenv("GROQ_API_KEY"):
        return {"error": "GROQ_API_KEY no está configurada. Añádela como variable de entorno."}
    
    if request.model not in AVAILABLE_MODELS:
        return {"error": f"Modelo no válido. Usa uno de: {AVAILABLE_MODELS}"}
    
    try:
        llm = ChatGroq(model_name=request.model, temperature=0.7)
        response = llm.invoke([HumanMessage(content=request.prompt)])
        return {"response": response.content}
    except Exception as e:
        return {"error": str(e)}

@router.get("/models")
async def list_models():
    return {"models": AVAILABLE_MODELS}