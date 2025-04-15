import streamlit as st
import pandas as pd
from utils.buscadores.situacao import mapa_cores_situacao
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

def mostrar_tabela(df, altura_max_linhas=10, nome_tabela="Tabela de Dados", mostrar_na_tela=False):

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

    from st_aggrid import JsCode

    # Defina a função onGridReady em JavaScript diretamente
    on_grid_ready_js = JsCode("""
    function(params) {
        const api = params.api;
        const event = { api: api };
        // Chama a função Python para salvar os filtros
        const onReady = function(event) {
            // Chama a função Python para salvar filtros e ordenação
            // Adapte conforme necessário.
            const filterModel = api.getFilterModel();
            const sortModel = api.getSortModel();
            window.parent.postMessage({ type: "save_filter", filterModel: filterModel, sortModel: sortModel }, "*");
        };
        onReady(event);
    }
    """)

    # A seguir, use o código diretamente na configuração do grid
    grid_options['onGridReady'] = on_grid_ready_js
