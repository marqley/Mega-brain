import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.ingestion.loader import load_pdf
from src.ingestion.chunker import split_by_section
from src.rag.embeddings import embed_document
from src.rag.vectorstore import add_chunk

arquivos = [
    "politica-de-privacidade.pdf",
    "base-conhecimento-produto.pdf",
    "faq-suporte.pdf",
    "planos-precos.pdf",
    "termos-de-uso.pdf",
]

for arquivo in arquivos:
    caminho = f"data/raw/{arquivo}"
    texto = load_pdf(caminho)
    chunks = split_by_section(texto)

    for i, chunk in enumerate(chunks):
        embedding = embed_document(chunk["content"])
        chunk_id = f"{arquivo}-{i}"

        add_chunk(
            chunk_id=chunk_id,
            embedding=embedding,
            texto=chunk["content"],
            metadata={"source": arquivo, "section": chunk["section"]}
        )

        print(f"Indexado: {chunk_id} — {chunk['section']}")

print("\nIngestão concluída.")