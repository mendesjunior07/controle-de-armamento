# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         if not username or not password:
#             messages.error(request, 'Por favor, preencha ambos os campos.')
#             return render(request, 'login.html')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'Nome de usuário ou senha incorretos.')

#     return render(request, 'login.html')


# ##################################################################

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest,HttpResponse
from django.db.models import Sum
from django.db import transaction
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
import json
import logging
from django.utils import timezone
from .models import (
    Categoria, 
    CautelaDeArmamento, 
    Subcategoria, 
    Policial, 
    DescautelasCa,
    CategoriaMunicao, 
    SubcategoriaMunicao, 
    CautelaDeMunicoes,
    RegistroCautelaCompleta,
    RegistroDescautelamento,
)

def index(request):
    return render(request, 'cautelaarmamento/index.html')


def cautela_de_armamento_view(request):
    if request.method == 'POST':
        # Obtém os dados do formulário
        policial_id = request.POST.get('policial')
        tipo_servico = request.POST.get('tipo_servico')
        categorias_armamento = request.POST.getlist('categorias[]')
        subcategorias_armamento = request.POST.getlist('subcategorias[]')
        categorias_municao = request.POST.getlist('categoria_municoes[]')
        subcategorias_municao = request.POST.getlist('subcategoria_municoes[]')
        quantidades_municao = request.POST.getlist('quantidade[]')

        # Verifica se os campos obrigatórios foram preenchidos
        if not policial_id or not tipo_servico:
            return JsonResponse({'error': 'Os campos Nome do Policial e Tipo de Serviço são obrigatórios.'}, status=400)

        policial = get_object_or_404(Policial, id=policial_id)
        armeiro = request.user

        try:
            with transaction.atomic():
                # Inicializa variáveis para munição e armamento
                categoria_armamento_nome = None
                subcategoria_armamento_nome = None
                categoria_municao_nome = None
                subcategoria_municao_nome = None
                quantidade_total_municao = 0

                # Processa o armamento, se presente

                if categorias_armamento and subcategorias_armamento:
                    for i in range(len(categorias_armamento)):
                        categoria_id = categorias_armamento[i]
                        subcategoria_id = subcategorias_armamento[i]
                        if categoria_id and subcategoria_id:
                            categoria_armamento = get_object_or_404(Categoria, id=categoria_id)
                            subcategoria_armamento = get_object_or_404(Subcategoria, id=subcategoria_id)

                            # Salva registro no modelo de Cautela de Armamento
                            CautelaDeArmamento.objects.create(
                                policial=policial,
                                tipo_servico=tipo_servico,
                                categoria=categoria_armamento,
                                subcategoria=subcategoria_armamento,
                                armeiro=armeiro
                            )

                            subcategoria_armamento.situacao = 'cautelada'
                            subcategoria_armamento.save()

                            # Registro na nova model com todos os detalhes para cada linha
                            RegistroCautelaCompleta.objects.create(
                                policial=policial,
                                tipo_servico=tipo_servico,
                                categoria_armamento=categoria_armamento.nome,  # Aqui pode permanecer igual
                                subcategoria_armamento=subcategoria_armamento.descricao_completa,  # Mudança feita aqui
                                categoria_municao=None,
                                subcategoria_municao=None,
                                quantidade_municao=0,
                                armeiro=armeiro
                            )
                # Processa as munições

                if categorias_municao and subcategorias_municao and quantidades_municao:
                    for i in range(len(categorias_municao)):
                        categoria_id = categorias_municao[i]
                        subcategoria_id = subcategorias_municao[i]
                        quantidade = quantidades_municao[i]
                        if categoria_id and subcategoria_id and quantidade:
                            categoria_municao = get_object_or_404(CategoriaMunicao, id=categoria_id)
                            subcategoria_municao = get_object_or_404(SubcategoriaMunicao, id=subcategoria_id)

                            quantidade = int(quantidade)
                            if quantidade > subcategoria_municao.total_de_municoes:
                                return JsonResponse({'error': 'A quantidade solicitada excede o total disponível.'}, status=400)

                            # Debita o valor no banco de dados
                            subcategoria_municao.total_de_municoes -= quantidade
                            subcategoria_municao.save()

                            # Salva registro no modelo de Cautela de Munição
                            CautelaDeMunicoes.objects.create(
                                policial=policial,
                                categoria=categoria_municao,
                                subcategoria=subcategoria_municao,
                                quantidade=quantidade
                            )

                            # Registro na nova model com todos os detalhes para cada linha - Munição
                            RegistroCautelaCompleta.objects.create(
                                policial=policial,
                                tipo_servico=tipo_servico,
                                categoria_armamento=None,
                                subcategoria_armamento=None,
                                categoria_municao=categoria_municao.nome,  # Aqui pode permanecer igual
                                subcategoria_municao=subcategoria_municao.nome,  # Atualize aqui para o atributo correto
                                quantidade_municao=quantidade,
                                armeiro=armeiro
                            )

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return redirect('sucesso')

    # Renderiza o template de cautela
    policiais = Policial.objects.all()
    tipos_servico = CautelaDeArmamento.SERVICO_CHOICES
    categorias_servico = Categoria.objects.all()
    subcategoria_armamento = Subcategoria.objects.all()
    categoria_municoes = CategoriaMunicao.objects.all()
    subcategoria_municoes = SubcategoriaMunicao.objects.all()

    # Calcula a quantidade total de munições
    quantidade_total = CautelaDeMunicoes.objects.aggregate(total=Sum('quantidade'))['total']
    if quantidade_total is None:
        quantidade_total = 0

    context = {
        'policiais': policiais,
        'categorias': categorias_servico,
        'tipos_servico': tipos_servico,
        'subcategorias_armamento': subcategoria_armamento,
        'categorias_municoes': categoria_municoes,
        'subcategorias_municoes': subcategoria_municoes,
        'quantidade_total': quantidade_total
    }

    return render(request, 'armamento/cautela.html', context)


############################# AJAX ###################################
######################################################################
# busca todas as subcategorias relacionadas a armamento
def get_subcategorias_armamento(request, categoria_id):
    try:
        categoria = Categoria.objects.get(id=categoria_id)
        subcategorias = categoria.subcategorias_armamento.filter(situacao='disponivel')
    except Categoria.DoesNotExist:
        return JsonResponse({'error': 'Categoria não encontrada'}, status=404)

    # Altere o valor aqui de subcategoria.nome para subcategoria.descricao_completa
    data = [{"id": subcategoria.id, "nome": subcategoria.descricao_completa} for subcategoria in subcategorias]
    return JsonResponse(data, safe=False)

# busca todas as subcategorias relacionadas a munição
def get_subcategorias_municao(request, categoria_id):
    categoria = get_object_or_404(CategoriaMunicao, id=categoria_id)
    subcategorias = categoria.subcategorias.all()
    # Altere "nome" para "descricao_completa" abaixo:
    data = [{"id": subcategoria.id, "nome": subcategoria.nome} for subcategoria in subcategorias]
    return JsonResponse(data, safe=False)

# busca todas as quantidades de munições
def obter_quantidade_total(request, subcategoria_id):
    try:
        subcategoria = get_object_or_404(SubcategoriaMunicao, id=subcategoria_id)
        total_municoes = subcategoria.total_de_municoes
        return JsonResponse({'quantidade': total_municoes})
    except SubcategoriaMunicao.DoesNotExist:
        return JsonResponse({'error': 'Subcategoria não encontrada'}, status=404)
    
def listar_registros_cautela(request):
    # Recupera todos os registros de cautela do banco de dados
    registros = RegistroCautelaCompleta.objects.all()

    # Passa os registros para o template
    context = {
        'registros': registros
    }

    return render(request, 'armamento/descautela.html', context)

######################################################################
######################################################################

# def inventario_equipamentos(request):
#     equipamentos = CautelaDeArmamento.objects.all()
#     context = {'equipamentos': equipamentos}
#     return render(request, 'inventario.html', context)

# def descautelar_armamento(request):
#     if request.method == 'POST':
#         cautela_id = request.POST.get('cautela_id')
#         cautela = get_object_or_404(CautelaDeArmamento, id=cautela_id)
#         cautela.delete()
#         return JsonResponse({'success': True})
#     return JsonResponse({'success': False})

# def listar_armamentos(request):
#     armamentos = CautelaDeArmamento.objects.all()
#     context = {'armamentos': armamentos}
#     return render(request, 'listar_armamentos.html', context)

def cadastrar_pessoa(request):
    if request.method == 'POST':
        nome_completo = request.POST.get('nome_completo')
        nome_guerra = request.POST.get('nome_guerra')
        posto_graduacao = request.POST.get('posto_graduacao')
        matricula = request.POST.get('matricula')
        rgpm = request.POST.get('rgpm')
        lotacao = request.POST.get('lotacao')
        data_nascimento = request.POST.get('data_nascimento')
        cpf = request.POST.get('cpf')

        try:
            # Verificar se já existe um policial com o mesmo CPF
            if Policial.objects.filter(cpf=cpf).exists():
                return render(request, 'armamento/cadastrar_pessoa.html', {
                    'error': 'Um policial com este CPF já está cadastrado.'
                })

            # Criar e salvar o novo policial
            policial = Policial(
                nome_completo=nome_completo,
                nome_guerra=nome_guerra,
                posto_graduacao=posto_graduacao,
                matricula=matricula,
                rgpm=rgpm,
                lotacao=lotacao,
                data_nascimento=data_nascimento,
                cpf=cpf
            )
            policial.save()

            # Redirecionar para a página de sucesso
            return redirect('sucesso')

        except IntegrityError:
            # Renderizar a página com uma mensagem de erro caso ocorra um problema de integridade
            return render(request, 'armamento/cadastrar_pessoa.html', {
                'error': 'Ocorreu um erro ao tentar salvar o policial. Verifique os dados e tente novamente.'
            })

    # Renderizar a página de cadastro se a requisição for GET
    return render(request, 'armamento/cadastrar_pessoa.html')


def sucesso_view(request):
    # Função de visualização de sucesso após o cadastro de uma pessoa
    return render(request, 'armamento\sucesso.html')

#############################################################
###########################################################
def descautelar_sa(request):
    if request.method == 'POST':
        registro_id = request.POST.get('registro_id')
        
        # Buscando o registro no banco de dados com base no ID
        registro = get_object_or_404(RegistroCautelaCompleta, id=registro_id)
        
        # Obter a data e hora atuais para o descautelamento
        data_hora_atual = timezone.now()
        
        # Verificar se a categoria de armamento está presente
        if registro.categoria_armamento:
            # Buscar a subcategoria de armamento associada ao registro
            subcategoria = get_object_or_404(Subcategoria, descricao_completa=registro.subcategoria_armamento)
            
            # Alterar o campo situacao para 'disponivel'
            subcategoria.situacao = 'disponivel'
            subcategoria.save()
            
            # Registrar o descautelamento no novo modelo
            RegistroDescautelamento.objects.create(
                data_hora_cautela=data_hora_atual,
                policial=registro.policial,
                tipo_servico=registro.tipo_servico,
                categoria_armamento=registro.categoria_armamento,
                subcategoria_armamento=registro.subcategoria_armamento,
                situacao_armamento='disponível',  # Situação após descautela
                armeiro=request.user,  # Usuário que realizou o descautelamento
                observacao='Descautela de armamento realizada automaticamente.'
            )
            
            # Imprimir o valor da categoria armamento no terminal
            print(f"Categoria de Armamento: {registro.categoria_armamento}")
            print(f"Subcategoria '{subcategoria.descricao_completa}' alterada para situação: {subcategoria.situacao}")
        
        # Caso a categoria de armamento seja None, trabalhar com munição
        elif registro.categoria_armamento is None and registro.quantidade_municao > 0:
            # Buscar a subcategoria de munição associada ao registro
            subcategoria_municao = get_object_or_404(SubcategoriaMunicao, nome=registro.subcategoria_municao)
            
            # Atualizar o total de munições
            subcategoria_municao.total_de_municoes += registro.quantidade_municao
            subcategoria_municao.save()
            
            # Registrar o descautelamento no novo modelo
            RegistroDescautelamento.objects.create(
                data_hora_cautela=data_hora_atual,
                policial=registro.policial,
                tipo_servico=registro.tipo_servico,
                categoria_municao=registro.categoria_municao,
                subcategoria_municao=registro.subcategoria_municao,
                quantidade_municao=registro.quantidade_municao,
                situacao_armamento='N/A',  # Não se aplica a munições
                armeiro=request.user,  # Usuário que realizou o descautelamento
                observacao='Descautela de munição realizada automaticamente.'
            )
            
            # Imprimir o valor da quantidade de munições no terminal
            print(f"Quantidade de Munição: {registro.quantidade_municao}")
            print(f"Subcategoria de Munição '{subcategoria_municao.nome}' agora tem {subcategoria_municao.total_de_municoes} munições.")
            
        # Após o processo, excluir o registro de cautela completa
        registro.delete()
        print(f"Registro de cautela completa {registro_id} excluído do banco de dados.")
        
        # Retornar uma resposta de sucesso
        return JsonResponse({'status': 'success', 'registro_id': registro_id})
    
    # Caso não seja POST, retornar uma resposta de erro
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'})


# def descautelar_ca(request):
#     if request.method == 'POST':
#         try:
#             # Obter os dados diretamente de request.POST
#             registro_id = request.POST.get('registro_id')
#             situacao_armamento = request.POST.get('situacao')
#             observacao = request.POST.get('observacao', '')

#             # Obter o valor digitado no campo de quantidade de munição
#             quantidade_digitada = int(request.POST.get('quantidade_municao', 0))

#             # Exibir o valor digitado no campo de quantidade de munição no terminal
#             print(f"Quantidade de Munição Digitada pelo Usuário: {quantidade_digitada}")

#             # Obtém o registro específico usando o ID fornecido
#             registro = get_object_or_404(RegistroCautelaCompleta, pk=registro_id)

#             # Verificar se a subcategoria de munição é `None`
#             if registro.subcategoria_municao is None:
#                 # Caso a subcategoria de munição seja None, continuar com o fluxo normal

#                 # Obtém o policial associado ao registro
#                 policial = registro.policial

#                 # Obtém o usuário atual como armeiro descautelante
#                 armeiro_descautela = request.user

#                 # Captura a data e hora atuais para o descautelamento
#                 data_hora_atual = timezone.now()

#                 # Exibir a quantidade de munição original no terminal
#                 print(f"Quantidade Original de Munição no Registro: {registro.quantidade_municao}")

#                 # Cria um novo registro de descautelamento com os dados do registro original e os dados do modal
#                 novo_descautelamento = RegistroDescautelamento.objects.create(
#                     data_hora_cautela=registro.data_hora if hasattr(registro, 'data_hora') else data_hora_atual,
#                     policial=policial,
#                     tipo_servico=registro.tipo_servico,
#                     categoria_armamento=registro.categoria_armamento,
#                     subcategoria_armamento=registro.subcategoria_armamento,
#                     categoria_municao=registro.categoria_municao,
#                     subcategoria_municao=registro.subcategoria_municao,
#                     quantidade_municao=quantidade_digitada,  # Usar o valor digitado
#                     situacao_armamento=situacao_armamento,
#                     observacao=observacao,
#                     armeiro=registro.armeiro,
#                     armeiro_descautela=armeiro_descautela,
#                     data_descautelamento=data_hora_atual.date(),
#                     hora_descautelamento=data_hora_atual.time()
#                 )

#                 # Exibir a quantidade de munição utilizada no descautelamento no terminal
#                 print(f"Quantidade de Munição no Descautelamento: {novo_descautelamento.quantidade_municao}")
#                 print(f"Quantidade de Munição no Descautelamento: {novo_descautelamento.policial}")

#                 # Atualiza o campo `situacao` na tabela `Subcategoria` com o valor selecionado no modal
#                 if registro.subcategoria_armamento:
#                     subcategoria = get_object_or_404(Subcategoria, nome=registro.subcategoria_armamento)
#                     subcategoria.situacao = situacao_armamento
#                     subcategoria.save()

#                     # Exclui o registro de cautela completa após descautela
#                     registro.delete()

#                     # Retorna uma resposta de sucesso
#                     return JsonResponse({'success': True, 'descautelamento_id': novo_descautelamento.id})

#             else:
#                 # Caso a subcategoria de munição não seja None, enviar a quantidade de munição de volta ao modal como limite
#                 quantidade_municao_disponivel = registro.quantidade_municao

#                 # Exibir a quantidade de munição no terminal
#                 print(f"Quantidade de Munição Disponível: {quantidade_municao_disponivel}")

#                 # Calcular a diferença entre a quantidade disponível e a quantidade digitada
#                 quantidade_restante = quantidade_municao_disponivel - quantidade_digitada

#                 # Exibir o valor calculado no terminal
#                 print(f"Quantidade Restante após Descautela: {quantidade_restante}")

#                 # Se a quantidade restante for maior que 0, atualizar no banco de dados
#                 if quantidade_restante >= 0:
#                     # Atualizar o valor de munição disponível no banco de dados
#                     subcategoria_municao = get_object_or_404(SubcategoriaMunicao, nome=registro.subcategoria_municao)
#                     subcategoria_municao.total_de_municoes = subcategoria_municao.total_de_municoes + quantidade_restante
#                     subcategoria_municao.save()

#                     # Exibir a quantidade atualizada no terminal
#                     print(f"Quantidade Atualizada de Munições na Subcategoria: {subcategoria_municao.total_de_municoes}")

#                 # Excluir o registro de cautela completa após o processo
#                 registro.delete()

#                 # Retorna a quantidade de munição como limite para ser usada no modal
#                 return JsonResponse({'success': True, 'limite_municao': quantidade_municao_disponivel, 'quantidade_restante': quantidade_restante})

#         except Exception as e:
#             # Debug: Mostrar o erro no servidor
#             print(f"Erro: {str(e)}")
#             return JsonResponse({'success': False, 'error': str(e)})

#     return JsonResponse({'success': False, 'error': 'Método não suportado'})

# def descautelar_ca(request):
#     if request.method == 'POST':
#         try:
#             # Obter os dados diretamente de request.POST
#             registro_id = request.POST.get('registro_id')
#             situacao_armamento = request.POST.get('situacao')
#             observacao = request.POST.get('observacao', '')

#             # Obter o valor digitado no campo de quantidade de munição
#             quantidade_digitada = int(request.POST.get('quantidade_municao', 0))

#             # Exibir a quantidade de munição digitada no terminal
#             print(f"Quantidade de Munição Digitada pelo Usuário: {quantidade_digitada}")

#             # Obtém o registro específico usando o ID fornecido
#             registro = get_object_or_404(RegistroCautelaCompleta, pk=registro_id)
#             if registro.subcategoria_municao is None:
#                 # Caso a subcategoria de munição seja None, continuar com o fluxo normal

#                 # Obtém o policial associado ao registro
#                 policial = registro.policial

#                 # Obtém o usuário atual como armeiro descautelante
#                 armeiro_descautela = request.user

#                 # Captura a data e hora atuais para o descautelamento
#                 data_hora_atual = timezone.now()
#                 # Verificar se os campos obrigatórios estão presentes no registro
#                 categoria_municao = registro.categoria_municao if registro.categoria_municao else "Categoria Padrão"
#                 subcategoria_municao = registro.subcategoria_municao if registro.subcategoria_municao else "Subcategoria Padrão"

#                 # Exibir a quantidade de munição original no terminal
#                 print(f"Quantidade Original de Munição no Registro: {registro.quantidade_municao}")

#                 # Cria um novo registro de descautelamento
#                 novo_descautelamento = DescautelasCa.objects.create(
#                     data_hora_cautela=registro.data_hora if hasattr(registro, 'data_hora') else timezone.now(),
#                     policial=registro.policial,
#                     tipo_servico=registro.tipo_servico,
#                     categoria_armamento=registro.categoria_armamento,
#                     subcategoria_armamento=registro.subcategoria_armamento,
#                     categoria_municao=categoria_municao,
#                     subcategoria_municao=subcategoria_municao,
#                     quantidade_municao=quantidade_digitada,
#                     situacao_armamento=situacao_armamento,
#                     observacao=observacao,
#                     armeiro=registro.armeiro,
#                     armeiro_descautela=request.user,
#                     data_descautelamento=timezone.now().date(),
#                     hora_descautelamento=timezone.now().time()
#                 )

#                 # Criar uma lista com todos os dados de novo_descautelamento
#                 dados_descautelamento = [
#                     novo_descautelamento.data_hora_cautela,
#                     novo_descautelamento.policial,
#                     novo_descautelamento.tipo_servico,
#                     novo_descautelamento.categoria_armamento,
#                     novo_descautelamento.subcategoria_armamento,
#                     novo_descautelamento.categoria_municao,
#                     novo_descautelamento.subcategoria_municao,
#                     novo_descautelamento.quantidade_municao,
#                     novo_descautelamento.situacao_armamento,
#                     novo_descautelamento.observacao,
#                     novo_descautelamento.armeiro,
#                     novo_descautelamento.armeiro_descautela,
#                     novo_descautelamento.data_descautelamento,
#                     novo_descautelamento.hora_descautelamento
#                 ]

#                 # Imprimir a lista de dados de descautelamento
#                 print("Dados do Novo Registro de Descautelamento:")
#                 print(dados_descautelamento)

#                 # Atualiza o campo `situacao` na tabela `Subcategoria` se necessário
#                 if registro.subcategoria_armamento:
#                     subcategoria = get_object_or_404(Subcategoria, nome=registro.subcategoria_armamento)
#                     subcategoria.situacao = situacao_armamento
#                     subcategoria.save()
#             else:
#                 # Caso a subcategoria de munição não seja None, enviar a quantidade de munição de volta ao modal como limite
#                 quantidade_municao_disponivel = registro.quantidade_municao

#                 # Exibir a quantidade de munição no terminal
#                 print(f"Quantidade de Munição Disponível: {quantidade_municao_disponivel}")

#                 # Definir a categoria e subcategoria de munição corretamente
#                 categoria_municao = registro.categoria_municao if registro.categoria_municao else "Categoria Padrão"
#                 subcategoria_municao = registro.subcategoria_municao if registro.subcategoria_municao else "Subcategoria Padrão"

#                 # Exibir os valores das categorias para verificar se estão corretos
#                 print(f"Categoria de Munição: {categoria_municao}")
#                 print(f"Subcategoria de Munição: {subcategoria_municao}")

#                 # Cria um novo registro de descautelamento
#                 novo_descautelamento = DescautelasCa.objects.create(
#                     data_hora_cautela=registro.data_hora if hasattr(registro, 'data_hora') else timezone.now(),
#                     policial=registro.policial,
#                     tipo_servico=registro.tipo_servico,
#                     categoria_armamento=registro.categoria_armamento,
#                     subcategoria_armamento=registro.subcategoria_armamento,
#                     categoria_municao=categoria_municao,
#                     subcategoria_municao=subcategoria_municao,
#                     quantidade_municao=quantidade_digitada,
#                     situacao_armamento=situacao_armamento,
#                     observacao=observacao,
#                     armeiro=registro.armeiro,
#                     armeiro_descautela=request.user,
#                     data_descautelamento=timezone.now().date(),
#                     hora_descautelamento=timezone.now().time()
#                 )

#                 # Verifica se o objeto foi criado corretamente
#                 print("Novo registro de descautelamento criado com sucesso.")
#                 print(f"ID do novo descautelamento: {novo_descautelamento.id}")

#                 # Criar uma lista com todos os dados de novo_descautelamento
#                 dados_descautelamento = [
#                     novo_descautelamento.data_hora_cautela,
#                     novo_descautelamento.policial,
#                     novo_descautelamento.tipo_servico,
#                     novo_descautelamento.categoria_armamento,
#                     novo_descautelamento.subcategoria_armamento,
#                     novo_descautelamento.categoria_municao,
#                     novo_descautelamento.subcategoria_municao,
#                     novo_descautelamento.quantidade_municao,
#                     novo_descautelamento.situacao_armamento,
#                     novo_descautelamento.observacao,
#                     novo_descautelamento.armeiro,
#                     novo_descautelamento.armeiro_descautela,
#                     novo_descautelamento.data_descautelamento,
#                     novo_descautelamento.hora_descautelamento
#                 ]

#                 # Exibir a lista de dados de descautelamento para depuração
#                 print("Dados do Novo Registro de Descautelamento:")
#                 print(dados_descautelamento)

#                 # Calcular a diferença entre a quantidade disponível e a quantidade digitada
#                 quantidade_restante = quantidade_municao_disponivel - quantidade_digitada

#                 # Exibir o valor calculado no terminal
#                 print(f"Quantidade Restante após Descautela: {quantidade_restante}")

#                 # Se a quantidade restante for maior que 0, atualizar no banco de dados
#                 if quantidade_restante >= 0:
#                     # Atualizar o valor de munição disponível no banco de dados
#                     subcategoria_municao_obj = get_object_or_404(SubcategoriaMunicao, nome=registro.subcategoria_municao)
                    
#                     # Exibir valor atual para depuração
#                     print(f"Total de Munições Antes da Atualização: {subcategoria_municao_obj.total_de_municoes}")

#                     # Verificar se `total_de_municoes` é um número válido
#                     if subcategoria_municao_obj.total_de_municoes is None:
#                         subcategoria_municao_obj.total_de_municoes = 0

#                     # Atualiza a quantidade de munições
#                     subcategoria_municao_obj.total_de_municoes += quantidade_restante
#                     subcategoria_municao_obj.save()

#                     # Exibir a quantidade atualizada no terminal
#                     print(f"Quantidade Atualizada de Munições na Subcategoria: {subcategoria_municao_obj.total_de_municoes}")

#                 # Excluir o registro de cautela completa após o processo
#                 registro.delete()

#                 # Retorna a quantidade de munição como limite para ser usada no modal
#                 return JsonResponse({'success': True, 'limite_municao': quantidade_municao_disponivel, 'quantidade_restante': quantidade_restante})

#         except Exception as e:
#             # Captura e imprime qualquer erro que ocorra
#             print(f"Erro durante a criação do registro de descautelamento: {str(e)}")
#             return JsonResponse({'success': False, 'error': str(e)})




def descautelar_ca(request):
    if request.method == 'POST':
        try:
            # Obter os dados diretamente de request.POST
            registro_id = request.POST.get('registro_id')
            situacao_armamento = request.POST.get('situacao')
            observacao = request.POST.get('observacao', '')
            observacoes_input = request.POST.get('observacoes', '')

            # Obter a quantidade de munição digitada
            quantidade_digitada = int(request.POST.get('quantidade_municao', 0))

            # Exibir a quantidade de munição digitada no terminal
            print(f"Quantidade de Munição Digitada pelo Usuário: {quantidade_digitada}")

            # Obtém o registro específico usando o ID fornecido
            registro = get_object_or_404(RegistroCautelaCompleta, pk=registro_id)
            
            # Caso a subcategoria de munição seja None, continuar com o fluxo normal
            if registro.subcategoria_municao is None:
                policial = registro.policial
                armeiro_descautela = request.user
                data_hora_atual = timezone.now()
                
                categoria_municao = registro.categoria_municao if registro.categoria_municao else "Categoria Padrão"
                subcategoria_municao = registro.subcategoria_municao if registro.subcategoria_municao else "Subcategoria Padrão"

                print(f"Quantidade Original de Munição no Registro: {registro.quantidade_municao}")

                # Criação do novo registro de descautelamento
                novo_descautelamento = DescautelasCa.objects.create(
                    data_hora_cautela=registro.data_hora if hasattr(registro, 'data_hora') else timezone.now(),
                    policial=registro.policial,
                    tipo_servico=registro.tipo_servico,
                    categoria_armamento=registro.categoria_armamento,
                    subcategoria_armamento=registro.subcategoria_armamento,
                    categoria_municao=categoria_municao,
                    subcategoria_municao=subcategoria_municao,
                    quantidade_municao=quantidade_digitada,
                    situacao_armamento=situacao_armamento,
                    observacao=observacao,
                    armeiro=registro.armeiro,
                    armeiro_descautela=request.user,
                    data_descautelamento=timezone.now().date(),
                    hora_descautelamento=timezone.now().time()
                )

                print("Dados do Novo Registro de Descautelamento:")
                print([
                    novo_descautelamento.data_hora_cautela,
                    novo_descautelamento.policial,
                    novo_descautelamento.tipo_servico,
                    novo_descautelamento.categoria_armamento,
                    novo_descautelamento.subcategoria_armamento,
                    novo_descautelamento.categoria_municao,
                    novo_descautelamento.subcategoria_municao,
                    novo_descautelamento.quantidade_municao,
                    novo_descautelamento.situacao_armamento,
                    novo_descautelamento.observacao,
                    novo_descautelamento.armeiro,
                    novo_descautelamento.armeiro_descautela,
                    novo_descautelamento.data_descautelamento,
                    novo_descautelamento.hora_descautelamento
                ])

                if registro.subcategoria_armamento:
                    subcategoria = get_object_or_404(Subcategoria, descricao_completa=registro.subcategoria_armamento)

                    subcategoria.situacao = situacao_armamento
                    subcategoria.save()

                registro.delete()
                return JsonResponse({'success': True, 'message': 'Descautelamento realizado com sucesso.', 'registro_id': registro_id})

            
            else:
                quantidade_municao_disponivel = registro.quantidade_municao
                print(f"Quantidade de Munição Disponível: {quantidade_municao_disponivel}")

                categoria_municao = registro.categoria_municao if registro.categoria_municao else "Categoria Padrão"
                subcategoria_municao = registro.subcategoria_municao if registro.subcategoria_municao else "Subcategoria Padrão"

                print(f"Categoria de Munição: {categoria_municao}")
                print(f"Subcategoria de Munição: {subcategoria_municao}")
                novo_descautelamento = DescautelasCa.objects.create(
                    data_hora_cautela=registro.data_hora if hasattr(registro, 'data_hora') else timezone.now(),
                    policial=registro.policial,
                    tipo_servico=registro.tipo_servico,
                    categoria_armamento=registro.categoria_armamento,
                    subcategoria_armamento=registro.subcategoria_armamento,
                    categoria_municao=categoria_municao,
                    subcategoria_municao=subcategoria_municao,
                    quantidade_municao=quantidade_digitada,
                    situacao_armamento=situacao_armamento,
                    observacao=observacao,
                    observacoes=observacoes_input,  # Adicione esta linha
                    armeiro=registro.armeiro,
                    armeiro_descautela=request.user,
                    data_descautelamento=timezone.now().date(),
                    hora_descautelamento=timezone.now().time()
                )

                print("Novo registro de descautelamento criado com sucesso.")
                print(f"ID do novo descautelamento: {novo_descautelamento.id}")

                quantidade_restante = quantidade_municao_disponivel - quantidade_digitada
                print(f"Quantidade Restante após Descautela: {quantidade_restante}")

                if quantidade_restante >= 0:
                    subcategoria_municao_obj = get_object_or_404(SubcategoriaMunicao, nome=registro.subcategoria_municao)
                    print(f"Total de Munições Antes da Atualização: {subcategoria_municao_obj.total_de_municoes}")

                    if subcategoria_municao_obj.total_de_municoes is None:
                        subcategoria_municao_obj.total_de_municoes = 0

                    subcategoria_municao_obj.total_de_municoes += quantidade_restante
                    subcategoria_municao_obj.save()

                    print(f"Quantidade Atualizada de Munições na Subcategoria: {subcategoria_municao_obj.total_de_municoes}")

                registro.delete()
                return JsonResponse({'success': True, 'limite_municao': quantidade_municao_disponivel, 'quantidade_restante': quantidade_restante})

        except Exception as e:
            print(f"Erro durante a criação do registro de descautelamento: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)})
    
    # Caso o método não seja POST, renderize uma página de erro ou mensagem adequada
    return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)



def descautelar_municao_ca(request):
    if request.method == 'POST':
        print("Função descautelar_municao_ca foi chamada")  # Verifique se isto aparece no terminal
        # Seus dados aqui...
        registro_id = request.POST.get('registro_id')
        quantidade_municao = request.POST.get('quantidade_municao')
        situacao = request.POST.get('situacao')
        quantidade_atual = request.POST.get('quantidade_atual')

        # Exibindo os dados no terminal
        print(f"Registro ID: {registro_id}")
        print(f"Quantidade de Munição: {quantidade_municao}")
        print(f"Situação do Armamento: {situacao}")
        print(f"Quantidade Atual: {quantidade_atual}")

        # Retornar uma resposta de sucesso como JSON
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'message': 'Método inválido'}, status=400)

# def descautelar_ca(request):
#     # Verificar se é uma requisição POST
#     if request.method == "POST":
#         print("Recebido POST para descautela")
#         registro_id = request.POST.get('registro_id', '').strip()
#         situacao = request.POST.get('situacao', '').strip()
#         quantidade = request.POST.get('quantidade_municao', '').strip()
#         observacao = request.POST.get('observacao', '').strip()

#         # Exibir os valores recebidos
#         print(f"Valores recebidos - registro_id: {registro_id}, situacao: {situacao}, quantidade: {quantidade}, observacao: {observacao}")

#         # Validar se o ID do registro foi fornecido
#         if not registro_id:
#             print("ID do registro não fornecido!")
#             return HttpResponseBadRequest("O ID do registro não pode estar vazio.")

#         try:
#             # Tentar converter o ID para um inteiro
#             registro_id = int(registro_id)
#         except ValueError:
#             print("ID inválido. Valor recebido: ", registro_id)
#             return JsonResponse({'error': 'ID inválido. Insira um número válido.'}, status=400)

#         # Recuperar o registro de cautela completa
#         try:
#             registro = get_object_or_404(RegistroCautelaCompleta, id=registro_id)
#             print("Registro encontrado:", registro)
#         except Exception as e:
#             print("Erro ao recuperar registro:", e)
#             return JsonResponse({'error': f'Registro não encontrado. Detalhe: {str(e)}'}, status=404)

#         # Atualizar situação do armamento
#         if registro.categoria_armamento and registro.subcategoria_armamento:
#             try:
#                 subcategoria_armamento = get_object_or_404(Subcategoria, nome=registro.subcategoria_armamento)
#                 print("Subcategoria de armamento encontrada:", subcategoria_armamento)
#                 if situacao:
#                     subcategoria_armamento.situacao = situacao
#                     subcategoria_armamento.save()
#                     print("Situação do armamento atualizada para:", situacao)
#             except Exception as e:
#                 print("Erro ao atualizar a situação do armamento:", e)
#                 return JsonResponse({'error': f'Erro ao atualizar situação do armamento: {str(e)}'}, status=400)

#         # Caso tenha munição associada, atualizar a quantidade
#         nova_quantidade = 0
#         if registro.categoria_municao and registro.subcategoria_municao:
#             try:
#                 nova_quantidade = int(quantidade)
#                 print("Nova quantidade de munição:", nova_quantidade)
#             except ValueError:
#                 print("Quantidade de munição inválida:", quantidade)
#                 return HttpResponseBadRequest("Quantidade de munição inválida. Insira um valor numérico.")

#             # Lógica de descautelamento de munição
#             try:
#                 quantidade_total_disponivel = registro.quantidade_municao
#                 if nova_quantidade <= 0:
#                     return HttpResponseBadRequest("A quantidade deve ser maior que zero.")
#                 elif nova_quantidade > quantidade_total_disponivel:
#                     return HttpResponseBadRequest(
#                         f"A quantidade solicitada ({nova_quantidade}) excede o total disponível ({quantidade_total_disponivel})."
#                     )

#                 registro.quantidade_municao -= nova_quantidade
#                 registro_completo_excluido = registro.quantidade_municao == 0
#                 if registro_completo_excluido:
#                     registro.delete()
#                 else:
#                     registro.save()
#                 print("Munição atualizada. Nova quantidade no registro:", registro.quantidade_municao)
#             except Exception as e:
#                 print("Erro ao processar a descautela de munição:", e)
#                 return JsonResponse({'error': f'Erro ao processar a descautela de munição: {str(e)}'}, status=400)

#         # Registrar descautelamento
#         try:
#             RegistroDescautelamento.objects.create(
#                 data_hora_cautela=registro.data_hora,
#                 policial=registro.policial,
#                 tipo_servico=registro.tipo_servico,
#                 categoria_armamento=registro.categoria_armamento,
#                 subcategoria_armamento=registro.subcategoria_armamento,
#                 categoria_municao=registro.categoria_municao,
#                 subcategoria_municao=registro.subcategoria_municao,
#                 quantidade_municao=nova_quantidade,
#                 armeiro=registro.armeiro,
#                 data_descautelamento=timezone.now().date(),
#                 hora_descautelamento=timezone.now().time(),
#                 observacao=observacao,
#             )
#             print("Registro de descautelamento criado com sucesso.")
#         except Exception as e:
#             print("Erro ao registrar descautelamento:", e)
#             return JsonResponse({'error': f'Erro ao registrar descautelamento: {str(e)}'}, status=400)

#         return JsonResponse({'success': True, 'registro_completo_excluido': registro_completo_excluido})
#     else:
#         print("Método não permitido. Apenas POST é aceito.")
#         return JsonResponse({'error': 'Método não permitido'}, status=405)





    # View para exibir itens disponíveis
def itens_disponiveis(request):
    # Filtra todos os itens que estão marcados como 'disponível'
    itens_disponiveis = Subcategoria.objects.filter(situacao='disponivel')
    
    # Itera pelos itens disponíveis e imprime seus detalhes no terminal
    for item in itens_disponiveis:
        print(f"Nome: {item.descricao_completa}")
        print(f"Marca: {item.marca}")
        print(f"Modelo: {item.modelo}")
        print(f"Calibre: {item.cal}")
        print(f"Nº Arma: {item.num_arma}")
        print(f"Nº PMMA: {item.num_pmma}")
        print(f"Localização: {item.localizacao}")
        print(f"Estado de Conservação: {item.estado_conservacao}")
        print(f"Observação: {item.observacao}")
        print("----------------------------------------")
    
    return render(request, 'cautelaarmamento/templates/catalogo_de_equipamento/itens_disponiveis.html', {
        'itens_disponiveis': itens_disponiveis
    })