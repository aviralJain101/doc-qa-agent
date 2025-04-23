# app/vectorstore/chroma_store.py

import chromadb
from chromadb.config import Settings

# Setup Chroma client
chroma_client = chromadb.HttpClient(
    host="localhost",
    port=8000,
    settings=Settings(anonymized_telemetry=False)
)

# Create collection (will be reused if already exists)
collection = chroma_client.get_or_create_collection(name="docs")

def add_to_chroma(docs: list[str], embeddings: list[list[float]], filename: str):
    """
    Add chunks + embeddings + metadata (filename, chunk index) to ChromaDB.
    """
    ids = [f"{filename}_chunk_{i}" for i in range(len(docs))]
    
    metadatas = [
        {"source": filename, "chunk_index": i} for i in range(len(docs))
    ]

    collection.add(
        documents=docs,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )
    
    print(f"✅ Added {len(docs)} chunks from {filename} to ChromaDB")