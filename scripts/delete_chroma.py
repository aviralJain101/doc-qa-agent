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


def delete_collection():
    """
    Deletes the entire collection from ChromaDB.
    """
    chroma_client.delete_collection("docs")
    print("✅ Deleted 'docs' collection from ChromaDB.")


def delete_by_ids(ids: list[str]):
    """
    Deletes specific chunks by their IDs.
    """
    collection.delete(ids=ids)
    print(f"✅ Deleted {len(ids)} chunks by IDs from ChromaDB.")


def delete_by_metadata(metadata_filter: dict):
    """
    Deletes documents/embeddings based on metadata filter.
    """
    collection.delete(where=metadata_filter)
    print(f"✅ Deleted chunks matching metadata filter {metadata_filter} from ChromaDB.")


# Example: Deleting the entire collection
delete_collection()

# Example: Deleting specific chunks by their IDs
# delete_by_ids(["DocuChat.pdf_chunk_0", "DocuChat.pdf_chunk_1"])

# Example: Deleting all chunks from a specific file using metadata filter
# delete_by_metadata({"source": "DocuChat.pdf"})