import os
import requests
from dotenv import load_dotenv
from typing import Optional

script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
dotenv_path = os.path.join(project_root, ".env")
load_dotenv(dotenv_path)

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

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
        ) -> Optional[bytes]:
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
                return response.content
            else:
                print(f"Error de generación: {response.text}")
                return None
        except Exception as e:
            print(f"Error llamando a la API de Stability: {e}")
            return None