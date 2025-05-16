import streamlit as st

from sidebar.customizacao import customizar_sidebar
from utils.estilizacao.dataframe import mostrar_tabela 
from sidebar.page_cadastro import mudar_pagina_cadastrar_processo
from sidebar.sem_display import sem_display
from sidebar.page_home import mudar_pagina_home
from sidebar.page_relatorio import mudar_pagina_relatorio
from sidebar.page_editar import mudar_pagina_editar
from utils.sessao.login import verificar_permissao
from utils.processo.edicao_processo import formulario_edicao_processo
from utils.processo.filtros_visualizar import filtros_de_busca, resumo_processo_orcamentario, resumo_processo_publicado
from utils.formatar.formatar_valor import formatar_valor
from utils.processo.edicao_processo_em_bloco import formulario_edicao_processo_em_bloco
from sidebar.botao_logout import criar_botao_logout

from utils.marca.creditos import desenvolvido

verificar_permissao()
sem_display()
customizar_sidebar()
mudar_pagina_cadastrar_processo()
mudar_pagina_editar()
mudar_pagina_relatorio()
mudar_pagina_home()
criar_botao_logout()
desenvolvido()

st.header("Visualização dos Processos Cadastrados 📁")

opcoes = ["Processos de Execução Orçamentária", "Processos  de TED"]
escolha = st.selectbox("Selecione uma opção", opcoes)

if escolha == "Processos de Execução Orçamentária":

    df_filtrado = st.session_state.base.copy()

    try:
        df_filtrado = filtros_de_busca(df_filtrado)
    except Exception as e: # Tratando erro, caso por algum motivo, as opções antes selecionadas, não estejam mais disponíveis.
        st.session_state.situacao_selecionados = ["TODOS"]
        st.rerun()

    df_filtrado, selected_row = mostrar_tabela(df_filtrado, mostrar_na_tela=True, enable_click=True)
    valor_total = df_filtrado["Valor"].sum()
    st.write(f"**Valor Total dos Processos:** {formatar_valor(valor_total)}")

    editar_em_bloco = st.checkbox("Editar processos em bloco?", value=False)

    with st.container():
        if editar_em_bloco:

            situacoes = st.session_state.get("situacao_selecionados", [])

            processos_disponiveis = df_filtrado["Nº do Processo"].dropna().unique().tolist()

            with st.expander("🔍 - Processos disponíveis para edição em bloco", expanded=True):
                processos_selecionados = st.multiselect(
                    "Selecione os processos para edição em bloco:",
                    options=sorted(processos_disponiveis),
                    help="Você só pode editar a Situação de processos que estejam com o mesmo filtro de situação aplicado."
                )

            if processos_selecionados:
                situacao_selecionada = df_filtrado[df_filtrado["Nº do Processo"].isin(processos_selecionados)]["Situação"].unique()

                if len(situacao_selecionada) > 1:
                    st.warning("⚠️ Para edição em bloco, selecione processos com a mesma situação.")
                    processos_selecionados = []
            
                if processos_selecionados:
                    st.session_state["processos_edicao_massa"] = processos_selecionados
                    if "processos_edicao_massa" in st.session_state:
                        formulario_edicao_processo_em_bloco()

        else:
            # ✅ Modo tradicional (edição individual)
            try: 
                if selected_row:
                    numero_proc = selected_row["Nº do Processo"]
                    st.write(f"🔍 Você selecionou o processo: **{numero_proc}**")

                    if "processo_edit" in st.session_state:
                        if st.session_state["processo_edit"] != numero_proc:
                            del st.session_state["processo_edit"]
                            st.rerun()

                    if st.button("Editar", use_container_width=True, type="primary"):
                        st.session_state["processo_edit"] = numero_proc
                        st.rerun()

                if "processo_edit" in st.session_state:
                    formulario_edicao_processo()

                    if st.button("❌ Cancelar Edição", use_container_width=True):
                        del st.session_state["processo_edit"]
                        st.rerun()

            except KeyError:
                st.info("⚠️ Para editar um processo, saia do modo Pivot.")

    st.write('---')
    st.subheader("Outras funcionalidades")
    st.caption("Clique para expandir as opções.")
    
    df_filtrado['Valor'] = df_filtrado['Valor'].apply(formatar_valor)

    with st.expander("📑 **Gerador Automatico de Resumos** 📑", expanded=False):
        resumo_processo_orcamentario(df_filtrado)

    with st.expander("📑 **Gerador Automatico de Resumos para Processos Publicados** 📑", expanded=False):
        resumo_processo_publicado()

elif escolha == "Processos  de TED":
    # df_ted = st.session_state.base_ted.copy()
    # configurar_estado_ano_mes(df_ted)
    # df_ted = aplicar_filtro_ano_mes(df_ted)
    # df_ted = filtros_de_busca(df_ted)

    st.subheader('Em breve...')

else: # Nunca deve chegar aqui
    st.error("Opção inválida. Selecione 'Processos de Execução Orçamentária' ou 'Processos de TED'.")



