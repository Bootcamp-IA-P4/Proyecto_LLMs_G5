import os
from typing import Optional
import datetime
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import fal_client

script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
dotenv_path = os.path.join(project_root, ".env")
load_dotenv(dotenv_path)

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

def _save_image_and_get_url(image_bytes: bytes) -> str:
    """Saves image bytes to a file and returns the static URL."""
    image = Image.open(BytesIO(image_bytes))
    current_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    output_dir = os.path.join(project_root, "client", "static", "generated_images")
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"image_{timestamp}.png"
    file_path = os.path.join(output_dir, filename)
    image.save(file_path)
    image_url = f"/static/generated_images/{filename}"
    return image_url

class ImageGenerator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or STABILITY_API_KEY
        self.api_url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

    def generate_image(
        self, 
        prompt:str, 
        aspect_ratio: str = "1:1",
        negative_prompt: Optional[str] = None,
        style: Optional[str] = None,
        seed: int = 0,
        steps: int = 30,
        cfg_scale: int = 7,
        ) -> Optional[str]:
        if not self.api_key or not self.api_key.startswith("sk-"):
            print("❌ API KEY de Stability.ai no configurada o inválida. No se generará imagen.")
            return None
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "image/*"
        }
        payload = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "output_format": "png",
            "mode": "text-to-image",
            "seed": seed,
            "steps": steps,
            "cfg_scale": cfg_scale,
        }
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        if style:
            payload["style"] = style
        try:
            files = {k: (None, str(v)) for k, v in payload.items()}
            response = requests.post(self.api_url, headers=headers, files=files)
            if response.status_code == 200 and response.headers.get("Content-Type", "").startswith("image/"):
                return _save_image_and_get_url(response.content)
            else:
                print(f"Error de generación: {response.text}")
                return None
        except Exception as e:
            print(f"Error llamando a la API de Stability: {e}")
            return None

def generate_image_fal_ai(
    topic: str,
    platform: str,
    voice: str,
    company_info: str = "",
    language: str = "en",
    prompt: Optional[str] = None
) -> str:
    """
    Generates an image using the fal.ai API.
    Saves the image to a file and returns its URL.
    """
    # Use specific prompt if provided, otherwise construct one
    if not prompt:
        prompt = (
            f"Ultra-realistic, highly detailed illustration for {platform}. "
            f"Topic: {topic}. "
            f"Audience/Voice: {voice}. "
        )
        if company_info:
            prompt += f"Company info: {company_info}. "
        prompt += (
            "cinematic, sharp focus, 8k resolution, masterpiece, professional quality."
        )

    # Call fal.ai API
    handler = fal_client.submit(
        "fal-ai/flux/dev",
        arguments={"prompt": prompt},
    )
    result = handler.get()
    image_url_from_fal = result["images"][0]["url"]
    # Download the image from the URL provided by fal.ai
    image_response = requests.get(image_url_from_fal)
    image_response.raise_for_status()
    
    return _save_image_and_get_url(image_response.content)