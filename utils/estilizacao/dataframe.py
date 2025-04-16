import streamlit as st
import pandas as pd
from utils.buscadores.situacao import mapa_cores_situacao
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

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
from utils.formatar.formatar_numero_decreto import formatar_numero_decreto
from sidebar.page_relatorio import mudar_pagina_relatorio
from src.base import load_base_data
from utils.sessao.login import verificar_permissao



def mostrar_tabela(df, altura_max_linhas=10, nome_tabela="Tabela de Dados", mostrar_na_tela=False, enable_click=False):

    # Inicializa o estado da sessão para esta tabela se não existir
    if f'grid_options_{nome_tabela}' not in st.session_state:
        st.session_state[f'grid_options_{nome_tabela}'] = None
    if f'filtros_{nome_tabela}' not in st.session_state:
        st.session_state[f'filtros_{nome_tabela}'] = None
    if f'ordenacao_{nome_tabela}' not in st.session_state:
        st.session_state[f'ordenacao_{nome_tabela}'] = None

    if not mostrar_na_tela:
        return  # Silencia a exibição no app
    
 # Inicializa o estado da sessão para esta tabela se não existir
    if f'grid_options_{nome_tabela}' not in st.session_state:
        st.session_state[f'grid_options_{nome_tabela}'] = None
        st.session_state[f'filtros_{nome_tabela}'] = None

    if "Valor" in df.columns:
        df["Valor"] = df["Valor"].apply(
            lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )

    gb = GridOptionsBuilder.from_dataframe(df)

    cell_style_padrao = JsCode("""
    function(params) {
        return {
            'textAlign': 'center',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center'
        };
    }
    """)

    gb.configure_default_column(
        resizable=True,
        autoHeight=True,
        wrapText=True,
        sortable=True,
        filter=True,
        cellStyle=cell_style_padrao,
    )

    if "Situação" in df.columns:
        from utils.buscadores.situacao import mapa_cores_situacao
        cell_style_situacao = JsCode(f"""
        function(params) {{
            let cor = {{
                {','.join([f'"{sit}": "{cor}"' for sit, cor in mapa_cores_situacao.items()])}
            }};
            return {{
                'backgroundColor': cor[params.value] || '#ffffff',
                'color': 'black',
                'fontWeight': '500',
                'textAlign': 'center',
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'center'
            }};
        }}
        """)
        gb.configure_column("Situação", cellStyle=cell_style_situacao)


    def on_grid_ready(params):
            st.session_state[f'filtros_{nome_tabela}'] = params.api.getFilterModel()
            st.session_state[f'ordenacao_{nome_tabela}'] = params.api.getSortModel()

    if st.session_state[f'filtros_{nome_tabela}']:
        grid_options['initialFilterModel'] = st.session_state[f'filtros_{nome_tabela}']
    if st.session_state[f'ordenacao_{nome_tabela}']:
        grid_options['initialSortModel'] = st.session_state[f'ordenacao_{nome_tabela}']

    if enable_click:
        gb.configure_grid_options(
            rowSelection="single",
            suppressRowClickSelection=False,
            onRowDoubleClicked=JsCode("""
            function(event) {
                const rowData = event.data;
                window.parent.postMessage({ type: "row_double_click", data: rowData }, "*");
            }
            """)
        )

    grid_options = gb.build()
    grid_options['headerHeight'] = 60
    grid_options['autoHeaderHeight'] = True

    ALTURA_LINHA_ESTIMADA = 65
    ALTURA_HEADER = 44
    ALTURA_PADDING = 10
    linhas_exibidas = len(df)
    altura_minima = linhas_exibidas * ALTURA_LINHA_ESTIMADA + ALTURA_HEADER + ALTURA_PADDING
    altura_maxima = altura_max_linhas * ALTURA_LINHA_ESTIMADA + ALTURA_HEADER + ALTURA_PADDING
    altura_final = min(altura_minima, altura_maxima)

    muitas_colunas = len(df.columns) > 6

    st.markdown(f"##### {nome_tabela}")
    response = AgGrid(
        df,
        gridOptions=grid_options,
        theme="alpine",
        allow_unsafe_jscode=True,
        custom_css={
            ".ag-header": {"background-color": "#3064ad !important"},
            ".ag-header-cell-label": {
                "color": "#ffffff !important",
                "font-weight": "650",
                "font-size": "16px",
                "justify-content": "center"
            },
            ".ag-cell": {
                "font-size": "14px",
                "line-height": "1.4",
                "border-color": "#e6e6e6"
            },
            ".ag-row-hover": {
                "background-color": "#e8f0fe !important"
            },
            ".ag-row-selected": {
                "background-color": "#d0e8ff !important"
            },
            ".ag-root-wrapper": {
                "border": "1px solid #e0e0e0",
                "border-radius": "8px"
            },
        },
        fit_columns_on_grid_load=not muitas_colunas,
        reload_data=True,
        update_mode='MODEL_CHANGED',
        domLayout='autoHeight' if muitas_colunas else 'normal',
        height=altura_final if not muitas_colunas else None,
        enable_enterprise_modules=True if enable_click else False,
        return_mode="AS_INPUT" if enable_click else "NONE",
    )

    if enable_click:
        selected_rows = response.get("selected_rows")
        if selected_rows is not None and len(selected_rows) > 0:
            # Se for um DataFrame
            if isinstance(selected_rows, pd.DataFrame):
                selected_row = selected_rows.iloc[0].to_dict()
                return selected_row
            # Se for uma lista de dicionários
            elif isinstance(selected_rows, list) and isinstance(selected_rows[0], dict):
                selected_row = selected_rows[0]
                return selected_row
            else:
                st.warning("Formato inesperado na linha selecionada. Verifique os dados.")
                return None
    
    return None
