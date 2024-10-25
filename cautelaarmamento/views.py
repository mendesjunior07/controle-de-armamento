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

from .models import CautelaDeArmamento, PassagemDeServico, User
from django.shortcuts import render
import os
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models import Sum
from django.db import transaction
from django.core.paginator import Paginator
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.db import IntegrityError
from django.utils.html import strip_tags
import json
from .models import PassagemDeServico
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
    PassagemDeServico
)


def index(request):
    return render(request, 'cautelaarmamento/index.html')


def cautela_de_armamento_view(request):

    ############## PROCESSAMENTO DE REQUISIÇÃO POST ##########

    if request.method == 'POST':
        # Obtém os dados do formulário
        policial_id = request.POST.get('policial')
        tipo_servico = request.POST.get('tipo_servico')
        categorias_armamento = request.POST.getlist('categorias[]')
        subcategorias_armamento = request.POST.getlist('subcategorias[]')
        categorias_municao = request.POST.getlist('categoria_municoes[]')
        subcategorias_municao = request.POST.getlist('subcategoria_municoes[]')
        quantidades_municao = request.POST.getlist('quantidade[]')

############## OBTENÇÃO E VERIFICAÇÃO DOS DADOS ##########

        # # Busca o policial pelo ID
        # policial = get_object_or_404(Policial, id=policial_id)
        # # Certifique-se de que este é o nome correto no seu modelo
        # print(f"Policial Selecionado: {policial.nome_completo}")
        # print(f"Tipo de Serviço: {tipo_servico}")

        # # Imprime as categorias e subcategorias de armamento com nomes
        # print("Armamento Selecionado:")
        # for i in range(len(categorias_armamento)):
        #     categoria_armamento = get_object_or_404(
        #         Categoria, id=categorias_armamento[i])
        #     subcategoria_armamento = get_object_or_404(
        #         Subcategoria, id=subcategorias_armamento[i])
        #     print(f"Categoria de Armamento: {categoria_armamento.nome}")
        #     print(
        #         f"Subcategoria de Armamento: {subcategoria_armamento.descricao_completa}")

        # # Verifica se há categorias de munição válidas e imprime
        # # Verifica se não está vazio
        # if categorias_municao and subcategorias_municao and categorias_municao[0]:
        #     print("Munição Selecionada:")
        #     for i in range(len(categorias_municao)):
        #         # Se não estiver vazio
        #         if categorias_municao[i] and subcategorias_municao[i]:
        #             categoria_municao = get_object_or_404(
        #                 CategoriaMunicao, id=categorias_municao[i])
        #             subcategoria_municao = get_object_or_404(
        #                 SubcategoriaMunicao, id=subcategorias_municao[i])
        #             quantidade = quantidades_municao[i]
        #             print(f"Categoria de Munição: {categoria_municao.nome}")
        #             print(
        #                 f"Subcategoria de Munição: {subcategoria_municao.nome}")
        #             print(f"Quantidade de Munição: {quantidade}")
        # else:
        #     print("Nenhuma Munição Selecionada")

############## VALIDAÇÃO DOS CAMPOS OBRIGATÓRIOS ##########

        # Verifica se os campos obrigatórios foram preenchidos
        if not policial_id or not tipo_servico:
            return JsonResponse({'error': 'Os campos Nome do Policial e Tipo de Serviço são obrigatórios.'}, status=400)

        policial = get_object_or_404(Policial, id=policial_id)
        armeiro = request.user

############## PROCESSAMENTO DO ARMAMENTO ##########

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
                            categoria_armamento = get_object_or_404(
                                Categoria, id=categoria_id)
                            subcategoria_armamento = get_object_or_404(
                                Subcategoria, id=subcategoria_id)

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

############## PROCESSAMENTO DA MUNIÇÃO ##########

                if categorias_municao and subcategorias_municao and quantidades_municao:
                    for i in range(len(categorias_municao)):
                        categoria_id = categorias_municao[i]
                        subcategoria_id = subcategorias_municao[i]
                        quantidade = quantidades_municao[i]
                        if categoria_id and subcategoria_id and quantidade:
                            categoria_municao = get_object_or_404(
                                CategoriaMunicao, id=categoria_id)
                            subcategoria_municao = get_object_or_404(
                                SubcategoriaMunicao, id=subcategoria_id)

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
                                # Atualize aqui para o atributo correto
                                subcategoria_municao=subcategoria_municao.nome,
                                quantidade_municao=quantidade,
                                armeiro=armeiro
                            )

############## GERAÇÃO DE RELATÓRIO E ENVIO DE EMAIL ##########

        # Após o processamento bem-sucedido, gere o relatório e envie o email
            try:
                # Obtenha a data e hora atual
                data_hora_atual = timezone.now()
                with transaction.atomic():
                    # Seu código de processamento de armamento e munição...

                    # Aqui você gera o relatório para o email
                    email_subject = 'Relatório de Cautela de Armamento e Munição'
                    email_recipients = ['mendesjunior2007@hotmail.com']

                    # Crie o conteúdo do email com base nos dados processados
                    # Crie o conteúdo do email com base nos dados processados
                    context = {
                        'policial': policial.nome_completo,
                        'tipo_servico': tipo_servico,
                        'armamentos': [
                            {
                                'categoria': get_object_or_404(Categoria, id=categorias_armamento[i]).nome,
                                'subcategoria': get_object_or_404(Subcategoria, id=subcategorias_armamento[i]).descricao_completa
                            }
                            for i in range(len(categorias_armamento))
                        ],
                        'municoes': [
                            {
                                'categoria': get_object_or_404(CategoriaMunicao, id=categorias_municao[i]).nome,
                                'subcategoria': get_object_or_404(SubcategoriaMunicao, id=subcategorias_municao[i]).nome,
                                'quantidade': quantidades_municao[i]
                            }
                            # Verifica se existem munições
                            for i in range(len(categorias_municao)) if categorias_municao[i] and subcategorias_municao[i]
                        ],
                        # Formata a data e hora
                        'data_hora': data_hora_atual.strftime('%d/%m/%Y %H:%M'),
                        # Obtém o nome completo do usuário logado
                        'usuario': request.user.get_full_name()
                    }

                    # Use um template HTML para o email
                    html_message = render_to_string(
                        'email/relatorio_cautela.html', context)
                    plain_message = strip_tags(html_message)

                    # Envie o email
                    send_mail(
                        subject=email_subject,
                        message=plain_message,
                        from_email='seuemail@gmail.com',
                        recipient_list=email_recipients,
                        html_message=html_message,
                        fail_silently=False,
                    )

############## EXCEÇÃO GERAL E REDIRECIONAMENTO ##########

            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

            return redirect('sucesso')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return redirect('sucesso')

############## EXIBIÇÃO DO FORMULÁRIO E CONTEXTO ##########

    # Renderiza o template de cautela
    policiais = Policial.objects.all()
    tipos_servico = CautelaDeArmamento.SERVICO_CHOICES
    categorias_servico = Categoria.objects.all()
    subcategoria_armamento = Subcategoria.objects.all()
    categoria_municoes = CategoriaMunicao.objects.all()
    subcategoria_municoes = SubcategoriaMunicao.objects.all()

    # Calcula a quantidade total de munições
    quantidade_total = CautelaDeMunicoes.objects.aggregate(
        total=Sum('quantidade'))['total']
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
        subcategorias = categoria.subcategorias_armamento.filter(
            situacao='disponivel')
    except Categoria.DoesNotExist:
        return JsonResponse({'error': 'Categoria não encontrada'}, status=404)

    # Altere o valor aqui de subcategoria.nome para subcategoria.descricao_completa
    data = [{"id": subcategoria.id, "nome": subcategoria.descricao_completa}
            for subcategoria in subcategorias]
    return JsonResponse(data, safe=False)

# busca todas as subcategorias relacionadas a munição


def get_subcategorias_municao(request, categoria_id):
    categoria = get_object_or_404(CategoriaMunicao, id=categoria_id)
    subcategorias = categoria.subcategorias.all()
    # Altere "nome" para "descricao_completa" abaixo:
    data = [{"id": subcategoria.id, "nome": subcategoria.nome}
            for subcategoria in subcategorias]
    return JsonResponse(data, safe=False)

# busca todas as quantidades de munições


def obter_quantidade_total(request, subcategoria_id):
    try:
        subcategoria = get_object_or_404(
            SubcategoriaMunicao, id=subcategoria_id)
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
            subcategorias = Subcategoria.objects.filter(
                descricao_completa=registro.subcategoria_armamento)

            if subcategorias.exists():
                # Se houver múltiplas subcategorias, pegar a primeira
                subcategoria = subcategorias.first()

                # Alterar o campo situacao para 'disponivel'
                subcategoria.situacao = 'disponivel'
                subcategoria.save()

                # Registrar o descautelamento no novo modelo
                RegistroDescautelamento.objects.create(
                    data_hora_cautela=data_hora_atual,
                    policial=registro.policial,  # Atribuindo a instância do policial
                    tipo_servico=registro.tipo_servico,
                    categoria_armamento=registro.categoria_armamento,
                    subcategoria_armamento=registro.subcategoria_armamento,
                    situacao_armamento='disponível',  # Situação após descautela
                    armeiro=request.user,  # Usuário que realizou o descautelamento
                    observacao='Descautela de armamento realizada automaticamente.'
                )

                # Imprimir o valor da categoria armamento no terminal
                print(
                    f"Categoria de Armamento: {registro.categoria_armamento}")
                print(
                    f"Subcategoria '{subcategoria.descricao_completa}' alterada para situação: {subcategoria.situacao}")
            else:
                # Se não houver subcategorias, lidar com a situação (opcional)
                print("Nenhuma subcategoria encontrada.")

        # Caso a categoria de armamento seja None, trabalhar com munição
        elif registro.categoria_armamento is None and registro.quantidade_municao > 0:
            # Buscar a subcategoria de munição associada ao registro
            subcategoria_municao = get_object_or_404(
                SubcategoriaMunicao, nome=registro.subcategoria_municao)

            # Atualizar o total de munições
            subcategoria_municao.total_de_municoes += registro.quantidade_municao
            subcategoria_municao.save()

            # Registrar o descautelamento no novo modelo
            RegistroDescautelamento.objects.create(
                data_hora_cautela=data_hora_atual,
                policial=registro.policial,  # Atribuindo a instância do policial
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
            print(
                f"Subcategoria de Munição '{subcategoria_municao.nome}' agora tem {subcategoria_municao.total_de_municoes} munições.")

        # Após o processo, excluir o registro de cautela completa
        registro.delete()
        print(
            f"Registro de cautela completa {registro_id} excluído do banco de dados.")

        # Retornar uma resposta de sucesso
        return JsonResponse({'status': 'success', 'registro_id': registro_id})

    # Caso não seja POST, retornar uma resposta de erro
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'})


def descautelar_ca(request):
    if request.method == 'POST':
        try:
            # Obter os dados diretamente de request.POST
            registro_id = request.POST.get('registro_id')
            situacao_armamento = request.POST.get('situacao')
            observacao = request.POST.get('observacao', '')
            observacoes_input = request.POST.get('observacoes', '')

            # Obter a quantidade de munição digitada
            quantidade_digitada = int(
                request.POST.get('quantidade_municao', 0))

            # Exibir a quantidade de munição digitada no terminal
            print(
                f"Quantidade de Munição Digitada pelo Usuário: {quantidade_digitada}")

            # Obtém o registro específico usando o ID fornecido
            registro = get_object_or_404(
                RegistroCautelaCompleta, pk=registro_id)

            # Caso a subcategoria de munição seja None, continuar com o fluxo normal
            if registro.subcategoria_municao is None:
                policial = registro.policial
                armeiro_descautela = request.user
                data_hora_atual = timezone.now()

                categoria_municao = registro.categoria_municao if registro.categoria_municao else "Categoria Padrão"
                subcategoria_municao = registro.subcategoria_municao if registro.subcategoria_municao else "Subcategoria Padrão"

                print(
                    f"Quantidade Original de Munição no Registro: {registro.quantidade_municao}")

                # Criação do novo registro de descautelamento
                novo_descautelamento = DescautelasCa.objects.create(
                    data_hora_cautela=registro.data_hora if hasattr(
                        registro, 'data_hora') else timezone.now(),
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
                    subcategoria = get_object_or_404(
                        Subcategoria, descricao_completa=registro.subcategoria_armamento)

                    subcategoria.situacao = situacao_armamento
                    subcategoria.save()

                registro.delete()
                return JsonResponse({'success': True, 'message': 'Descautelamento realizado com sucesso.', 'registro_id': registro_id})

            else:
                quantidade_municao_disponivel = registro.quantidade_municao
                print(
                    f"Quantidade de Munição Disponível: {quantidade_municao_disponivel}")

                categoria_municao = registro.categoria_municao if registro.categoria_municao else "Categoria Padrão"
                subcategoria_municao = registro.subcategoria_municao if registro.subcategoria_municao else "Subcategoria Padrão"

                print(f"Categoria de Munição: {categoria_municao}")
                print(f"Subcategoria de Munição: {subcategoria_municao}")
                novo_descautelamento = DescautelasCa.objects.create(
                    data_hora_cautela=registro.data_hora if hasattr(
                        registro, 'data_hora') else timezone.now(),
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
                print(
                    f"Quantidade Restante após Descautela: {quantidade_restante}")

                if quantidade_restante >= 0:
                    subcategoria_municao_obj = get_object_or_404(
                        SubcategoriaMunicao, nome=registro.subcategoria_municao)
                    print(
                        f"Total de Munições Antes da Atualização: {subcategoria_municao_obj.total_de_municoes}")

                    if subcategoria_municao_obj.total_de_municoes is None:
                        subcategoria_municao_obj.total_de_municoes = 0

                    subcategoria_municao_obj.total_de_municoes += quantidade_restante
                    subcategoria_municao_obj.save()

                    print(
                        f"Quantidade Atualizada de Munições na Subcategoria: {subcategoria_municao_obj.total_de_municoes}")

                registro.delete()
                return JsonResponse({'success': True, 'limite_municao': quantidade_municao_disponivel, 'quantidade_restante': quantidade_restante})

        except Exception as e:
            print(
                f"Erro durante a criação do registro de descautelamento: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)})

    # Caso o método não seja POST, renderize uma página de erro ou mensagem adequada
    return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)


def descautelar_municao_ca(request):
    if request.method == 'POST':
        # Verifique se isto aparece no terminal
        print("Função descautelar_municao_ca foi chamada")
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


def itens_disponiveis(request):
    # Filtra todos os itens que estão marcados como 'disponível'
    itens_disponiveis = Subcategoria.objects.filter(situacao='disponivel')

    # Agrupa os itens por categoria
    itens_por_categoria = {}
    for item in itens_disponiveis:
        # Assumindo que 'categoria' é um campo relacionado ao modelo Categoria
        categoria = item.categoria
        if categoria not in itens_por_categoria:
            itens_por_categoria[categoria] = []
        itens_por_categoria[categoria].append(item)

    # Imprime detalhes dos itens no terminal
    for categoria, itens in itens_por_categoria.items():
        print(f"Categoria: {categoria}")
        for item in itens:
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
        'itens_por_categoria': itens_por_categoria
    })


def listar_inventario_equipamentos(request):
    # Filtra todos os itens disponíveis, ordenando-os por categoria
    itens_disponiveis = Subcategoria.objects.all().order_by('categoria')

    # Debug: Imprime os detalhes dos itens no terminal, organizados por categoria
    for item in itens_disponiveis:
        print(f"Categoria: {item.categoria}")
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

    # Renderiza o template com a lista de itens disponíveis organizados por categoria
    return render(request, 'cautelaarmamento/templates/catalogo_de_equipamento/inventario_equipamentos.html', {
        'itens_disponiveis': itens_disponiveis,
    })

#############################################################
########## 1. Função Principal: registrar_passagem ##########
#############################################################


def registrar_passagem(request):

########## 2. Obtenção dos Dados do Formulário ##########
    # 2.1. Verificação do Método HTTP

    if request.method == 'POST':

        # 2.2. Coleta dos Dados do Formulário

        registro_cautela_id = request.POST.get('registro_cautela_id')
        data_inicio_str = request.POST.get('dataInicio')
        nome_substituto = request.POST.get('nomeSubstituto')
        observacoes = request.POST.get('observacoes')

########## 3. Tratamento de Erros na Conversão de Data ##########
# 3.1. Bloco try-except para Evitar Erros

        try:
            # Converter a data de início
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d')
        except (ValueError, TypeError):
            return render(request, 'passagem_de_servico/registrar_passagem.html', {
                'error': 'Data de início inválida',
                'registro_cautela': registro_cautela_id,
                'usuarios': User.objects.all(),
                'dataInicio': data_inicio_str,
                'nomeSubstituto': nome_substituto,
                'observacoes': observacoes,
                'registros': PassagemDeServico.objects.all()
            })

########## 4. Definição da Data de Fim ##########

        data_fim = timezone.now().date()

########## 5. Filtragem de Cautelas ##########
# 5.1. Consulta ao Banco de Dados

        cautelas = CautelaDeArmamento.objects.filter(
            hora_cautela__range=(data_inicio, data_fim),
            armeiro_id=request.user.id
        )

        descautelas = RegistroDescautelamento.objects.filter(
            hora_descautelamento__range=(data_inicio, data_fim),
            armeiro_id=request.user.id
        )

########## 6. Criação e Salvamento da Passagem de Serviço ##########
# 6.1. Criação da Passagem de Serviço

        passagem = PassagemDeServico(
            registro_cautela_id=registro_cautela_id,
            data_inicio=data_inicio,
            data_fim=data_fim,
            nome_substituto=nome_substituto,
            observacoes=observacoes,
            usuario=request.user
        )

# 6.2. Salvamento no Banco de Dados

        passagem.save()

########## 7. Geração de Relatório HTML ##########
# 7.1. Geração do Conteúdo HTML a Partir do Template

        html_content = render_to_string('passagem_de_servico/relatorio.html', {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'nome_substituto': nome_substituto,
            'observacoes': observacoes,
            'cautelas': cautelas,
            'descautelas': descautelas,
            'usuario': request.user
        })

# 7.2. Criação do Diretório de Relatórios

        relatorio_dir = 'relatorios'
        if not os.path.exists(relatorio_dir):
            os.makedirs(relatorio_dir)  # Cria o diretório se não existir

# 7.3. Salvamento do Relatório HTML em Arquivo

        file_path = os.path.join(
            relatorio_dir, f'relatorio_passagem_{passagem.id}.html')
        with open(file_path, 'w') as file:
            file.write(html_content)

########## 8. Redirecionamento para a Página de Sucesso ##########
# 8.1. Renderização da Página de Sucesso

        return render(request, 'passagem_de_servico/sucesso.html', {'relatorio_path': file_path})

    else:

        ########## 9. Manipulação para Requisições GET ##########
        # 9.1. Obtenção de Usuários e Registros

        usuarios = User.objects.all()
        registros = PassagemDeServico.objects.all()

# 9.2. Configuração do Paginador

        paginator = Paginator(registros, 7)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

# 9.3. Renderização da Página Inicial

        return render(request, 'passagem_de_servico/registrar_passagem.html', {
            'registro_cautela': None,
            'usuarios': usuarios,
            'dataInicio': '',
            'nomeSubstituto': '',
            'observacoes': '',
            'page_obj': page_obj
        })


def listar_cautelas(request):
    # Obtém todas as instâncias de CautelaDeArmamento do banco de dados
    cautelas = CautelaDeArmamento.objects.all()

    # Renderiza os dados no template
    return render(request, 'passagem_de_servico/listar_amas_cauteladas.html', {'cautelas': cautelas})
