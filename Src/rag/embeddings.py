import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def embed_document(texto: str) -> list[float]:
    resultado = client.models.embed_content(
        model="gemini-embedding-001",
        contents=texto,
        config={"task_type": "RETRIEVAL_DOCUMENT"}
    )
    return resultado.embeddings[0].values


def embed_query(texto: str) -> list[float]:
    resultado = client.models.embed_content(
        model="gemini-embedding-001",
        contents=texto,
        config={"task_type": "RETRIEVAL_QUERY"}
    )
    return resultado.embeddings[0].values


if __name__ == "__main__":
    vetor = embed_document("O cancelamento pode ser feito a qualquer momento, sem multa.")
    print(f"Tamanho do vetor: {len(vetor)}")
    print(vetor[:5])