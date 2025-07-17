from langchain.prompts import PromptTemplate

blog_prompt = PromptTemplate.from_template(
    """
    Actúa como un experto en marketing de contenidos y redes sociales.
    Crea un artículo corto para un blog (2-3 párrafos) con un título atractivo, 
    basado en:
    - Tema: {tema}
    - Audiencia: {audiencia}
    - Tono: {tono}
    Responde SIEMPRE en español.
    """
)