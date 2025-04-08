import streamlit as st
import pandas as pd
from utils.buscadores.situacao import mapa_cores_situacao
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

def mostrar_tabela(df, altura_max_linhas=10, nome_tabela="Tabela de Dados", mostrar_na_tela=False):
    if not mostrar_na_tela:
        return  # Silencia a exibição no app

    from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

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

    largura_minima = {
        "Órgão (UO)": 150,
        "Nº do Processo": 220,
        "Valor": 130,
        "Situação": 180,
        "Tipo de Crédito": 160,
        "Fonte de Recursos": 150,
        "Objeto": 300
    }

    for coluna, largura in largura_minima.items():
        if coluna in df.columns:
            gb.configure_column(coluna, minWidth=largura)

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
    AgGrid(
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
        height=altura_final if not muitas_colunas else None
    )
