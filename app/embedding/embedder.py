# app/embedding/embedder.py

from sentence_transformers import SentenceTransformer

# Load model (you can use different models if desired)
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embeddings(text_chunks: list[str]) -> list[list[float]]:
    """
    Convert a list of text chunks into embeddings.
    """
    return model.encode(text_chunks, convert_to_numpy=True).tolist()