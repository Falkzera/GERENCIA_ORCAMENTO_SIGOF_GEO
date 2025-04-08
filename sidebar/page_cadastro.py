import streamlit as st

def mudar_pagina_cadastrar_processo():
    if st.sidebar.button("Cadastrar Processo 📂", use_container_width=True, type="primary"):
        st.switch_page("pages/cadastro.py")