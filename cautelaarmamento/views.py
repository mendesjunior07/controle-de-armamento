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
from django.views.decorators.http import require_POST
from .models import (
    Categoria, 
    CautelaDeArmamento, 
    Subcategoria, 
    Policial, 
    CategoriaMunicao, 
    MunicaoCautelada,
    SubcategoriaMunicao, 
    ArmamentoCautelado,
    CautelaDeMunicoes
)

def index(request):
    return render(request, 'cautelaarmamento/index.html')


def cautela_de_armamento_view(request):
    if request.method == 'POST':
        # Obtém os dados do formulário
        policial_id = request.POST.get('policial')
        tipo_servico = request.POST.get('tipo_servico')
        categorias = request.POST.getlist('categorias[]')
        subcategorias = request.POST.getlist('subcategorias[]')

        # Verifica se todos os dados obrigatórios foram fornecidos
        if not policial_id or not tipo_servico or not categorias or not subcategorias:
            return JsonResponse({'error': 'Todos os campos obrigatórios devem ser preenchidos.'}, status=400)

        # Recupera o policial selecionado
        policial = get_object_or_404(Policial, id=policial_id)

        # Inicia uma transação para garantir a integridade dos dados
        with transaction.atomic():
            # Cria instâncias de CautelaDeArmamento e atualiza subcategorias
            for categoria_id, subcategoria_id in zip(categorias, subcategorias):
                # Recupera a categoria e subcategoria para evitar IDs inválidos
                categoria = get_object_or_404(Categoria, id=categoria_id)
                subcategoria = get_object_or_404(Subcategoria, id=subcategoria_id)

                # Cria a instância de CautelaDeArmamento
                CautelaDeArmamento.objects.create(
                    policial=policial,
                    tipo_servico=tipo_servico,
                    categoria=categoria,  # Certifique-se de que a categoria é um objeto válido
                    subcategoria=subcategoria
                )

                # Atualiza a situação da subcategoria para "cautelada"
                subcategoria.situacao = 'cautelada'
                subcategoria.save()
                print(f"Subcategoria {subcategoria_id} atualizada para 'cautelada'.")

        # Redireciona para a página de sucesso após o processamento
        return redirect('sucesso')

    # Caso o método seja GET, busca os dados necessários para preencher o formulário
    policiais = Policial.objects.all()
    tipos_servico = CautelaDeArmamento.SERVICO_CHOICES
    categorias_servico = Categoria.objects.all()
    subcategoria_armamento = Subcategoria.objects.all()
    categoria_municoes = CategoriaMunicao.objects.all()
    subcategoria_municoes = SubcategoriaMunicao.objects.all()

    # Calcula a quantidade total de munições usando aggregate e Sum
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

    # Renderiza o template correto
    return render(request, 'armamento/cautela.html', context)


def get_subcategorias_armamento(request, categoria_id):
    try:
        categoria = Categoria.objects.get(id=categoria_id)
        subcategorias = categoria.subcategorias_armamento.filter(situacao='disponivel')
    except Categoria.DoesNotExist:
        return JsonResponse({'error': 'Categoria não encontrada'}, status=404)
    
    data = [{"id": subcategoria.id, "nome": subcategoria.nome} for subcategoria in subcategorias]
    return JsonResponse(data, safe=False)

def get_subcategorias_municao(request, categoria_id):
    categoria = get_object_or_404(CategoriaMunicao, id=categoria_id)
    subcategorias = categoria.subcategorias.all()
    data = [{"id": subcategoria.id, "nome": subcategoria.nome} for subcategoria in subcategorias]
    return JsonResponse(data, safe=False)

def obter_quantidade_total(request, subcategoria_id):
    try:
        subcategoria = get_object_or_404(SubcategoriaMunicao, id=subcategoria_id)
        total_municoes = subcategoria.total_de_municoes
        return JsonResponse({'quantidade': total_municoes})
    except SubcategoriaMunicao.DoesNotExist:
        return JsonResponse({'error': 'Subcategoria não encontrada'}, status=404)


def inventario_equipamentos(request):
    equipamentos = CautelaDeArmamento.objects.all()
    context = {'equipamentos': equipamentos}
    return render(request, 'inventario.html', context)

def descautelar_armamento(request):
    if request.method == 'POST':
        cautela_id = request.POST.get('cautela_id')
        cautela = get_object_or_404(CautelaDeArmamento, id=cautela_id)
        cautela.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def listar_armamentos(request):
    armamentos = CautelaDeArmamento.objects.all()
    context = {'armamentos': armamentos}
    return render(request, 'listar_armamentos.html', context)

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
