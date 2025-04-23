# scripts/check_chroma.py

from app.vectorstore.chroma_store import collection

results = collection.get(include=["documents", "embeddings", "metadatas"])

print(f"📦 Total documents in collection: {len(results['ids'])}")
for doc_id, doc in zip(results["ids"], results["documents"]):
    print(f"\n🧾 {doc_id}:\n{doc[:200]}...")  # print first 200 characters

# results = collection.query(
#     query_texts=["What is DocuChat?"], 
#     n_results=1
# )

# print(results)