from fastapi import APIRouter
from pydantic import BaseModel
import ollama

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/generate")
async def generate_text(prompt: str):
    try:
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        return {"response": response["message"]["content"]}
    except Exception as e:
        return {"error": str(e)}
