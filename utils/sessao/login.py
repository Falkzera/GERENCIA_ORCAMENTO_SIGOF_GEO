import streamlit as st

def verificar_permissao():

    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.switch_page("pages/login.py")

    if "page_access" not in st.session_state not in st.session_state.page_access:
        st.error("🚫 Você não tem permissão para acessar esta página.")
        st.stop()

    if "usuario_logado" in st.session_state:
        st.subheader(f"Você está logado como: {st.session_state.usuario_logado}")

