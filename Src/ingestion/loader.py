import pdfplumber


def format_table(tabela: list[list[str]]) -> str:
    cabecalho = tabela[0]
    linhas_formatadas = []

    for linha in tabela[1:]:
        rotulo = linha[0]
        pares = [f"{cabecalho[i]}: {linha[i]}" for i in range(1, len(linha))]
        linhas_formatadas.append(f"{rotulo} — " + ", ".join(pares))

    return "\n".join(linhas_formatadas)


def extract_page_content(pagina) -> str:
    tabelas = pagina.find_tables()

    if not tabelas:
        texto = pagina.extract_text()
        return texto + "\n" if texto else ""

    tabelas_ordenadas = sorted(tabelas, key=lambda t: t.bbox[1])
    partes = []
    y_atual = 0

    for tabela in tabelas_ordenadas:
        topo = tabela.bbox[1]
        regiao_antes = pagina.within_bbox((0, y_atual, pagina.width, topo))
        texto_antes = regiao_antes.extract_text()
        if texto_antes:
            partes.append(texto_antes)

        partes.append(format_table(tabela.extract()))
        y_atual = tabela.bbox[3]

    regiao_final = pagina.within_bbox((0, y_atual, pagina.width, pagina.height))
    texto_final = regiao_final.extract_text()
    if texto_final:
        partes.append(texto_final)

    return "\n".join(partes) + "\n"


def load_pdf(caminho_arquivo: str) -> str:
    texto_completo = ""

    with pdfplumber.open(caminho_arquivo) as pdf:
        for pagina in pdf.pages:
            texto_completo += extract_page_content(pagina)

    return texto_completo


if __name__ == "__main__":
    texto = load_pdf("data/raw/faq-suporte.pdf")
    print(texto)