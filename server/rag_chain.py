from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq  # O tu LLM preferido
from .prompts_1 import DIVULGATION_PROMPT
from server.vector_db import VectorStore

class ScientificRAG:
    def __init__(self, vector_db_path):
        self.vector_db = VectorStore()
        self.vector_db.load(vector_db_path)
        self.llm = ChatGroq(temperature=0.3, model_name="llama3-70b")
        
        self.prompt = ChatPromptTemplate.from_template(DIVULGATION_PROMPT)
    
    def explain_concept(self, topic: str, k=3):
        # 1. Recuperación
        relevant_docs = self.vector_db.db.similarity_search(topic, k=k)
        context = "\n\n".join([
            f"Artículo: {doc.metadata['title']}\nResumen: {doc.page_content}"
            for doc in relevant_docs
        ])
        
        # 2. Generación
        chain = self.prompt | self.llm
        return chain.invoke({
            "topic": topic,
            "context": context
        })