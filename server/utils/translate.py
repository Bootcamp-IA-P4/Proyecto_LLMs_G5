import requests
from libretranslatepy import LibreTranslateAPI

# Si usas docker-compose, usa el nombre del servicio
lt = LibreTranslateAPI("http://libretranslate:5000/")

def translate_es_to_en(text: str) -> str:
    return lt.translate(text, "es", "en")