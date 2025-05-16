import streamlit as st

def criar_botao_logout():
    if st.sidebar.button("Sair 🚪", use_container_width=True, type="primary"):
        for chave in ["logged_in", "username", "page_access", "selected_page"]:
            st.session_state.pop(chave, None)
        st.switch_page("pages/login.py")
