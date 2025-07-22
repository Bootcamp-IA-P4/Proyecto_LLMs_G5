import requests
import os
from dotenv import load_dotenv
from server.config.settings import settings
from server.utils.translate import translate_es_to_en
load_dotenv()

def generate_image_stability(tema: str, plataforma: str, audiencia: str, tono: str) -> bytes:
    """
    Genera una imagen usando la API de Stability AI basada en los parámetros dados.
    Devuelve los bytes de la imagen generada.
    """
    api_key = settings.STABILITY_API_KEY

    # Construir un prompt adecuado para la imagen
    prompt_es = f"Ilustración para {plataforma}. Tema: {tema}. Audiencia: {audiencia}. Tono: {tono}. Genera una imagen atractiva y relevante."
    prompt_en = translate_es_to_en(prompt_es)

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
