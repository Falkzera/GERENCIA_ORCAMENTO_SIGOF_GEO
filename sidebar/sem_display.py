import streamlit as st

def sem_display():
    """
    Função para ocultar a barra lateral do Streamlit.
    """
    # CSS para ocultar a barra lateral
    st.markdown("""
        <style>
        [data-testid="stSidebarNav"] {display: none;}
        </style>
    """, unsafe_allow_html=True)
