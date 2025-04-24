# scripts/query_llama.py

from app.vectorstore.chroma_store import collection
from app.embedding.embedder import get_embeddings
from app.llm.llama_client import ask_llama
from app.prompts.templates import DEFAULT_PROMPT

def retrieve_context(query: str, k: int = 3) -> str:
    embedding = get_embeddings(query)
    results = collection.query(
        query_embeddings=[embedding],
        n_results=k,
        include=["documents"]
    )
    return "\n\n".join(results["documents"][0])

if __name__ == "__main__":
    query = "What is DocuChat?"
    context = retrieve_context(query)
    answer = ask_llama(query, context, DEFAULT_PROMPT)

    print(f"❓ Question: {query}\n")
    print(f"📄 Context:\n{context[:300]}...\n")
    print(f"💬 Answer:\n{answer}")