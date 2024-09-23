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
from django.http import JsonResponse
from django.db.models import Sum
from django.db import transaction
from django.contrib import messages
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
    RegistroDescautelamento
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
                    for categoria_id, subcategoria_id in zip(categorias_armamento, subcategorias_armamento):
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

                            # Armazena os nomes para o registro final
                            categoria_armamento_nome = categoria_armamento.nome
                            subcategoria_armamento_nome = subcategoria_armamento.nome

                # Processa as munições
                if categorias_municao and subcategorias_municao and quantidades_municao:
                    for categoria_id, subcategoria_id, quantidade in zip(categorias_municao, subcategorias_municao, quantidades_municao):
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

                            # Armazena os nomes para o registro final
                            categoria_municao_nome = categoria_municao.nome
                            subcategoria_municao_nome = subcategoria_municao.nome
                            quantidade_total_municao += quantidade

                # Registro na nova model com todos os detalhes
                RegistroCautelaCompleta.objects.create(
                    policial=policial,
                    tipo_servico=tipo_servico,
                    categoria_armamento=categoria_armamento_nome,
                    subcategoria_armamento=subcategoria_armamento_nome,
                    categoria_municao=categoria_municao_nome,
                    subcategoria_municao=subcategoria_municao_nome,
                    quantidade_municao=quantidade_total_municao,
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

        # Verifica se há munições cauteladas
        if registro.categoria_municao and registro.subcategoria_municao:
            try:
                # Recupera a subcategoria de munição
                subcategoria_municao = get_object_or_404(SubcategoriaMunicao, nome=registro.subcategoria_municao)

                # Retorna a quantidade de munições ao estoque
                subcategoria_municao.total_de_municoes += registro.quantidade_municao
                subcategoria_municao.save()

                # Registra o descautelamento no banco de dados
                RegistroDescautelamento.objects.create(
                    data_hora_cautela=registro.data_hora,
                    policial=registro.policial,
                    tipo_servico=registro.tipo_servico,
                    categoria_armamento=None,  # S/A não tem armamento
                    subcategoria_armamento=None,  # S/A não tem armamento
                    categoria_municao=registro.categoria_municao,
                    subcategoria_municao=registro.subcategoria_municao,
                    quantidade_municao=registro.quantidade_municao,
                    armeiro=registro.armeiro,
                    data_descautelamento=timezone.now().date(),
                    hora_descautelamento=timezone.now().time(),
                )

                # Mensagem de sucesso para munições
                messages.success(request, 'Munições descauteladas com sucesso e retornadas ao estoque.')
            except SubcategoriaMunicao.DoesNotExist:
                messages.error(request, 'Erro ao encontrar a subcategoria de munição.')

        # Exclui o registro da cautela após o descautelamento
        registro.delete()

        # Redireciona de volta para a lista de registros
        return redirect('listar_cautelas')

    return JsonResponse({'error': 'Método não permitido'}, status=405)

def descautelar_ca(request):
    if request.method == 'POST':
        registro_id = request.POST.get('registro_id')
        situacao = request.POST.get('situacao')  # Obter a nova situação
        observacao = request.POST.get('observacao', '')  # Obter a observação (opcional)

        # Busca o registro da cautela
        registro = get_object_or_404(RegistroCautelaCompleta, id=registro_id)

        # Atualiza a situação do armamento
        if registro.categoria_armamento and registro.subcategoria_armamento:
            subcategoria_armamento = get_object_or_404(Subcategoria, nome=registro.subcategoria_armamento)

            # Atualiza a situação do armamento
            subcategoria_armamento.situacao = situacao  # Atualiza a situação com a escolha do modal
            subcategoria_armamento.save()

            # Registra o descautelamento no novo banco de dados
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

            # Mensagem de sucesso
            messages.success(request, f'Armamento descautelado com sucesso e marcado como {situacao}. Observação: {observacao}')
        
        # Se o registro tiver um armamento associado, ou mesmo sem, ele será excluído
        registro.delete()  # Exclui o registro da tabela de cautelas

        return redirect('listar_cautelas')

    return JsonResponse({'error': 'Método não permitido'}, status=405)