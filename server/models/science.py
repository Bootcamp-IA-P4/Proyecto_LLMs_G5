from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from uuid import UUID

class ScienceRequest(BaseModel):
    topic: str
    audience: str  
    language: str
    model: str = Field(default="llama3-8b-8192")
    max_docs: int = Field(default=5, ge=1, le=20)

class SourceInfo(BaseModel):
    title: str
    authors: Optional[str] = None
    published: Optional[str] = None
    url: Optional[str] = None
    relevance_score: Optional[float] = None

class ScienceResponse(BaseModel):
    id: UUID
    text_content: str
    sources: List[SourceInfo]
    total_sources: int

class SciencePostDB(BaseModel):
    id: UUID
    user_id: UUID
    topic: str
    audience: str
    language: str
    model: str
    max_docs: int
    text_content: str
    sources: List[Dict[str, Any]]
    created_at: str