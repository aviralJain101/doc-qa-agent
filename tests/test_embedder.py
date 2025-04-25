from app.embedding.embedder import get_embeddings

def test_get_embeddings():
    texts = ["What is DeepSeek?", "Explain RAG."]
    embeddings = get_embeddings(texts)
    
    assert len(embeddings) == 2
    assert all(isinstance(e, list) for e in embeddings)
    assert all(len(e) > 0 for e in embeddings)