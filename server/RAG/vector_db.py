# server/vector_db.py
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document # Necesario para FAISS.from_documents
import os
import numpy as np # Necesario para SentenceTransformer.encode si lo usaras fuera de LangChain, pero no aquí.

class VectorStore:
    def __init__(self):
        # Usamos HuggingFaceEmbeddings de LangChain, que es el Wrapper correcto.
        self.encoder = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

    def create_from_arxiv(self, papers: list):
        """Convierte papers de arXiv en objetos Document y crea la DB."""
        documents = []
        for paper in papers:
            # Aseguramos que 'summary' es una cadena y los metadatos son un diccionario.
            if isinstance(paper.get('summary'), str):
                doc = Document(
                    page_content=paper['summary'],
                    metadata={
                        'title': paper.get('title', 'N/A'),
                        'authors': paper.get('authors', []),
                        'url': paper.get('url', 'N/A')
                    }
                )
                documents.append(doc)
            else:
                print(f"Advertencia: Resumen de paper no es una cadena y será omitido: {paper.get('summary')}")


        if not documents:
            raise ValueError("No se pudieron crear documentos válidos para la base de datos de vectores.")

        # Crea la base de datos a partir de los objetos Document y el encoder de LangChain.
        # Esto asegura que los textos se manejen internamente como strings.
        self.db = FAISS.from_documents(documents, self.encoder)

    def save(self, path: str):
        # Asegúrate de que el directorio exista antes de guardar
        os.makedirs(path, exist_ok=True)
        self.db.save_local(path)

    def load(self, path: str):
        # Al cargar, pasamos la misma función de embeddings para consistencia.
        self.db = FAISS.load_local(
            folder_path=path,
            embeddings=self.encoder, # ¡Importante! Usamos self.encoder (HuggingFaceEmbeddings)
            allow_dangerous_deserialization=True # Necesario para versiones recientes de LangChain al cargar bases de datos
        )