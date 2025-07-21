from langchain.prompts import PromptTemplate

threads_prompt = PromptTemplate.from_template(
    """
    Actúa como un experto en marketing de contenidos y redes sociales.
    Genera una publicación para Threads, similar a Twitter, que fomente la conversación y la participación. Incluye:
    - Tema: {tema}
    - Audiencia: {audiencia}
    - Tono: {tono}
    Responde SIEMPRE en español y asegúrate de que el contenido sea adecuado para Threads.
    """
) 