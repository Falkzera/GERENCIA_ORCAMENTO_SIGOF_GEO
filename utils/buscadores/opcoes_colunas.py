import streamlit as st

def obter_opcoes_coluna(nome_coluna):
    base = st.session_state.base  
    opcoes = sorted(set(base[nome_coluna]))
    return opcoes

# EXCELENTE RESUMO, MAS INEFICAZ POIS SÓ GUARDA OS QUE JÁ TEM CADASTRADO, INEFICIENTE PARA O INICIO DO ANO

# opcoes_orgao_uo = obter_opcoes_coluna("Órgão (UO)")
# opcoes_fonte_recurso = obter_opcoes_coluna("Fonte de Recursos")
# opcoes_tipo_credito = obter_opcoes_coluna("Tipo de Crédito")
# opcoes_situacao = obter_opcoes_coluna("Situação")
# opcoes_grupo_despesa = obter_opcoes_coluna("Grupo de Despesas")
# opcoes_origem_recursos = obter_opcoes_coluna("Origem de Recursos")