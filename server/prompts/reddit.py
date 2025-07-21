from langchain.prompts import PromptTemplate

reddit_prompt = PromptTemplate.from_template(
    """
    Actúa como un experto en marketing de contenidos y redes sociales.
    Genera una publicación para Reddit, adecuada para un subreddit temático, que fomente el debate y la participación. Incluye:
    - Tema: {tema}
    - Audiencia: {audiencia}
    - Tono: {tono}
    Puedes sugerir una pregunta para iniciar la discusión. Responde SIEMPRE en español y asegúrate de que el contenido sea adecuado para Reddit.
    """
) 