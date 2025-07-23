from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain # Nuevo import
from langchain.chains.combine_documents import create_stuff_documents_chain # Nuevo import
from .prompts_1 import DIVULGATION_PROMPT
from server.vector_db import VectorStore
import os # Necesario para os.getenv

class ScientificRAG:
    def __init__(self, vector_db_path):
        self.vector_db = VectorStore()
        # Asegúrate de que esta línea carga la DB existente, no crea una nueva si ya la tienes.
        # Si la carpeta 'server/vectorstore' no existe o está vacía, esto fallará.
        try:
            self.vector_db.load(vector_db_path)
        except Exception as e:
            raise RuntimeError(f"Error al cargar la base de datos de vectores en {vector_db_path}: {e}. Asegúrate de ejecutar 'python initialize_db.py' primero.")

        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY no está configurada como variable de entorno. Asegúrate de tener un archivo .env en la raíz de tu proyecto con GROQ_API_KEY=\"TU_CLAVE\"")
        self.llm = ChatGroq(temperature=0.3, model_name="llama3-70b", groq_api_key=groq_api_key)

        self.prompt = ChatPromptTemplate.from_template(DIVULGATION_PROMPT)

        # Paso 1: Crea la cadena para combinar los documentos con el LLM y el prompt
        # Esta cadena toma los documentos recuperados y el 'topic' y genera la respuesta.
        document_chain = create_stuff_documents_chain(self.llm, self.prompt)

        # Paso 2: Configura el retriever a partir de tu base de datos de vectores
        # 'search_kwargs={"k": 3}' le dice al retriever que busque los 3 documentos más relevantes.
        self.retriever = self.vector_db.db.as_retriever(search_kwargs={"k": 3})

        # Paso 3: Crea la cadena RAG completa
        # Esta cadena primero recupera documentos y luego los pasa a la document_chain para generar la respuesta.
        # El resultado de invoke() será un diccionario con 'answer' (la explicación) y 'context' (los documentos fuente).
        self.rag_chain = create_retrieval_chain(self.retriever, document_chain)

    def explain_concept(self, topic: str):
        # La cadena RAG ya maneja tanto la recuperación como la generación.
        # El 'topic' se mapea automáticamente a 'input' en la cadena de recuperación.
        response = self.rag_chain.invoke({"input": topic})

        # 'response' ahora es un diccionario con 'answer' y 'context'.
        # Formateamos la salida para que main.py pueda usarla fácilmente.
        return {
            "content": response["answer"],
            "metadata": {"source_docs": response["context"]} # 'context' contiene los Documentos originales
        }