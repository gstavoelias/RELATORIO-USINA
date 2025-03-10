
import streamlit as st
from lora_communication import LoRaCommunication
import pandas as pd
import plotly.graph_objects as go
import json


lora = st.session_state["lora"] if "lora" in st.session_state else None
tcus = st.session_state["tcus"] if "tcus" in st.session_state else []
usinas = {
    "Bebedouro": "http://10.8.0.9:8087/api/v1.0/",
    "Tangará da Serra":  "http://10.8.0.13:8087/api/v1.0/",
    "Loanda": "http://10.8.0.26:8087/api/v1.0/"
}

st.set_page_config(
    page_title="Monitoramento das Usinas TECSCI",
    page_icon="assets/icon.ico",
    layout="wide"
)
with st.sidebar:
    st.image("assets/logo-dark.png")

st.title("Monitoramento das Usinas TECSCI")


with st.container(border=True):
    st.header("SELECIONE A USINA")
    usina_selecionada = st.selectbox(label="Usinas TECSCI:", options=[usina for usina in usinas.keys()])
    if st.button("Confirmar"):
        lora = LoRaCommunication(usinas[usina_selecionada])
        st.session_state["tcus"] = [tcu["id"] for tcu in lora.get_tcus()]
        st.session_state["lora"] = lora

# with st.expander("VER DADOS DE UMA TCU"):
#     dev_eui = st.selectbox("ID da TCU:", options=tcus)
#     sample_size = int(st.text_input("Número de amostras:", value=5))
#     if st.button("Buscar", disabled= "lora" not in st.session_state):
#         response = lora.create_tcu_dataframe(dev_eui.upper())
#         if type(response) == str:
#             st.error(response)
#         else:
#             df = pd.json_normalize(response).head(sample_size)
#             st.dataframe(df, use_container_width=True)
#             fig = go.Figure()
#             fig.add_trace(go.Scatter(x=df["datetime"], y=df["posicao_angular"], mode="lines+markers", name="Posição"))
#             fig.add_trace(go.Scatter(x=df["datetime"], y=df["angulo_calculado"], mode="lines+markers", name="Target"))
#             st.plotly_chart(fig)

# with st.expander("MOSTRAR POSICIONAMENTO DAS TCUS"):
#     if st.button("Ir", disabled="lora" not in st.session_state):
#         data = [lora.get_last_angle(tcu) for tcu in tcus]
#         st.write(data)

                

