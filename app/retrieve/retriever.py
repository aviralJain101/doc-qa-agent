# app/retrieve/retriever.py

from typing import List
from app.embedding.embedder import get_embeddings
import chromadb

# Setup ChromaDB client and collection
client = chromadb.HttpClient(host="localhost", port=8000)
collection = client.get_collection(name="docs")

def retrieve_relevant_chunks(query: str, top_k: int = 5) -> List[str]:
    # Step 1: Convert query to embedding
    query_embedding = get_embeddings(query)

    # Step 2: Perform vector search
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents"]
    )

    # Step 3: Return matched chunks
    return results["documents"][0]