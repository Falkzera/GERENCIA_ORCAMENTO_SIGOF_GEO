import streamlit as st

def mudar_pagina_home():
    if st.sidebar.button("Página Inicial", use_container_width=True, type="primary"):
        st.switch_page("Home.py")