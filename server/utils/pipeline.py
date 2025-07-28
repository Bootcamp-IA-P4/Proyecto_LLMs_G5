from typing import Dict, Any, Optional
from server.generators.text import generate_text
from server.generators.image import ImageGenerator
from deep_translator import GoogleTranslator
from server.utils.cloudinary import upload_image_bytes

def translate_text(texto):
    return GoogleTranslator(source='auto', target='en').translate(texto)


def run_pipeline(
    topic: str,
    platform: str,
    model_name: str = "llama3-8b-8192",
    voice: str = "general",
    company_info: str = "",
    language: str = "es",
    include_image: bool = False,
    image_prompt: Optional[str] = None,
    **kwargs    
) -> Dict[str, Any]:
    results = {}
    text_result = generate_text(
        topic=topic,
        platform=platform,
        model_name=model_name,
        voice=voice,
        company_info=company_info,
        language=language
    )
    results["text"] = text_result

    if include_image:
        prompt_img = image_prompt if image_prompt else text_result
        prompt_img_en = translate_text(prompt_img)
        image_generator = ImageGenerator()
        image_bytes = image_generator.generate_image(prompt_img_en)
        if image_bytes:
            image_url = upload_image_bytes(image_bytes)
            results["image_url"] = image_url
        else:
            results["image"] = None

    return results
