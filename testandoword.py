from docx import Document
from datetime import datetime
import datetime



# Abrir o documento existente
doc = Document(r'C:\Users\junior\Desktop\PROGRAMAS\meusprojeto\controle-de-armamento\cautelaarmamento\templates\cautelaarmamento\templates\passagem_de_servico\LIVRO DE CAUTELA DIÁRIA.docx')

# Dados da lista
dados = ['0', datetime.datetime(2024, 10, 27, 0, 0), datetime.date(2024, 10, 27), 'samuel', 'aaaaaaaaaa']

# Função para substituir placeholder no texto
def substituir_placeholder(doc, placeholder, novo_valor):
    for paragrafo in doc.paragraphs:
        if placeholder in paragrafo.text:
            # Substitui o texto do placeholder pelo novo valor
            paragrafo.text = paragrafo.text.replace(placeholder, novo_valor)

# Substituindo o placeholder '{{NOME}}' pelo item 3 da lista ('samuel')
substituir_placeholder(doc, '{{NOME_DO_ARMEIRO}}', dados[3])
substituir_placeholder(doc, '{{NOME_DO_SUBSTITUTO}}', dados[3])

# Salvar o documento com as alterações
doc.save('documento_final.docx')

print("Placeholder substituído e documento salvo com sucesso!")