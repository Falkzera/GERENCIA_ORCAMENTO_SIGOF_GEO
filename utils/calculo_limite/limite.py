import pandas as pd
import streamlit as st

ORÇAMENTO_APROVADO_2025 = 18544820466.00
VALOR_DO_LIMITE = ORÇAMENTO_APROVADO_2025 * 0.1

def calcular_limite_atual():

    df = pd.DataFrame(st.session_state.base)
    df['Valor'] = df['Valor'].astype(float)
  
    df = df[df['Contabilizar no Limite?'] == 'SIM']
    df = df[df['Situação'] == 'Publicado']



    valor_utilizado = df['Valor'].sum()
    return {
        "valor_utilizado": valor_utilizado,
        "valor_limite": VALOR_DO_LIMITE,
        "valor_disponivel": VALOR_DO_LIMITE - valor_utilizado,
        "orcamento_aprovado": ORÇAMENTO_APROVADO_2025
    }