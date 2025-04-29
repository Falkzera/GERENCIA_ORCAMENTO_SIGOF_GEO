import streamlit as st
import inspect

def botao_gerar_e_baixar_arquivo(
    nome_botao: str,
    montar_conteudo_funcao,
    parametros_funcao: dict,
    nome_arquivo: str,
    tipo_arquivo: str = "pdf"
):
    """
    Botão genérico para gerar e baixar arquivos (PDF ou DOCX), adaptável a diferentes funções de montagem.
    """

    with st.container():
        if st.button(f"📄 {nome_botao}", use_container_width=True, type="primary", key=f"botao_{nome_botao}"):
            st.session_state["gerando_arquivo"] = True
            st.session_state["contador_quadro"] = 1
            st.session_state["contador_grafico"] = 1
            st.session_state["conteudo_pdf"] = []

            # 1️⃣ Coleta apenas os parâmetros que a função precisa
            assinatura = inspect.signature(montar_conteudo_funcao)
            parametros_necessarios = assinatura.parameters.keys()

            parametros_filtrados = {
                nome: valor
                for nome, valor in parametros_funcao.items()
                if nome in parametros_necessarios
            }

            # 2️⃣ Montar o conteúdo com os parâmetros corretos
            montar_conteudo_funcao(**parametros_filtrados)

            conteudo = st.session_state.get("conteudo_pdf", [])
            if not conteudo:
                st.warning("⚠️ Nenhum conteúdo foi gerado.")
                st.session_state["gerando_arquivo"] = False
                return

            # 3️⃣ Gerar o arquivo conforme tipo
            if tipo_arquivo.lower() == "pdf":
                from utils.digitacao.gerar_relatorio import gerar_pdf_weasy
                arquivo_path = gerar_pdf_weasy(conteudo)
            elif tipo_arquivo.lower() == "docx":
                from utils.digitacao.gerar_relatorio import gerar_docx
                arquivo_path = gerar_docx(conteudo)
            else:
                st.error(f"❌ Tipo de arquivo '{tipo_arquivo}' não suportado.")
                st.session_state["gerando_arquivo"] = False
                return

            # 4️⃣ Ler o arquivo
            with open(arquivo_path, "rb") as f:
                arquivo_bytes = f.read()

            # 5️⃣ Botão de download
            st.download_button(
                label=f"📥 Clique aqui para baixar o {tipo_arquivo.upper()}",
                data=arquivo_bytes,
                file_name=nome_arquivo,
                mime="application/pdf" if tipo_arquivo.lower() == "pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
                type="primary",
                key=f"download_{nome_botao}"
            )

            st.session_state["gerando_arquivo"] = False
