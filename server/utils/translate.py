import requests
from libretranslatepy import LibreTranslateAPI

lt = LibreTranslateAPI("http://libretranslate:5000/")

def detect_language(text: str) -> str:
    return lt.detect(text)[0]['language']

def translate_to_en(text: str) -> str:
    detected_lang = detect_language(text)
    if detected_lang == "en":
        return text
    return lt.translate(text, detected_lang, "en")