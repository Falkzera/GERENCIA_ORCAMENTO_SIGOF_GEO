import streamlit as st

def desenvolvido():
    st.sidebar.write("---")
    st.sidebar.write("##")
    st.sidebar.markdown("""
    <style>
    .creditos-dev {
        background: #EAEDF1;
        color: #3064AD;
        border-radius: 10px;
        padding: 18px 12px 14px 12px;
        margin-bottom: 10px;
        font-size: 1.05em;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(48,100,173,0.08);
    }
    .creditos-dev a {
        color: #3064AD;
        text-decoration: underline;
        font-weight: bold;
    }
    .creditos-dev a:hover {
        color: #18325e;
        text-decoration: underline;
    }
    </style>
    <div class="creditos-dev">
        Desenvolvido por: <a href="https://www.linkedin.com/in/falkzera/" target="_blank">Lucas Falcão</a>
    </div>
    """, unsafe_allow_html=True)