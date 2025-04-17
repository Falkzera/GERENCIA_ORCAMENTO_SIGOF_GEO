import streamlit as st
import base64


def wallpaper(image_file="image/default.jpg"):
    try:
        with open(image_file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()

        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}

        [data-testid="stSidebar"] > div:first-child {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
        }}

        header {{
            background: transparent !important;
        }}

        [data-testid="stHeader"] {{
            background: transparent !important;
        }}

        .css-18ni7ap.e8zbici2 {{
            background-color: rgba(0,0,0,0) !important;
        }}

        .block-container {{
            background-color: rgba(255,255,255,0);
        }}
        </style>
        """
        
        st.markdown(css, unsafe_allow_html=True)
    except FileNotFoundError:
        pass
