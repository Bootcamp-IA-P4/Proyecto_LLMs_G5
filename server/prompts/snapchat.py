from langchain.prompts import PromptTemplate

snapchat_prompt = PromptTemplate.from_template(
    """
    Actúa como un experto en marketing de contenidos y redes sociales.
    Genera una idea de story para Snapchat, breve, visual y dirigida a un público joven. Incluye:
    - Tema: {tema}
    - Audiencia: {audiencia}
    - Tono: {tono}
    Sugiere un filtro o efecto visual. Responde SIEMPRE en español y asegúrate de que el contenido sea adecuado para Snapchat.
    """
) 