import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)

base = conn.read(worksheet="Processos Base", header=4)
st.dataframe(base)

manter_apenas_essas_colunas=[
    "Situação", "Origem de Recursos", "Órgão (UO)", "Nº do Processo", "Tipo de Crédito", "Fonte de Recursos", "Grupo de Despesas",
    "Valor", "Objetivo", "Observação", "Data de Recebimento", "Data de Publicação", "Nº do decreto"]

def load_base_data():
    if "base" not in st.session_state:
        st.session_state.base = base  # <-- Aqui você define

        st.session_state.base = st.session_state.base.iloc[:, 1:]
        st.session_state.base = st.session_state.base[manter_apenas_essas_colunas]
        st.session_state.base["Fonte de Recursos"] = st.session_state.base["Fonte de Recursos"].astype(str)
        st.session_state.base["Grupo de Despesas"] = st.session_state.base["Grupo de Despesas"].astype(str)

        st.session_state.base['Data de Recebimento'] = pd.to_datetime(
            st.session_state.base['Data de Recebimento'] - 2, origin='1900-01-01', unit='D')
        st.session_state.base['Data de Recebimento'] = st.session_state.base['Data de Recebimento'].dt.strftime('%d/%m/%Y')

        st.session_state.base['Data de Publicação'] = pd.to_datetime(
            st.session_state.base['Data de Publicação'] - 2, origin='1900-01-01', unit='D')
        st.session_state.base['Data de Publicação'] = st.session_state.base['Data de Publicação'].dt.strftime('%d/%m/%Y')

