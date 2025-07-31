import requests
import time

def detect_language(text: str, retries: int = 3, delay: float = 2.0) -> str:
    for attempt in range(retries):
        try:
            response = requests.post(
                "http://libretranslate:5000/detect",
                json={"q": text}
            )
            response.raise_for_status()
            return response.json()[0]["language"]
        except requests.exceptions.ConnectionError as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise e

def translate_to_en(text: str, retries: int = 3, delay: float = 2.0) -> str:
    detected_lang = detect_language(text, retries=retries, delay=delay)
    if detected_lang == "en":
        return text
    for attempt in range(retries):
        try:
            response = requests.post(
                "http://libretranslate:5000/translate",
                json={
                    "q": text,
                    "source": detected_lang,
                    "target": "en",
                    "format": "text"
                }
            )
            response.raise_for_status()
            return response.json()["translatedText"]
        except requests.exceptions.ConnectionError as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise e
