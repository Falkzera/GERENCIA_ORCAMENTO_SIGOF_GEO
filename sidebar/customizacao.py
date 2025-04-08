import streamlit as st

def customizar_sidebar():

    st.sidebar.image("image/SEPLAG.png")
    st.sidebar.caption('---')
    st.sidebar.markdown("<div style='text-align: center;'>Informações:</div>", unsafe_allow_html=True)
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([2,1.2])
    col1.title("Sistema de Gestão Orçamentária")
    col2.image("image/SEPLAG.png")
    st.write('---')


        
