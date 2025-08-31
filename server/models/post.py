from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from server.config.settings import settings

class ContentRequest(BaseModel):
    platform: str  
    topic: str
    audience: str  # juvenil, general, técnica
    language: str  # es, en, fr
    model: Optional[str] = settings.GROQ_DEFAULT_MODEL  # modelo de Groq seleccionado
    include_image: Optional[bool] = False
    image_generator: Optional[str] = 'fal_ai'
    image_prompt: Optional[str] = None

class ContentResponse(BaseModel):
    text_content: str
    image_url: Optional[str] = None

class Post(BaseModel):
    id: UUID
    user_id: UUID
    platform: str
    audience: str
    language: str
    model: str
    text_content: str
    image_url: Optional[str] = None
    created_at: datetime

class PostHistory(BaseModel):
    posts: List[Post]