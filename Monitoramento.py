import streamlit as st
from usina import Usina
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime 
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import struct
import time

usinas = {
    "Bebedouro": {"host": "10.8.0.9", "password": "Stemis%%2024"},
    "Tangará da Serra":  {"host": "10.8.0.13", "password": "1234"},
    "Loanda": {"host": "10.8.0.26", "password": "Stemis%%2022"},
    "Ilha das Palmas": {"host": "10.8.0.28", "password": "Stemis%%2022"},
    "Bálsamo": {"host": "10.8.0.36", "password": "Stemis%%2022"}
}

if "usina" not in st.session_state:
    st.session_state["usina"] = None
if "tcus" not in st.session_state:
    st.session_state["tcus"] = []
if "df_uplinks" not in st.session_state:
    st.session_state["df_uplinks"] = None
if "df_overview" not in st.session_state:
    st.session_state["df_overview"] = None

st.set_page_config(
    page_title="Monitoramento das Usinas TECSCI",
    page_icon="assets/icon.ico",
    layout="wide"
)

with st.sidebar:
    st.image("assets/logo-dark.png")
    with st.expander("Comandos LoRa"):
        if st.button("TIMESTAMP"):
            timestamp = float(int(time.time())) 
            hex_representation = struct.unpack(">I", struct.pack(">f", timestamp))[0] 
            st.write(f"e1{hex_representation:08x}")
        latitude = st.text_input("Latitude", "0")
        longitude = st.text_input("Longitude", "0")
        if st.button("POSIÇÃO"):
            latitude_res = struct.unpack(">I", struct.pack(">f", float(latitude)))[0] 
            longitude_res = struct.unpack(">I", struct.pack(">f", float(longitude)))[0]
            st.write("Latitude: ", f"01{latitude_res:08x}")
            st.write("Longitude: ", f"02{longitude_res:08x}")

st.title("MONITORAMENTO DE USINAS TECSCI")

with st.container(border=False):
    st.header("1️⃣ SELECIONE A USINA")
    usina_selecionada = st.selectbox(label="Opções", label_visibility="hidden",options=[usina for usina in usinas.keys()])
    if st.button("Confirmar"):
        DB_CONNECTION = URL.create(
        drivername="postgresql",
        username="postgres",
        password= usinas[usina_selecionada]["password"],
        host= usinas[usina_selecionada]["host"],
        port=5432,
        database="stemis"
        )
        engine = create_engine(DB_CONNECTION, echo=False)
        Base = declarative_base()
        Session = sessionmaker(bind=engine)
        st.session_state["usina"] = Usina(Session)
        st.session_state["tcus"] = st.session_state["usina"].get_tcus()



st.header("2️⃣ SELECIONE AS INFORMAÇÕES QUE DESEJA VISUALIZAR")
with st.expander("VER TCUs DA USINA"):
    if st.button("Buscar"):
        inicio = datetime.now()
        st.session_state["df_tcus"] = pd.DataFrame(st.session_state["tcus"])
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=st.session_state["df_tcus"]["longitude"],
            y=st.session_state["df_tcus"]["latitude"], 
            text=st.session_state["df_tcus"]["name"],
            textposition="top center",
            mode="markers", 
            name="TCUs"))
        st.session_state["fig_tcus"] = fig
        st.write(f"Tempo de execução: {datetime.now() - inicio}")

    # Exibe o DataFrame somente se já tiver sido carregado
    if "df_tcus" in st.session_state:
        st.plotly_chart(st.session_state["fig_tcus"])
        st.dataframe(st.session_state["df_tcus"], use_container_width=True)

with st.expander("Ver Histórico de uma TCU"):
    dev_eui = st.selectbox("ID da TCU:", options=[f"{tcu["name"]} - {tcu["id"]}" for tcu in st.session_state["tcus"]])
    n = st.number_input("Número de registros:", min_value=1, max_value=500)
    if st.button("Buscar 2"):
        inicio = datetime.now()
        st.session_state["df_uplinks"] = pd.DataFrame(st.session_state["usina"].get_tcu_uplinks(dev_eui.split(" - ")[-1], n))
        st.write(f"Tempo de execução: {datetime.now() - inicio}")

    # Exibe apenas se já houver dados
    if st.session_state["df_uplinks"] is not None:
        st.dataframe(st.session_state["df_uplinks"], use_container_width=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=st.session_state["df_uplinks"]["datetime"], 
                                y=st.session_state["df_uplinks"]["angular_position"], 
                                mode="lines", name="Posição Angular"))
        fig.add_trace(go.Scatter(x=st.session_state["df_uplinks"]["datetime"], 
                                y=st.session_state["df_uplinks"]["target_angle"], 
                                mode="lines", name="Ângulo Alvo"))
        st.plotly_chart(fig)

with st.expander("Visão Geral da Usina"):
    if st.button("Buscar 3"):
        inicio = datetime.now()
        st.session_state["df_overview"] = pd.DataFrame(st.session_state["usina"].get_plant_summary())
        st.write(f"Tempo de execução: {datetime.now() - inicio}")

    if st.session_state["df_overview"] is not None:
        st.dataframe(st.session_state["df_overview"], use_container_width=True)
