from langchain.prompts import PromptTemplate

medium_prompt = PromptTemplate.from_template(
    """
    Actúa como un experto en marketing de contenidos y redes sociales.
    Genera un artículo largo para Medium, bien estructurado, con título atractivo, introducción, desarrollo y conclusión. Incluye:
    - Tema: {tema}
    - Audiencia: {audiencia}
    - Tono: {tono}
    Responde SIEMPRE en español y asegúrate de que el contenido sea adecuado para Medium.
    """
) 