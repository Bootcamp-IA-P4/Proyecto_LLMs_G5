from fastapi import APIRouter, Depends, HTTPException, Query
from uuid import UUID
from typing import List

from server.models.science import ScienceRequest, ScienceResponse, SciencePostDB
from server.services.science_service import generate_science_content, AVAILABLE_MODELS
from server.utils.dependencies import get_current_user
from server.utils.database import get_supabase

router = APIRouter()

@router.get("/models")
async def get_available_models():
    """Obtener modelos disponibles para generación científica"""
    return {
        "models": list(AVAILABLE_MODELS.keys()),
        "default": "llama3-8b-8192"
    }

@router.post("/generate", response_model=ScienceResponse)
async def generate_science(
    request: ScienceRequest,
    current_user: UUID = Depends(get_current_user)
):
    """Generar artículo divulgativo científico con RAG de ArXiv"""
    try:
        result = await generate_science_content(request, current_user)
        return ScienceResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[SciencePostDB])
async def get_science_history(
    current_user: UUID = Depends(get_current_user),
    limit: int = Query(default=10, le=50),
    offset: int = Query(default=0, ge=0)
):
    """Obtener historial de posts científicos del usuario"""
    try:
        supabase = get_supabase()
        result = supabase.table("science_posts").select("*").eq(
            "user_id", str(current_user)
        ).order("created_at", desc=True).range(offset, offset + limit - 1).execute()
        
        return [SciencePostDB(**post) for post in result.data]
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al obtener historial científico: {str(e)}"
        )