import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Define as colunas que você quer manter da planilha
manter_apenas_essas_colunas = [
    "Situação", "Origem de Recursos", "Órgão (UO)", "Nº do Processo", "Tipo de Crédito", "Fonte de Recursos", "Grupo de Despesas",
    "Valor", "Objetivo", "Observação", "Data de Recebimento", "Data de Publicação", "Nº do decreto", "Contabilizar no Limite?"
]

# Função para tratar datas: tenta como Excel, senão tenta como string dd/mm/yyyy
def tratar_data(coluna):
    try:
        # Converte como número de dias desde 1900 (formato Excel)
        datas = pd.to_datetime(coluna.astype(float) - 2, origin='1900-01-01', unit='D')
    except Exception:
        # Se falhar, tenta como string no formato dd/mm/yyyy
        datas = pd.to_datetime(coluna, format='%d/%m/%Y', errors='coerce')
    return datas.dt.strftime('%d/%m/%Y')

# Função principal de carregamento da base
def load_base_data(forcar_recarregar=False):
    if "base" not in st.session_state or forcar_recarregar:
        with st.spinner("🔄 Carregando base de dados..."):
            conn = st.connection("gsheets", type=GSheetsConnection)
            base = conn.read(worksheet="Processos Base", ttl=0)

            # Filtra e trata os dados
            base = base[manter_apenas_essas_colunas]
            base["Fonte de Recursos"] = base["Fonte de Recursos"].astype(str)
            base["Grupo de Despesas"] = base["Grupo de Despesas"].astype(str)
            base["Nº do Processo"] = base["Nº do Processo"].astype(str).str.strip()

            base['Data de Recebimento'] = tratar_data(base['Data de Recebimento'])
            base['Data de Publicação'] = tratar_data(base['Data de Publicação'])

            st.session_state.base = base
