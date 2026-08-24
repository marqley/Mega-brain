import chromadb

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="catracloud")


def add_chunk(chunk_id: str, embedding: list[float], texto: str, metadata: dict):
    collection.add(
        ids=[chunk_id],
        embeddings=[embedding],
        documents=[texto],
        metadatas=[metadata]
    )


def query(embedding: list[float], n_results: int = 4):
    return collection.query(
        query_embeddings=[embedding],
        n_results=n_results
    )