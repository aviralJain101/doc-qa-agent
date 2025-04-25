# scripts/test_retrieve.py
import time
from app.vectorstore.chroma_store import retrieve_relevant_chunks

start = time.time()
query = "What is DocuChat?"
results = retrieve_relevant_chunks(query)
print("⏱️ Retrieval time:", round(time.time() - start, 3), "seconds")

print(f"\nTop chunks for query: '{query}'")
for i, chunk in enumerate(results):
    print(f"\n--- Result {i+1} ---\n{chunk[:300]}...\n")