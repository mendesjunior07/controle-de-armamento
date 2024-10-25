import requests

# Substitua pelas suas credenciais
client_id = '65380088368'
client_secret = 'Er150457'

# URL para obter o token de acesso
token_url = 'https://sso.acesso.gov.br/oauth/token'

# Dados para a requisição do token
token_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret
}

# Fazendo a requisição do token
token_response = requests.post(token_url, data=token_data)

# Verificando se a requisição do token foi bem-sucedida
if token_response.status_code == 200:
    # Obtendo o token de acesso
    access_token = token_response.json()['access_token']
else:
    print(f'Erro ao obter token: {token_response.status_code}')
    print(token_response.text)
    exit()  # Encerra o programa se não conseguir o token

# URL para assinar o documento
assinatura_url = 'https://assinatura.servicos.gov.br/assinatura/v1/assinaturas'

# Dados para a requisição de assinatura (ajuste conforme necessário)
assinatura_data = {
    'documento': {
        'tipo': 'pdf',  # ou outro tipo de documento
        'conteudo': 'base64_encoded_document_content'  # Conteúdo do documento em base64
    },
    'certificado': {
        'tipo': 'A1',  # ou A3, dependendo do seu certificado
        'senha': 'sua_senha_do_certificado'  # Senha do certificado, se necessário
    },
    # Outros parâmetros necessários para a assinatura
}

# Headers da requisição com o token de acesso
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'  # Defina o tipo de conteúdo como JSON
}

# Fazendo a requisição de assinatura
assinatura_response = requests.post(assinatura_url, json=assinatura_data, headers=headers)

# Verificando a resposta
if assinatura_response.status_code == 200:
    # Assinatura realizada com sucesso
    print(assinatura_response.json())
else:
    # Erro na assinatura
    print(f'Erro: {assinatura_response.status_code}')
    print(assinatura_response.text)
