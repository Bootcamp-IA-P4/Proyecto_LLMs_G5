# server/rag_chain.py
# server/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import traceback
import logging


# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ... el resto de tu código permanece igual ...
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from server.prompts_1 import DIVULGATION_PROMPT
from server.vector_db import VectorStore
import os
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter # ¡NUEVO IMPORT!




class ScientificRAG:
    def __init__(self, vector_db_path):
        self.vector_db = VectorStore()
        try:
            self.vector_db.load(vector_db_path)
        except Exception as e:
            raise RuntimeError(f"Error al cargar la base de datos de vectores en {vector_db_path}: {e}. Asegúrate de ejecutar 'python -m server.initialize_db' primero.")

        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY no está configurada como variable de entorno. Asegúrate de tener un archivo .env en la raíz de tu proyecto con GROQ_API_KEY=\"TU_CLAVE\"")
        self.llm = ChatGroq(temperature=0.3, model_name="llama-3.3-70b-versatile", groq_api_key=groq_api_key)

        self.prompt = ChatPromptTemplate.from_template(DIVULGATION_PROMPT)

        # Paso 1: Crea la cadena para combinar los documentos con el LLM y el prompt.
        combine_docs_chain = create_stuff_documents_chain(self.llm, self.prompt) | StrOutputParser()

        # Paso 2: Configura el retriever.
        self.retriever = self.vector_db.db.as_retriever(search_kwargs={"k": 3})

        # Paso 3: Construye la cadena RAG completa usando RunnablePassthrough
        # ¡La clave está aquí! itemgetter("input") extrae el valor de 'input' antes de pasárselo al retriever.
        self.rag_chain = (
            {
                "context": itemgetter("input") | self.retriever, # Asegura que el retriever recibe solo la cadena del topic
                "topic": RunnablePassthrough() # Pasa el diccionario completo para que la clave 'topic' en el prompt se llene con 'input'
            }
            | combine_docs_chain
        )

    def explain_concept(self, topic: str, k=3):
        # 1. Recuperación de documentos relevantes
        relevant_docs = self.vector_db.db.similarity_search(topic, k=k)
        
        # 2. Construir contexto
        context = "\n\n".join([
            f"📄 {doc.metadata['title']}\n"
            f"👤 Autores: {', '.join(doc.metadata.get('authors', ['N/A']))}\n"
            f"📝 {doc.page_content[:500]}..."
            for doc in relevant_docs
        ])
        
        # 3. Generar explicación
        chain = self.prompt | self.llm
        response = chain.invoke({
            "topic": topic,
            "context": context
        })
        
        # 4. Formatear respuesta
        return {
            "answer": response.content,  # Acceso directo al contenido
            "sources": [{
                "title": doc.metadata.get("title", "N/A"),
                "authors": doc.metadata.get("authors", []),
                "url": doc.metadata.get("url", "N/A")
            } for doc in relevant_docs]
        }