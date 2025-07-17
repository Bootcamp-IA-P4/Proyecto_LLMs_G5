import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Cargar variables de entorno
load_dotenv()

class GroqGenerator:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama3-8b-8192",
            temperature=0.7
        )
        
        # Plantilla de prompt mejorada
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """
            Eres un creador de contenido experto. Genera un {tipo_contenido} sobre {tema} para {audiencia}.
            - Plataforma: {plataforma}
            - Estilo: {tono}
            - Longitud: {longitud}
            - Incluye: {elementos_adicionales}
            """),
        ])

    def generar_contenido(self, tema, plataforma, audiencia, tono="profesional"):
        # Configuración por plataforma
        config = {
            "blog": {
                "tipo_contenido": "artículo detallado",
                "longitud": "800-1000 palabras",
                "elementos_adicionales": "subtítulos y conclusión"
            },
            "twitter": {
                "tipo_contenido": "tweet impactante",
                "longitud": "280 caracteres máximo",
                "elementos_adicionales": "2-3 hashtags relevantes"
            },
            "instagram": {
                "tipo_contenido": "post visual",
                "longitud": "2-3 párrafos breves",
                "elementos_adicionales": "emojis y llamada a acción"
            }
        }
        
        # Obtener configuración específica
        plataforma = plataforma.lower()
        config_platform = config.get(plataforma, config["blog"])
        
        # Generar cadena de ejecución
        chain = self.prompt_template | self.llm
        
        # Invocar el modelo
        response = chain.invoke({
            "tipo_contenido": config_platform["tipo_contenido"],
            "tema": tema,
            "audiencia": audiencia,
            "plataforma": plataforma,
            "tono": tono,
            "longitud": config_platform["longitud"],
            "elementos_adicionales": config_platform["elementos_adicionales"]
        })
        
        return response.content