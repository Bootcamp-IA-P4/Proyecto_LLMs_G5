from langchain.prompts import PromptTemplate

linkedin_prompt = PromptTemplate.from_template(
    """
    Actúa como un experto en marketing de contenidos y redes sociales.
    Genera una publicación profesional para LinkedIn, estructurada y clara, usando saltos de línea para facilitar la lectura,
    basado en:
    - Tema: {tema}
    - Audiencia: {audiencia}
    - Tono: {tono}
    Responde SIEMPRE en español.
    """
)