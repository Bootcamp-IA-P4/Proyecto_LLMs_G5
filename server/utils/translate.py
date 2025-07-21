import requests

def translate_es_to_en(text: str) -> str:
    response = requests.post(
        "https://libretranslate.de/translate",
        data={
            "q": text,
            "source": "es",
            "target": "en",
            "format": "text"
        }
    )
    # debug
    print("--------------------------------")
    print("Text:", text)
    print("Source:", "es")
    print("Target:", "en")
    print("Format:", "text")
    print("Status code:", response.status_code)
    print("Response text:", response.text)
    response.raise_for_status()
    return response.json()["translatedText"]