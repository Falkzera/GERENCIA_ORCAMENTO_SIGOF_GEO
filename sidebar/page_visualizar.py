import streamlit as st

def mudar_pagina_visualizar_processo():
    if st.sidebar.button("Visualizar Processos 🔍", use_container_width=True, type="primary"):
        st.switch_page("pages/visualizar.py")