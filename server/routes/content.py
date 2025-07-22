from fastapi import APIRouter, Depends, HTTPException
from server.models.post import ContentRequest, ContentResponse, PostHistory
from server.services.content_service import generate_content, get_user_posts
from server.utils.dependencies import get_current_user
from uuid import UUID

router = APIRouter()

@router.post("/generate", response_model=ContentResponse)
async def generate_post(
    request: ContentRequest,
    current_user: UUID = Depends(get_current_user)
):
    """Generar contenido de texto e imagen"""
    try:
        result = await generate_content(request, current_user)
        return result
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