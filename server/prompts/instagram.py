from langchain.prompts import PromptTemplate

instagram_prompt = PromptTemplate.from_template(
    """
    Actúa como un experto en marketing de contenidos y redes sociales.
    Escribe un pie de foto para Instagram, atractivo y sugiere una idea para la imagen, 
    basado en:
    - Tema: {tema}
    - Audiencia: {audiencia}
    - Tono: {tono}
    Responde SIEMPRE en español.
    """
)