from datetime import datetime, timedelta
from jose import jwt
import bcrypt
from server.utils.database import get_supabase
from server.config.settings import settings
from server.models.user import UserCreate, UserLogin
from fastapi import HTTPException, status

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_access_token(user_id: str):
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": user_id, "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def register_user(user_data: UserCreate):
    supabase = get_supabase()
    
    # Verificar si el usuario ya existe
    existing_user = supabase.table("users").select("*").eq("email", user_data.email).execute()
    if existing_user.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Crear usuario
    hashed_password = get_password_hash(user_data.password)
    result = supabase.table("users").insert({
        "email": user_data.email,
        "password_hash": hashed_password
    }).execute()
    
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el usuario"
        )
    
    user = result.data[0]
    access_token = create_access_token(str(user["id"]))
    
    return {"access_token": access_token, "token_type": "bearer"}

async def login_user(user_data: UserLogin):
    supabase = get_supabase()
    
    # Buscar usuario
    user_result = supabase.table("users").select("*").eq("email", user_data.email).execute()
    if not user_result.data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    user = user_result.data[0]
    
    # Verificar contraseña
    if not verify_password(user_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    access_token = create_access_token(str(user["id"]))
    return {"access_token": access_token, "token_type": "bearer"}