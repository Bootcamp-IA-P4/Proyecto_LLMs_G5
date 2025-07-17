from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate

llm = Ollama(model="phi")  # Cambia a "gemma", "stablelm-zephyr", etc.

# Prompt dinámico
prompt_template = ChatPromptTemplate.from_messages([
    ("system", """
    Genera un {tipo_contenido} sobre {tema} para {audiencia}.
    - Plataforma: {plataforma}.
    - Estilo: {estilo}.
    - Longitud: {longitud}.
    """),
])

def generar_contenido(tema, plataforma, audiencia):
    # Define parámetros según plataforma
    if plataforma.lower() == "blog":
        tipo_contenido = "artículo detallado"
        estilo = "profesional con ejemplos prácticos"
        longitud = "800 palabras"
    elif plataforma.lower() == "twitter":
        tipo_contenido = "tweet impactante"
        estilo = "directo y con hashtags relevantes"
        longitud = "280 caracteres máximo"
    else:
        tipo_contenido = "post"
        estilo = "adaptado a la plataforma"
        longitud = "variable"

    # Ejecuta el prompt
    chain = prompt_template | llm
    respuesta = chain.invoke({
        "tipo_contenido": tipo_contenido,
        "tema": tema,
        "audiencia": audiencia,
        "plataforma": plataforma,
        "estilo": estilo,
        "longitud": longitud
    })
    return respuesta

# ¡Prueba la función!
if __name__ == "__main__":
    tema = input("Tema del contenido: ")
    plataforma = input("Plataforma (Blog/Twitter/Instagram): ")
    audiencia = input("Audiencia (General/Técnica/Infantil): ")
    
    contenido = generar_contenido(tema, plataforma, audiencia)
    print("\n--- Contenido Generado ---")
    print(contenido)