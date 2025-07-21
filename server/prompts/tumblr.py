from langchain.prompts import PromptTemplate

tumblr_prompt = PromptTemplate.from_template(
    """
    Actúa como un experto en marketing de contenidos y redes sociales.
    Genera una publicación para Tumblr, creativa y multimedia, que combine texto e ideas para imágenes o gifs. Incluye:
    - Tema: {tema}
    - Audiencia: {audiencia}
    - Tono: {tono}
    Responde SIEMPRE en español y asegúrate de que el contenido sea adecuado para Tumblr.
    """
) 