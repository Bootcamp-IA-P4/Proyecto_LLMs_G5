from fastapi import APIRouter, Depends, HTTPException, Request
from server.models.post import ContentRequest, ContentResponse, PostHistory
from server.services.content_service import generate_content, get_user_posts
from server.utils.dependencies import get_current_user
from uuid import UUID

router = APIRouter()

@router.post("/generate", response_model=ContentResponse)
async def generate_post(
    request: Request,
    request_data: ContentRequest,
    current_user: UUID = Depends(get_current_user)
):
    """Generar contenido de texto e imagen"""
    try:
        text, image_path = await generate_content(request_data, current_user)
        
        # Construir la URL completa de la imagen
        image_url = f"{request.base_url}{image_path.lstrip('/')}"
        
        return ContentResponse(
            text_content=text,
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