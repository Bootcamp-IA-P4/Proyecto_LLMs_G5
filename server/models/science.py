from pydantic import BaseModel

class ScienceRequest(BaseModel):
    topic: str
    audience: str  
    language: str  

class ScienceResponse(BaseModel):
    text_content: str