import requests
from server.config.settings import settings
from server.utils.translate import translate_to_en

def generate_image_huggingface(
    topic: str,
    platform: str,
    voice: str,
    company_info: str = "",
    language: str = "en"
) -> bytes:
    """
    Generates an image using the Hugging Face Diffusers API based on the provided parameters.
    Returns the generated image bytes.
    """
    api_key = settings.HUGGINGFACE_API_KEY
    # Free models for text-to-image generation:
    #model_id = "runwayml/stable-diffusion-v1-5"
    #model_id = "stabilityai/stable-diffusion-2"
    #model_id = "runwayml/stable-diffusion-v1-5"
    model_id = "prompthero/openjourney"
    # model_id = "runwayml/stable-diffusion-v1-5"
    # model_id = "dreamlike-art/dreamlike-photoreal-2.0"
    # model_id = "stabilityai/stable-diffusion-2-1"
    # model_id = "stabilityai/stable-diffusion-2-base"
    # model_id = "stabilityai/sdxl-turbo"
    
    # Traduce los campos al inglés si es necesario
    topic_en = translate_to_en(topic)
    voice_en = translate_to_en(voice)
    company_info_en = translate_to_en(company_info) if company_info else ""

    # Añade el idioma de salida al prompt para orientar el estilo si es relevante
    language_str = f"Output language: {language}. " if language and language != "en" else ""

    # Build a powerful, detailed prompt in English for a highly realistic image, including company info if provided
    prompt = (
        f"Ultra-realistic, highly detailed illustration for {platform}. "
        f"Topic: {topic_en}. "
        f"Audience/Voice: {voice_en}. "
    )
    if company_info_en:
        prompt += f"Company info: {company_info_en}. "
    prompt += language_str
    prompt += (
        "Photorealistic, intricate textures, vivid colors, sharp focus, natural lighting, "
        "cinematic composition, lifelike details, realistic proportions, 8k resolution, "
        "masterpiece, trending on artstation, hyper-detailed, professional quality. "
        "Generate an attractive and visually stunning image."
    )

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{model_id}",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Accept": "image/png"
        },
        json={
            "inputs": prompt,
        },
        timeout=60
    )

    if response.status_code == 200:
        print(response.status_code)
        if response.status_code == 200:
            with open("output.png", "wb") as f:
                f.write(response.content)
        return response.content  # Return the image bytes
    else:
        try:
            raise Exception(str(response.json()))
        except Exception:
            raise Exception(f"Error {response.status_code}: {response.text}")
