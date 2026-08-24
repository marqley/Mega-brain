import os
from dotenv import load_dotenv
from google import genai

from src.rag.embeddings import embed_query
from src.rag.vectorstore import query as buscar_chunks

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

PROMPT_SISTEMA = """Você é um assistente que responde exclusivamente com base no contexto fornecido abaixo.
Se a resposta não estiver no contexto, diga que não encontrou essa informação na base — não invente.

Contexto:
{contexto}

Pergunta: {pergunta}

Responda de forma direta e cite a fonte (documento/seção) quando possível."""


def montar_contexto(resultados) -> str:
    documentos = resultados["documents"][0]
    metadados = resultados["metadatas"][0]

    partes = []
    for texto, meta in zip(documentos, metadados):
        partes.append(f"[Fonte: {meta['source']} — {meta['section']}]\n{texto}")

    return "\n\n".join(partes)


def responder(pergunta: str) -> str:
    embedding_pergunta = embed_query(pergunta)
    resultados = buscar_chunks(embedding_pergunta, n_results=4)
    contexto = montar_contexto(resultados)

    prompt_final = PROMPT_SISTEMA.format(contexto=contexto, pergunta=pergunta)

    resposta = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt_final
    )

    return resposta.text


if __name__ == "__main__":
    pergunta = "Quanto custa o plano Enterprise?"
    print(responder(pergunta))