from weasyprint import HTML

# Caminho do arquivo HTML ou string com o conteúdo HTML
import os

# Caminho do arquivo HTML ou string com o conteúdo HTML
html = os.path.join(os.path.dirname(__file__), 'relatorio_20250120_214032.html')

# Verificando se o arquivo HTML existe antes de gerar o PDF
if os.path.exists(html):
	# Gerando o PDF a partir do HTML
	HTML(html).write_pdf("relatorio.pdf")
else:
	print(f"Arquivo HTML não encontrado: {html}")
