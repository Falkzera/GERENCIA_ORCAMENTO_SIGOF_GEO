import streamlit as st
import pandas as pd
from utils.relatorio.botao_cpof import botao_gerar_e_baixar_pdf_cpof
from utils.relatorio.relatorio_cpof import filtro_ano_mes
from sidebar.customizacao import customizar_sidebar
from sidebar.page_editar import mudar_pagina_editar_processo
from sidebar.page_visualizar import mudar_pagina_visualizar_processo
from sidebar.page_resumos import mudar_pagina_resumos_processo
from sidebar.sem_display import sem_display
from sidebar.page_home import mudar_pagina_home
from sidebar.page_cadastro import mudar_pagina_cadastrar_processo
from src.base import load_base_data

# st.set_page_config(page_title="Relatórios", page_icon='', layout="wide")

with st.container():  # PÁGINAS E CONFIGURAÇÃO SIDEBAR
    sem_display()
    customizar_sidebar()
    mudar_pagina_cadastrar_processo()
    mudar_pagina_visualizar_processo()
    mudar_pagina_editar_processo()
    mudar_pagina_resumos_processo()
    st.sidebar.write('---')
    mudar_pagina_home()
    

st.subheader("Relatório CPOF 📊")

load_base_data(forcar_recarregar=True)  
df = pd.DataFrame(st.session_state.base)
ano, mes, df_filtrado, df_mes_anterior = filtro_ano_mes(df, exibir_na_tela=True, key_prefix="home")
botao_gerar_e_baixar_pdf_cpof(ano, mes, df_filtrado, df_mes_anterior)

