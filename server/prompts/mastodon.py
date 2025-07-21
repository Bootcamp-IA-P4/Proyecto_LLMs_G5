from langchain.prompts import PromptTemplate

mastodon_prompt = PromptTemplate.from_template(
    """
    Actúa como un experto en marketing de contenidos y redes sociales.
    Genera una publicación para Mastodon, microblogging federado, que fomente la conversación y la participación en comunidades temáticas. Incluye:
    - Tema: {tema}
    - Audiencia: {audiencia}
    - Tono: {tono}
    Responde SIEMPRE en español y asegúrate de que el contenido sea adecuado para Mastodon.
    """
) 