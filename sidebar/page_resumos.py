import streamlit as st

def mudar_pagina_resumos_processo():
    if st.sidebar.button("Gerar Resumos ⌨️", use_container_width=True, type="primary"):
        st.switch_page("pages/resumos.py")