from fastapi import APIRouter, HTTPException
from server.models.user import UserCreate, UserLogin, Token
from server.services.auth_service import register_user, login_user

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    """Registrar nuevo usuario"""
    return await register_user(user)

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    """Iniciar sesión"""
    return await login_user(user)