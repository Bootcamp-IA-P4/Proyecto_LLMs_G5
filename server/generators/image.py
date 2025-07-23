import torch
from diffusers import DiffusionPipeline
from server.utils.translate import translate_to_en
import io
import os
import datetime

def generate_image_huggingface(
    topic: str,
    platform: str,
    voice: str,
    company_info: str = "",
    language: str = "en"
) -> str:
    """
    Generates an image using a local Stable Diffusion pipeline.
    Saves the image to a file and returns its URL.
    """
    model_id = "stabilityai/stable-diffusion-2-1-base"
    
    # Check for CUDA GPU and set device, otherwise use CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Load the pipeline from local cache or download if not present
    # For ldm-text2im-large-256, float32 is usually sufficient and avoids issues with float16 on CPU
    pipe = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
    pipe = pipe.to(device)

    # Translate the inputs to English
    topic_en = topic
    voice_en = voice
    company_info_en = company_info if company_info else ""

    language_str = f"Output language: {language}. " if language and language != "en" else ""

    prompt = (
        f"Ultra-realistic, highly detailed illustration for {platform}. "
        f"Topic: {topic_en}. "
        f"Audience/Voice: {voice_en}. "
    )
    if company_info_en:
        prompt += f"Company info: {company_info_en}. "
    prompt += language_str
    prompt += (
        "cinematic, sharp focus, 8k resolution, masterpiece, professional quality."
    )

    # Generate the image
    image = pipe(prompt).images[0]

    # Define the directory to save images
    # This path is relative to the server's root, which is /app in the Docker container
    output_dir = "/app/client/static/generated_images"
    os.makedirs(output_dir, exist_ok=True)

    # Generate a unique filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"image_{timestamp}.png"
    file_path = os.path.join(output_dir, filename)

    # Save the image
    image.save(file_path)

    # Return the URL relative to the static files served by FastAPI
    image_url = f"/static/generated_images/{filename}"
    return image_url
