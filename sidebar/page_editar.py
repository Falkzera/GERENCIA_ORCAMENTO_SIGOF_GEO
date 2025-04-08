import streamlit as st

def mudar_pagina_editar_processo():
    if st.sidebar.button("Editar Processo 🔄", use_container_width=True, type="primary"):
        st.switch_page("pages/editar.py")