import re


def split_by_section(texto: str) -> list[dict]:
    padrao_secao = re.compile(r"^\d+\.\s+.+$", re.MULTILINE)

    titulos = padrao_secao.findall(texto)
    posicoes = [m.start() for m in padrao_secao.finditer(texto)]

    chunks = []
    for i, titulo in enumerate(titulos):
        inicio = posicoes[i]
        fim = posicoes[i + 1] if i + 1 < len(posicoes) else len(texto)
        conteudo = texto[inicio:fim].strip()
        chunks.append({
            "section": titulo.strip(),
            "content": conteudo
        })

    return chunks


if __name__ == "__main__":
    from loader import load_pdf

    texto = load_pdf("data/raw/politica-de-privacidade.pdf")
    chunks = split_by_section(texto)

    print(f"Total de chunks: {len(chunks)}\n")
    for chunk in chunks:
        print(f"[{chunk['section']}]")
        print(chunk['content'][:150])
        print()