# app/vectorstore/chroma_store.py

import chromadb
from typing import List
from chromadb.config import Settings

from app.embedding.embedder import get_embeddings

# Setup Chroma client
chroma_client = chromadb.HttpClient(
    host="chromadb",
    port=8000,
    settings=Settings(anonymized_telemetry=False)
)

def get_chroma_collection(user_id: str):
    return chroma_client.get_or_create_collection(name=f"docs_{user_id}")

def add_to_chroma(docs: list[str], embeddings: list[list[float]], filename: str, user_id: str):
    """
    Add chunks + embeddings + metadata (filename, chunk index) to ChromaDB.
    """
    ids = [f"{filename}_chunk_{i}" for i in range(len(docs))]
    
    metadatas = [
        {"source": filename, "chunk_index": i} for i in range(len(docs))
    ]

    collection = get_chroma_collection(user_id)
    collection.add(
        documents=docs,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )
    
    print(f"✅ Added {len(docs)} chunks from {filename} to ChromaDB")

def check_chroma(user_id: str):
    collection = get_chroma_collection(user_id)
    results = collection.get(include=["documents", "embeddings", "metadatas"])

    print(f"📦 Total documents in collection: {len(results['ids'])}")
    for doc_id, doc in zip(results["ids"], results["documents"]):
        print(f"\n🧾 {doc_id}:\n{doc[:200]}...")  # print first 200 characters

    # results = collection.query(
    #     query_texts=["What is DocuChat?"], 
    #     n_results=1
    # )

    # print(results)

def delete_collection(user_id: str):
    """
    Deletes the entire collection from ChromaDB.
    """
    try:
        # collection.delete() it somehow keeps the context or embeddings of the previous doc also even when deleted.
        chroma_client.delete_collection(name=f"docs_{user_id}")
        print(f"✅ Deleted docs_{user_id} collection from ChromaDB.")
    except chromadb.errors.NotFoundError:
        print(f"⚠️ Collection docs_{user_id} did not exist. Skipping deletion.")


def delete_by_ids(ids: list[str], user_id: str):
    """
    Deletes specific chunks by their IDs.
    """
    collection = get_chroma_collection(user_id)
    collection.delete(ids=ids)
    print(f"✅ Deleted {len(ids)} chunks by IDs from ChromaDB.")


def delete_by_metadata(metadata_filter: dict, user_id: str):
    """
    Deletes documents/embeddings based on metadata filter.
    """
    collection = get_chroma_collection(user_id)
    collection.delete(where=metadata_filter)
    print(f"✅ Deleted chunks matching metadata filter {metadata_filter} from ChromaDB.")

def retrieve_relevant_chunks(query: str, top_k: int = 5, user_id: str = None) -> List[str]:
    # Step 1: Convert query to embedding
    query_embedding = get_embeddings(query)

    # Step 2: Perform vector search
    collection = get_chroma_collection(user_id)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents"]
    )

    # Step 3: Return matched chunks
    return results["documents"][0]