from langchain.prompts import PromptTemplate

bluesky_prompt = PromptTemplate.from_template(
    """
    Actúa como un experto en marketing de contenidos y redes sociales.
    Genera una publicación para Bluesky, microblogging descentralizado, que fomente la conversación y la participación. Incluye:
    - Tema: {tema}
    - Audiencia: {audiencia}
    - Tono: {tono}
    Responde SIEMPRE en español y asegúrate de que el contenido sea adecuado para Bluesky.
    """
) 