from fastapi import APIRouter, Depends, HTTPException, Request
from server.models.post import ContentRequest, ContentResponse, PostHistory
from server.services.content_service import generate_content, get_user_posts
from server.utils.dependencies import get_current_user
from uuid import UUID
import os
import httpx

router = APIRouter()

@router.post("/generate", response_model=ContentResponse)
async def generate_post(
    request: Request,
    request_data: ContentRequest,
    current_user: UUID = Depends(get_current_user)
):
    """Generar contenido de texto e imagen"""
    try:
        response_data = await generate_content(request_data, current_user)
        
        # Construir la URL completa de la imagen si existe
        image_url = None
        if response_data.image_url:
            image_url = f"{request.base_url}{response_data.image_url.lstrip('/')}"
        
        return ContentResponse(
            text_content=response_data.text_content,
            image_url=image_url
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_history(current_user: UUID = Depends(get_current_user)):
    """Obtener historial de posts del usuario"""
    try:
        posts = await get_user_posts(current_user)
        return {"posts": posts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/langsmith")
async def get_langsmith_logs(request: Request, limit: int = 10):
    api_key = os.getenv("LANGSMITH_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="LANGSMITH_API_KEY not set")

    session_id = "28a1c2c1-6d28-4fd0-8fc8-4306127e67c2"
    url = "https://api.smith.langchain.com/api/v1/runs/query"
    headers = {
        "x-api-key": api_key,
        "Accept": "application/json"
    }
    payload = {
        "session": [session_id],
        "limit": limit,
        "order": "desc"
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers, json=payload)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        data = resp.json()
        return data