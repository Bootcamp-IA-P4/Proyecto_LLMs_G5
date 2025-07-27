from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from server.models.science import ScienceRequest, ScienceResponse
from server.services.science_service import generate_science_content
from server.utils.dependencies import get_current_user

router = APIRouter()

@router.post("/science", response_model=ScienceResponse)
async def generate_science(
    request: ScienceRequest,
    current_user: UUID = Depends(get_current_user)
):
    """Generar artículo divulgativo de biomedicina"""
    try:
        result = await generate_science_content(request, current_user)
        return ScienceResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
