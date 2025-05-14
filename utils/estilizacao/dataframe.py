import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional
from utils.buscadores.situacao import mapa_cores_situacao
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, DataReturnMode, GridUpdateMode

# Estilos e JS reutilizáveis
CELL_STYLE_PADRAO = JsCode(
    "function(params) {"
    "  return {"
    "    'textAlign': 'center',"
    "    'display': 'flex',"
    "    'alignItems': 'center',"
    "    'justifyContent': 'center'"
    "  };"
    "}"
)

CSS_CUSTOMIZADO = {
    ".ag-header": {"background-color": "#3064ad !important"},
    ".ag-header-cell-label": {
        "color": "#ffffff !important",
        "font-weight": "650",
        "font-size": "12px",
        "justify-content": "center",
    },
    ".ag-cell": {
        "font-size": "12px",
        "line-height": "1.4",
        "border-color": "#e6e6e6",
    },
    ".ag-row-hover": {"background-color": "#e8f0fe !important"},
    ".ag-row-selected": {"background-color": "#d0e8ff !important"},
    ".ag-root-wrapper": {"border": "1px solid #e0e0e0", "border-radius": "8px"},
}



def build_grid_options(
    columns: tuple,
    altura_max_linhas: int,
    enable_click: bool,
    set_filter_cols: list[str] = None,
    unique_vals: dict[str,list] = None
) -> Dict[str, Any]:
    """
    Gera e retorna o dict de gridOptions para AgGrid com base nas colunas,
    quantidade de linhas por página e se permite clique.
    """
    # Criamos um DataFrame vazio apenas para inicializar o builder
    empty_df = pd.DataFrame({col: [] for col in columns})
    gb = GridOptionsBuilder.from_dataframe(empty_df)

    # Configurações padrão de coluna
    gb.configure_default_column(
        resizable=True,
        autoHeight=True,
        wrapText=True,
        sortable=True,
        filter=True,
        floatingFilter=False,
        cellStyle=CELL_STYLE_PADRAO,
        enableRowGroup=True,    # permite agrupar linhas
        enablePivot=True,       # permite usar como coluna de pivot
        enableValue=True, 
    )

    # Paginação ao invés de scroll manual
    gb.configure_pagination(
        paginationAutoPageSize=False,
        # paginationPageSize=altura_max_linhas,
        paginationPageSize=20,
    )

    # Barra lateral de filtros (enterprise)
    gb.configure_side_bar()

    # dentro da função build_grid_options, antes do gb.build()
    if "Valor" in columns:
        gb.configure_column(
            "Valor",
            type=["numericColumn"],      # habilita tratamento numérico
            aggFunc="sum",               # usa soma como agregação padrão
            valueFormatter=JsCode("""
                function(params) {
                    if (params.value == null) return '';
                    // toLocaleString no pt-BR com 2 dígitos
                    return 'R$ ' + params.value.toLocaleString('pt-BR', {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                    });
                }
            """)
        )

    # Seleção de linha e callback de duplo clique
    if enable_click:
        gb.configure_selection(selection_mode="single", use_checkbox=False)
        gb.configure_grid_options(
            onRowDoubleClicked=JsCode(
                "function(event) {"
                "  window.parent.postMessage({"
                "    type: 'row_double_click',"
                "    data: event.data"
                "  }, '*');"
                "}"
            )
        )

    # Estilo condicional da coluna 'Situação', se existir
    if "Situação" in columns:
        mapa_js = ", ".join(f"'{sit}': '{cor}'" for sit, cor in mapa_cores_situacao.items())
        cell_style_situacao = JsCode(
            "function(params) {\n"
            f"  let cor = {{{mapa_js}}};\n"
            "  return {\n"
            "    backgroundColor: cor[params.value] || '#ffffff',\n"
            "    color: 'black',\n"
            "    fontWeight: '500',\n"
            "    textAlign: 'center',\n"
            "    display: 'flex',\n"
            "    alignItems: 'center',\n"
            "    justifyContent: 'center'\n"
            "  };\n"
            "}"
        )
        gb.configure_column("Situação", cellStyle=cell_style_situacao)


    # Se foi passada alguma coluna para Set Filter, configura cada uma
    if set_filter_cols:
        for col in set_filter_cols:
            # entrega a lista de valores únicos para popular o checkbox
            # (pode também passar um filterParams fixo se quiser)
            gb.configure_column(
                col,
                filter="agSetColumnFilter",
                filterParams={
                    "values": sorted(empty_df[col].dropna().unique().tolist()),
                    "suppressSelectAll": False,
                    "suppressMiniFilter": False
                }
            )


    # se houver colunas para Set Filter, use unique_vals
    if set_filter_cols and unique_vals:
        for col in set_filter_cols:
            gb.configure_column(
                col,
                filter="agSetColumnFilter",
                filterParams={
                    "values": unique_vals[col],
                    "suppressSelectAll": False,
                    "suppressMiniFilter": False
                }
            )

    opts = gb.build()
    opts["autoHeaderHeight"] = True
    opts["enableRangeSelection"]        = True   # permite selecionar células individualmente
    opts["suppressCopyRowsToClipboard"] = True   # impede copiar a linha inteira
    opts["suppressRowClickSelection"] = False

      # <<< Duplo‑clique copia a célula >>>
    opts["onCellDoubleClicked"] = JsCode("""
    +   function(event) {
    +       // limpa seleção anterior
    +       event.api.clearRangeSelection();
    +       // seleciona só esta célula
    +       event.api.addCellRange({
    +           rowStartIndex: event.rowIndex,
    +           rowEndIndex: event.rowIndex,
    +           columns: [event.column.getId()]
    +       });
    +       // copia o conteúdo do range (esta célula) para o clipboard
    +       event.api.copySelectedRangeToClipboard();
    +   }
    +   """)

    return opts

def mostrar_tabela(
    df: pd.DataFrame,
    altura_max_linhas: int = None,
    nome_tabela: str = "Tabela de Dados",
    mostrar_na_tela: bool = False,
    enable_click: bool = False
) -> tuple[pd.DataFrame, dict | None]:
    """
    Exibe um DataFrame no Streamlit com AgGrid e retorna:
     - df_filtrado: DataFrame já aplicado com os filtros do usuário
     - selected_row: dict da linha selecionada (se enable_click=True e houver duplo clique)
    """
    if not mostrar_na_tela:
        return df, None

    # Inicializa session_state para this tabela, se necessário
    for key in ("grid_options", "filtros", "ordenacao"):
        estado = f"{key}_{nome_tabela}"
        if estado not in st.session_state:
            st.session_state[estado] = None

    # Definição das opções de filtros
    UNIQUE_THRESHOLD = 100
    # encontra colunas de texto com poucos valores únicos
    set_filter_cols = [
        col for col in df.select_dtypes(include=['object', 'category']).columns
        if df[col].nunique() <= UNIQUE_THRESHOLD and col not in ["Última Edição", "Cadastrado Por"]
    ]

    # Aqui vem a diferença: pegue os valores do df de verdade
    unique_vals = {
        col: (df[col].dropna().unique().tolist())
        for col in set_filter_cols
    }

    # Constrói grid_options (cacheado)
    grid_options = build_grid_options(
        columns=tuple(df.columns),
        altura_max_linhas=altura_max_linhas,
        enable_click=enable_click,
        set_filter_cols=set_filter_cols,
        unique_vals=unique_vals 
    )

    # Restaura filtros e ordenação do último estado
    filtros_key = f"filtros_{nome_tabela}"
    ordenacao_key = f"ordenacao_{nome_tabela}"
    if st.session_state[filtros_key]:
        grid_options["initialFilterModel"] = st.session_state[filtros_key]
    if st.session_state[ordenacao_key]:
        grid_options["initialSortModel"] = st.session_state[ordenacao_key]

    # Título
    st.markdown(f"##### {nome_tabela}")

    # # Tentativa de ordenar as colunas
    # try:
    #     # Restaura a ordenação anterior e tenta aplicar na tabela
    #     for col in df.columns:
    #         try:
    #             # Tenta ordenar a coluna
    #             df = df.sort_values(by=col, ascending=True)
    #         except Exception as e:
    #             # Se não for possível ordenar, ignora e vai para a próxima
    #             st.warning(f"Não foi possível ordenar a coluna '{col}': {e}")
    #             continue  # Ignora e passa para a próxima coluna

    # except Exception as e:
    #     st.error(f"Ocorreu um erro ao tentar ordenar a tabela: {e}")


    # Renderiza a AgGrid
    response = AgGrid(
        df,
        gridOptions=grid_options,
        theme="alpine", # opções
        allow_unsafe_jscode=True,
        custom_css=CSS_CUSTOMIZADO,
        height=700,          # altura em pixels
        width='100%',
        reload_data=True,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        enable_enterprise_modules=enable_click,
        return_mode="AS_INPUT" if enable_click else "NONE",
    )

    # Armazena filtros e ordenação atuais
    st.session_state[filtros_key] = response.get("filter_model")
    st.session_state[ordenacao_key] = response.get("sort_model")

    df_filtrado_pelo_grid = pd.DataFrame(response["data"])

    # Se click estiver habilitado, retorna a linha selecionada
    # Se click estiver habilitado, captura a linha selecionada (sem dar return aqui)
    selected_row = None
    if enable_click:
        try:
            sel = response.get("selected_rows")
            if isinstance(sel, list) and sel:
                selected_row = sel[0]
            elif hasattr(sel, "iloc") and len(sel) > 0:
                selected_row = sel.iloc[0].to_dict()
        except Exception:
            st.error("Não foi possível obter a linha selecionada.")



    return df_filtrado_pelo_grid, selected_row
