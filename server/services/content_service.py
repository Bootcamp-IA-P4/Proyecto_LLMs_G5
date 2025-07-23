import base64
from server.config.settings import settings
from server.utils.database import get_supabase
from server.generators.text import generate_text
from server.generators.image import generate_image_huggingface
from server.models.post import ContentRequest, ContentResponse
from server.utils.pipeline import run_pipeline
from uuid import UUID
import base64

async def generate_content(request: ContentRequest, user_id: UUID):
    model_used = request.model if request.model and request.model.strip() else "llama3-8b-8192"
    
    try:
        generated_text = generate_text(
            topic=request.topic,
            platform=request.platform,
            model_name=model_used,
            voice=request.audience, 
            company_info="",
            language=request.language
        )
        print(f"✅ Generated text: {generated_text[:100]}...")
    except Exception as e:
        print(f"❌ Error generating text: {e}")
        raise Exception(f"Text generation failed: {str(e)}")
    # Si el usuario solicita imagen:
    image_url = None
    image_base64 = None
    if getattr(request, "include_image", False):
        pipeline_result = run_pipeline(
            topic=request.topic,
            platform=request.platform,
            model_name=model_used,
            voice=request.audience,
            company_info="",
            language=request.language,
            include_image=True,
            image_prompt=getattr(request, "image_prompt", None)           
        )
        image_url = pipeline_result.get("image_url")
        image_bytes = pipeline_result.get("image")
        if image_bytes:
            image_base64 = "data:image/png;base64," + base64.b64encode(image_bytes).decode("utf-8")


    # Nueva generación de imagen
    try:
        image_url = generate_image_huggingface(
            topic=request.topic,
            platform=request.platform,
            voice=request.audience,           # Usamos audience como voice
            company_info="",                  # Puede ser nulo o vacío
            language=request.language         # Pasamos el idioma de salida
        )
    except Exception as e:
        print(f"❌ Error generating image: {e}")
        image_url = None

    # Guardar en base de datos
    supabase = get_supabase()
    post_data = {
        "user_id": str(user_id),
        "platform": request.platform,
        "audience": request.audience,
        "language": request.language,
        "model": model_used,
        "text_content": generated_text,
        "image_url": image_url
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
        image_url=image_url or image_base64
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