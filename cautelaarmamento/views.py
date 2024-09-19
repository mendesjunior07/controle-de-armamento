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
from .models import (
    Categoria, 
    CautelaDeArmamento, 
    Subcategoria, 
    Policial, 
    CategoriaMunicao, 
    SubcategoriaMunicao, 
    CautelaDeMunicoes,
    RegistroCautelaCompleta
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

        # Verifica se pelo menos um grupo (armamento ou munição) foi preenchido
        if not (categorias_armamento and subcategorias_armamento) and not (categorias_municao and subcategorias_municao and quantidades_municao):
            return JsonResponse({'error': 'Preencha pelo menos um dos grupos: armamento ou munição.'}, status=400)

        policial = get_object_or_404(Policial, id=policial_id)
        armeiro = request.user

        try:
            with transaction.atomic():
                # Inicializa variáveis para munição e armamento para uso posterior
                categoria_armamento_nome = None
                subcategoria_armamento_nome = None
                categoria_municao_nome = None
                subcategoria_municao_nome = None
                quantidade_total_municao = 0

                # Salvar dados da cautela de armamento, se presentes
                if categorias_armamento and subcategorias_armamento:
                    for categoria_id, subcategoria_id in zip(categorias_armamento, subcategorias_armamento):
                        if categoria_id and subcategoria_id:  # Verifica se os IDs não estão em branco
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

                # Salvar dados de munições, se presentes
                if categorias_municao and subcategorias_municao and quantidades_municao:
                    for categoria_id, subcategoria_id, quantidade in zip(categorias_municao, subcategorias_municao, quantidades_municao):
                        if categoria_id and subcategoria_id and quantidade:  # Verifica se os IDs e quantidade não estão em branco
                            categoria_municao = get_object_or_404(CategoriaMunicao, id=categoria_id)
                            subcategoria_municao = get_object_or_404(SubcategoriaMunicao, id=subcategoria_id)

                            # Salva registro no modelo de Cautela de Munição
                            CautelaDeMunicoes.objects.create(
                                policial=policial,
                                categoria=categoria_municao,
                                subcategoria=subcategoria_municao,
                                quantidade=int(quantidade)
                            )

                            # Armazena os nomes para o registro final
                            categoria_municao_nome = categoria_municao.nome
                            subcategoria_municao_nome = subcategoria_municao.nome
                            quantidade_total_municao += int(quantidade)

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

    # Monta o contexto corretamente como um dicionário
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
