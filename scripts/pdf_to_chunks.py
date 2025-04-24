import os
from app.embedding.embedder import get_embeddings
from app.ingestion.parsers import parse_pdf
from app.ingestion.chunker import chunk_text
from app.vectorstore.chroma_store import add_to_chroma


def ingest_pdf(file_path: str):
    print(f"Reading: {file_path}")
    raw_text = parse_pdf(file_path)
    chunks = chunk_text(raw_text)

    print(f"Total chunks: {len(chunks)}")

    embeddings = get_embeddings(chunks)
    print(f"Generated {len(embeddings)} embeddings.")
    print(f"Sample embedding (first 5 values):\n{embeddings[0][:5]}")

    filename = os.path.basename(file_path)
    add_to_chroma(chunks, embeddings, filename)

# ✅ This block ensures the script runs only when executed directly
if __name__ == "__main__":
    ingest_pdf("sts.pdf")
    print("Ingestion complete.")