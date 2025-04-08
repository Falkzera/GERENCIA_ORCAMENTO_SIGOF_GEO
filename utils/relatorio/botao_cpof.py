import streamlit as st
from datetime import datetime
from utils.digitacao.gerar_relatorio import gerar_pdf_weasy
from utils.relatorio.relatorio_cpof import montar_relatorio_pdf
from utils.digitacao.digitacao import mes_por_extenso
def botao_gerar_e_baixar_pdf_cpof(ano, mes, df_filtrado, df_mes_anterior):
    with st.container():
        if st.button("📄 Gerar e Baixar Relatório", use_container_width=True, type="primary", key="botao_pdf_cpof"):
            st.session_state["gerando_pdf"] = True
            st.session_state["contador_quadro"] = 1
            st.session_state["contador_grafico"] = 1
            st.session_state["conteudo_pdf"] = []

            # Chama a função que monta o relatório
            from utils.relatorio.relatorio_cpof import montar_relatorio_pdf
            montar_relatorio_pdf(ano, mes, df_filtrado, df_mes_anterior)

            # Gera o PDF e botão de download
            from utils.digitacao.gerar_relatorio import gerar_pdf_weasy
            conteudo = st.session_state.get("conteudo_pdf", [])
            if not conteudo:
                st.warning("⚠️ Nenhum conteúdo foi gerado para o relatório.")
                return

            pdf_path = gerar_pdf_weasy(conteudo)

            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Clique aqui para baixar o PDF",
                    data=f,
                    file_name=f"Relatorio_CPOF_{mes_por_extenso(mes)}_{ano}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary",
                    key="download_pdf_cpof"
                )

            st.session_state["gerando_pdf"] = False
