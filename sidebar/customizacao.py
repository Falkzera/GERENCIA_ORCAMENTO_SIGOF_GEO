import streamlit as st

def customizar_sidebar():

    st.sidebar.image("image/ALAGOAS.png")
    # st.sidebar.image("image/ALAGOAS_BRANCO.png")
    st.sidebar.caption('---')
    col1, col2 = st.columns([2,1.2])
    col1.title("Sistema de Gestão Orçamentária")
    col2.image("image/SEPLAG.png")
    st.write('---') 

    if "username" in st.session_state:
        st.sidebar.markdown(f"""
        <style>
        .creditos-dev {{
            background: #EAEDF1;
            color: #3064AD;
            border-radius: 10px;
            padding: 18px 12px 14px 12px;
            margin-bottom: 10px;
            font-size: 1.05em;
            font-weight: 500;
            box-shadow: 0 2px 8px rgba(48,100,173,0.08);
            text-align: center;
        }}
        .creditos-dev a {{
            color: #3064AD;
            text-decoration: underline;
            font-weight: bold;
        }}
        .creditos-dev a:hover {{
            color: #18325e;
            text-decoration: underline;
        }}
        </style>
        <div class="creditos-dev">
            {st.session_state.username.upper()}
        </div>
        """, unsafe_allow_html=True)
        st.sidebar.markdown("<br>", unsafe_allow_html=True)
            
