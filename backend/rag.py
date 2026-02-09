import pickle
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

faiss_store = FAISS.load_local(
    "data/faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

with open("data/bm25.pkl", "rb") as f:
    bm25 = pickle.load(f)

def hybrid_retrieve(query, k=4):
    dense_docs = faiss_store.similarity_search(query, k=k)
    sparse_docs = bm25.invoke(query)[:k]

    seen, combined = set(), []
    for doc in dense_docs + sparse_docs:
        if doc.page_content not in seen:
            seen.add(doc.page_content)
            combined.append(doc)

    return combined[:k]