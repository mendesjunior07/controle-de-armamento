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
import logging
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
    if request.method == 'POST':
        registro_id = request.POST.get('registro_id')
        
        # Buscando o registro no banco de dados com base no ID
        registro = get_object_or_404(RegistroCautelaCompleta, id=registro_id)
        
        # Verificar se a categoria de armamento está presente
        if registro.categoria_armamento:
            # Buscar a subcategoria de armamento associada ao registro
            subcategoria = get_object_or_404(Subcategoria, nome=registro.subcategoria_armamento)
            
            # Alterar o campo situacao para 'disponivel'
            subcategoria.situacao = 'disponivel'
            subcategoria.save()
            
            # Imprimir o valor da categoria armamento no terminal
            print(f"Categoria de Armamento: {registro.categoria_armamento}")
            print(f"Subcategoria '{subcategoria.nome}' alterada para situação: {subcategoria.situacao}")
            
            # Retornar uma resposta de sucesso
            return JsonResponse({'status': 'success', 'categoria_armamento': registro.categoria_armamento})
        
        # Caso a categoria de armamento seja None
        return JsonResponse({'status': 'failed', 'message': 'Categoria de Armamento não encontrada'})
    
    # Caso não seja POST, retornar uma resposta de erro
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'})

def descautelar_ca(request):
    if request.method == 'POST':
        try:
            # Lê o corpo da requisição como JSON
            data = json.loads(request.body)

            # Debug: Verificar os dados recebidos
            print(f"Dados recebidos no request: {data}")

            # Obtém o registro específico usando o ID fornecido
            registro = get_object_or_404(RegistroCautelaCompleta, pk=data['registro_id'])

            # Debug: Verificar se o registro foi recuperado corretamente
            print(f"Registro encontrado: {registro}")

            # Obtém o policial associado ao registro
            policial = get_object_or_404(Policial, nome=data['policial'])

            # Debug: Verificar se o policial foi encontrado
            print(f"Policial encontrado: {policial}")

            # Obtém o usuário atual como armeiro descautelante
            armeiro_descautela = request.user

            # Cria um novo registro de descautelamento
            novo_descautelamento = RegistroDescautelamento.objects.create(
                data_hora_cautela=registro.data_hora,
                policial=policial,
                tipo_servico=data['tipo_servico'],
                categoria_armamento=data['categoria_armamento'],
                subcategoria_armamento=data['subcategoria_armamento'],
                categoria_municao=data['categoria_municao'],
                subcategoria_municao=data['subcategoria_municao'],
                quantidade_municao=int(data['quantidade_municao']),
                situacao_armamento=data['situacao_armamento'],
                observacao=data.get('observacao', ''),  # Observação é opcional
                armeiro=registro.armeiro,
                armeiro_descautela=armeiro_descautela,
            )

            # Atualiza o campo `situacao` na tabela `Subcategoria`
            subcategoria = get_object_or_404(Subcategoria, nome=data['subcategoria_armamento'])
            subcategoria.situacao = data['situacao_armamento']
            subcategoria.save()

            # Exclui o registro de cautela completa após descautela
            print(f"Excluindo o registro de cautela: {registro}")
            registro.delete()

            # Debug: Confirmar exclusão
            if not RegistroCautelaCompleta.objects.filter(pk=data['registro_id']).exists():
                print("Registro excluído com sucesso!")
            else:
                print("Erro: O registro ainda existe no banco de dados!")

            # Retorna uma resposta de sucesso
            return JsonResponse({'success': True, 'descautelamento_id': novo_descautelamento.id})

        except Exception as e:
            # Debug: Mostrar o erro no servidor
            print(f"Erro: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Método não suportado'})

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





