import streamlit as st
import time
import struct

st.set_page_config(
    page_title="Monitoramento das Usinas TECSCI",
    page_icon="assets/icon.ico",
    layout="wide"
)

with st.sidebar:
    st.image("assets/logo-dark.png")
st.title("TUTORIAL DE USO DO CHIRPSTACK")

st.header("1️⃣ Acessando o Chirpstack")
st.write("Para acessar o Chirpstack, acesse o IP da Usina na porta 8080. Em seguida, faça o login com as credenciais admin e admin.")
