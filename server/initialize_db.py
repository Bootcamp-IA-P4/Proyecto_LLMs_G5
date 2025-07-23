from server.arxiv_processor import get_arxiv_papers
from server.vector_db import VectorStore

papers = get_arxiv_papers("quantum computing", max_results=50)
vector_db = VectorStore()
vector_db.create_from_arxiv(papers)
vector_db.save("server/vectorstore")  

