import streamlit as st
import pandas as pd
from utils.validadores.data import validar_data_recebimento, validar_data_publicacao
from utils.buscadores.tipo_credito import tipo_credito as opcoes_tipo_credito
from utils.validadores.valor import validar_valor
from utils.buscadores.grupo_despesa import opcoes_grupo_despesa
from utils.buscadores.fonte_recurso import opcoes_fonte_recurso
from utils.validadores.numero_processo import validar_numero_processo
from utils.buscadores.orgao_uo import opcoes_orgao_uo
from utils.buscadores.origem_recurso import opcoes_origem_recursos
from utils.buscadores.contabilizar_limite import opcoes_contabilizar_limite
from utils.buscadores.situacao import opcoes_situacao
from utils.validadores.numero_decreto import validar_numero_decreto
from sidebar.page_cadastro import mudar_pagina_cadastrar_processo
from sidebar.sem_display import sem_display
from sidebar.page_visualizar import mudar_pagina_visualizar_processo
from sidebar.customizacao import customizar_sidebar
from sidebar.page_home import mudar_pagina_home
from utils.formatar.formatar_valor import formatar_valor_sem_cifrao
from utils.estilizacao.dataframe import mostrar_tabela 
from utils.formatar.formatar_numero_decreto import formatar_numero_decreto
from sidebar.page_relatorio import mudar_pagina_relatorio
from src.base import load_base_data
from utils.sessao.login import verificar_permissao

st.set_page_config(
    page_title="Editar Processo Orçamentário",
    page_icon="✏️",
    layout="wide",
)

with st.container(): # SIDEBAR
    verificar_permissao()
    sem_display()
    customizar_sidebar()
    mudar_pagina_cadastrar_processo()
    mudar_pagina_visualizar_processo()
    st.sidebar.write('---')
    mudar_pagina_relatorio()
    mudar_pagina_home()

with st.container(): # Recarregamento da BASE

    load_base_data(forcar_recarregar=True)

with st.container(): # TÍTULO
    st.header("Editar Processo Orçamentário 📁")

with st.container(): # MAIN

    salvar = []

    # Verificar se há processos filtrados na sessão
    if "processos_filtrados" in st.session_state and not st.session_state.processos_filtrados.empty:
        processos_disponiveis = st.session_state.processos_filtrados["Nº do Processo"].tolist()
    else:
        processos_disponiveis = st.session_state.base["Nº do Processo"].tolist()

    processo_edit = st.selectbox(
        "Selecione um processo para editar", 
        [""] + processos_disponiveis
    )

    if processo_edit:
        row_index = st.session_state.base[st.session_state.base["Nº do Processo"] == processo_edit].index[0]
        processo = st.session_state.base.loc[row_index]        

        if pd.notna(processo["Nº do decreto"]): # BLOCO DE VERIFICAÇÕES!
            if isinstance(processo["Nº do decreto"], (int, float)): # Verifica se o valor é numérico
                numero_decreto = str(int(processo["Nº do decreto"]))   # Converte para inteiro e depois para string
            else:
                numero_decreto = processo["Nº do decreto"]  
            if len(numero_decreto) == 6: # VERIFICAÇÃO DECRETO: Se o número do decreto tiver 6 dígitos.
                numero_decreto_formatado = f"{numero_decreto[:3]}.{numero_decreto[3:]}" # Formato: 000.000
            else:
                numero_decreto_formatado = numero_decreto  # Se já estiver no padrão, só mantém
            processo["Nº do decreto"] = numero_decreto_formatado # O mesmo vale aqui
        else:
            processo["Nº do decreto"] = "" # Também é aceito número de decreto vazio

        with st.form("form_edicao"): # CONSTRUÇÃO DO FORMS PARA EDIÇÃO

            def editar_select(label, opcoes, coluna): # Função para Construção dos Campos de selectbox.
                valor_atual = processo[coluna]
                return st.selectbox(f"{label} (Editar)", opcoes, index=opcoes.index(valor_atual))

            def editar_texto(label, coluna, tipo="input"): # Função para Construção dos Campos de texto.
                if tipo == "area":
                    return st.text_area(f"{label} (Editar)", value=processo[coluna])
                return st.text_input(f"{label} (Editar)", value=processo[coluna])
            
            # TODOS OS CAMPOS E OPÇÕES POSSÍVEIS!
            nova_situacao = editar_select("Situação", opcoes_situacao, "Situação")
            nova_origem = editar_select("Origem de Recursos", opcoes_origem_recursos, "Origem de Recursos")
            novo_orgao = editar_select("Órgão (UO)", opcoes_orgao_uo, "Órgão (UO)")
            novo_contabilizar_limite = editar_select("Contabilizar no Limite?", opcoes_contabilizar_limite, "Contabilizar no Limite?")
            novo_processo = editar_texto("Nº do Processo", "Nº do Processo")
            novo_tipo_credito = editar_select("Tipo de Crédito", opcoes_tipo_credito, "Tipo de Crédito")
            nova_fonte = editar_select("Fonte de Recursos", opcoes_fonte_recurso, "Fonte de Recursos")
            novo_grupo = editar_select("Grupo de Despesas", opcoes_grupo_despesa, "Grupo de Despesas")
            valor_edit = st.text_input("Valor (Editar)", value=str(formatar_valor_sem_cifrao(processo["Valor"])))
            objetivo_edit = editar_texto("Objetivo", "Objetivo", tipo="area")
            observacao_edit = st.text_input("Observação (Editar)", value="" if pd.isna(processo["Observação"]) else processo["Observação"])
            data_recebimento_edit = st.text_input("Data de Recebimento (Editar)", value=processo["Data de Recebimento"])
            data_publicacao_edit = st.text_input("Data de Publicação (Editar)", value="" if pd.isna(processo["Data de Publicação"]) else processo["Data de Publicação"])

            if pd.notna(processo["Nº do decreto"]): # Verifica se o número do decreto não é vazio
                numero_decreto_edit = st.text_input(
                    "Nº do Decreto (Editar)", 
                    value=str(formatar_numero_decreto(str(processo["Nº do decreto"])))) # Garante que o número do decreto seja exibido no formato correto com a função "formatar_numero_decreto"
            else:
                numero_decreto_edit = st.text_input("Nº do Decreto (Editar)", value="") # Aceitando também preenchimento vazio!

            st.write('---')

            salvar = st.form_submit_button("Salvar Edição", use_container_width=True, type="primary", help='Clique para salvar a edição do processo na base 📁') # Salvando o forms

    if salvar: # Lógicas de verificações após clicar em SALVAR! Só será salvo caso passe por todoas as verificações!!!
        
        erros = [] # Validações 

        # Validação
        validacoes = [
            (validar_numero_processo(novo_processo), "Número do processo inválido."),
            (validar_valor(valor_edit), "Valor inválido."),
            (validar_data_recebimento(data_recebimento_edit), "Data de recebimento inválida."),
            (validar_data_publicacao(data_publicacao_edit), "Data de publicação inválida."),
            (validar_numero_decreto(numero_decreto_edit), "Número do decreto inválido, Utilize o formato: 000.000")
        ]

        for valido, mensagem in validacoes:
            if not valido:
                erros.append(mensagem)

        if erros:
            for erro in erros:
                st.error(f"❌ {erro}")

        if not erros: # Caso não tenha erros, busca mapear o que foi que o usuário modificou, comparando o antigo com o novo.
            
            if (
                nova_situacao == processo["Situação"] and
                nova_origem == processo["Origem de Recursos"] and
                novo_orgao == processo["Órgão (UO)"] and
                novo_contabilizar_limite == processo["Contabilizar no Limite?"] and
                novo_processo == processo["Nº do Processo"] and
                novo_tipo_credito == processo["Tipo de Crédito"] and
                nova_fonte == processo["Fonte de Recursos"] and
                novo_grupo == processo["Grupo de Despesas"] and
                float(valor_edit.replace(".", "").replace(",", ".")) == processo["Valor"] and
                objetivo_edit == processo["Objetivo"] and
                observacao_edit == processo["Observação"] and
                data_recebimento_edit == processo["Data de Recebimento"] and
                data_publicacao_edit == processo["Data de Publicação"] and
                numero_decreto_edit == processo["Nº do decreto"]
            ):
                st.info("ℹ️ Nenhuma modificação foi realizada no processo, o processo permanece inalterado.")

            else: # Realiza a edição do processo

                base = st.session_state.base
                base.loc[row_index, "Situação"] = nova_situacao
                base.loc[row_index, "Origem de Recursos"] = nova_origem
                base.loc[row_index, "Órgão (UO)"] = novo_orgao
                base.loc[row_index, "Contabilizar no Limite?"] = novo_contabilizar_limite
                base.loc[row_index, "Nº do Processo"] = novo_processo
                base.loc[row_index, "Tipo de Crédito"] = novo_tipo_credito
                base.loc[row_index, "Fonte de Recursos"] = nova_fonte
                base.loc[row_index, "Grupo de Despesas"] = novo_grupo
                base.loc[row_index, "Valor"] = float(valor_edit.replace(".", "").replace(",", "."))
                base.loc[row_index, "Objetivo"] = objetivo_edit
                base.loc[row_index, "Observação"] = observacao_edit
                base.loc[row_index, "Data de Recebimento"] = data_recebimento_edit
                base.loc[row_index, "Data de Publicação"] = data_publicacao_edit
                base.loc[row_index, "Nº do decreto"] = numero_decreto_edit

                try: # Atualiza a planilha do Google Sheets
                    from streamlit_gsheets import GSheetsConnection
                    conn = st.connection("gsheets", type=GSheetsConnection)  # Reabre a conexão, se necessário
                    conn.update(worksheet="Processos Base", data=st.session_state.base) # google sheets
                    st.success("✅ ✔️ Edição salva com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao atualizar a planilha: {e}")
                    st.stop()

                modificacoes = [] # Uma lista para destrinchar o que foi modificado!

                def is_not_nan(value):
                    return not pd.isna(value)

                if nova_situacao != processo["Situação"] and is_not_nan(nova_situacao) and is_not_nan(processo["Situação"]):
                    modificacoes.append(f"Situação: {processo['Situação']} -> {nova_situacao}")
                if nova_origem != processo["Origem de Recursos"] and is_not_nan(nova_origem) and is_not_nan(processo["Origem de Recursos"]):
                    modificacoes.append(f"Origem de Recursos: {processo['Origem de Recursos']} -> {nova_origem}")
                if novo_orgao != processo["Órgão (UO)"] and is_not_nan(novo_orgao) and is_not_nan(processo["Órgão (UO)"]):
                    modificacoes.append(f"Órgão (UO): {processo['Órgão (UO)']} -> {novo_orgao}")
                if novo_contabilizar_limite != processo["Contabilizar no Limite?"] and is_not_nan(novo_contabilizar_limite) and is_not_nan(processo["Contabilizar no Limite?"]):
                    modificacoes.append(f"Contabilizar no Limite?: {processo['Contabilizar no Limite?']} -> {novo_contabilizar_limite}")
                if novo_processo != processo["Nº do Processo"] and is_not_nan(novo_processo) and is_not_nan(processo["Nº do Processo"]):
                    modificacoes.append(f"Nº do Processo: {processo['Nº do Processo']} -> {novo_processo}")
                if novo_tipo_credito != processo["Tipo de Crédito"] and is_not_nan(novo_tipo_credito) and is_not_nan(processo["Tipo de Crédito"]):
                    modificacoes.append(f"Tipo de Crédito: {processo['Tipo de Crédito']} -> {novo_tipo_credito}")
                if nova_fonte != processo["Fonte de Recursos"] and is_not_nan(nova_fonte) and is_not_nan(processo["Fonte de Recursos"]):
                    modificacoes.append(f"Fonte de Recursos: {processo['Fonte de Recursos']} -> {nova_fonte}")
                if novo_grupo != processo["Grupo de Despesas"] and is_not_nan(novo_grupo) and is_not_nan(processo["Grupo de Despesas"]):
                    modificacoes.append(f"Grupo de Despesas: {processo['Grupo de Despesas']} -> {novo_grupo}")
                if float(valor_edit.replace(".", "").replace(",", ".")) != processo["Valor"] and is_not_nan(valor_edit) and is_not_nan(processo["Valor"]):
                    modificacoes.append(f"Valor: {processo['Valor']} -> {valor_edit}")
                if objetivo_edit != processo["Objetivo"] and is_not_nan(objetivo_edit) and is_not_nan(processo["Objetivo"]):
                    modificacoes.append(f"Objetivo: {processo['Objetivo']} -> {objetivo_edit}")
                if observacao_edit != processo["Observação"] and is_not_nan(observacao_edit) and is_not_nan(processo["Observação"]):
                    modificacoes.append(f"Observação: {processo['Observação']} -> {observacao_edit}")
                if data_recebimento_edit != processo["Data de Recebimento"] and is_not_nan(data_recebimento_edit) and is_not_nan(processo["Data de Recebimento"]):
                    modificacoes.append(f"Data de Recebimento: {processo['Data de Recebimento']} -> {data_recebimento_edit}")
                if data_publicacao_edit != processo["Data de Publicação"] and is_not_nan(data_publicacao_edit) and is_not_nan(processo["Data de Publicação"]):
                    modificacoes.append(f"Data de Publicação: {processo['Data de Publicação']} -> {data_publicacao_edit}")
                if numero_decreto_edit != processo["Nº do decreto"] and is_not_nan(numero_decreto_edit) and is_not_nan(processo["Nº do decreto"]):
                    modificacoes.append(f"Nº do Decreto: {processo['Nº do decreto']} -> {numero_decreto_edit}")

                if modificacoes: # Mostrar a destrinchação do que foi modificado
                    st.write("### Modificações realizadas:")
                    for mod in modificacoes:
                        st.write(f"- {mod}")

                mostrar_tabela(base[base["Nº do Processo"] == novo_processo], altura_max_linhas=99, nome_tabela="Processo Editado!", mostrar_na_tela=True) # Visualização do processo editado

    st.write('---')