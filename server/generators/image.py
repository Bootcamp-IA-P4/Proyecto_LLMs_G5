import os
from typing import Optional
import datetime
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from server.utils.image_processor import resize_image_to_width

script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
dotenv_path = os.path.join(project_root, ".env")
load_dotenv(dotenv_path)

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

def _save_image_and_get_url(image_bytes: bytes, resize_width: Optional[int] = None) -> str:
    """
    Guarda los bytes de una imagen, opcionalmente la redimensiona y devuelve la URL estática.
    """
    image = Image.open(BytesIO(image_bytes))
    current_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    output_dir = os.path.join(project_root, "client", "static", "generated_images")
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    original_filename = f"image_{timestamp}_orig.png"
    original_filepath = os.path.join(output_dir, original_filename)
    
    # Guardar siempre la imagen original
    image.save(original_filepath)

    if resize_width:
        resized_filename = f"image_{timestamp}_w{resize_width}.png"
        resized_filepath = os.path.join(output_dir, resized_filename)
        
        # Redimensionar la imagen original
        resize_image_to_width(original_filepath, resized_filepath, resize_width)
        
        # Devolver la URL de la imagen redimensionada
        return f"/static/generated_images/{resized_filename}"
    
    # Si no se redimensiona, devolver la URL de la original
    return f"/static/generated_images/{original_filename}"

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

def generate_image_huggingface(
    topic: str,
    platform: str,
    voice: str,
    company_info: str = "",
    language: str = "en",
    prompt: Optional[str] = None
) -> Optional[str]:
    """
    Generates an image using the Hugging Face Inference Client.
    Saves the image to a file and returns its static URL.
    """
    if not HF_TOKEN:
        print("❌ Token de Hugging Face (HF_TOKEN) no configurado. No se generará imagen.")
        return None

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
    try:
        client = InferenceClient(
            provider="nebius",
            token=HF_TOKEN,
        )
        image = client.text_to_image(
            prompt,
            model="black-forest-labs/FLUX.1-dev",
        )
        # Convert PIL Image to bytes
        with BytesIO() as buffer:
            image.save(buffer, format="PNG")
            image_bytes = buffer.getvalue()

        # Guardar y redimensionar la imagen a un ancho de 768px
        return _save_image_and_get_url(image_bytes, resize_width=768)

    except Exception as e:
        print(f"Error inesperado en la generación de imagen con Hugging Face Inference Client: {e}")
        return None