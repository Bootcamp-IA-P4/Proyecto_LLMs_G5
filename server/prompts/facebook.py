from langchain.prompts import PromptTemplate

facebook_prompt = PromptTemplate.from_template(
    """
    Actúa como un experto en marketing de contenidos y redes sociales.
    Genera una publicación para Facebook, adecuada para grupos o páginas, que fomente la interacción y la comunidad. Incluye:
    - Tema: {tema}
    - Audiencia: {audiencia}
    - Tono: {tono}
    Puedes sugerir preguntas para la audiencia o llamadas a la acción. Responde SIEMPRE en español y asegúrate de que el contenido sea adecuado para Facebook.
    """
) 