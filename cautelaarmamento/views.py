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
import json
from django.utils import timezone
from .models import (
    Categoria, 
    CautelaDeArmamento, 
    Subcategoria, 
    Policial, 
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
                                categoria_armamento=categoria_armamento.nome,
                                subcategoria_armamento=subcategoria_armamento.nome,
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

                            # Registro na nova model com todos os detalhes para cada linha
                            RegistroCautelaCompleta.objects.create(
                                policial=policial,
                                tipo_servico=tipo_servico,
                                categoria_armamento=None,
                                subcategoria_armamento=None,
                                categoria_municao=categoria_municao.nome,
                                subcategoria_municao=subcategoria_municao.nome,
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
    
    data = [{"id": subcategoria.id, "nome": subcategoria.nome} for subcategoria in subcategorias]
    return JsonResponse(data, safe=False)

# busca todas as subcategorias relacionadas a munição

def get_subcategorias_municao(request, categoria_id):
    categoria = get_object_or_404(CategoriaMunicao, id=categoria_id)
    subcategorias = categoria.subcategorias.all()
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
        matricula = request.POST.get('matricula')
        # Lógica de salvamento do policial
        return redirect('sucesso_cadastro')
    return render(request, 'cadastrar_pessoa.html')


def sucesso_view(request):
    # Função de visualização de sucesso após o cadastro de uma pessoa
    return render(request, 'armamento\sucesso.html')

#############################################################
###########################################################

def descautelar_sa(request):
    if request.method == "POST":
        registro_id = request.POST.get('registro_id')
        registro = get_object_or_404(RegistroCautelaCompleta, id=registro_id)

        try:
            # Verifica se há armamentos cautelados
            if registro.categoria_armamento and registro.subcategoria_armamento:
                subcategoria_armamento = get_object_or_404(Subcategoria, nome=registro.subcategoria_armamento)
                subcategoria_armamento.situacao = 'disponivel'
                subcategoria_armamento.save()

            # Verifica se há munições cauteladas
            if registro.categoria_municao and registro.subcategoria_municao:
                subcategoria_municao = get_object_or_404(SubcategoriaMunicao, nome=registro.subcategoria_municao)
                
                # Retorna a quantidade ao estoque
                if registro.quantidade_municao > 0:
                    subcategoria_municao.total_de_municoes += registro.quantidade_municao
                    subcategoria_municao.save()

            # Registra o descautelamento
            RegistroDescautelamento.objects.create(
                data_hora_cautela=registro.data_hora,
                policial=registro.policial,
                tipo_servico=registro.tipo_servico,
                categoria_armamento=registro.categoria_armamento,
                subcategoria_armamento=registro.subcategoria_armamento,
                categoria_municao=registro.categoria_municao,
                subcategoria_municao=registro.subcategoria_municao,
                quantidade_municao=registro.quantidade_municao,
                armeiro=registro.armeiro,
                data_descautelamento=timezone.now().date(),
                hora_descautelamento=timezone.now().time(),
            )

            # Exclui o registro de cautela após o descautelamento
            registro.delete()

            # Resposta de sucesso como JSON
            return JsonResponse({'success': True})

        except Exception as e:
            # Retorna erro com JSON
            return JsonResponse({'success': False, 'message': f'Erro ao descautelar: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

# def descautelar_ca(request):
#     if request.method == "POST":
#         # Captura o ID do registro e outras informações do POST
#         registro_id = request.POST.get('registro_id', '').strip()
#         situacao = request.POST.get('situacao', '').strip()
#         quantidade = request.POST.get('quantidade', '').strip()
#         observacao = request.POST.get('observacao', '').strip()

#         # Verifica se o ID do registro foi fornecido
#         if not registro_id:
#             return HttpResponseBadRequest("O ID do registro não pode estar vazio.")

#         try:
#             # Tenta converter o registro_id para inteiro
#             registro_id = int(registro_id)
#         except ValueError:
#             return HttpResponseBadRequest("ID inválido.")

#         # Recupera o registro de cautela ou retorna erro 404
#         registro = get_object_or_404(RegistroCautelaCompleta, id=registro_id)

#         # Verifica se há armamento associado ao registro e atualiza a situação
#         if registro.categoria_armamento and registro.subcategoria_armamento:
#             subcategoria_armamento = get_object_or_404(Subcategoria, nome=registro.subcategoria_armamento)
#             if situacao:
#                 subcategoria_armamento.situacao = situacao
#                 subcategoria_armamento.save()

#         # Verifica se há munições associadas e atualiza a quantidade
#         if registro.categoria_municao and registro.subcategoria_municao:
#             subcategoria_municao = get_object_or_404(SubcategoriaMunicao, nome=registro.subcategoria_municao)

#             try:
#                 nova_quantidade = int(quantidade)
#             except ValueError:
#                 return HttpResponseBadRequest("Quantidade de munição inválida.")

#             # Verifica se a quantidade de munição é válida e não excede o disponível
#             if nova_quantidade <= 0:
#                 return HttpResponseBadRequest("A quantidade deve ser maior que zero.")
#             elif nova_quantidade > subcategoria_municao.total_de_municoes:
#                 return HttpResponseBadRequest("A quantidade solicitada excede o total disponível.")

#             # Atualiza o total de munições após descautela
#             subcategoria_municao.total_de_municoes -= nova_quantidade
#             subcategoria_municao.save()

#         # Registra o descautelamento no banco de dados
#         RegistroDescautelamento.objects.create(
#             data_hora_cautela=registro.data_hora,
#             policial=registro.policial,
#             tipo_servico=registro.tipo_servico,
#             categoria_armamento=registro.categoria_armamento,
#             subcategoria_armamento=registro.subcategoria_armamento,
#             categoria_municao=registro.categoria_municao,
#             subcategoria_municao=registro.subcategoria_municao,
#             quantidade_municao=nova_quantidade,
#             armeiro=registro.armeiro,
#             data_descautelamento=timezone.now().date(),
#             hora_descautelamento=timezone.now().time(),
#             observacao=observacao,  # Adiciona observação ao registro de descautelamento
#         )

#         # Exclui o registro de cautela original
#         registro.delete()

#         return JsonResponse({'success': True})

#     # Retorna erro se o método não for POST
#     return JsonResponse({'error': 'Método não permitido'}, status=405)

def descautelar_ca(request):
    if request.method == 'POST':
        # Verifica se o ID do registro foi enviado
        registro_id = request.POST.get('registro_id')
        if not registro_id:
            return JsonResponse({'error': 'ID do registro não foi fornecido.'}, status=400)

        # Verifica se a nova situação foi enviada
        nova_situacao = request.POST.get('situacao')
        if not nova_situacao:
            return JsonResponse({'error': 'A nova situação não foi fornecida.'}, status=400)

        # Captura as observações do modal
        observacao = request.POST.get('observacao', '')  # Observação pode estar vazia
        
        # Verifica se a quantidade de munição foi enviada, se não, atribui 0
        quantidade_descautela = request.POST.get("quantidade_municao", "0")  # Se não enviada, define como "0"

        try:
            # Converte a quantidade de munição para um inteiro
            quantidade_descautela = int(quantidade_descautela)
        except ValueError:
            return JsonResponse({'error': 'Quantidade de munição inválida.'}, status=400)

        try:
            # Obter o registro do banco de dados de RegistroCautelaCompleta
            registro = get_object_or_404(RegistroCautelaCompleta, id=registro_id)

            # Atualiza a situação do armamento
            if registro.categoria_armamento and registro.subcategoria_armamento:
                subcategoria = get_object_or_404(Subcategoria, nome=registro.subcategoria_armamento)
                subcategoria.situacao = nova_situacao
                subcategoria.save()

            # Verifica se há munição cautelada e processa
            if registro.categoria_municao and registro.subcategoria_municao:
                # Buscar pela subcategoria de munição e o policial para garantir que está acessando o item correto
                cautela = get_object_or_404(
                    CautelaDeMunicoes,
                    policial=registro.policial,
                    categoria__nome=registro.categoria_municao,
                    subcategoria__nome=registro.subcategoria_municao
                )
                # Atualiza a quantidade de munição
                nova_quantidade = cautela.quantidade + quantidade_descautela
                cautela.quantidade = nova_quantidade
                cautela.save()

            # Registrar o descautelamento no banco de dados com as observações
            RegistroDescautelamento.objects.create(
                data_hora_cautela=registro.data_hora,
                policial=registro.policial,
                tipo_servico=registro.tipo_servico,
                categoria_armamento=registro.categoria_armamento,
                subcategoria_armamento=registro.subcategoria_armamento,
                quantidade_municao=quantidade_descautela,  # Usamos a quantidade descautelada aqui
                situacao_armamento=nova_situacao,
                observacao=observacao,  # Salva as observações do modal
                armeiro=registro.armeiro,
                data_descautelamento=timezone.now().date(),
                hora_descautelamento=timezone.now().time(),
                armeiro_descautela=request.user  # Associa o usuário que realizou a descautela
            )

            # Exclui o registro de cautela do banco de dados
            registro.delete()

            # Retorna uma resposta JSON de sucesso
            return JsonResponse({'success': True})

        except Exception as e:
            # Em caso de erro, retorne uma mensagem de erro detalhada
            return JsonResponse({'error': f'Erro no processamento: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Método inválido'}, status=400)




def atualizar_quantidade_municao(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            registro_id = data.get('registro_id')
            nova_quantidade = int(data.get('nova_quantidade'))

            if registro_id is None or nova_quantidade is None:
                return HttpResponseBadRequest("ID do registro ou nova quantidade não podem ser nulos.")

            # Atualiza a quantidade de munição no banco de dados
            cautela = get_object_or_404(CautelaDeMunicoes, id=registro_id)

            # Certifique-se de que a quantidade de munição não se torna negativa
            if cautela.quantidade + nova_quantidade < 0:
                return JsonResponse({'error': 'Quantidade inválida, estoque não pode ser negativo.'}, status=400)

            cautela.quantidade += nova_quantidade  # Atualiza a quantidade de munição
            cautela.save()
            
            return JsonResponse({'success': True})
        
        except Exception as e:
            return HttpResponseBadRequest(f"Erro: {str(e)}")

    return JsonResponse({'error': 'Método não permitido'}, status=405)

