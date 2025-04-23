
import io
import pandas as pd
import streamlit as st

from datetime import datetime
from streamlit_tags import st_tags
from utils.formatar.formatar_valor import formatar_valor
from utils.digitacao.digitacao import mes_por_extenso, por_extenso_reais, por_extenso


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
        if "processo_edit" in st.session_state:
            del st.session_state["processo_edit"]
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
        # load_base_data(forcar_recarregar=True)  # Recarrega a base de dados
        
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

        if "processo_edit" in st.session_state:
            del st.session_state["processo_edit"]
            
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

    st.write('---')

    return df_filtrado

def resumo_processo_orcamentario(df_filtrado):
    st.subheader("Gerarador de Resumos 📄")

    def formatar_linha(numero):
        linha = df_filtrado[df_filtrado["Nº do Processo"] == numero].iloc[0]
        return f"{linha['Situação']} | {linha['Nº do Processo']} | {linha['Órgão (UO)']} | {linha['Valor']} | {linha['Origem de Recursos']}"
    

    opcoes_processo = ["TODOS"] + df_filtrado["Nº do Processo"].tolist()
    numero_processo = st.multiselect(
        "Selecione a linha do dataframe",
        options=opcoes_processo,
        format_func=lambda x: "TODOS" if x == "TODOS" else formatar_linha(x)
    )
    if "TODOS" in numero_processo:
        numero_processo = df_filtrado["Nº do Processo"].tolist()
    
    if numero_processo:
        processo_selecionado = df_filtrado[df_filtrado["Nº do Processo"].isin(numero_processo)]

        colunas_desejadas = ["Nº do Processo", "Órgão (UO)", "Objetivo", "Fonte de Recursos", "Valor"]
        cada_tipo_origem = processo_selecionado['Origem de Recursos'].unique()  

        processo_selecionado = processo_selecionado.copy()
        processo_selecionado['Valor_sem_formatacao'] = (
            processo_selecionado['Valor']
            .fillna('0')
            .replace({r'R\$ ': '', r'\.': '', ',': '.'}, regex=True)
            .astype(float, errors='ignore')
        )
    
        descricao_texto = f"*Resumo das solicitações de créditos orçamentários - SOP*\n"
        descricao_texto += f"_Atualizado em_: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        descricao_texto += f"*Quantidade de solicitações*: _{len(processo_selecionado)} ({por_extenso(len(processo_selecionado)).title()}) Processo{'s' if len(processo_selecionado) > 1 else ''}_\n"
        descricao_texto += f"*Valor total das solicitações*: {formatar_valor(processo_selecionado['Valor_sem_formatacao'].sum())}\n"

        for tipo_origem in cada_tipo_origem:
            processos_por_origem = processo_selecionado[processo_selecionado['Origem de Recursos'] == tipo_origem]
            descricao_texto += f"\n"
            descricao_texto += f"*{tipo_origem.title()}*: _{len(processos_por_origem)} ({por_extenso(len(processos_por_origem)).title()}) Processo{'s' if len(processos_por_origem) > 1 else ''}_\n"
            
            processos_por_origem.loc[:, 'Valor_sem_formatacao'] = (
                processos_por_origem['Valor']
                .fillna('0')
                .replace({'R\$ ': '', '\.': '', ',': '.'}, regex=True)
                .astype(float, errors='ignore')
                )
            
            descricao_texto += f"*Valor total das solicitações {tipo_origem.lower()}*: {formatar_valor(processos_por_origem['Valor_sem_formatacao'].sum())}\n"

            for _, row in processos_por_origem.iterrows():
                descricao = f"\n"
                for coluna in colunas_desejadas:
                    if coluna in row:
                        descricao += f"*{coluna}*: {row[coluna]}\n"
                descricao_texto += descricao

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