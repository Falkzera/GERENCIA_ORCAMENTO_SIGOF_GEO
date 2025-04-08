import streamlit as st

def mudar_pagina_relatorio():
    if st.sidebar.button("Relatórios", use_container_width=True, type="primary"):
        st.switch_page("pages/relatorio.py")