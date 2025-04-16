import streamlit as st

from sidebar.customizacao import customizar_sidebar
from utils.estilizacao.dataframe import mostrar_tabela 
from sidebar.page_cadastro import mudar_pagina_cadastrar_processo
from sidebar.sem_display import sem_display
from sidebar.page_home import mudar_pagina_home
from sidebar.page_relatorio import mudar_pagina_relatorio
from utils.digitacao.digitacao import mes_por_extenso
from utils.sessao.login import verificar_permissao
from utils.processo.edicao_processo import formulario_edicao_processo
from utils.processo.filtros_visualizar import aplicar_filtro_ano_mes, configurar_estado_ano_mes, filtros_de_busca, resumo_processo_orcamentario


verificar_permissao()
sem_display()
customizar_sidebar()
mudar_pagina_cadastrar_processo()
st.sidebar.write('---')
mudar_pagina_home()
mudar_pagina_relatorio()

st.header("Visualização dos Processos Cadastrados 📁")

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

    selected_row = mostrar_tabela(df_filtrado, mostrar_na_tela=True, enable_click=True)

    if selected_row:
        st.write(f"🔍 Você selecionou o processo: **{selected_row['Nº do Processo']}**")

        if "processo_edit" in st.session_state:
            if st.session_state["processo_edit"] != selected_row["Nº do Processo"]:
                del st.session_state["processo_edit"]
                st.rerun()

        if st.button("Editar", use_container_width=True, type="primary"):
            st.session_state["processo_edit"] = selected_row["Nº do Processo"]
            st.rerun()  # 🔁 Força recarregamento para mostrar o formulário

    if "processo_edit" in st.session_state:
        
        formulario_edicao_processo()
        if st.button("❌ Cancelar Edição", use_container_width=True):
            del st.session_state["processo_edit"]
            st.rerun()

    st.write('---')
    resumo_processo_orcamentario(df_filtrado)

elif escolha == "Processos  de TED":
    # df_ted = st.session_state.base_ted.copy()
    # configurar_estado_ano_mes(df_ted)
    # df_ted = aplicar_filtro_ano_mes(df_ted)
    # df_ted = filtros_de_busca(df_ted)

    st.subheader('Em breve...')

else:
    st.error("Opção inválida. Selecione 'Processos de Execução Orçamentária' ou 'Processos de TED'.")