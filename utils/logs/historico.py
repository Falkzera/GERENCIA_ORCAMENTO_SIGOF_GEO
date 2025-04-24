import json
import os
import streamlit as st
from datetime import datetime

# Função para carregar o histórico de modificações
def carregar_historico():
    if os.path.exists('historico_modificacoes.json'):
        with open('historico_modificacoes.json', 'r') as f:
            return json.load(f)
    else:
        return {}

# Função para salvar a modificação no histórico
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

def salvar_modificacao(processo_id, modificacao, usuario):
    # Conexão com o Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Data e hora da modificação
    agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Preparar dados para salvar no Google Sheets
    nova_modificacao = [processo_id, agora, modificacao, usuario]
    
    try:
        # Conectar ao Google Sheets e obter o worksheet da aba "Histórico de Modificações"
        worksheet = conn.read(worksheet="Histórico de Modificações", ttl=0)
        
        # Utiliza append_row para adicionar a nova modificação na planilha
        # worksheet.append_row adiciona a nova linha ao final da planilha
        conn.append_row(worksheet="Histórico de Modificações", row=nova_modificacao)
        
        st.success("✅ ✔️ Modificação salva com sucesso no Google Sheets.")
    except Exception as e:
        st.error(f"Erro ao salvar a modificação: {e}")
        st.stop()



def exibir_historico(processo_id):
    # Conectar ao Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Carregar a aba de Histórico de Modificações
    worksheet = conn.read(worksheet="Histórico de Modificações", ttl=0)
    
    # Filtrar modificações por processo_id
    modificacoes = worksheet.get_all_values()
    modificacoes_filtradas = [mod for mod in modificacoes if mod[0] == processo_id]

    # Exibir o histórico filtrado
    if modificacoes_filtradas:
        st.write(f"### Histórico de Modificações para o Processo {processo_id}")
        for mod in modificacoes_filtradas:
            st.write(f"- **Data**: {mod[1]}")
            st.write(f"- **Modificação**: {mod[2]}")
            st.write(f"- **Usuário**: {mod[3]}")
            st.write("---")
    else:
        st.write("Nenhuma modificação registrada para este processo.")
