# Mega-brain — Agente Inteligente CatraCloud

Projeto desenvolvido para o **Challenge Alura Agente**: um agente de IA baseado em RAG (Retrieval-Augmented Generation) capaz de responder perguntas em linguagem natural sobre a documentação de um SaaS fictício de controle de acesso por catraca, a **CatraCloud**.

## Sobre o projeto

O agente responde perguntas de usuários com base em 5 documentos da base de conhecimento da CatraCloud:

- Base de conhecimento do produto
- FAQ de suporte
- Política de privacidade
- Planos e preços
- Termos de uso

Todo o conteúdo é fictício, criado especificamente para este projeto.

## Arquitetura

```
[PDFs em data/raw/]
        │
        ▼
  loader.py (pdfplumber)
  extrai texto + tabelas de cada PDF
        │
        ▼
  chunker.py
  divide o texto por seção numerada (regex)
        │
        ▼
  embeddings.py (Gemini API — gemini-embedding-001)
  gera um vetor por chunk
        │
        ▼
  vectorstore.py (Chroma)
  persiste os vetores em chroma_db/
        │
        ▼
  pipeline.py
  busca os chunks mais relevantes para a pergunta,
  monta o prompt com o contexto recuperado
  e chama o Gemini (gemini-3.5-flash) para gerar a resposta
        │
        ▼
  streamlit_app.py
  interface de chat que consome o pipeline diretamente
```

### Por que essas escolhas

- **Chunking por seção numerada, não por tamanho fixo**: preserva o sentido completo de cada trecho, já que cada seção do conteúdo é uma unidade de significado própria.
- **Extração de tabelas com posicionamento correto**: as tabelas de "Planos e Preços" e "Métodos de identificação" são extraídas respeitando sua posição na página, evitando que o conteúdo de uma tabela seja misturado à seção errada do texto.
- **`task_type` diferente para indexação e busca**: os documentos são indexados com `RETRIEVAL_DOCUMENT` e a pergunta do usuário é embedada com `RETRIEVAL_QUERY`, melhorando a precisão da busca por similaridade.
- **Sem camada de API separada**: o Streamlit chama o pipeline diretamente, reduzindo complexidade de deploy sem abrir mão de nenhum requisito do projeto.
- **Chroma com persistência local**: dispensa infraestrutura de banco de dados adicional, adequado ao escopo de demonstração do projeto.

## Estrutura do repositório

```
Mega-brain/
├── data/
│   └── raw/                     # PDFs da base de conhecimento
├── src/
│   ├── ingestion/
│   │   ├── loader.py            # extração de texto e tabelas dos PDFs
│   │   └── chunker.py           # divisão em chunks por seção
│   └── rag/
│       ├── embeddings.py        # geração de embeddings via Gemini
│       ├── vectorstore.py       # persistência e busca no Chroma
│       └── pipeline.py          # busca + prompt + geração de resposta
├── scripts/
│   └── ingest.py                # roda a ingestão completa da base
├── streamlit_app.py             # interface de chat
├── requirements.txt
├── .env.example
└── .gitignore
```

## Como executar

### 1. Pré-requisitos

- Python 3.10+
- Uma chave de API do Gemini ([Google AI Studio](https://aistudio.google.com/apikey))

### 2. Instalação

```bash
git clone https://github.com/marqley/Mega-brain.git
cd Mega-brain
pip install -r requirements.txt
```

### 3. Configuração

Copie o arquivo de exemplo e adicione sua chave:

```bash
cp .env.example .env
```

Edite o `.env` e insira sua `GEMINI_API_KEY`.

### 4. Ingestão da base de conhecimento

Roda uma vez para processar os PDFs e indexá-los no Chroma:

```bash
python scripts/ingest.py
```

### 5. Executando o agente

```bash
streamlit run streamlit_app.py
```

A interface abre automaticamente no navegador.

## Evidências de funcionamento

**Pergunta que cruza múltiplos documentos:**

> **Pergunta:** Quais métodos de identificação existem e em qual plano cada um está disponível?
>
> **Resposta do agente:**
> - Cartão RFID: Disponível em Todos os planos (Básico, Profissional e Enterprise).
> - QR Code (app ou impresso): Disponível em Todos os planos (Básico, Profissional e Enterprise).
> - Biometria digital: Disponível nos planos Profissional e Enterprise.
> - Reconhecimento facial: Disponível apenas no plano Enterprise.
>
> Fontes citadas: `base-conhecimento-produto.pdf` (seção 3) e `planos-precos.pdf` (seções 2 e 5).

Essa resposta demonstra que o agente combina corretamente informações vindas de **duas tabelas em dois documentos diferentes**, com citação precisa da fonte.

**Pergunta sobre dados tabulares:**

> **Pergunta:** Quanto custa o plano Enterprise?
>
> **Resposta do agente:** O plano Enterprise custa R$ 349 por catraca/mês.
> Fonte: `planos-precos.pdf` — 2. Tabela comparativa.

## Deploy

*Seção em construção — deploy na Oracle Cloud Infrastructure (OCI), nível Always Free.*

## Tecnologias utilizadas

- Python
- pdfplumber (extração de PDF)
- Google Gemini API (embeddings e geração de texto)
- ChromaDB (vector store)
- Streamlit (interface)

## Contexto do desafio

Este projeto simplifica deliberadamente algumas etapas de um pipeline de RAG corporativo (curadoria de múltiplas fontes, ownership por área de negócio, controle de acesso por permissão) por se tratar de um projeto individual com conteúdo fictício e escopo de demonstração. Em um cenário empresarial real, essas etapas seriam necessárias e caberiam a diferentes times (RH, Jurídico, TI) definir e manter.