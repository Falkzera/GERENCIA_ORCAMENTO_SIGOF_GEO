import io
import streamlit as st
from sidebar.page_editar import mudar_pagina_editar_processo
from sidebar.page_cadastro import mudar_pagina_cadastrar_processo
from sidebar.page_visualizar import mudar_pagina_visualizar_processo
from sidebar.sem_display import sem_display
from sidebar.customizacao import customizar_sidebar
from sidebar.page_home import mudar_pagina_home
from utils.formatar.formatar_valor import formatar_valor
from sidebar.page_relatorio import mudar_pagina_relatorio
from src.base import load_base_data
from utils.sessao.login import verificar_permissao

customizar_sidebar()
verificar_permissao()
sem_display()
mudar_pagina_cadastrar_processo()
mudar_pagina_editar_processo()
mudar_pagina_visualizar_processo()
st.sidebar.write('---')
mudar_pagina_home()
mudar_pagina_relatorio()

load_base_data(forcar_recarregar=True)  # Carrega a base de dados

def resumo_geo():
    with st.container():  # TÍTULOS

        st.header("Resumos dos Processos 📁")

    # Verificando se o DataFrame está presente no session_state
    if "base" not in st.session_state:
        st.error("O DataFrame base não foi encontrado no session_state.")
        return

    df = st.session_state.base

    if "Nº do Processo" not in df.columns:
        st.error("A coluna 'Nº do Processo' não foi encontrada no DataFrame.")
        return

    # Selecionar o número do processo no selectbox
    numero_processo = st.multiselect("Selecione o número do processo:", df["Nº do Processo"].unique())

    if numero_processo:
        # Filtrando o DataFrame para o número do processo selecionado
        processo_selecionado = df[df["Nº do Processo"].isin(numero_processo)]

        # Exibir um resumo apenas das colunas especificadas
        colunas_desejadas = ["Nº do Processo", "Órgão (UO)", "Objetivo", "Fonte de Recursos", "Origem de Recursos", "Valor"]
        descricao_texto = ""
        
        # Inicializando um contador para as posições
        contador = 1
        
        for index, row in processo_selecionado.iterrows():
            descricao = f" *{contador}* \n"  # Usar o contador em vez de index + 1
            for coluna in colunas_desejadas:
                if coluna in row:  # Verifica se a coluna existe no DataFrame
                    if coluna == "Valor":
                        descricao += f"{coluna}: {formatar_valor(row[coluna])}\n"
                    else:
                        descricao += f"{coluna}: {row[coluna]}\n"
            descricao += "-----------------------------\n"
            descricao_texto += descricao + "\n"
            contador += 1  # Incrementa o contador para a próxima posição

        # Exibir o resumo gerado
        st.text_area("📝 Resultados:", descricao_texto, height=400)

        # Adicionando a funcionalidade de download do relatório
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

resumo_geo()
