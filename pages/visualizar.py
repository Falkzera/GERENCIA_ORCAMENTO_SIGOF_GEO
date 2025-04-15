import io
import streamlit as st
import pandas as pd
from datetime import datetime

from streamlit_tags import st_tags

# from src.base import load_base_ted
from sidebar.customizacao import customizar_sidebar
from utils.estilizacao.dataframe import mostrar_tabela 
from sidebar.page_editar import mudar_pagina_editar_processo
from sidebar.page_cadastro import mudar_pagina_cadastrar_processo
from sidebar.sem_display import sem_display
from sidebar.page_home import mudar_pagina_home
from sidebar.page_relatorio import mudar_pagina_relatorio
from utils.digitacao.digitacao import mes_por_extenso
from utils.sessao.login import verificar_permissao


verificar_permissao()
sem_display()
customizar_sidebar()
mudar_pagina_cadastrar_processo()
mudar_pagina_editar_processo()
st.sidebar.write('---')
mudar_pagina_home()
mudar_pagina_relatorio()

st.header("Visualização dos Processos Cadastrados 📁")


def configurar_estado_ano_mes(df: pd.DataFrame):
    hoje = datetime.today()
    mes_padrao = hoje.month if hoje.month > 1 else 12
    ano_padrao = hoje.year if hoje.month > 1 else hoje.year - 1
    mes_atual_e_passado = [mes_padrao, mes_padrao - 1] if mes_padrao > 1 else [12, 11]

    df['Data de Recebimento'] = pd.to_datetime(df['Data de Recebimento'], format='%d/%m/%Y')
    df['Ano'] = df['Data de Recebimento'].dt.year
    df['Mês'] = df['Data de Recebimento'].dt.month

    anos_disponiveis = sorted(df['Ano'].unique())
    meses_disponiveis = sorted(df['Mês'].unique())

    if 'ano' not in st.session_state:
        st.session_state.ano = ano_padrao
    if 'meses_selecionados' not in st.session_state:
        st.session_state.meses_selecionados = [mes_atual_e_passado[0], mes_atual_e_passado[1]]

    col1, col2 = st.columns(2)
    
    novo_ano = col1.selectbox(
        "Selecione o Ano",
        anos_disponiveis,
        index=anos_disponiveis.index(st.session_state.ano)
    )
    
    novos_meses = col2.multiselect(
        "Selecione os Meses",
        meses_disponiveis,
        default=st.session_state.meses_selecionados,
        format_func=mes_por_extenso
    )

    # Atualizar o estado apenas se houver mudanças
    if novo_ano != st.session_state.ano or novos_meses != st.session_state.meses_selecionados:
        st.session_state.ano = novo_ano
        st.session_state.meses_selecionados = novos_meses
        st.rerun()  # Forçar a atualização da interface


def aplicar_filtro_ano_mes(df: pd.DataFrame):
    if st.session_state.meses_selecionados:
        df_filtrado = df[(df['Ano'] == st.session_state.ano) & (df['Mês'].isin(st.session_state.meses_selecionados))].copy()
    else:
        df_filtrado = df[df['Ano'] == st.session_state.ano].copy()

    return df_filtrado


def filtros_de_busca(df_filtrado):

    if 'palavras_chave' not in st.session_state:
        st.session_state.palavras_chave = [] 

    if 'situacao_selecionados' not in st.session_state:
        st.session_state.situacao_selecionados = ["TODOS"]

    col1, col2 = st.columns(2)

    with col1:
        opcoes_situacao = ["TODOS"] + sorted(list(df_filtrado["Situação"].unique()))
        novas_situacoes = st.multiselect(
            "Filtre por Situação", 
            opcoes_situacao,
            default=st.session_state.situacao_selecionados,
            key="Situação",
            placeholder="Selecione a Situação",
        )
        
        if not novas_situacoes:
            novas_situacoes = ["TODOS"]

    with col2:
        st.write("<style>div[data-baseweb='select'] { margin-top: 11px; }</style>", unsafe_allow_html=True)
        
        novas_palavras_chave = st_tags(
            label="",
            text='Filtre por palavra-chave',
            value=st.session_state.palavras_chave,  
            maxtags=10,
            key='tags_busca',
        )

    # Atualizar o estado apenas se houver mudanças
    if novas_situacoes != st.session_state.situacao_selecionados or novas_palavras_chave != st.session_state.palavras_chave:
        st.session_state.situacao_selecionados = novas_situacoes
        st.session_state.palavras_chave = novas_palavras_chave
        st.rerun()  # Forçar a atualização da interface

    if "TODOS" not in st.session_state.situacao_selecionados:
        df_filtrado = df_filtrado[df_filtrado["Situação"].isin(st.session_state.situacao_selecionados)]

    if st.session_state.palavras_chave:
        palavras_chave_lower = [p.lower() for p in st.session_state.palavras_chave]

        def contem_palavras(row):
            return all(
                any(p in str(cell).lower() for cell in row)
                for p in palavras_chave_lower
            )

        df_filtrado = df_filtrado[df_filtrado.apply(contem_palavras, axis=1)]

    mostrar_tabela(df_filtrado, mostrar_na_tela=True)
    st.write('---')

    return df_filtrado

def resumo_processo_orcamentario(df_filtrado):
    st.subheader("Gerarador de Resumos 📄")

    def formatar_linha(numero):
        linha = df_filtrado[df_filtrado["Nº do Processo"] == numero].iloc[0]
        return f"{linha['Situação']} | {linha['Nº do Processo']} | {linha['Órgão (UO)']} | {linha['Valor']}"

    numero_processo = st.multiselect(
    "Selecione a linha do dataframe",
    options=df_filtrado["Nº do Processo"].tolist(), 
    format_func=formatar_linha
)

    if numero_processo:
        processo_selecionado = df_filtrado[df_filtrado["Nº do Processo"].isin(numero_processo)]

        colunas_desejadas = ["Nº do Processo", "Órgão (UO)", "Objetivo", "Fonte de Recursos", "Origem de Recursos", "Valor"]
        descricao_texto = ""

        contador = 1
    
        for index, row in processo_selecionado.iterrows():
            descricao = f" *{contador}* \n"  # Usar o contador em vez de index + 1
            for coluna in colunas_desejadas:
                if coluna in row:  # Verifica se a coluna existe no DataFrame
                    if coluna == "Valor":
                        descricao += f"{coluna}: {(row[coluna])}\n"
                    else:
                        descricao += f"{coluna}: {row[coluna]}\n"
            descricao += "-----------------------------\n"
            descricao_texto += descricao + "\n"
            contador += 1  # Incrementa o contador para a próxima posição

        st.text_area("📝 Resultados:", descricao_texto, height=400)
        output = io.BytesIO()
        output.write(descricao_texto.encode("utf-8"))
        output.seek(0)

        st.download_button(
        label="📥 Baixar Relatório 📥", 
        data=output, 
        file_name=f"relatorio_processo_{numero_processo}.txt", 
        mime="text/plain", 
        use_container_width=True, 
        type='primary'
    )
    else:
        st.warning("Selecione um número de processo para visualizar o resumo.")

opcoes = ["Processos de Execução Orçamentária", "Processos  de TED"]
escolha = st.selectbox("Selecione uma opção", opcoes)

if escolha == "Processos de Execução Orçamentária":

    df_filtrado = st.session_state.base.copy()
    configurar_estado_ano_mes(df_filtrado)
    df_filtrado = aplicar_filtro_ano_mes(df_filtrado)
    try:
        df_filtrado = filtros_de_busca(df_filtrado)
    except Exception as e:
        situacoes_selecionadas = ", ".join(st.session_state.situacao_selecionados)
        meses_escolhidos = ", ".join([mes_por_extenso(m) for m in st.session_state.meses_selecionados])
        st.error(f"Não há dados disponíveis para a combinação dos meses e situações selecionados.")
        st.warning(f"Mês escolhido: {meses_escolhidos}" if len(st.session_state.meses_selecionados) == 1 else f"Meses escolhidos: {meses_escolhidos}.")
        st.warning(f"Situação escolhida: {situacoes_selecionadas}" if len(st.session_state.situacao_selecionados) == 1 else f"Situações escolhidas: {situacoes_selecionadas}")
        st.stop()

    resumo_processo_orcamentario(df_filtrado)

elif escolha == "Processos  de TED":
    # df_ted = st.session_state.base_ted.copy()
    # configurar_estado_ano_mes(df_ted)
    # df_ted = aplicar_filtro_ano_mes(df_ted)
    # df_ted = filtros_de_busca(df_ted)

    st.subheader('Em breve...')

else:
    st.error("Opção inválida. Selecione 'Processos de Execução Orçamentária' ou 'Processos de TED'.")