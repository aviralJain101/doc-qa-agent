# main.py
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os

from app.vectorstore.chroma_store import get_chroma_collection
from app.embedding.embedder import get_embeddings
from app.ingestion.parsers import parse_file
from app.ingestion.chunker import chunk_text
from app.vectorstore.chroma_store import add_to_chroma
from app.vectorstore.chroma_store import delete_collection
from app.llm.groq_client import ask_groq
from app.prompts.templates import DEFAULT_PROMPT

app = FastAPI()

UPLOAD_FOLDER = "uploaded_docs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class QueryRequest(BaseModel):
    question: str
    k: int = 5  # optional, default to 5

class QueryResponse(BaseModel):
    answer: str
    context: str

def retrieve_context(query: str, k: int = 5) -> str:
    embedding = get_embeddings(query)
    collection = get_chroma_collection()
    if not collection:
        raise HTTPException(status_code=500, detail="ChromaDB collection not found.")
    results = collection.query(
        query_embeddings=[embedding],
        n_results=k,
        include=["documents"]
    )
    if not results["documents"]:
        raise HTTPException(status_code=404, detail="No relevant documents found.")
    return "\n\n".join(results["documents"][0])

@app.post("/query", response_model=QueryResponse)
def query_doc(request: QueryRequest):
    context = retrieve_context(request.question, request.k)
    answer = ask_groq(request.question, context, DEFAULT_PROMPT)
    return QueryResponse(answer=answer, context=context)


@app.post("/upload")
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