from server.config.settings import settings
from server.utils.database import get_supabase
from server.generators.text import generate_text
from server.models.post import ContentRequest, ContentResponse
from uuid import UUID
import json

async def generate_content(request: ContentRequest, user_id):
    audience_voice_map = {
        "juvenil": "a fresh, youthful and engaging voice",
        "general": "a neutral and informative tone",
        "técnica": "a formal and technical tone"
    }

    voice = audience_voice_map.get(request.audience.lower(), "a neutral and informative tone")
    model_used = request.model or "llama3-8b-8192"

    print(f"🔧 Generating text for '{request.platform}' with model '{model_used}'")
    generated_text = generate_text(
        topic=request.topic,
        platform=request.platform,
        model_name=model_used,
        voice=voice,
        company_info="",
        language=request.language
    )

    supabase = get_supabase()
    post_data = {
        "user_id": str(user_id),
        "platform": request.platform,
        "audience": request.audience,
        "language": request.language,
        "model": model_used,
        "text_content": generated_text,
        "image_url": None
    }

    print("💾 Saving to Supabase...")
    response = supabase.table("posts").insert(post_data).execute()
    print("📦 Supabase response:", response.data)

    if response.status_code >= 400:
        raise Exception(f"Supabase insert failed with status {response.status_code}: {json.dumps(response.data)}")

    return ContentResponse(
        text_content=generated_text,
        image_url=None
    )


async def get_user_posts(user_id: UUID):
    """Obtiene el historial de posts del usuario"""
    supabase = get_supabase()

    print(f"📄 Getting posts for user {user_id}")
    result = supabase.table("posts").select("*").eq("user_id", str(user_id)).order("created_at", desc=True).execute()

    if result.status_code >= 400:
        raise Exception(f"Supabase fetch failed: {result.json()}")

    return result.data
