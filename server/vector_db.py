from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
import numpy as np



class VectorStore:
    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')  # Modelo ligero
    
    def create_from_arxiv(self, papers: list):
        """Convierte papers de arXiv en vectores"""
        texts = [paper['summary'] for paper in papers]
        metadatos = [{
            'title': paper['title'],
            'authors': paper['authors'],
            'url': paper['url']
        } for paper in papers]
        
        embeddings = self.encoder.encode(texts)
        self.db = FAISS.from_embeddings(
            text_embeddings=list(zip(texts, embeddings)),
            embedding=self.encoder,
            metadatas=metadatos
        )
    
    def save(self, path: str):
        self.db.save_local(path)
    
    def load(self, path: str):
      self.db = FAISS.load_local(
    folder_path=path,
    embeddings=self.encoder,
    allow_dangerous_deserialization=True
)
