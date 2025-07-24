import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def get_arxiv_papers(query: str, max_results: int = 3) -> List[Dict]:
    """
    Versión corregida con manejo de parsers
    """
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&max_results={max_results}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Intenta primero con lxml, luego con html.parser
        try:
            soup = BeautifulSoup(response.text, 'lxml-xml')  # Versión XML específica
        except:
            soup = BeautifulSoup(response.text, 'html.parser')
        
        papers = []
        for entry in soup.find_all('entry'):
            paper = {
                'title': entry.title.text.strip(),
                'authors': [author.find('name').text.strip() for author in entry.find_all('author')],
                'summary': entry.summary.text.strip(),
                'published': entry.published.text.strip(),
                'url': entry.id.text.strip()
            }
            papers.append(paper)
        
        return papers
    
    except Exception as e:
        print(f"🚨 Error al consultar arXiv: {str(e)}")
        return []

if __name__ == "__main__":
    print("🔍 Buscando papers en arXiv sobre 'quantum computing'...")
    papers = get_arxiv_papers("quantum computing")
    
    if not papers:
        print("⚠️ No se encontraron resultados o hubo un error")
    else:
        for i, paper in enumerate(papers):
            print(f"\n📄 Paper #{i+1}")
            print(f"🏷️ Título: {paper['title']}")
            print(f"👥 Autores: {', '.join(paper['authors'])}")
            print(f"📅 Fecha: {paper['published']}")
            print(f"🌐 URL: {paper['url']}")
            print(f"📝 Resumen: {paper['summary'][:200]}...")