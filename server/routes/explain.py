from fastapi import APIRouter, Query
import os
import logging
from server.RAG.rag_chain import ScientificRAG

router = APIRouter()

@router.get("")
async def explain_science(
    social_network: str = Query(...),
    topic: str = Query(...),
    company_info: str = Query(""),
    voice: str = Query(""),
    language: str = Query("es")
):
    try:
        rag = ScientificRAG(os.path.join("server", "RAG", "server", "vectorstore"))
        rag.initialize_prompt(social_network, topic, company_info, voice, language)
        result = rag.explain_concept(topic)
        return {
            "topic": topic,
            "social_network": social_network,
            "explanation": result["answer"],
            "sources": result["sources"]
        }
    except Exception as e:
        logging.error(f"Error en /explain: {str(e)}")
        return {"error": str(e)}, 500