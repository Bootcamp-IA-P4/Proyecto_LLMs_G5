from langchain.prompts import PromptTemplate

youtube_prompt = PromptTemplate.from_template(
    """
    Actúa como un experto en marketing de contenidos y redes sociales.
    Genera una idea de vídeo para YouTube, incluyendo título atractivo, descripción optimizada para SEO y una estructura de secciones. Incluye:
    - Tema: {tema}
    - Audiencia: {audiencia}
    - Tono: {tono}
    Responde SIEMPRE en español y asegúrate de que el contenido sea adecuado para YouTube.
    """
) 