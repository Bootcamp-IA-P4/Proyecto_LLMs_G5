import base64
from server.config.settings import settings
from server.utils.database import get_supabase
from server.generators.text import generate_text
from server.generators.image import generate_image_fal_ai, ImageGenerator
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

    image_url = None
    if request.include_image:
        try:
            prompt = request.image_prompt or request.topic
            if request.image_generator == 'stability_ai':
                print("🖼️ Generating image with Stability AI...")
                stability_client = ImageGenerator()
                image_url = stability_client.generate_image(prompt=prompt)
            else: # Default to fal_ai
                print("🖼️ Generating image with Fal AI...")
                image_url = generate_image_fal_ai(
                    topic=request.topic,
                    platform=request.platform,
                    voice=request.audience,
                    company_info="",
                    language=request.language,
                    prompt=request.image_prompt
                )
            if image_url:
                print(f"✅ Generated image: {image_url}...")
            else:
                print("❌ Image generation failed, no URL returned.")
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            # No relanzar la excepción, simplemente no habrá imagen
            image_url = None

    # Ensure image_url is a string or None, extract if it's a tuple
    if isinstance(image_url, tuple):
        # Assuming the format is ('key', actual_url) or ('key', None)
        # We want the second element of the tuple
        actual_image_url = image_url[1]
        print(f"DEBUG: Extracted actual_image_url from tuple: {actual_image_url}")
    else:
        actual_image_url = image_url

    # Guardar en base de datos
    supabase = get_supabase()
    post_data = {
        "user_id": str(user_id),
        "platform": request.platform,
        "audience": request.audience,
        "language": request.language,
        "model": model_used,
        "text_content": generated_text,
        "image_url": actual_image_url
    }

    print("💾 Saving to Supabase...")
    try:
        response = supabase.table("posts").insert(post_data).execute()
        if not response.data:
            raise Exception("No data returned from Supabase insert")
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        print("⚠️ Content generated but not saved to database")

    return ContentResponse(
        text_content=generated_text,
        image_url=actual_image_url
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