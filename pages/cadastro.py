import streamlit as st
import pandas as pd
from utils.buscadores.tipo_credito import tipo_credito as opcoes_tipo_credito
from utils.buscadores.grupo_despesa import opcoes_grupo_despesa
from utils.buscadores.fonte_recurso import opcoes_fonte_recurso
from utils.buscadores.orgao_uo import opcoes_orgao_uo
from utils.buscadores.contabilizar_limite import opcoes_contabilizar_limite
from utils.buscadores.origem_recurso import opcoes_origem_recursos
from utils.buscadores.situacao import opcoes_situacao
from utils.validadores.processo import validar_processamento_campos
from utils.validadores.valor import formatar_valor_br
from sidebar.customizacao import customizar_sidebar
from sidebar.page_visualizar import mudar_pagina_visualizar_processo
from sidebar.sem_display import sem_display
from sidebar.page_home import mudar_pagina_home
from sidebar.page_editar import mudar_pagina_editar
from utils.estilizacao.dataframe import mostrar_tabela 
from src.base import load_base_data
from datetime import datetime
ano_corrente = datetime.now().year
from sidebar.page_relatorio import mudar_pagina_relatorio
from utils.sessao.login import verificar_permissao
from utils.marca.creditos import  desenvolvido
from sidebar.botao_logout import criar_botao_logout


st.set_page_config(
    page_title="Cadastro de Processos Orçamentários",
    page_icon="📁",
    layout="wide",
)
verificar_permissao()
sem_display()
customizar_sidebar()
mudar_pagina_visualizar_processo()
mudar_pagina_editar()
mudar_pagina_relatorio()
mudar_pagina_home()
criar_botao_logout()
desenvolvido()

from utils.estilizacao.background import wallpaper
wallpaper()

st.header("Cadastro de Processos de Execução Orçamentária 📁")
st.write("######")

col1, col2, col3 = st.columns(3)

numero_processo = col1.text_input("Nº do Processo (Obrigatório)",placeholder=f"E:00000.0000000000/{ano_corrente}",help=f"Digite o número do processo no formato: E:00000.0000000000/{ano_corrente}")
numero_processo = str(numero_processo).strip() 
situacao = col2.selectbox("Situação (Obrigatório)",opcoes_situacao,index=None,help="Selecione a situação do processo.", placeholder="Selecione a Situação")
origem_recursos = col3.selectbox("Origem de Recursos (Obrigatório)",opcoes_origem_recursos,index=None,help="Selecione a origem dos recursos.", placeholder="Selecione a Origem de Recursos")

col1, col2 = st.columns(2)
orgao_uo = col1.selectbox("Órgão/Unidade Orçamentária (Obrigatório)",opcoes_orgao_uo,index=None,help="Selecione a Unidade Orçamentária.", placeholder="Selecione a UO")
contabilizar_limite = col2.selectbox("Contabilizar no Limite? (Obrigatório)",opcoes_contabilizar_limite,index=None,help="Selecione se o processo deve ser contabilizado no limite.", placeholder="Selecione Sim ou Não")

col1, col2, col3 = st.columns(3)
tipo_credito = col1.selectbox("Tipo de Crédito (Obrigatório)",opcoes_tipo_credito,index=None,help="Selecione o tipo de crédito.", placeholder="Selecione o Tipo de Crédito")
fonte_recurso = col2.selectbox("Fonte de Recrusos (Obrigatório)",opcoes_fonte_recurso,index=None,help="Selecione a Unidade Orçamentária.", placeholder="Selecione a Fonte de Recursos")
grupo_despesa = col3.selectbox("Grupo de Despesas (Obrigatório)",opcoes_grupo_despesa,index=None,help="Selecione o grupo de despesa.", placeholder="Selecione um Grupo de Despesas")

col1, col2 = st.columns(2)
valor_input = col1.text_input("Valor (Obrigatório)", placeholder="Ex: 1.234,56", help="Digite o valor do processo no formato: 1.234,56")
data_recebimento = col2.text_input("Data de recebimento (Obrigatório)", placeholder="DD/MM/AAAA", help="Digite a data de recebimento do processo no formato: DD/MM/AAAA")

if valor_input and valor_input.isnumeric():
    valor_input = formatar_valor_br(valor_input)

col1, col2 = st.columns(2)
objetivo = col1.text_input("Objetivo (Obrigatório)", placeholder="Ex: Descrição do objetivo do processo.", help="Digite o objetivo do processo.")
observacao = col2.text_input("Observação", placeholder="Ex: Digite se houver alguma observação.", help="Digite uma observação ao processo, normalmente utilizado para descrever erros no processo.")

data_publicacao = ''
numero_decreto = ''

nao_podem_estar_vazios = [
    situacao,
    origem_recursos,
    orgao_uo,
    numero_processo,
    tipo_credito,
    fonte_recurso,
    grupo_despesa,
    valor_input,
    objetivo,
    data_recebimento, 
    contabilizar_limite   
]
if any(not campo for campo in nao_podem_estar_vazios):
    st.info("⚠️ Preencha todos os campos obrigatórios.")
    st.stop()

st.write('---')
if st.button("Cadastrar Processo 📁", use_container_width=True, type="primary", help='Clique para cadastrar o processo na base 📁'):

    # 🔄 Atualiza a base direto do Sheets
    load_base_data(forcar_recarregar=True)

     # ✅ Valida os campos
    erros = validar_processamento_campos(
        numero_processo,
        valor_input,
        objetivo,
        data_recebimento,
        data_publicacao,
        numero_decreto
    )
    if erros:
        for erro in erros:
            st.error(erro)
        st.stop()
    if numero_processo in st.session_state.base["Nº do Processo"].values:
        st.error("⚠️ Esse processo já foi cadastrado! Veja abaixo:")
        mostrar_tabela(st.session_state.base[st.session_state.base["Nº do Processo"] == numero_processo],altura_max_linhas=99, 
                       nome_tabela="Processo já cadastrado!", mostrar_na_tela=True)
        st.stop()
    else:
        agora = datetime.now()
        novo = pd.DataFrame([{
            "Situação": situacao,
            "Origem de Recursos": origem_recursos,
            "Órgão (UO)": orgao_uo,
            "Nº do Processo": numero_processo,
            "Tipo de Crédito": tipo_credito,
            "Fonte de Recursos": fonte_recurso,
            "Grupo de Despesas": grupo_despesa,
            "Valor": valor_input,
            "Objetivo": objetivo,
            "Observação": observacao,
            "Data de Recebimento": data_recebimento,
            "Data de Publicação": data_publicacao,
            "Nº do decreto": numero_decreto,
            "Contabilizar no Limite?": contabilizar_limite,
            "Cadastrado Por": st.session_state.username.title() + ' - ' + agora.strftime("%d/%m/%Y %H:%M:%S"),
        }])

        # TRATAR O VALOR (DE R$ 1.234,56 PARA 1234.56)
        novo["Valor"] = novo["Valor"].apply(
            lambda x: float(x.replace(".", "").replace(",", "."))
        )

        st.session_state.base = pd.concat([st.session_state.base, novo], ignore_index=True)
        try:
            from streamlit_gsheets import GSheetsConnection
            conn = st.connection("gsheets", type=GSheetsConnection)  # Reabre a conexão, se necessário
            conn.update(worksheet="Processos Base", data=st.session_state.base) # google sheets
            st.success("✅ Processo Cadastrado Com Sucesso!")
        except Exception as e:
            st.error(f"Erro ao atualizar a planilha: {e}")
            st.stop()

        mostrar_tabela(st.session_state.base[st.session_state.base["Nº do Processo"] == numero_processo],altura_max_linhas=99, 
                       nome_tabela="Processo Cadastrado!", mostrar_na_tela=True)
        


