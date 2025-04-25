from app.vectorstore.chroma_store import get_chroma_collection

def test_collection_query():
    collection = get_chroma_collection()
    results = collection.query(query_texts=["What is context?"], n_results=2, include=["documents"])
    
    assert "documents" in results
    assert len(results["documents"][0]) > 0