"""Lab 12 — Ingestion stage: chunk policy documents, embed, store in ChromaDB."""
from sentence_transformers import SentenceTransformer
import chromadb


def chunk_document(text, chunk_size=300, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def build_collection():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    client = chromadb.Client()
    collection = client.create_collection("datashop_policies")

    policies = {
        "annual_leave": open("annual_leave_policy.txt").read(),
        "travel_expense": open("travel_expense_policy.txt").read(),
        "office": open("office_policy.txt").read(),
        "data_platform": open("data_platform_policy.txt").read(),
    }

    ids = []
    documents = []
    metadatas = []
    embeddings = []

    for policy_name, text in policies.items():
        chunks = chunk_document(text)
        for i, chunk in enumerate(chunks):
            ids.append(f"{policy_name}_chunk_{i}")
            documents.append(chunk)
            metadatas.append({"source": policy_name, "chunk_index": i})
            embeddings.append(model.encode(chunk).tolist())
        print(f"{policy_name}: {len(chunks)} chunks")

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    print(f"\nStored {len(ids)} chunks across {len(policies)} policy documents")
    return model, collection


if __name__ == "__main__":
    build_collection()
