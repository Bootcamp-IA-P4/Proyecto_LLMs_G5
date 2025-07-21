import requests
import os
from dotenv import load_dotenv
from server.utils import translate
load_dotenv()

def generate_image_with_grok(prompt: str) -> str:
    # Implementa la generación de imágenes con Grok
    api_key = os.getenv("GROK_API_KEY")
    url = "https://api.grok.com/v1/generate-image"
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {"prompt": prompt, "model": "meta-llama/llama-4-scout-17b-16e-instruct"}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["image_url"]

def generate_image_stability(tema: str, plataforma: str, audiencia: str, tono: str) -> bytes:
    """
    Genera una imagen usando la API de Stability AI basada en los parámetros dados.
    Devuelve los bytes de la imagen generada.
    """
    api_key = os.getenv("STABILITY_API_KEY")
    if not api_key:
        raise ValueError("No se encontró la variable de entorno STABILITY_API_KEY")

    # Construir un prompt adecuado para la imagen
    prompt_es = f"Ilustración para {plataforma}. Tema: {tema}. Audiencia: {audiencia}. Tono: {tono}. Genera una imagen atractiva y relevante."
    prompt_en = translate.translate_es_to_en(prompt_es)

    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/generate/ultra",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": prompt_en,
            "output_format": "webp",
        },
    )

    if response.status_code == 200:
        return response.content  # Devuelve los bytes de la imagen
    else:
        raise Exception(str(response.json()))
