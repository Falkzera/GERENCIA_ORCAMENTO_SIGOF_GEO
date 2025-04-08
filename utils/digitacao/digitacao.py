import re
import streamlit as st
from utils.formatar.formatar_valor import formatar_valor, formatar_valor_arredondado
from utils.estilizacao.dataframe import mostrar_tabela 

def digitacao(texto, acumular_pdf=True, mostrar_na_tela=False):
    """
    Adiciona texto ao PDF (sempre) e opcionalmente exibe no Streamlit.

    Args:
        texto (str): O conteúdo textual a ser usado.
        acumular_pdf (bool): Se True, adiciona ao conteúdo do PDF.
        mostrar_na_tela (bool): Se True, renderiza na interface do app. Padrão é False.
    """
    if mostrar_na_tela:
        st.markdown(
            f"<div style='text-align: justify; font-size: 22px;'>{texto}</div>",
            unsafe_allow_html=True
        )

    if acumular_pdf:
        if "conteudo_pdf" not in st.session_state:
            st.session_state["conteudo_pdf"] = []
        st.session_state["conteudo_pdf"].append(f"<p>{texto}</p>")



import re
import streamlit as st

def titulo_dinamico(titulo_markdown, acumular_pdf=True, mostrar_na_tela=False):
    """
    Adiciona título ao PDF (sempre) e opcionalmente exibe no Streamlit.

    Args:
        titulo_markdown (str): Título em formato markdown (ex: "### Meu Título")
        acumular_pdf (bool): Se True, acumula no conteúdo do PDF
        mostrar_na_tela (bool): Se True, renderiza no app (padrão: False)
    """
    if mostrar_na_tela:
        st.markdown(titulo_markdown)

    match = re.match(r"(#+)\s+(.*)", titulo_markdown.strip())
    if not match:
        return  # Se não for um markdown válido, ignora

    hashes, texto = match.groups()
    nivel = min(len(hashes), 6)

    if acumular_pdf:
        if "conteudo_pdf" not in st.session_state:
            st.session_state["conteudo_pdf"] = []
        st.session_state["conteudo_pdf"].append(f"<h{nivel}>{texto}</h{nivel}>")


def gerar_relatorio_origem_recursos(df_filtrado, origem_recurso, n=3):
    # Filtrando os dados conforme a origem de recurso
    df_origem_recurso = df_filtrado[df_filtrado['Origem de Recursos'] == origem_recurso]

    # Calculando os n maiores montantes por órgão (UO)
    maiores_montantes = df_origem_recurso.groupby('Órgão (UO)')['Valor'].sum().nlargest(n)

    # Iterando sobre os maiores montantes
    for idx, (orgao, valor) in enumerate(maiores_montantes.items()):
        # Filtrando os dados do órgão
        df_maior_montante = df_origem_recurso[df_origem_recurso['Órgão (UO)'] == orgao]
        solicitacoes = df_maior_montante['Nº do Processo'].tolist()
        fontes = df_maior_montante['Fonte de Recursos'].unique()
        grupos_despesas = df_maior_montante['Grupo de Despesas'].unique()

        # Formatando os dados
        solicitacoes_texto = ', '.join(solicitacoes)
        fontes_texto = ', '.join(fontes)
        grupos_despesas_texto = ', '.join(map(str, grupos_despesas))

        # Determinando a introdução com base no índice
        if idx == 0:
            introducao = "O maior montante em relação à quantia foi"
        elif idx == 1:
            introducao = "Em seguida, o segundo maior montante foi"
        else:
            introducao = "Por fim, o terceiro maior montante foi"

        # Exibindo o resultado
        digitacao(
            f'''{introducao} da {orgao}, com um valor total de {formatar_valor(valor)} ({por_extenso_reais(valor)}), 
            divididos em {len(solicitacoes)} ({por_extenso(len(solicitacoes))}) solicitações, sendo elas:
            {solicitacoes_texto}, presentes na fonte {fontes_texto} e grupos de despesas {grupos_despesas_texto}.'''
        )




from num2words import num2words

def por_extenso(valor):
    """
    Converte um número em palavras por extenso em português.

    Args:
    valor (int, float): Número a ser convertido para palavras.

    Returns:
    str: O número por extenso em português.
    """
    return num2words(valor, lang='pt')

from num2words import num2words

from num2words import num2words

def por_extenso_reais(valor):
    """
    Converte um valor monetário em reais (float ou int) para texto por extenso.
    Suporta valores até trilhões com centavos.
    """
    inteiro = int(valor)
    centavos = round((valor - inteiro) * 100)

    partes = []

    unidades = [
        (1_000_000_000_000, "trilhão", "trilhões"),
        (1_000_000_000, "bilhão", "bilhões"),
        (1_000_000, "milhão", "milhões"),
        (1_000, "mil", "mil"),
        (1, "", "")
    ]

    restante = inteiro

    for base, singular, plural in unidades:
        if restante >= base:
            valor_parte = restante // base
            restante = restante % base

            extenso = num2words(valor_parte, lang='pt')

            if base == 1:
                partes.append(extenso)
            elif valor_parte == 1:
                partes.append(f"{extenso} {singular}")
            else:
                partes.append(f"{extenso} {plural}")

    reais_extenso = " ".join(partes) + (" real" if inteiro == 1 else " reais")

    if centavos > 0:
        centavos_extenso = num2words(centavos, lang='pt')
        centavos_texto = "centavo" if centavos == 1 else "centavos"
        return f"{reais_extenso} e {centavos_extenso} {centavos_texto}"
    else:
        return reais_extenso



def mes_por_extenso(mes_num):
    """
    Converte o número do mês para o nome do mês por extenso.
    
    Args:
    mes_num (int): Número do mês (1 a 12).
    
    Returns:
    str: Nome do mês por extenso.
    """
    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    
    # Verifica se o mês é válido (1 a 12)
    if 1 <= mes_num <= 12:
        return meses[mes_num - 1]  # Subtrai 1 porque o índice do Python começa do 0
    else:
        return "Mês inválido"  # Caso o mês não seja válido


import plotly.graph_objects as go



import plotly.io as pio
import tempfile
import base64
import os

import streamlit as st
import plotly.io as pio
import base64
import tempfile
import os
import base64
import uuid
from utils.digitacao.digitacao import titulo_dinamico  # garante compatibilidade

def inserir_grafico_pdf(fig, titulo):
    import tempfile
    import os

    # Gerar nome único
    nome_arquivo = f"{uuid.uuid4()}.png"

    # Salva o gráfico como imagem temporária
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        fig.write_image(tmpfile.name, format="png", scale=3)
        caminho_imagem = tmpfile.name

    # Número do gráfico
    if "contador_grafico" not in st.session_state:
        st.session_state["contador_grafico"] = 1

    num = st.session_state["contador_grafico"]
    st.session_state["contador_grafico"] += 1

    # Título do gráfico no PDF (em negrito)
    titulo_html = f"""
    <div style="text-align: center; font-family: Times New Roman, serif; font-size: 12pt; font-weight: bold; margin-bottom: 5px;">
        Gráfico {num} - {titulo}
    </div>
    """

    # Fonte do gráfico
    fonte_html = """
        <div class='fonte'>
            <strong>Fonte:</strong> elaboração própria a partir de dados de processos do SEI e SIAFE - 2025.
        </div>
        <div style="height: 18px;"></div> <!-- Espaço abaixo da fonte -->
        """

    # Converter imagem para base64
    with open(caminho_imagem, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    imagem_html = f"""
    <div style="text-align: center; margin: 20px 0;">
        <img src="data:image/png;base64,{encoded}" style="width:99%; max-width:600px;" />
    </div>
    """

    # Adiciona tudo ao conteúdo PDF
    if "conteudo_pdf" not in st.session_state:
        st.session_state["conteudo_pdf"] = []

    bloco_html = f"""
    <div style="page-break-inside: avoid; margin-bottom: 20px;">
        {titulo_html}
        {imagem_html}
        {fonte_html}
    </div>
    """

    st.session_state["conteudo_pdf"].append(bloco_html)



def mostrar_tabela_pdf(df, nome_tabela=None, mostrar_na_tela=False):
    """
    Adiciona uma tabela formatada ao PDF, e opcionalmente exibe no app com AgGrid.

    Args:
        df (pd.DataFrame): Tabela a ser renderizada.
        nome_tabela (str): Título da tabela (será usado no PDF e opcionalmente na interface).
        mostrar_na_tela (bool): Se True, mostra no app com estilo; padrão é False.
    """

    if mostrar_na_tela:
        from utils.estilizacao.dataframe import mostrar_tabela
        mostrar_tabela(df, nome_tabela=nome_tabela)

    # Título para o PDF
    titulo = f"<h4>{nome_tabela}</h4>" if nome_tabela else ""

    # Tabela em HTML
    html_tabela = df.to_html(index=False, border=0, justify="center")

    # Adiciona ao conteúdo do PDF
    if "conteudo_pdf" not in st.session_state:
        st.session_state["conteudo_pdf"] = []

    st.session_state["conteudo_pdf"].append(titulo + html_tabela)


import streamlit as st
from utils.estilizacao.dataframe import mostrar_tabela  # Agora com o caminho correto

def mostrar_tabela_pdf(df, nome_tabela=None):
    # Mostrar no app
    mostrar_tabela(df, nome_tabela=nome_tabela)

    # Estilo CSS
    estilo_tabela = """
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 10px;
            margin-bottom: 5px;
            font-family: 'Times New Roman', serif;
            font-size: 12pt;
            page-break-inside: auto;
        }
        th, td {
            border: 1px solid #000;
            padding: 6px 10px;
            text-align: center;
            vertical-align: middle;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        tr {
            page-break-inside: avoid;
            page-break-after: auto;
        }
        .quadro-titulo {
            text-align: center;
            font-size: 12pt;
            font-weight: bold;
            margin-top: 24px;
            margin-bottom: 8px;
        }
        .fonte {
            text-align: center;
            font-size: 10pt;
            font-weight: normal;
            margin-top: 6px;
        }
    </style>
    """

    # Numeração de quadros (mantida na sessão)
    if "contador_quadro" not in st.session_state:
        st.session_state.contador_quadro = 1
    numero_quadro = st.session_state.contador_quadro
    st.session_state.contador_quadro += 1

    # HTML final com título + tabela + fonte
    titulo_html = f"<div class='quadro-titulo'>Quadro {numero_quadro}: {nome_tabela}</div>" if nome_tabela else ""
    html_tabela = df.to_html(index=False, border=0, justify="center")
    fonte_html = """
        <div class='fonte'>
            <strong>Fonte:</strong> elaboração própria a partir de dados de processos do SEI e SIAFE - 2025.
        </div>
        <div style="height: 18px;"></div> <!-- Espaço abaixo da fonte -->
        """


    bloco_html = f"""
    {estilo_tabela}
    {titulo_html}
    {html_tabela}
    {fonte_html}
    """

    if "conteudo_pdf" not in st.session_state:
        st.session_state["conteudo_pdf"] = []

    st.session_state["conteudo_pdf"].append(bloco_html)

import plotly.graph_objects as go
import streamlit as st
from utils.digitacao.digitacao import inserir_grafico_pdf  # ajuste se estiver em outro módulo

def gerar_grafico_pizza(labels, values, titulo_pdf="Gráfico: Pizza", cores=None, mostrar_na_tela=False):
    if cores is None:
        cores = [
            "#095AA2", "#0A6BB5", "#0B7CC8", "#0C8DDB", "#0D9EEE",
            "#E0E0E0", "#D0D0D0", "#C0C0C0", "#B0B0B0", "#A0A0A0"
        ]

    fig = go.Figure(
        data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=cores),
            textinfo="percent",
            textfont=dict(
                family="Times New Roman, serif",
                size=20,
            ),
            insidetextorientation="radial"
        )]
    )

    fig.update_layout(
        title=None,
        font=dict(
            family="Times New Roman, serif",
            size=20,
            color="black"
        ),
        uniformtext_minsize=20,
        uniformtext_mode='hide',
        margin=dict(t=30, b=30, l=30, r=30),
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            y=-0.15,
            x=0.5,
            xanchor="center",
            font=dict(
                family="Times New Roman, serif",
                size=20
            )
        )
    )

    if mostrar_na_tela:
        st.plotly_chart(fig, use_container_width=True)
    inserir_grafico_pdf(fig, titulo=titulo_pdf)

import plotly.graph_objects as go
import streamlit as st
from utils.digitacao.digitacao import inserir_grafico_pdf  # ajuste se necessário

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def gerar_grafico_barra(x, y, titulo_pdf="Gráfico: Barras", cores=None, texto_formatado=None, mostrar_na_tela=False):
    # Transforma em DataFrame para manipular
    df = pd.DataFrame({'x': x, 'y': y})

    # Ordena decrescentemente pelos valores
    df = df.sort_values(by='y', ascending=False).reset_index(drop=True)

    # Se houver mais que 5 categorias, agrupa o restante em "Outros"
    if len(df) > 5:
        top5 = df.iloc[:5]
        outros = df.iloc[5:]
        total_outros = outros['y'].sum()
        outros_row = pd.DataFrame({'x': ['Outros'], 'y': [total_outros]})
        df = pd.concat([top5, outros_row], ignore_index=True)

    # Ordena novamente exceto "Outros", que fica por último
    df_sem_outros = df[df['x'] != 'Outros'].sort_values(by='y', ascending=False)
    df_outros = df[df['x'] == 'Outros']
    df = pd.concat([df_sem_outros, df_outros], ignore_index=True)

    # Definições finais
    x = df['x']
    y = df['y']
    texto_formatado = texto_formatado if texto_formatado else y

    if cores is None:
        cores_padrao = [
            "#095AA2", "#0A6BB5", "#0B7CC8", "#0C8DDB", "#0D9EEE",
            "#E0E0E0", "#D0D0D0", "#C0C0C0", "#B0B0B0", "#A0A0A0"
        ]
        cores = cores_padrao[:len(x)]
        if len(cores) < len(x):
            cores += ["#AAAAAA"] * (len(x) - len(cores))  # preenche se faltar cor

    fig = go.Figure(
        data=[go.Bar(
            x=x,
            y=y,
            marker=dict(color=cores),
            text=texto_formatado,
            textposition="outside",
            textangle=0
        )]
    )

    fig.update_traces(
        textfont=dict(
            family="Times New Roman, serif",
            size=14,
            color="black"
        )
    )

    fig.update_layout(
        title=None,
        font=dict(family="Times New Roman, serif", size=14, color="black"),
        uniformtext_minsize=14,
        uniformtext_mode='show',
        margin=dict(t=60, b=100, l=40, r=20),
        height=600,
        xaxis=dict(
            title=None,
            tickfont=dict(family="Times New Roman, serif", size=14),
            showgrid=False,
            showticklabels=True,
            tickangle=0,
            automargin=True
        ),
        yaxis=dict(
            title=None,
            tickfont=dict(family="Times New Roman, serif", size=14),
            showgrid=False,
            showticklabels=True,
        ),
    )

    if mostrar_na_tela:
        st.plotly_chart(fig, use_container_width=True)

    inserir_grafico_pdf(fig, titulo=titulo_pdf)




def gerar_relatorio_origem_recurso_com_graficos(df_filtrado, origem_recurso, n=3, tipo_grafico='nenhum'):
    # Filtrando os dados conforme a origem de recurso
    df_origem_recurso = df_filtrado[df_filtrado['Origem de Recursos'] == origem_recurso]

    # Cálculo dos maiores montantes por órgão (UO)
    maiores_montantes = df_origem_recurso.groupby('Órgão (UO)')['Valor'].sum().nlargest(n)

    # Contagem e valor total dos órgãos
    qtd_orgaos = df_origem_recurso['Órgão (UO)'].nunique()
    qntd_valor_total = df_origem_recurso['Valor'].sum()
    fontes_recurso = df_origem_recurso['Fonte de Recursos'].unique()
    
    fontes_recurso_texto = ', '.join(fontes_recurso)

    # Gerando o texto detalhado
    if qtd_orgaos == 0:
        digitacao(
            f'''Não foram encontrados órgãos solicitantes para a origem de recurso {origem_recurso}.'''
        )
        return
    digitacao(
        f'''Dos {qtd_orgaos} órgãos solicitantes, o montante total de créditos sem cobertura foi de {formatar_valor(qntd_valor_total)} ({por_extenso_reais(qntd_valor_total)}), 
        divididos entre as fontes de recursos: {fontes_recurso_texto}.'''
    )

    # Ordena ANTES de formatar (com base no valor numérico real e agrupando órgãos)
    df_origem_recurso_tabela = df_origem_recurso[['Órgão (UO)', 'Nº do Processo', 'Fonte de Recursos', 'Grupo de Despesas', 'Valor']] \
        .sort_values(by=['Órgão (UO)','Valor' ], ascending=[False, False]).copy()

    # Formata os valores depois de ordenar
    df_origem_recurso_tabela['Valor'] = df_origem_recurso_tabela['Valor'].apply(formatar_valor)

    # Mostra a tabela no PDF
    mostrar_tabela_pdf(
        df_origem_recurso_tabela,
        nome_tabela=f"Tabela de Dados - {origem_recurso}"
    )

 
    # Iterando sobre os maiores montantes
    for idx, (orgao, valor) in enumerate(maiores_montantes.items()):
        # Filtrando os dados do órgão
        df_maior_montante = df_origem_recurso[df_origem_recurso['Órgão (UO)'] == orgao]
        solicitacoes = df_maior_montante['Nº do Processo'].tolist()
        fontes = df_maior_montante['Fonte de Recursos'].unique()
        grupos_despesas = df_maior_montante['Grupo de Despesas'].unique()

        # Formatando os dados
        solicitacoes_texto = ', '.join(solicitacoes)
        fontes_texto = ', '.join(fontes)
        grupos_despesas_texto = ', '.join(map(str, grupos_despesas))

        # Determinando a introdução com base no índice
        if idx == 0:
            introducao = "O maior montante em relação à quantia foi"
        elif idx == 1:
            introducao = "Em seguida, o segundo maior montante foi"
        else:
            introducao = "Por fim, o terceiro maior montante foi"

        # Exibindo o resultado
        digitacao(
            f'''{introducao} da {orgao}, com um valor total de {formatar_valor(valor)} ({por_extenso_reais(valor)}), 
            divididos em {len(solicitacoes)} ({por_extenso(len(solicitacoes))}) solicitações, sendo elas:
            {solicitacoes_texto}, presentes na fonte {fontes_texto} e grupos de despesas {grupos_despesas_texto}.'''
        )

    orgaos_por_valor = df_origem_recurso.groupby('Órgão (UO)')['Valor'].sum().sort_values(ascending=False)

    azul_tons = [
    "#095AA2", "#0A6BB5", "#0B7CC8", "#0C8DDB", "#0D9EEE",
    "#E0E0E0", "#D0D0D0", "#C0C0C0", "#B0B0B0", "#A0A0A0"]

    if tipo_grafico == 'pizza':

        gerar_grafico_pizza(
            labels=orgaos_por_valor.index,
            values=orgaos_por_valor.values,
            titulo_pdf=f"Solicitação de Crédito por Órgão ({origem_recurso})",
            cores=azul_tons
        )

    elif tipo_grafico == 'barra':
        # Gráfico de barras (Solicitação de Crédito por Órgão)
        valores_formatados = [formatar_valor_arredondado(valor) for valor in orgaos_por_valor.values]

        # Gera e exibe o gráfico, e envia para o PDF
        gerar_grafico_barra(
            x=orgaos_por_valor.index,
            y=orgaos_por_valor.values,
            cores=azul_tons[:len(orgaos_por_valor)],
            texto_formatado=valores_formatados,
            titulo_pdf=f"Solicitação de Crédito por Órgão ({origem_recurso})"
        )

    # Se o tipo de gráfico for 'nenhum', não gera gráfico algum
    elif tipo_grafico == 'nenhum':
        print("Nenhum gráfico foi gerado.")