import streamlit as st
import pandas as pd

from streamlit_tags import st_tags
from utils.estilizacao.dataframe import mostrar_tabela 
from sidebar.page_editar import mudar_pagina_editar_processo
from sidebar.page_cadastro import mudar_pagina_cadastrar_processo
from sidebar.sem_display import sem_display
from sidebar.page_resumos import mudar_pagina_resumos_processo
from sidebar.customizacao import customizar_sidebar
from sidebar.page_home import mudar_pagina_home
from sidebar.page_relatorio import mudar_pagina_relatorio
from utils.digitacao.digitacao import mes_por_extenso
from src.base import load_base_data

sem_display()
customizar_sidebar()
mudar_pagina_cadastrar_processo()
mudar_pagina_editar_processo()
mudar_pagina_resumos_processo()
st.sidebar.write('---')
mudar_pagina_home()
mudar_pagina_relatorio()

st.header("Visualização dos Processos Cadastrados 📁")

load_base_data(forcar_recarregar=True)  # Carrega a base de dados
df_original = st.session_state.base.copy()

def filtro_ano_mes(df: pd.DataFrame):
    from datetime import datetime
    hoje = datetime.today()
    mes_padrao = hoje.month if hoje.month > 1 else 12
    ano_padrao = hoje.year if hoje.month > 1 else hoje.year - 1
    mes_atual_e_passado = [mes_padrao, mes_padrao - 1] if mes_padrao > 1 else [12, 11]

    df['Data de Recebimento'] = pd.to_datetime(df['Data de Recebimento'], format='%d/%m/%Y')
    df['Ano'] = df['Data de Recebimento'].dt.year
    df['Mês'] = df['Data de Recebimento'].dt.month

    anos_disponiveis = sorted(df['Ano'].unique())
    meses_disponiveis = sorted(df['Mês'].unique())

    col1, col2 = st.columns(2)
    ano = col1.selectbox(
        "Selecione o Ano",
        anos_disponiveis,
        index=anos_disponiveis.index(ano_padrao)
    )
    meses_selecionados = col2.multiselect(
        "Selecione os Meses",
        meses_disponiveis,
        default=[mes_atual_e_passado[0], mes_atual_e_passado[1]],
        format_func=mes_por_extenso
    )

    if meses_selecionados:
        df_filtrado = df[(df['Ano'] == ano) & (df['Mês'].isin(meses_selecionados))].copy()
    else:
        df_filtrado = df[df['Ano'] == ano].copy()

    return df_filtrado

df_filtrado = filtro_ano_mes(df_original)

col1, col2 = st.columns(2)

with col1:
    opcoes_situacao = ["TODOS"] + sorted(list(df_filtrado["Situação"].unique()))
    escolha_situacoes = st.multiselect(
        "",
        opcoes_situacao,
        default=None,
        key="Situação",
        placeholder="Filtre por Situação",
    )

if not escolha_situacoes:
    escolha_situacoes = ["TODOS"]

with col2:
    st.write("<style>div[data-baseweb='select'] { margin-top: 11px; }</style>", unsafe_allow_html=True)
    palavras_chave = st_tags(
        label="",
        text='Filtre por palavra-chave',
        value=[],
        maxtags=10,
        key='tags_busca',
    )

if "TODOS" not in escolha_situacoes:
    df_filtrado = df_filtrado[df_filtrado["Situação"].isin(escolha_situacoes)]

if palavras_chave:
    palavras_chave_lower = [p.lower() for p in palavras_chave]

    def contem_palavras(row):
        return all(
            any(p in str(cell).lower() for cell in row)
            for p in palavras_chave_lower
        )

    df_filtrado = df_filtrado[df_filtrado.apply(contem_palavras, axis=1)]

mostrar_tabela(df_filtrado, mostrar_na_tela=True)
st.write('---')
