from uuid import UUID
from typing import List

from fastapi import HTTPException, status

from langchain_community.document_loaders import ArxivLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import SystemMessage, HumanMessage
from langchain_groq import ChatGroq

from server.config.settings import settings
from server.models.science import ScienceRequest 

# Modelos disponibles
AVAILABLE_MODELS = {
    "llama3-8b-8192": "llama3-8b-8192",
    "gemma2-9b-it": "gemma2-9b-it",
}

# Mapeo de idioma para el prompt
LANG_LABEL = {
    "es": "español",
    "en": "English",
    "fr": "français"
}

async def generate_science_content(request: ScienceRequest, user_id: UUID) -> dict:
    # 1. Cargar solo desde ArXiv
    try:
        loader = ArxivLoader(query=request.topic, load_max_docs=5)
        docs = loader.load()
    except Exception as e:
        docs = []
        print(f"[warning] ArxivLoader falló: {e}")

    if not docs:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se han encontrado documentos en ArXiv."
        )

    # 2. Dividir en chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    # 3. Embeddings + FAISS
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    store = FAISS.from_documents(chunks, embeddings)

    # 4. Recuperar los 3 más relevantes
    relevant = store.similarity_search(request.topic, k=3)
    snippets = [
        f"Fuente: {d.metadata.get('Title','Documento')}\n{d.page_content[:300].replace(chr(10),' ')}..."
        for d in relevant
    ]
    context = "DOCUMENTOS RELEVANTES:\n\n" + "\n\n".join(snippets)

    # 5. Preparar prompt
    lang_instr = {
        "es": "Responde ÚNICAMENTE en español.",
        "en": "Respond ONLY in English.",
        "fr": "Réponds UNIQUEMENT en français."
    }.get(request.language, "Responde en español.")
    system_prompt = f"""
Eres un experto divulgador científico.
{lang_instr}

{context}

IMPORTANTE:
- Usa únicamente información de ArXiv.
- Explica conceptos técnicos con claridad.
- Tono accesible, estructura: introducción, desarrollo, conclusión.
"""
    user_prompt = f"Crea un artículo divulgativo sobre: {request.topic}"

    # 6. Invocar LLM
    llm = ChatGroq(
        groq_api_key=settings.GROQ_API_KEY,
        model_name=AVAILABLE_MODELS.get(request.language, AVAILABLE_MODELS["llama3-8b-8192"]),
        temperature=0.7
    )
    try:
        resp = llm.invoke([SystemMessage(content=system_prompt),
                           HumanMessage(content=user_prompt)])
        text = resp.content
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error en la generación del LLM: {e}"
        )

    return {"text_content": text}
