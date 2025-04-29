import streamlit as st
import pandas as pd

from utils.relatorio.relatorio_cpof import filtro_ano_mes
from sidebar.customizacao import customizar_sidebar
from sidebar.page_visualizar import mudar_pagina_visualizar_processo
from sidebar.sem_display import sem_display
from sidebar.page_home import mudar_pagina_home
from sidebar.page_cadastro import mudar_pagina_cadastrar_processo
from sidebar.page_editar import mudar_pagina_editar
from src.base import load_base_data
from utils.sessao.login import verificar_permissao
from utils.marca.creditos import desenvolvido
from utils.digitacao.digitacao import mes_por_extenso  # Só se precisar

# st.set_page_config(page_title="Relatórios", page_icon='', layout="wide")

with st.container():  # PÁGINAS E CONFIGURAÇÃO SIDEBAR
    verificar_permissao()
    sem_display()
    customizar_sidebar()
    mudar_pagina_cadastrar_processo()
    mudar_pagina_visualizar_processo()
    mudar_pagina_editar()
    mudar_pagina_home()
    desenvolvido()
    

st.subheader("Relatório CPOF 📊")

load_base_data(forcar_recarregar=True)  
df = pd.DataFrame(st.session_state.base)
ano, mes, df_filtrado, df_filtrado_mes_anterior = filtro_ano_mes(df, exibir_na_tela=True, key_prefix="home")

from utils.relatorio.montar_relatorio import botao_gerar_e_baixar_arquivo
from utils.relatorio.relatorio_cpof import montar_relatorio_cpof

botao_gerar_e_baixar_arquivo(
    nome_botao="Gerar Relatório CPOF (Docx)",
    montar_conteudo_funcao=montar_relatorio_cpof,
    parametros_funcao={
        "ano": ano,
        "mes": mes,
        "df_filtrado": df_filtrado,
        "df_filtrado_mes_anterior": df_filtrado_mes_anterior
    },
    nome_arquivo=f"Relatorio_CPOF_{mes_por_extenso(mes)}_{ano}.docx",
    tipo_arquivo="docx"
)


from utils.estilizacao.background import wallpaper
wallpaper()

