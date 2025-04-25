from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_query_endpoint():
    response = client.post("/query", json={"question": "What is RAG?", "k": 2})
    
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "context" in data