from langchain.prompts import PromptTemplate

telegram_prompt = PromptTemplate.from_template(
    """
    Actúa como un experto en marketing de contenidos y redes sociales.
    Genera un mensaje para un canal de Telegram, informativo y directo, que invite a la acción o a compartir. Incluye:
    - Tema: {tema}
    - Audiencia: {audiencia}
    - Tono: {tono}
    Responde SIEMPRE en español y asegúrate de que el contenido sea adecuado para Telegram.
    """
) 