from langchain.prompts import PromptTemplate

whatsapp_prompt = PromptTemplate.from_template(
    """
    Actúa como un experto en marketing de contenidos y redes sociales.
    Genera un mensaje para un canal de WhatsApp, breve, claro y con llamada a la acción. Incluye:
    - Tema: {tema}
    - Audiencia: {audiencia}
    - Tono: {tono}
    Responde SIEMPRE en español y asegúrate de que el contenido sea adecuado para WhatsApp Channels.
    """
) 