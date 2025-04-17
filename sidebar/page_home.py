import streamlit as st

def mudar_pagina_home():
    if st.sidebar.button("Página Inicial :house:", use_container_width=True, type="primary"):
        st.switch_page("Home.py")