from langchain.prompts import PromptTemplate

tiktok_prompt = PromptTemplate.from_template(
    """
    Actúa como un experto en marketing de contenidos y redes sociales.
    Genera una idea de vídeo viral para TikTok, incluyendo una breve descripción del guion, hashtags relevantes y una sugerencia de música o efecto visual. Incluye:
    - Tema: {tema}
    - Audiencia: {audiencia}
    - Tono: {tono}
    Responde SIEMPRE en español y asegúrate de que el contenido sea adecuado para TikTok.
    """
) 