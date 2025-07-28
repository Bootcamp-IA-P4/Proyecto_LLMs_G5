# server/RAG/rag_chain.py

import os
import logging
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from server.prompts.prompts import PROMPTS
from server.RAG.vector_db import VectorStore

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScientificRAG:
    def __init__(self, vector_db_path):
        self.vector_db = VectorStore()
        try:
            self.vector_db.load(vector_db_path)
        except Exception as e:
            raise RuntimeError(f"Error al cargar la base de datos de vectores en {vector_db_path}: {e}. Asegúrate de ejecutar 'python -m server.initialize_db' primero.")

        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY no está configurada como variable de entorno.")
        
        self.llm = ChatGroq(temperature=0.3, model_name="llama3-8b-8192", groq_api_key=groq_api_key)

    def initialize_prompt(self, social_network: str, topic: str, company_info: str, voice: str, language: str):
        self.topic = topic
        self.company_info = company_info
        self.voice = voice
        self.language = language

        raw_prompt = PROMPTS.get(social_network.lower(), PROMPTS["default"])
        self.prompt = ChatPromptTemplate.from_template(raw_prompt)

        combine_docs_chain = create_stuff_documents_chain(self.llm, self.prompt) | StrOutputParser()
        self.retriever = self.vector_db.db.as_retriever(search_kwargs={"k": 3})

        self.rag_chain = (
            {
                "context": itemgetter("input") | self.retriever,
                "topic": RunnablePassthrough()
            }
            | combine_docs_chain
        )

    def explain_concept(self, topic: str, k=3):
        relevant_docs = self.vector_db.db.similarity_search(topic, k=k)
        context = "\n\n".join([
            f"📄 {doc.metadata['title']}\n"
            f"👤 Autores: {', '.join(doc.metadata.get('authors', ['N/A']))}\n"
            f"📝 {doc.page_content[:500]}..."
            for doc in relevant_docs
        ])

        # Ejecutar el LLM con el prompt y contexto + demás variables
        response = self.prompt | self.llm
        result = response.invoke({
            "topic": topic,
            "context": context,
            "voice": self.voice,
            "company_info": self.company_info,
            "language": self.language
        })

        return {
            "answer": result.content,
            "sources": [{
                "title": doc.metadata.get("title", "N/A"),
                "authors": doc.metadata.get("authors", []),
                "url": doc.metadata.get("url", "N/A")
            } for doc in relevant_docs]
        }
