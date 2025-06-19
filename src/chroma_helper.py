import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from uuid import uuid4

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(
    name="book_versions",
    embedding_function=SentenceTransformerEmbeddingFunction()
)

def save_version_to_chroma(content, label):
    doc_id = str(uuid4())
    collection.add(
        documents=[content],
        ids=[doc_id],
        metadatas=[{"label": label}]
    )
    return doc_id

def query_similar_versions(query_text, n_results=3):
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return results
