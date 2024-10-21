import pdfkit

def convert_html_to_pdf(html_file, pdf_file):
    # Configure the path to wkhtmltopdf
    try:
        # Configure the path to wkhtmltopdf
        path_to_wkhtmltopdf = r"/home/leonardo/Downloads\wkhtmltox_0.12.6.1-2.jammy_arm64.deb"
        config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
        options = {
            'encoding': 'UTF-8',  # Força a codificação correta
        }

        # Converter HTML para PDF
        pdfkit.from_file(html_file, pdf_file, configuration=config, options=options)
        print(f"PDF gerado com sucesso: {pdf_file}")
    except OSError as e:
        print(f"Erro ao gerar PDF: {e}")