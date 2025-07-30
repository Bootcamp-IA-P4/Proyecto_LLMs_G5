import chromadb
from server.config.settings import settings

import os
client = chromadb.CloudClient(
    api_key=settings.CHROMA_API_KEY,
    tenant=settings.CHROMA_TENANT,
    database=settings.CHROMA_DATABASE)