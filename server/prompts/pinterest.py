from langchain.prompts import PromptTemplate

pinterest_prompt = PromptTemplate.from_template(
    """
    Actúa como un experto en marketing de contenidos y redes sociales.
    Genera una idea de pin para Pinterest, incluyendo una breve descripción inspiradora y una sugerencia de imagen. Incluye:
    - Tema: {tema}
    - Audiencia: {audiencia}
    - Tono: {tono}
    Responde SIEMPRE en español y asegúrate de que el contenido sea adecuado para Pinterest.
    """
) 