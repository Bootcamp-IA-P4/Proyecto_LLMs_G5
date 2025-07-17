from langchain_ollama import OllamaLLM

# Ahora vamos a crear una instancia del modelo que vamos a usar.
# llm = OllamaLLM(model="llama3")

# Vamos a crear un prompt para probar, más adelante lo haremss en la carpeta de prompts.
# prompt = "Escribe un tweet corto y atractivo sobre la llegada del hombre a la Luna, incluyendo hashtags relevantes."

# Ahora vamos invocar al modelo con el prompt.
# response = llm.invoke(prompt)
# print(response)


# Ahora vamos a crear una función para que sea reutilizable con otros temas, ya que antes he sido muy específica.
def generate_text(topic: str, platform: str) -> str:
    llm = OllamaLLM(model="llama3")

    # Seleccionamos el prompt adecuado según la plataforma.
    if platform == "twitter":
        prompt = f"Escribe un tweet corto y atractivo sobre '{topic}', incluyendo hashtags relevantes."
    elif platform == "blog":
        prompt = f"Escribe un párrafo de introducción para una entrada de blog sobre '{topic}'. El tono debe ser informativo y atractivo."
    else:
        prompt = f"Escribe un texto corto sobre '{topic}'."

    print(f"--- Generando texto para '{platform}' sobre el tema: {topic} ---")
    response = llm.invoke(prompt)
    return response

if __name__ == '__main__':
    example_topic = "el futuro de los viajes espaciales"
    
    print("\n Twitter ---")
    generated_tweet = generate_text(example_topic, "twitter")
    print(generated_tweet)
    
    # Prueba para un Blog
    print("\nBlog ---")
    generated_blog_intro = generate_text(example_topic, "blog")
    print(generated_blog_intro)
    print("---------------------------")