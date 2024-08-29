from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Cautela, Armas, PolicialMilitar, Vtr
from django.utils import timezone
from django.db.models import Q

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
    equipamentos = Vtr.objects.all()
    return render(request, 'catalogo_de_equipamento/inventario_equipamentos.html', {'equipamentos': equipamentos})

@login_required
def registro_view(request):
    return render(request, 'cautelaarmamento/registro.html')

@login_required
def cautelar_de_armamento(request):
    policiais = PolicialMilitar.objects.all()
    armamento = Armas.objects.all()
    armamentos = Armas.objects.filter(disponivel='Disponivel')
    policiais = PolicialMilitar.objects.all()

    if request.method == 'POST':
        policial_id = request.POST.get('policial')
        armamento_id = request.POST.get('armamento')
        policial = get_object_or_404(PolicialMilitar, id=policial_id)
        armamento = get_object_or_404(Armas, id=armamento_id)

        
        Cautela.objects.create(policial=policial, armamento=armamento)
        armamento.disponivel = False
        armamento.save()

        return redirect('cautelar_de_armamento')

    return render(request, 'armamento/cautela.html', {'policiais': policiais, 'armamentos': armamentos})

def formulario_sucesso(request):
    return render(request, 'armamento/formulario_sucesso.html')


@login_required
def descautelar_armamento(request):
    cautelas = Cautela.objects.filter(data_descautela__isnull=True)

    # Obtém as opções de escolhas do campo 'disponivel' do modelo Armas
    status_disponibilidade_choices = Armas.STATUS_DISPONIBILIDADE

    if request.method == 'POST':
        cautela_id = request.POST.get('cautela_id')
        alteracao = request.POST.get('alteracao', None)

        # Verifica se a ID da cautela é válida
        cautela = get_object_or_404(Cautela, id=cautela_id)

        # Atualiza a data de descautelamento
        cautela.data_descautela = timezone.now()

        if alteracao:
            # Se o usuário escolheu uma alteração, salva o novo status selecionado
            if alteracao in dict(Armas.STATUS_DISPONIBILIDADE).keys():
                cautela.armamento.disponivel = alteracao
        else:
            # Caso contrário, define o status como "Disponivel"
            cautela.armamento.disponivel = 'Disponivel'

        # Salva as alterações no armamento e na cautela
        cautela.armamento.save()
        cautela.save()

        return redirect('descautelar_armamento')

    return render(request, 'armamento/descautela.html', {
        'cautelas': cautelas,
        'status_disponibilidade_choices': status_disponibilidade_choices
    })


@login_required
def listar_armamentos(request):
    # Obtém o termo de busca do campo de pesquisa
    query = request.GET.get('query')

    if query:
        # Filtra os armamentos com base no termo de busca
        armamentos = Armas.objects.filter(
            Q(tipo__icontains=query) | 
            Q(modelo__icontains=query) | 
            Q(numero_de_serie__icontains=query)
        )
    else:
        # Se não houver busca, retorna todos os armamentos
        armamentos = Armas.objects.all()

    # Renderiza o template 'armamento/armas_e_materiais.html' com a lista de armamentos filtrada
    return render(request, 'catalogo_de_equipamento/armas_e_materiais.html', {'armamentos': armamentos})