from uuid import UUID
from typing import List, Dict, Any
import json

from fastapi import HTTPException, status

from langchain_community.document_loaders import ArxivLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import SystemMessage, HumanMessage
from langchain_groq import ChatGroq

from server.config.settings import settings
from server.models.science import ScienceRequest, SourceInfo
from server.utils.database import get_supabase

from langchain_chroma import Chroma
from server.chroma_db.connection_db import client

# Modelos disponibles
AVAILABLE_MODELS = {
    "llama3-8b-8192": "llama3-8b-8192",
    "gemma2-9b-it": "gemma2-9b-it",
}

# Mapeo de idioma para el prompt
LANG_INSTRUCTIONS = {
    "es": "Responde ÚNICAMENTE en español.",
    "en": "Respond ONLY in English.",
    "fr": "Réponds UNIQUEMENT en français."
}

def extract_source_info(doc) -> Dict[str, Any]:
    """Extrae información relevante de los metadatos del documento"""
    metadata = doc.metadata
    return {
        "title": metadata.get('Title', 'Documento sin título'),
        "authors": metadata.get('Authors', None),
        "published": metadata.get('Published', None),
        "url": metadata.get('entry_id', None),
        "summary": doc.page_content[:200].replace('\n', ' ').strip() + "..."
    }

async def save_science_post(user_id: UUID, request: ScienceRequest, content: str, sources: List[Dict[str, Any]]) -> UUID:
    """Guarda el post científico en la base de datos"""
    try:
        supabase = get_supabase()
        result = supabase.table("science_posts").insert({
            "user_id": str(user_id),
            "topic": request.topic,
            "audience": request.audience,
            "language": request.language,
            "model": request.model,
            "max_docs": request.max_docs,
            "text_content": content,
            "sources": sources
        }).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al guardar el post científico"
            )
        
        return UUID(result.data[0]["id"])
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al guardar en base de datos: {str(e)}"
        )

async def generate_science_content(request: ScienceRequest, user_id: UUID) -> dict:
    # Validar modelo
    if request.model not in AVAILABLE_MODELS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Modelo no disponible. Opciones: {list(AVAILABLE_MODELS.keys())}"
        )
    
    # 1. Cargar desde ArXiv
    try:
        loader = ArxivLoader(query=request.topic, load_max_docs=request.max_docs)
        docs = loader.load()
    except Exception as e:
        docs = []
        print(f"[warning] ArxivLoader falló: {e}")

    if not docs:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se han encontrado documentos en ArXiv para el tema especificado."
        )

    # 2. Dividir en chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    # 3. Embeddings + FAISS
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Si se usa FAISS, descomentar la siguiente línea:
    # store = FAISS.from_documents(chunks, embeddings)

    collection_name = "science_arxiv"

    vector_store = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings,
    )
    
    # Añadir documentos a la colección
    print(len(chunks))
    vector_store.add_documents(chunks)

    # 4. Recuperar los más relevantes (máximo 5)
    k_relevant = min(5, len(chunks))
    relevant = vector_store.similarity_search_with_score(request.topic, k=k_relevant)
    
    # Extraer información de fuentes
    sources_info = []
    unique_sources = set()
    
    for doc, score in relevant:
        source_info = extract_source_info(doc)
        source_key = source_info["title"]
        
        # Evitar duplicados por título
        if source_key not in unique_sources:
            source_info["relevance_score"] = float(1 - score)  # Convertir distancia a relevancia
            sources_info.append(source_info)
            unique_sources.add(source_key)

    # Preparar contexto para el LLM
    snippets = []
    for i, (doc, score) in enumerate(relevant):
        title = doc.metadata.get('Title', f'Documento {i+1}')
        content = doc.page_content[:400].replace('\n', ' ').strip()
        snippets.append(f"Fuente {i+1}: {title}\n{content}...")
    
    context = "DOCUMENTOS CIENTÍFICOS DE ARXIV:\n\n" + "\n\n".join(snippets)

    # 5. Preparar prompt
    lang_instr = LANG_INSTRUCTIONS.get(request.language, "Responde en español.")
    
    system_prompt = f"""Eres un experto divulgador científico especializado en biomedicina.

{lang_instr}

Tienes acceso a los siguientes documentos científicos de ArXiv:

{context}

INSTRUCCIONES:
- Crea un artículo divulgativo dirigido a: {request.audience}
- Usa ÚNICAMENTE la información de los documentos proporcionados
- Explica conceptos técnicos con claridad y precisión
- Estructura: introducción, desarrollo con subtemas, conclusión
- Menciona las fuentes cuando sea relevante
- Mantén rigor científico pero lenguaje accesible"""

    user_prompt = f"Crea un artículo divulgativo sobre: {request.topic}"

    # 6. Invocar LLM
    llm = ChatGroq(
        groq_api_key=settings.GROQ_API_KEY,
        model_name=request.model,
        temperature=0.7
    )
    
    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        text_content = response.content
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error en la generación del LLM: {str(e)}"
        )

    # 7. Guardar en base de datos
    post_id = await save_science_post(user_id, request, text_content, sources_info)

    # 8. Preparar respuesta
    source_objects = [
        SourceInfo(
            title=src["title"],
            authors=src.get("authors"),
            published=src.get("published"),
            url=src.get("url"),
            relevance_score=src.get("relevance_score")
        ) for src in sources_info
    ]

    return {
        "id": post_id,
        "text_content": text_content,
        "sources": source_objects,
        "total_sources": len(source_objects)
    }