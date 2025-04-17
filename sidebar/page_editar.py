import streamlit as st

def mudar_pagina_editar():
    if st.sidebar.button("Consulta Única 🎯", use_container_width=True, type="primary"):
        st.switch_page("pages/editar.py")