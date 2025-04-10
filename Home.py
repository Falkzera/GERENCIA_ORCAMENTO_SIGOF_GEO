import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.sessao.login import verificar_permissao

from src.base import load_base_data

st.set_page_config(page_title="Dashboard de Processos", page_icon="📊", layout="wide")
verificar_permissao()

load_base_data()

from sidebar.customizacao import customizar_sidebar
from sidebar.page_editar import mudar_pagina_editar_processo
from sidebar.page_visualizar import mudar_pagina_visualizar_processo
from sidebar.page_resumos import mudar_pagina_resumos_processo
from sidebar.sem_display import sem_display
from sidebar.page_cadastro import mudar_pagina_cadastrar_processo
from utils.formatar.formatar_valor import formatar_valor, formatar_valor2
from sidebar.page_relatorio import mudar_pagina_relatorio
from utils.calculo_limite.limite import calcular_limite_atual
from utils.relatorio.botao_cpof import botao_gerar_e_baixar_pdf_cpof
from utils.relatorio.relatorio_cpof import filtro_ano_mes



sem_display()
customizar_sidebar()
mudar_pagina_cadastrar_processo()
mudar_pagina_editar_processo()
mudar_pagina_visualizar_processo()
mudar_pagina_resumos_processo()
st.sidebar.write('---')
mudar_pagina_relatorio()


limite = calcular_limite_atual()

VALOR_UTILIZADO_LIMITE = limite["valor_utilizado"]
VALOR_DO_LIMITE = limite["valor_limite"]
ORÇAMENTO_APROVADO_2025 = limite["orcamento_aprovado"]



with st.container():

    with st.container(): # VALOR DO LIMITE (CÁLCULO)
            
        df = pd.DataFrame(st.session_state.base)

        df['Valor'] = df['Valor'].astype(float) # FILTRAR DE ACORDO COM O FILTRO DE QUEM ENTRA!

    with st.container():  # MÉTRICAS

        # ---------- Cabeçalho ----------
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            st.markdown("### 💰 Indicadores Orçamentários")
        with col2:
            mostrar_info = st.toggle("ℹ️", key="mostrar_tooltips")

        # ---------- Dados ----------
        indicadores = {
            "Orçamento Aprovado - 2025": ORÇAMENTO_APROVADO_2025,
            "Limite de Execução (10%)": VALOR_DO_LIMITE,
            "Limite Executado": VALOR_UTILIZADO_LIMITE
        }

        tooltips = [
            "O orçamento aprovado é a estimativa legalmente autorizada das receitas e despesas públicas para um determinado exercício financeiro, aprovada pelo Poder Legislativo com base na proposta enviada pelo Executivo. Ele serve como instrumento de planejamento e controle da administração pública, estabelecendo limites para os gastos governamentais em diversas áreas, como saúde, educação, infraestrutura, entre outras. Sua aprovação ocorre por meio da Lei Orçamentária Anual (LOA), em conformidade com as diretrizes da Lei de Diretrizes Orçamentárias (LDO) e do Plano Plurianual (PPA), compondo o ciclo orçamentário brasileiro (GIACOMONI, 2021).",
            "O valor do limite corresponde a um percentual máximo do orçamento aprovado que pode ser utilizado ou comprometido com despesas em determinada etapa da execução orçamentária, funcionando como um mecanismo de controle fiscal e responsabilidade na gestão dos recursos públicos. No estado de Alagoas, esse limite é tradicionalmente fixado em 10% do Orçamento Aprovado, conforme práticas adotadas para garantir o equilíbrio das contas públicas e prevenir a execução de gastos além da capacidade financeira do ente federativo. Esse valor serve como um parâmetro inicial para autorização de despesas, podendo ser revisto conforme a evolução da arrecadação e das prioridades governamentais (GIACOMONI, 2021).",
            "O valor do limite utilizado representa a parcela efetivamente executada ou comprometida dentro do limite previamente autorizado do orçamento — no caso de Alagoas, 10% do Orçamento Aprovado. Ele indica o quanto já foi consumido do total permitido, sendo um importante indicador de acompanhamento da execução orçamentária e da capacidade remanescente para novas despesas. Monitorar esse valor permite ao gestor público tomar decisões fundamentadas, evitando extrapolar os limites legais e promovendo uma gestão fiscal responsável e transparente (GIACOMONI, 2021)."
        ]

        cores_financas = ["#095AA2"] * len(indicadores)

        # ---------- Blocos ----------
        cols_kpi = st.columns(len(indicadores))
        for idx, (titulo, valor) in enumerate(indicadores.items()):
            with cols_kpi[idx]:
                st.markdown(f"""
                <div style='background-color:{cores_financas[idx]};
                            padding:25px;
                            border-radius:10px;
                            text-align:center;
                            color:white;
                            border:2px solid #b5cee3;
                            animation: fadeIn 0.5s ease-in-out;'>
                    <b style='font-size:18px;'>{titulo}</b><br>
                    <span style='font-size:26px;font-weight:bold;'>{formatar_valor(valor)}</span>
                </div>
                <style>
                @keyframes fadeIn {{
                    from {{ opacity: 0; }}
                    to {{ opacity: 1; }}
                }}
                </style>
                """, unsafe_allow_html=True)

                if mostrar_info:
                    st.markdown(f"""
                    <div style='background-color:#f0f0f0;
                                padding: 10px;
                                border-radius:10px;
                                text-align:;
                                color:black;
                                border:1px solid #ccc;
                                margin-top:10px;
                                max-height:100px;
                                overflow-y:auto;
                                animation: fadeIn 0.5s ease-in-out;'>
                        {tooltips[idx]}
                    </div>
                    <style>
                    @keyframes fadeIn {{
                        from {{ opacity: 0; }}
                        to {{ opacity: 1; }}
                    }}
                    </style>
                    """, unsafe_allow_html=True)



    # espaço
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # sessão em baixo coluna 1 e coluna 2
    with st.container():  # MÉTRICAS


        # Cálculos
        valor_orcamento_anual_e_executado = (VALOR_UTILIZADO_LIMITE / ORÇAMENTO_APROVADO_2025) * 100
        valor_limite_sobre_usado = (VALOR_UTILIZADO_LIMITE / VALOR_DO_LIMITE) * 100

        # Dados
        indicadores = {
            "Percentual Executado do Total": valor_orcamento_anual_e_executado,
            "Percentual Executado do Limite": valor_limite_sobre_usado,
            "Valor Disponível": VALOR_DO_LIMITE - VALOR_UTILIZADO_LIMITE
        }

        cores_financas = ["#095AA2", "#095AA2", "#095AA2"]

        # Layout mais equilibrado
        col1, col2 = st.columns([1, 2])  # aumenta o espaço para os cards

        with col1:
            st.markdown("<div style='display: flex; flex-wrap: wrap; gap: 20px;'>", unsafe_allow_html=True)

            for idx, (titulo, valor) in enumerate(indicadores.items()):
                if idx < 2:  # Os dois primeiros índices são em porcentagem
                    valor_formatado = f"{formatar_valor2(valor)}"
                else:  # O terceiro índice é um valor monetário
                    valor_formatado = formatar_valor(valor)

                st.markdown(f"""
                <div style='background-color:{cores_financas[idx]};
                    padding:15px;
                    border-radius:10px;
                    text-align:center;
                    color:white;
                    border:2px solid #b5cee3;
                    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
                    max-width:300px; margin:auto;
                    animation: fadeInSlow 1.5s ease-in-out;'>
                <b style='font-size:18px;'>{titulo}</b><br>
                <span style='font-size:26px;font-weight:bold;'>{valor_formatado}</span>
                </div>
                <style>
                @keyframes fadeInSlow {{
                    from {{ opacity: 0; }}
                    to {{ opacity: 1; }}
                }}
                </style>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            fig = go.Figure(
                data=[go.Pie(
                    labels=["Executado", "Disponível"],
                    values=[valor_limite_sobre_usado, 100 - valor_limite_sobre_usado],
                    hole=0.4,
                    marker=dict(colors=["#095AA2", "#E0E0E0"]),
                    textinfo="percent+label",
                    insidetextorientation="radial"
                )]
            )

            fig.update_layout(
                margin=dict(t=0, b=0),
                height=400,
                showlegend=False,
                legend=dict(
                    orientation="h",
                    y=-0.1,
                    x=0.5,
                    xanchor="center"
                ),
            )

            st.plotly_chart(fig, use_container_width=True)


with st.container():  # RELATÓRIO CPOF
    st.write('---')




    df = pd.DataFrame(st.session_state.base)
    ano, mes, df_filtrado, df_mes_anterior = filtro_ano_mes(df, exibir_na_tela=True, key_prefix="home")

    botao_gerar_e_baixar_pdf_cpof(ano, mes, df_filtrado, df_mes_anterior)

