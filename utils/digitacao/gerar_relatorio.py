from weasyprint import HTML
import markdown
import tempfile

def gerar_pdf_weasy(conteudo_pdf, nome_arquivo="relatorio.pdf"):
    # Juntar o conteúdo e converter markdown → HTML
    html_conteudo = "\n".join(conteudo_pdf)  # conteúdo já é HTML, não precisa de conversão
    html_final = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>

            /* Define a página */
            @page {{
                size: A4;
                margin: 3cm 2cm 2cm 3cm;  /* topo, direita, inferior, esquerda */
                
                @bottom-right {{
                    font-family: 'Times New Roman', serif;
                    content: "Página " counter(page);
                    font-size: 10pt;
                }}
            }}

            body {{
                font-family: 'Times New Roman', serif;
                font-size: 12pt;
                line-height: 1.5;
                color: #000;
                text-align: justify;
            }}

            h1 {{
                text-align: center;
                font-size: 20pt;
                font-weight: bold;
                margin-top: 0;
                margin-bottom: 20px;
            }}

            h2 {{
                font-size: 16pt;
                font-weight: bold;
                margin-top: 30px;
                margin-bottom: 15px;
            }}

            h3 {{
                font-size: 14pt;
                font-weight: bold;
                margin-top: 20px;
                margin-bottom: 10px;
            }}

            p {{
                text-indent: 1.25cm;
                margin: 0 0 12pt 0;
            }}

            strong {{
                font-weight: bold;
            }}

            em {{
                font-style: italic;
            }}

        </style>
    </head>
    <body>
        {html_conteudo}
    </body>
    </html>
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        HTML(string=html_final).write_pdf(f.name)
        return f.name


