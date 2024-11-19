from weasyprint import HTML
import os

# Caminho do arquivo HTML local
html_path = r'relatorios\relatorio_20241118_143058.html'  # Certifique-se de colocar o caminho correto para o seu arquivo

# Definir o caminho do PDF de saída na pasta "relatorios"
output_pdf_path = os.path.join('relatorios', 'saida.pdf')  # Caminho relativo para salvar o PDF na pasta relatorios

# Converter o arquivo HTML para PDF e salvar na pasta "relatorios"
HTML(html_path).write_pdf(output_pdf_path)
