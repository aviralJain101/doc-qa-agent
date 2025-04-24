from scripts.pdf_to_chunks import ingest_pdf
from app.vectorstore.chroma_store import delete_collection
from app.vectorstore.chroma_store import check_chroma


if __name__ == "__main__":
    delete_collection()

    file_path = "sts.pdf"
    ingest_pdf(file_path)
    print("Ingestion complete.")

    check_chroma()