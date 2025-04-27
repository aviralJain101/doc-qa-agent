# app/api/upload.py
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import os
from app.ingestion.parsers import parse_file
from app.embedding.embedder import get_embeddings
from app.ingestion.chunker import chunk_text
from app.vectorstore.chroma_store import add_to_chroma, delete_collection

router = APIRouter()

UPLOAD_FOLDER = "uploaded_docs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # Save uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Currently only single file support is implemented so delete any existing collections
    delete_collection()
    # Parse, chunk, embed, and store
    raw_text = parse_file(file_path)
    chunks = chunk_text(raw_text)
    embeddings = get_embeddings(chunks)
    add_to_chroma(chunks, embeddings, file.filename)

    # 🧹 Auto-delete file after ingestion
    try:
        os.remove(file_path)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"File ingested, but failed to delete {file_path}: {str(e)}"}
        )

    return {"message": f"✅ {file.filename} uploaded, indexed and deleted successfully."}