import streamlit as st
from sidebar.sem_display import sem_display
from sidebar.customizacao import customizar_sidebar

st.set_page_config(page_title="Sistema de Login", page_icon="🔐", layout="wide")


sem_display()
customizar_sidebar()

def controle_sessao():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "page_access" not in st.session_state:
        st.session_state.page_access = []
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "🏠 Home"


def login(username, password):
    users = st.secrets["users"]
    page_access = st.secrets["page_access"]


    if username in users and users[username] == password:
        return page_access.get(username, [])
    return None

st.title("🔐 Sistema de Login")

username = st.text_input("Usuário")
password = st.text_input("Senha", type="password")

if st.button("Entrar", help="Clique para fazer login", icon="🚪", use_container_width=True, type='primary'):
    page_access = login(username, password)

    if page_access:
        # Armazena permissões na sessão do usuário
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.page_access = page_access

        st.switch_page("Home.py") # Direciona para Home.py

    else:
        st.error("Usuário ou senha incorretos.")
