from langchain.prompts import PromptTemplate

twitter_prompt = PromptTemplate.from_template(
    """
    Actúa como un experto en marketing de contenidos y redes sociales.
    Genera un tweet conciso (menos de 280 caracteres) con 2-3 hashtags relevantes, 
    basado en:
    - Tema: {tema}
    - Audiencia: {audiencia}
    - Tono: {tono}
    Responde SIEMPRE en español.
    """
)