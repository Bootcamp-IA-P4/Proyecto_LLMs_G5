from server.generators.text import generate_text
## Este archivo sirve de prueba para pasarle los parámetros y ver si funciona la generación de texto
if __name__ == "__main__":
    topic = "Cómo hacer albóndigas de carne veganas"
    platform = "blog"
    voice = "una voz cercana, motivadora y experta"
    model_name = "mistral-saba-24b"
    company_info = "Recetas veganas de cocina saludable"
    language = "es"

    result = generate_text(topic=topic, platform=platform, model_name=model_name, voice=voice)
    print("Generated content:\n", result)