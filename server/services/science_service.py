from uuid import UUID
from typing import List
from fastapi import HTTPException, status

from langchain_community.document_loaders import PubMedLoader, ArxivLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import SystemMessage, HumanMessage
from langchain_groq import ChatGroq

from server.config.settings import settings
from server.models.science import ScienceRequest

# Mapeo de idioma para el prompt
LANG_LABEL = {
    "es": "español",
    "en": "English",
    "fr": "français"
}

async def generate_science_content(request: ScienceRequest, user_id: UUID) -> dict:
    # 1. Cargar documentos de PubMed y arXiv
    docs = []
    try:
        pm_loader = PubMedLoader(query=request.topic, load_max_docs=3)
        docs += pm_loader.load()
    except Exception as e:
        print(f"[warning] PubMedLoader falló: {e}")
    try:
        arx_loader = ArxivLoader(query=request.topic, load_max_docs=2)
        docs += arx_loader.load()
    except Exception as e:
        print(f"[warning] ArxivLoader falló: {e}")

    if not docs:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se han podido cargar documentos científicos."
        )

    # 2. Dividir en chunks semánticos
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    # 3. Crear vectorstore FAISS con embeddings gratuitos
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # 4. Recuperar los fragmentos más relevantes
    relevant_docs = vectorstore.similarity_search(request.topic, k=3)
    relevant_chunks: List[str] = []
    for doc in relevant_docs:
        title = doc.metadata.get("Title", "Documento científico")
        snippet = doc.page_content[:500].replace("\n", " ").strip()
        relevant_chunks.append(f"Fuente: {title}\n{snippet}...")

    # 5. Construir contexto para el LLM
    scientific_context = (
        "DOCUMENTOS CIENTÍFICOS RELEVANTES:\n"
        + ("\n\n".join(relevant_chunks) if relevant_chunks else "No se encontraron documentos.")
    )
    language_instruction = {
        "es": "Responde ÚNICAMENTE en español.",
        "en": "Respond ONLY in English.",
        "fr": "Réponds UNIQUEMENT en français."
    }.get(request.language, "Responde en español.")

    system_prompt = f"""
Eres un experto divulgador científico en biomedicina.
{language_instruction}
{scientific_context}

IMPORTANTE:
- Usa solo la información de las fuentes proporcionadas.
- Explica conceptos técnicos con claridad.
- Mantén un tono accesible para el público general.
- Estructura el artículo con introducción, desarrollo y conclusión.
"""

    user_prompt = f"Crea un artículo divulgativo sobre: {request.topic}"

    # 6. Llamada al LLM con manejo de errores
    llm = ChatGroq(
        groq_api_key=settings.GROQ_API_KEY,
        model_name="llama3-8b-8192",
        temperature=0.7
    )
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    try:
        response = llm.invoke(messages)
        text = response.content
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error en la generación del LLM: {e}"
        )

    return {"text_content": text}
