# app/api/query.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.vectorstore.chroma_store import get_chroma_collection
from app.embedding.embedder import get_embeddings
from app.llm.groq_client import ask_groq
from app.prompts.templates import DEFAULT_PROMPT

router = APIRouter()

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

@router.post("/query", response_model=QueryResponse)
def query_doc(request: QueryRequest):
    context = retrieve_context(request.question, request.k)
    answer = ask_groq(request.question, context, DEFAULT_PROMPT)
    return QueryResponse(answer=answer, context=context)