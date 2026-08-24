import streamlit as st

from src.rag.pipeline import responder

st.set_page_config(page_title="CatraCloud - Assistente", page_icon="🎫")
st.title("Assistente CatraCloud")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

pergunta = st.chat_input("Faça uma pergunta sobre a CatraCloud")

if pergunta:
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            resposta = responder(pergunta)
            st.markdown(resposta)

    st.session_state.mensagens.append({"role": "assistant", "content": resposta})