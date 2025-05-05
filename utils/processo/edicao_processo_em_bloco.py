import streamlit as st
import pandas as pd
from datetime import datetime
from utils.buscadores.situacao import opcoes_situacao
from src.base import load_base_data

def formulario_edicao_processo_em_bloco():
    processos = st.session_state.get("processos_edicao_massa", [])
    base = st.session_state.base

    if not processos:
        st.warning("⚠️ Nenhum processo selecionado para edição em massa.")
        return

    situacao_atual = base[base["Nº do Processo"].isin(processos)]["Situação"].unique()

    st.info(f"📌 Situação atual dos {len(processos)} processo(s): **{situacao_atual[0]}**")

    with st.form("form_edicao_massa"):
        nova_situacao = st.selectbox("Nova Situação", opcoes_situacao)
        salvar = st.form_submit_button("Salvar Edição em Bloco", use_container_width=True, type="primary")

    if salvar:
        st.success("✅ Edição em massa concluída com sucesso!")
        agora = datetime.now()
        usuario = st.session_state.username.title()
        modificados = 0

        for proc in processos:
            indices = base[base["Nº do Processo"] == proc].index
            if not indices.empty:
                base.loc[indices, "Situação"] = nova_situacao
                base.loc[indices, "Última Edição"] = f"{usuario} - {agora.strftime('%d/%m/%Y %H:%M:%S')}"
                modificados += 1

        try:
            from streamlit_gsheets import GSheetsConnection
            conn = st.connection("gsheets", type=GSheetsConnection)
            conn.update(worksheet="Processos Base", data=base)
            st.success(f"✅ Situação atualizada com sucesso em {modificados} processo(s)!")
        except Exception as e:
            st.error(f"❌ Erro ao atualizar a planilha: {e}")
            st.stop()

        # Limpa o estado
        del st.session_state["processos_edicao_massa"]
        
        st.rerun()
