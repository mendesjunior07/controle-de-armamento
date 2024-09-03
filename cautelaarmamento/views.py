from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
# from .models import Categoria, Subcategoria, Cautela, Nome_dos_Policiais
from .models import Categoria, Subcategoria, CautelaDeArmamento, Policial
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Por favor, preencha ambos os campos.')
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Nome de usuário ou senha incorretos.')

    return render(request, 'login.html')

@login_required
def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        context = {'username': username}
        # Faça algo com o username
        print(f"Usuário logado: {username}")
    else:
        context = {}
        print("Nenhum usuário logado.")
    return render(request, 'cautelaarmamento/index.html', context)

@login_required
def profile(request):
    return render(request, 'cautelaarmamento/profile.html')

@login_required
def inventario_equipamentos(request):
    pass
#     equipamentos = Vtr.objects.all()
#     return render(request, 'catalogo_de_equipamento/inventario_equipamentos.html', {'equipamentos': equipamentos})

@login_required
def registro_view(request):
    return render(request, 'cautelaarmamento/registro.html')

#########################################################

# @login_required
# def cautelar_de_armamento(request):
#     # Obter todos os policiais disponíveis no banco de dados
#     policiais = PolicialMilitar.objects.all()
    
#     # Obter todos os armamentos que estão marcados como disponíveis no banco de dados
#     armamentos = Armas.objects.filter(disponivel='Disponivel')

#     # Obter todas as categorias de armamentos
#     categorias = Categoria.objects.all()
    
#     # Obter todas as subcategorias associadas às categorias
#     # No código atual, as subcategorias são tratadas como todos os armamentos disponíveis.
#     subcategorias = Armas.objects.all()  # Todas as armas são usadas como subcategorias

#     # Verifica se a requisição é do tipo POST (submissão de formulário)
#     if request.method == 'POST':
#         # Obtém o ID do policial selecionado a partir dos dados do formulário POST
#         policial_id = request.POST.get('policial')
        
#         # Obtém o ID do armamento selecionado a partir dos dados do formulário POST
#         armamento_id = request.POST.get('armamento')
        
#         # Recupera o objeto PolicialMilitar correspondente ao ID fornecido; se não encontrado, gera um erro 404
#         policial = get_object_or_404(PolicialMilitar, id=policial_id)
        
#         # Recupera o objeto Armas correspondente ao ID fornecido; se não encontrado, gera um erro 404
#         armamento = get_object_or_404(Armas, id=armamento_id)

#         # Cria uma nova instância de Cautela associando o policial e o armamento selecionados
#         Cautela.objects.create(policial=policial, armamento=armamento)
        
#         # Atualiza o status do armamento para 'Indisponível'
#         armamento.disponivel = 'Indisponivel'
#         armamento.save()  # Salva as alterações no banco de dados

#         # Redireciona para a mesma página após o processamento do formulário
#         return redirect('cautelar_de_armamento')

#     # Renderiza o template 'armamento/cautela.html' e passa os dados obtidos para o template
#     return render(request, 'armamento/cautela.html', {
#         'policiais': policiais,       # Lista de policiais para exibição no formulário
#         'armamentos': armamentos,     # Lista de armamentos disponíveis para seleção
#         'categorias': categorias,     # Lista de categorias de armamentos
#         'subcategorias': subcategorias  # Lista de subcategorias (armamentos) para exibição no formulário
#     })

#########################################################

# A função cautelar_de_armamento exige que o usuário esteja logado para acessá-la.
# @login_required
# def cautelar_de_armamento(request):
#     if request.method == 'POST':
#         categorias = request.POST.getlist('categorias[]')
#         subcategorias = request.POST.getlist('subcategorias[]')
#         policial_id = request.POST.get('policial')  # Obtém o policial selecionado
        
#         # Validação e busca do policial
#         if policial_id:
#             try:
#                 policial = Nome_dos_Policiais.objects.get(id=policial_id)
#             except Nome_dos_Policiais.DoesNotExist:
#                 return render(request, 'armamento/cautela.html', {
#                     'categorias': Categoria.objects.all(), 
#                     'policiais': Nome_dos_Policiais.objects.all(), 
#                     'error': 'O policial selecionado não existe.'
#                 })
#         else:
#             return render(request, 'armamento/cautela.html', {
#                 'categorias': Categoria.objects.all(), 
#                 'policiais': Nome_dos_Policiais.objects.all(), 
#                 'error': 'Por favor, selecione um policial.'
#             })

#         # Criar instâncias de Cautela
#         for categoria_id, subcategoria_id in zip(categorias, subcategorias):
#             try:
#                 categoria = Categoria.objects.get(id=categoria_id)
#                 subcategoria = Subcategoria.objects.get(id=subcategoria_id)
#                 Cautela.objects.create(
#                     policial_responsavel=policial,  # Use o nome correto do campo
#                     categoria=categoria,
#                     subcategoria=subcategoria
#                 )
#             except (Categoria.DoesNotExist, Subcategoria.DoesNotExist):
#                 return render(request, 'armamento/cautela.html', {
#                     'categorias': Categoria.objects.all(), 
#                     'policiais': Nome_dos_Policiais.objects.all(), 
#                     'error': 'Categoria ou subcategoria inválida.'
#                 })

#         return redirect('index')

#     categorias = Categoria.objects.all()
#     policiais = Nome_dos_Policiais.objects.all()
#     return render(request, 'armamento/cautela.html', {'categorias': categorias, 'policiais': policiais})


# def subcategorias_por_categoria(request, categoria_id):
#     """
#     Retorna uma lista de subcategorias em formato JSON para uma determinada categoria.
#     """
#     subcategorias = Subcategoria.objects.filter(categoria_id=categoria_id).values('id', 'nome')
#     return JsonResponse(list(subcategorias), safe=False)

#########################################################

# def formulario_sucesso(request):
#     return render(request, 'armamento/sucesso.html')


@login_required
def descautelar_armamento(request):
    pass
    # cautelas = Cautela.objects.filter(data_descautela__isnull=True)

    # # Obtém as opções de escolhas do campo 'disponivel' do modelo Armas
    # status_disponibilidade_choices = Armas.STATUS_DISPONIBILIDADE

    # if request.method == 'POST':
    #     cautela_id = request.POST.get('cautela_id')
    #     alteracao = request.POST.get('alteracao', None)

    #     # Verifica se a ID da cautela é válida
    #     cautela = get_object_or_404(Cautela, id=cautela_id)

    #     # Atualiza a data de descautelamento
    #     cautela.data_descautela = timezone.now()

    #     if alteracao:
    #         # Se o usuário escolheu uma alteração, salva o novo status selecionado
    #         if alteracao in dict(Armas.STATUS_DISPONIBILIDADE).keys():
    #             cautela.armamento.disponivel = alteracao
    #     else:
    #         # Caso contrário, define o status como "Disponivel"
    #         cautela.armamento.disponivel = 'Disponivel'

    #     # Salva as alterações no armamento e na cautela
    #     cautela.armamento.save()
    #     cautela.save()

    #     return redirect('descautelar_armamento')

    # return render(request, 'armamento/descautela.html', {
    #     'cautelas': cautelas,
    #     'status_disponibilidade_choices': status_disponibilidade_choices
    # })


@login_required
def listar_armamentos(request):
    pass
    # # Obtém o termo de busca do campo de pesquisa
    # query = request.GET.get('query')

    # if query:
    #     # Filtra os armamentos com base no termo de busca
    #     armamentos = Armas.objects.filter(
    #         Q(tipo__icontains=query) | 
    #         Q(modelo__icontains=query) | 
    #         Q(numero_de_serie__icontains=query)
    #     )
    # else:
    #     # Se não houver busca, retorna todos os armamentos
    #     armamentos = Armas.objects.all()

    # # Renderiza o template 'armamento/armas_e_materiais.html' com a lista de armamentos filtrada
    # return render(request, 'catalogo_de_equipamento/armas_e_materiais.html', {'armamentos': armamentos})


####################################################################
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.exceptions import ValidationError
from .models import Categoria, Subcategoria, Policial, CautelaDeArmamento, Pessoa

def cautela_de_armamento_view(request):
    # Obtém todas as categorias e policiais do banco de dados para exibir no formulário
    categorias = Categoria.objects.all()
    policiais = Policial.objects.all()

    # Verifica se a requisição é do tipo POST, indicando que o formulário foi submetido
    if request.method == 'POST':
        # Obtém o ID do policial a partir dos dados enviados na requisição POST
        policial_id = request.POST.get('policial')

        # Obtém a lista de IDs das categorias e subcategorias a partir dos dados enviados na requisição POST
        categorias_ids = request.POST.getlist('categorias[]')
        subcategorias_ids = request.POST.getlist('subcategorias[]')

        # Verifica se todos os dados necessários estão presentes
        if policial_id and categorias_ids and subcategorias_ids:
            try:
                # Busca o objeto Policial no banco de dados correspondente ao ID fornecido
                policial = Policial.objects.get(id=policial_id)

                # Itera sobre as listas de IDs de categorias e subcategorias simultaneamente
                for categoria_id, subcategoria_id in zip(categorias_ids, subcategorias_ids):
                    # Busca o objeto Categoria e Subcategoria no banco de dados correspondentes aos IDs fornecidos
                    categoria = Categoria.objects.get(id=categoria_id)
                    subcategoria = Subcategoria.objects.get(id=subcategoria_id)

                    # Cria uma nova instância de CautelaDeArmamento no banco de dados
                    CautelaDeArmamento.objects.create(policial=policial, categoria=categoria, subcategoria=subcategoria)

                # Redireciona o usuário para a URL de sucesso após a criação da cautela
                return redirect('sucesso')  # Substitua 'sucesso' pela sua URL de sucesso.

            except (Policial.DoesNotExist, Categoria.DoesNotExist, Subcategoria.DoesNotExist) as e:
                # Retorna uma resposta de erro se algum dos objetos não for encontrado
                return HttpResponseBadRequest(f"Erro: {str(e)}")

        else:
            # Retorna uma resposta de erro se algum dos dados necessários estiver ausente
            return HttpResponseBadRequest("Dados insuficientes para processar o formulário.")

    # Renderiza o template 'cautela.html' com as categorias e policiais para exibição na página
    return render(request, 'armamento/cautela.html', {
        'categorias': categorias,
        'policiais': policiais,
    })


def get_subcategorias(request, categoria_id):
    # Filtra todas as subcategorias do banco de dados que pertencem à categoria especificada pelo categoria_id
    subcategorias = Subcategoria.objects.filter(categoria_id=categoria_id)

    # Cria uma lista de dicionários contendo o 'id' e o 'nome' de cada subcategoria filtrada
    subcategorias_list = [{'id': subcategoria.id, 'nome': subcategoria.nome} for subcategoria in subcategorias]

    # Retorna a lista de subcategorias em formato JSON para ser consumido por uma requisição AJAX
    return JsonResponse(subcategorias_list, safe=False)


def formulario_sucesso(request):
    # Renderiza o template 'sucesso.html' que exibe uma mensagem de sucesso ou confirmação após o formulário ser enviado com sucesso
    return render(request, 'armamento/sucesso.html')


def cadastrar_pessoa(request):
    if request.method == 'POST':
        # Obtendo os dados do formulário
        nome_completo = request.POST.get('nome_completo')
        nome_guerra = request.POST.get('nome_guerra')
        posto_graduacao = request.POST.get('posto_graduacao')
        matricula = request.POST.get('matricula')
        rgpm = request.POST.get('rgpm')
        lotacao = request.POST.get('lotacao')
        data_nascimento = request.POST.get('data_nascimento')
        restricao = request.POST.get('restricao', False)
        cpf = request.POST.get('cpf')

        # Cria uma instância do modelo para usar a validação
        pessoa = Pessoa(
            nome_completo=nome_completo,
            nome_guerra=nome_guerra,
            posto_graduacao=posto_graduacao,
            matricula=matricula,
            rgpm=rgpm,
            lotacao=lotacao,
            data_nascimento=data_nascimento,
            restricao=bool(restricao),
            cpf=cpf
        )

        try:
            pessoa.clean()  # Executa as validações do modelo
            pessoa.save()  # Salva a instância no banco de dados se for válida
            return redirect('sucesso_cadastro')  # Redireciona para a página de sucesso
        except ValidationError as e:
            # Certifique-se de usar o caminho completo para o template
            return render(request, 'armamento/cadastrar_pessoa.html', {'error': e.message, 'pessoa': pessoa})

    # Certifique-se de usar o caminho completo para o template
    return render(request, 'armamento/cadastrar_pessoa.html')



def sucesso_view(request):
    # Renderiza o template de sucesso para qualquer ação que precise de uma confirmação genérica
    return render(request, 'sucesso.html')
