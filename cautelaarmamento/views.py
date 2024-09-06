# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.contrib.auth import authenticate, login
# # from .models import Categoria, Subcategoria, Cautela, Nome_dos_Policiais
# from .models import Categoria, Subcategoria, CautelaDeArmamento, Policial
# from django.utils import timezone
# from django.db.models import Q
# from django.http import JsonResponse

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

# @login_required
# def index(request):
#     if request.user.is_authenticated:
#         username = request.user.username
#         context = {'username': username}
#         # Faça algo com o username
#         print(f"Usuário logado: {username}")
#     else:
#         context = {}
#         print("Nenhum usuário logado.")
#     return render(request, 'cautelaarmamento/index.html', context)

# @login_required
# def profile(request):
#     return render(request, 'cautelaarmamento/profile.html')

# @login_required
# def inventario_equipamentos(request):
#     pass
# #     equipamentos = Vtr.objects.all()
# #     return render(request, 'catalogo_de_equipamento/inventario_equipamentos.html', {'equipamentos': equipamentos})

# @login_required
# def registro_view(request):
#     return render(request, 'cautelaarmamento/registro.html')

# #########################################################

# # @login_required
# # def cautelar_de_armamento(request):
# #     # Obter todos os policiais disponíveis no banco de dados
# #     policiais = PolicialMilitar.objects.all()
    
# #     # Obter todos os armamentos que estão marcados como disponíveis no banco de dados
# #     armamentos = Armas.objects.filter(disponivel='Disponivel')

# #     # Obter todas as categorias de armamentos
# #     categorias = Categoria.objects.all()
    
# #     # Obter todas as subcategorias associadas às categorias
# #     # No código atual, as subcategorias são tratadas como todos os armamentos disponíveis.
# #     subcategorias = Armas.objects.all()  # Todas as armas são usadas como subcategorias

# #     # Verifica se a requisição é do tipo POST (submissão de formulário)
# #     if request.method == 'POST':
# #         # Obtém o ID do policial selecionado a partir dos dados do formulário POST
# #         policial_id = request.POST.get('policial')
        
# #         # Obtém o ID do armamento selecionado a partir dos dados do formulário POST
# #         armamento_id = request.POST.get('armamento')
        
# #         # Recupera o objeto PolicialMilitar correspondente ao ID fornecido; se não encontrado, gera um erro 404
# #         policial = get_object_or_404(PolicialMilitar, id=policial_id)
        
# #         # Recupera o objeto Armas correspondente ao ID fornecido; se não encontrado, gera um erro 404
# #         armamento = get_object_or_404(Armas, id=armamento_id)

# #         # Cria uma nova instância de Cautela associando o policial e o armamento selecionados
# #         Cautela.objects.create(policial=policial, armamento=armamento)
        
# #         # Atualiza o status do armamento para 'Indisponível'
# #         armamento.disponivel = 'Indisponivel'
# #         armamento.save()  # Salva as alterações no banco de dados

# #         # Redireciona para a mesma página após o processamento do formulário
# #         return redirect('cautelar_de_armamento')

# #     # Renderiza o template 'armamento/cautela.html' e passa os dados obtidos para o template
# #     return render(request, 'armamento/cautela.html', {
# #         'policiais': policiais,       # Lista de policiais para exibição no formulário
# #         'armamentos': armamentos,     # Lista de armamentos disponíveis para seleção
# #         'categorias': categorias,     # Lista de categorias de armamentos
# #         'subcategorias': subcategorias  # Lista de subcategorias (armamentos) para exibição no formulário
# #     })

# #########################################################

# # A função cautelar_de_armamento exige que o usuário esteja logado para acessá-la.
# # @login_required
# # def cautelar_de_armamento(request):
# #     if request.method == 'POST':
# #         categorias = request.POST.getlist('categorias[]')
# #         subcategorias = request.POST.getlist('subcategorias[]')
# #         policial_id = request.POST.get('policial')  # Obtém o policial selecionado
        
# #         # Validação e busca do policial
# #         if policial_id:
# #             try:
# #                 policial = Nome_dos_Policiais.objects.get(id=policial_id)
# #             except Nome_dos_Policiais.DoesNotExist:
# #                 return render(request, 'armamento/cautela.html', {
# #                     'categorias': Categoria.objects.all(), 
# #                     'policiais': Nome_dos_Policiais.objects.all(), 
# #                     'error': 'O policial selecionado não existe.'
# #                 })
# #         else:
# #             return render(request, 'armamento/cautela.html', {
# #                 'categorias': Categoria.objects.all(), 
# #                 'policiais': Nome_dos_Policiais.objects.all(), 
# #                 'error': 'Por favor, selecione um policial.'
# #             })

# #         # Criar instâncias de Cautela
# #         for categoria_id, subcategoria_id in zip(categorias, subcategorias):
# #             try:
# #                 categoria = Categoria.objects.get(id=categoria_id)
# #                 subcategoria = Subcategoria.objects.get(id=subcategoria_id)
# #                 Cautela.objects.create(
# #                     policial_responsavel=policial,  # Use o nome correto do campo
# #                     categoria=categoria,
# #                     subcategoria=subcategoria
# #                 )
# #             except (Categoria.DoesNotExist, Subcategoria.DoesNotExist):
# #                 return render(request, 'armamento/cautela.html', {
# #                     'categorias': Categoria.objects.all(), 
# #                     'policiais': Nome_dos_Policiais.objects.all(), 
# #                     'error': 'Categoria ou subcategoria inválida.'
# #                 })

# #         return redirect('index')

# #     categorias = Categoria.objects.all()
# #     policiais = Nome_dos_Policiais.objects.all()
# #     return render(request, 'armamento/cautela.html', {'categorias': categorias, 'policiais': policiais})


# # def subcategorias_por_categoria(request, categoria_id):
# #     """
# #     Retorna uma lista de subcategorias em formato JSON para uma determinada categoria.
# #     """
# #     subcategorias = Subcategoria.objects.filter(categoria_id=categoria_id).values('id', 'nome')
# #     return JsonResponse(list(subcategorias), safe=False)

# #########################################################

# # def formulario_sucesso(request):
# #     return render(request, 'armamento/sucesso.html')


# @login_required
# def descautelar_armamento(request):
#     pass
#     # cautelas = Cautela.objects.filter(data_descautela__isnull=True)

#     # # Obtém as opções de escolhas do campo 'disponivel' do modelo Armas
#     # status_disponibilidade_choices = Armas.STATUS_DISPONIBILIDADE

#     # if request.method == 'POST':
#     #     cautela_id = request.POST.get('cautela_id')
#     #     alteracao = request.POST.get('alteracao', None)

#     #     # Verifica se a ID da cautela é válida
#     #     cautela = get_object_or_404(Cautela, id=cautela_id)

#     #     # Atualiza a data de descautelamento
#     #     cautela.data_descautela = timezone.now()

#     #     if alteracao:
#     #         # Se o usuário escolheu uma alteração, salva o novo status selecionado
#     #         if alteracao in dict(Armas.STATUS_DISPONIBILIDADE).keys():
#     #             cautela.armamento.disponivel = alteracao
#     #     else:
#     #         # Caso contrário, define o status como "Disponivel"
#     #         cautela.armamento.disponivel = 'Disponivel'

#     #     # Salva as alterações no armamento e na cautela
#     #     cautela.armamento.save()
#     #     cautela.save()

#     #     return redirect('descautelar_armamento')

#     # return render(request, 'armamento/descautela.html', {
#     #     'cautelas': cautelas,
#     #     'status_disponibilidade_choices': status_disponibilidade_choices
#     # })


# @login_required
# def listar_armamentos(request):
#     pass
#     # # Obtém o termo de busca do campo de pesquisa
#     # query = request.GET.get('query')

#     # if query:
#     #     # Filtra os armamentos com base no termo de busca
#     #     armamentos = Armas.objects.filter(
#     #         Q(tipo__icontains=query) | 
#     #         Q(modelo__icontains=query) | 
#     #         Q(numero_de_serie__icontains=query)
#     #     )
#     # else:
#     #     # Se não houver busca, retorna todos os armamentos
#     #     armamentos = Armas.objects.all()

#     # # Renderiza o template 'armamento/armas_e_materiais.html' com a lista de armamentos filtrada
#     # return render(request, 'catalogo_de_equipamento/armas_e_materiais.html', {'armamentos': armamentos})


# ####################################################################
# from django.shortcuts import render, redirect
# from django.http import JsonResponse, HttpResponseBadRequest
# from django.core.exceptions import ValidationError
# from django.db import IntegrityError
# from django.shortcuts import render, get_object_or_404
# from django.views.decorators.csrf import csrf_exempt
# from django.views import View
# from .models import (
#     Categoria,
#     Subcategoria,
#     Policial,
#     CautelaDeArmamento,
#     SubcategoriaMunicao,  # Nome correto
#     CategoriaMunicao,      # Nome correto             # Adicionado para incluir a classe Municao
# )
# from django.http import HttpResponseBadRequest

# @login_required
# def cautela_de_armamento_view(request):
#     # Busca todas as categorias e subcategorias necessárias do banco de dados
#     categorias = Categoria.objects.all()
#     policiais = Policial.objects.all()
#     tipos_servico = CautelaDeArmamento.SERVICO_CHOICES


#     if request.method == 'POST':
#         # Captura os dados enviados pelo formulário
#         policial_id = request.POST.get('policial')
#         tipo_servico = request.POST.get('tipo_servico')
#         categorias_ids = request.POST.getlist('categorias[]')
#         subcategorias_ids = request.POST.getlist('subcategorias[]')

#         # Captura de dados para munições
#         categorias_municoes_ids = request.POST.getlist('categorias_municoes[]')
#         subcategorias_municoes_ids = request.POST.getlist('subcategorias_municoes[]')
#         quantidades_municoes = request.POST.getlist('quantidades_municoes[]')

#         # Verifica se os dados obrigatórios foram fornecidos
#         if policial_id and tipo_servico and categorias_ids and subcategorias_ids:
#             try:
#                 # Obtém a instância do policial selecionado
#                 policial_instance = Policial.objects.get(id=policial_id)

#                 # Processa as categorias e subcategorias de armamento
#                 for categoria_id, subcategoria_id in zip(categorias_ids, subcategorias_ids):
#                     categoria = Categoria.objects.get(id=categoria_id)
#                     subcategoria = Subcategoria.objects.get(id=subcategoria_id)

#                     # Cria uma nova instância de CautelaDeArmamento no banco de dados
#                     CautelaDeArmamento.objects.create(
#                         policial=policial_instance,
#                         categoria=categoria,
#                         subcategoria=subcategoria,
#                         tipo_servico=tipo_servico
#                     )

#                     # Atualiza a situação da subcategoria para "cautelada"
#                     subcategoria.situacao = 'cautelada'
#                     subcategoria.save()

#                 # Lida com a parte de munições


#                 return redirect('sucesso')

#             except (Policial.DoesNotExist, Categoria.DoesNotExist, Subcategoria.DoesNotExist.DoesNotExist) as e:
#                 # Captura qualquer erro relacionado à não existência dos objetos
#                 return HttpResponseBadRequest(f"Erro: {str(e)}")

#         else:
#             # Retorna erro caso dados obrigatórios estejam faltando
#             return HttpResponseBadRequest("Dados insuficientes para processar o formulário.")

#     # Filtra apenas subcategorias com situação "disponível"
#     subcategorias = Subcategoria.objects.filter(situacao='disponivel')


#     # Renderiza o template HTML com os dados necessários
#     return render(request, 'armamento/cautela.html', {
#         'categorias': categorias,
#         'policiais': policiais,
#         'tipos_servico': tipos_servico,
#         'subcategorias': subcategorias,
#     })



# def get_subcategorias(request, categoria_id):
#     try:
#         # Filtra as subcategorias pela categoria e situação "disponivel"
#         subcategorias = Subcategoria.objects.filter(categoria_id=categoria_id, situacao='disponivel')
#         data = [{'id': subcategoria.id, 'nome': subcategoria.nome} for subcategoria in subcategorias]
#         return JsonResponse(data, safe=False)
#     except Categoria.DoesNotExist:
#         return JsonResponse({'error': 'Categoria não encontrada'}, status=404)


# def cadastrar_pessoa(request):
#     if request.method == 'POST':
#         # Obtendo os dados do formulário
#         nome_completo = request.POST.get('nome_completo')
#         nome_guerra = request.POST.get('nome_guerra')
#         posto_graduacao = request.POST.get('posto_graduacao')
#         matricula = request.POST.get('matricula')
#         rgpm = request.POST.get('rgpm')
#         lotacao = request.POST.get('lotacao')
#         data_nascimento = request.POST.get('data_nascimento')
#         # restricao = request.POST.get('restricao', False)
#         cpf = request.POST.get('cpf')

#         # Verifica se já existe um policial com o mesmo CPF
#         if Policial.objects.filter(cpf=cpf).exists():
#             return render(request, 'armamento/cadastrar_pessoa.html', {
#                 'error': 'Já existe um policial com este CPF.',
#                 'pessoa': request.POST
#             })

#         # Cria uma instância do modelo para usar a validação
#         pessoa = Policial(
#             nome_completo=nome_completo,
#             nome_guerra=nome_guerra,
#             posto_graduacao=posto_graduacao,
#             matricula=matricula,
#             rgpm=rgpm,
#             lotacao=lotacao,
#             data_nascimento=data_nascimento,
#             # restricao=bool(restricao),
#             cpf=cpf
#         )

#         try:
#             pessoa.clean()  # Executa as validações do modelo
#             pessoa.save()  # Salva a instância no banco de dados se for válida
#             return redirect('sucesso')  # Ajustado para o nome correto da URL
#         except ValidationError as e:
#             return render(request, 'armamento/cadastrar_pessoa.html', {'error': e.message, 'pessoa': pessoa})
#         except IntegrityError:
#             return render(request, 'armamento/cadastrar_pessoa.html', {
#                 'error': 'Erro ao salvar o policial. Certifique-se de que o CPF é único.',
#                 'pessoa': pessoa
#             })

#     return render(request, 'armamento/cadastrar_pessoa.html')


# def formulario_sucesso(request):
#     # Renderiza o template 'sucesso.html' que exibe uma mensagem de sucesso ou confirmação após o formulário ser enviado com sucesso
#     return render(request, 'armamento/sucesso.html')

# def sucesso_view(request):
#     # Renderiza o template de sucesso para qualquer ação que precise de uma confirmação genérica
#     return render(request, 'sucesso-cadastro.html')

# def atualizar_subcategorias(request):
#     if request.method == 'POST':
#         # Recebe os dados da requisição
#         categorias = request.POST.getlist('categorias[]')
#         subcategorias = request.POST.getlist('subcategorias[]')
        
#         # Atualiza o estado das subcategorias
#         for subcategoria_id in subcategorias:
#             if subcategoria_id:
#                 Subcategoria.objects.filter(id=subcategoria_id).update(situacao='cautelada')
        
#         return JsonResponse({'success': True})
#     return JsonResponse({'success': False}, status=400)

# ########################################################################################

# # View para exibir a página de cautela de munições
# def cautela_municoes(request):
#     categorias = CategoriaMunicao.objects.all()  # Obtém todas as categorias de CategoriaMunicao
#     return render(request, 'armamento/cautela_municoes.html', {'categorias': categorias})

# # View para obter subcategorias com base na categoria selecionada
# def obter_subcategorias(request, categoria_id):
#     if request.method == 'GET':
#         subcategorias = SubcategoriaMunicao.objects.filter(categoria_id=categoria_id)
#         subcategoria_data = [{'id': sub.id, 'text': sub.nome} for sub in subcategorias]
#         return JsonResponse(subcategoria_data, safe=False)
#     return HttpResponseBadRequest('Requisição inválida.')

# # View para processar a submissão do formulário
# @csrf_exempt
# def atualizar_subcategorias(request):
#     if request.method == 'POST':
#         # Obter os dados do formulário
#         categorias = request.POST.getlist('categoria')
#         subcategorias = request.POST.getlist('subcategoria')
#         quantidades = request.POST.getlist('quantidade')

#         try:
#             for categoria, subcategoria, quantidade in zip(categorias, subcategorias, quantidades):
#                 cat = get_object_or_404(CategoriaMunicao, id=categoria)
#                 subcat = get_object_or_404(SubcategoriaMunicao, id=subcategoria, categoria=cat)
#                 quantidade = int(quantidade)
                
#                 # Criar um novo registro de munição
#                 # Municao.objects.create(categoria=cat, subcategoria=subcat, quantidade=quantidade)

#             # Retornar resposta de sucesso em JSON
#             return JsonResponse({'success': True})
#         except ValidationError as e:
#             return JsonResponse({'success': False, 'error': str(e)})
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': 'Erro desconhecido.'})

#     return HttpResponseBadRequest('Requisição inválida.')

# ##################################################################

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Categoria, Subcategoria, Policial, CautelaDeArmamento, CategoriaMunicao, SubcategoriaMunicao, CautelaDeMunicoes

def index(request):
    # Função para renderizar a página inicial ou qualquer outro contexto desejado
    return render(request, 'index.html')

def registro_view(request):
    # Função de visualização para o registro de um novo formulário de cautela
    policiais = Policial.objects.all()
    categorias = Categoria.objects.all()
    tipos_servico = CautelaDeArmamento.SERVICO_CHOICES

    context = {
        'policiais': policiais,
        'categorias': categorias,
        'tipos_servico': tipos_servico
    }
    return render(request, 'registro.html', context)

def inventario_equipamentos(request):
    # Função de visualização para o inventário de equipamentos
    equipamentos = CautelaDeArmamento.objects.all()
    context = {'equipamentos': equipamentos}
    return render(request, 'inventario.html', context)

def cautela_de_armamento_view(request):
    # Função de visualização para registrar a cautela de armamentos
    if request.method == 'POST':
        policial_id = request.POST.get('policial')
        tipo_servico = request.POST.get('tipo_servico')
        categorias = request.POST.getlist('categorias[]')
        subcategorias = request.POST.getlist('subcategorias[]')

        policial = get_object_or_404(Policial, id=policial_id)

        for categoria_id, subcategoria_id in zip(categorias, subcategorias):
            categoria = get_object_or_404(Categoria, id=categoria_id)
            subcategoria = get_object_or_404(Subcategoria, id=subcategoria_id)
            CautelaDeArmamento.objects.create(
                policial=policial,
                tipo_servico=tipo_servico,
                categoria=categoria,
                subcategoria=subcategoria
            )

        return redirect('sucesso')

    policiais = Policial.objects.all()
    categorias = Categoria.objects.all()
    tipos_servico = CautelaDeArmamento.SERVICO_CHOICES

    context = {
        'policiais': policiais,
        'categorias': categorias,
        'tipos_servico': tipos_servico
    }
    return render(request, 'armamento\cautela.html', context)

def formulario_sucesso(request):
    # Função de visualização de sucesso após o envio do formulário
    return render(request, 'sucesso.html')

def descautelar_armamento(request):
    # Função de visualização para descautelar armamento
    if request.method == 'POST':
        cautela_id = request.POST.get('cautela_id')
        cautela = get_object_or_404(CautelaDeArmamento, id=cautela_id)
        cautela.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def listar_armamentos(request):
    # Função de visualização para listar todos os armamentos
    armamentos = CautelaDeArmamento.objects.all()
    context = {'armamentos': armamentos}
    return render(request, 'listar_armamentos.html', context)

def get_subcategorias(request, categoria_id):
    # Função para obter subcategorias disponíveis com base na categoria selecionada
    subcategorias = Subcategoria.objects.filter(categoria_id=categoria_id, situacao='disponivel')
    data = [{'id': subcategoria.id, 'nome': subcategoria.nome} for subcategoria in subcategorias]
    return JsonResponse(data, safe=False)

def cadastrar_pessoa(request):
    # Função para cadastrar uma nova pessoa (policial)
    if request.method == 'POST':
        nome_completo = request.POST.get('nome_completo')
        matricula = request.POST.get('matricula')
        # Suponha que mais campos sejam processados aqui
        # Implementar a lógica de salvamento do policial
        return redirect('sucesso_cadastro')
    return render(request, 'cadastrar_pessoa.html')

def sucesso_view(request):
    # Função de visualização de sucesso após o cadastro de uma pessoa
    return render(request, 'sucesso_cadastro.html')

@require_POST
def atualizar_subcategorias(request):
    # Função para atualizar as subcategorias
    categoria_id = request.POST.get('categoria_id')
    situacao = request.GET.get('situacao', 'disponivel')
    subcategorias = Subcategoria.objects.filter(categoria_id=categoria_id, situacao=situacao)
    data = [{'id': subcategoria.id, 'nome': subcategoria.nome} for subcategoria in subcategorias]
    return JsonResponse(data, safe=False)

def cautela_municoes(request):
    # Função para a cautela de munições
    if request.method == 'POST':
        categorias = request.POST.getlist('categoria_municoes[]')
        subcategorias = request.POST.getlist('subcategoria_municoes[]')
        quantidades = request.POST.getlist('quantidade_municoes[]')

        for categoria_id, subcategoria_id, quantidade in zip(categorias, subcategorias, quantidades):
            categoria = get_object_or_404(CategoriaMunicao, id=categoria_id)
            subcategoria = get_object_or_404(SubcategoriaMunicao, id=subcategoria_id)
            CautelaDeMunicoes.objects.create(
                categoria=categoria,
                subcategoria=subcategoria,
                quantidade=quantidade
            )
        return redirect('sucesso')

    categorias = CategoriaMunicao.objects.all()
    subcategorias = SubcategoriaMunicao.objects.all()
    context = {
        'categorias': categorias,
        'subcategorias': subcategorias
    }
    return render(request, 'cautela_municoes.html', context)

def obter_subcategorias(request, categoria_id):
    # Função para obter subcategorias de munição com base na categoria selecionada
    subcategorias = SubcategoriaMunicao.objects.filter(categoria_id=categoria_id)
    data = [{'id': subcategoria.id, 'nome': subcategoria.nome} for subcategoria in subcategorias]
    return JsonResponse(data, safe=False)
