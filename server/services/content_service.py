from server.config.settings import settings
from server.utils.database import get_supabase
from server.generators.text import generate_text
from server.models.post import ContentRequest, ContentResponse
from uuid import UUID

async def generate_content(request: ContentRequest, user_id: UUID):
    audience_voice_map = {
        "juvenil": "a fresh, youthful and engaging voice",
        "general": "a neutral and informative tone",
        "técnica": "a formal and technical tone"
    }

    voice = audience_voice_map.get(request.audience.lower(), "a neutral and informative tone")
    model_used = request.model if request.model and request.model.strip() else "llama3-8b-8192"

    print(f"🔧 Generating text for '{request.platform}' with model '{model_used}'")
    print(f"📝 Topic: {request.topic}")
    print(f"🎯 Voice: {voice}")
    
    try:
        generated_text = generate_text(
            topic=request.topic,
            platform=request.platform,
            model_name=model_used,
            voice=voice,
            company_info="",
            language=request.language
        )
        print(f"✅ Generated text: {generated_text[:100]}...")
    except Exception as e:
        print(f"❌ Error generating text: {e}")
        raise Exception(f"Text generation failed: {str(e)}")

    # Guardar en base de datos
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
    try:
        response = supabase.table("posts").insert(post_data).execute()        
        # Supabase no tiene status_code, solo verifica si hay data
        if not response.data:
            raise Exception("No data returned from Supabase insert")
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        # No relanzar la excepción si es solo el guardado, devolver el contenido generado
        print("⚠️ Content generated but not saved to database")

    return ContentResponse(
        text_content=generated_text,
        image_url=None
    )


async def get_user_posts(user_id: UUID):
    """Obtiene el historial de posts del usuario"""
    supabase = get_supabase()

    print(f"📄 Getting posts for user {user_id}")
    try:
        result = supabase.table("posts").select("*").eq("user_id", str(user_id)).order("created_at", desc=True).execute()
        
        return result.data if result.data else []
        
    except Exception as e:
        print(f"❌ Error fetching posts: {e}")
        raise Exception(f"Failed to fetch user posts: {str(e)}")