# scripts/eval_recall.py

from app.vectorstore.chroma_store import collection
from app.embedding.embedder import get_embeddings  # your embedding logic

# Define evaluation set: queries and expected phrases
eval_set = [
    {
        "query": "What file formats are supported?",
        "expected_snippet": "pdf, markdown, txt"
    },
    {
        "query": "What is the purpose of DocuChat?",
        "expected_snippet": "end-to-end document Q&A microservice"
    },
    {
        "query": "How is the system tested?",
        "expected_snippet": "automated tests covering"
    },
]

TOP_K = 3
hits = 0

for i, item in enumerate(eval_set):
    query = item["query"]
    expected = item["expected_snippet"].lower()

    print(f"\n🔎 Query {i+1}: {query}")
    embedding = get_embeddings(query)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=TOP_K,
        include=["documents"]
    )

    documents = results["documents"][0]

    # Check if expected snippet is present in any of the returned documents
    found = any(expected in doc.lower() for doc in documents)

    if found:
        print("✅ Match found!")
        hits += 1
    else:
        print("❌ Match NOT found!")
        print("Returned chunks:")
        for doc in documents:
            print("—", doc[:100].replace("\n", " "), "...")

recall = hits / len(eval_set)
print(f"\n📊 Recall @ top-{TOP_K}: {recall:.2f}")