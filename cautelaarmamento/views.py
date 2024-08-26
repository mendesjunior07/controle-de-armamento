from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Vtr,Cautela
from .forms import CautelaForm, CautelamentodeViatura, CautelamentodeBicicleta, NomedosPms
from django.shortcuts import get_object_or_404
from django.utils import timezone

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
    return render(request, 'cautelaarmamento/index.html')


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

# @login_required
# def cautela_de_armamento(request):
#     if request.method == 'POST':
#         form = CautelaForm(request.POST)
#         if form.is_valid():
#             cautela = form.save()

#             # Marcar como cautelado
#             if cautela.arma:
#                 cautela.arma.cautelado = True
#                 cautela.arma.save()
#             if cautela.municao:
#                 cautela.municao.cautelado = True
#                 cautela.municao.save()
#             if cautela.vtr:
#                 cautela.vtr.cautelado = True
#                 cautela.vtr.save()
#             if cautela.bicicleta:
#                 cautela.bicicleta.cautelado = True
#                 cautela.bicicleta.save()
#             if cautela.moto:
#                 cautela.moto.cautelado = True
#                 cautela.moto.save()

#             return redirect('formulario_sucesso')
#     else:
#         form = CautelaForm()

#     return render(request, 'armamento\cautela.html', {'form': form})

# def formulario_sucesso(request):
#     return render(request, 'armamento/formulario_sucesso.html')

def cautelar_armamento(request):
    policiais = Policial.objects.all()
    armamentos = Armamento.objects.filter(disponivel=True)

    if request.method == 'POST':
        policial_id = request.POST.get('policial')
        armamento_id = request.POST.get('armamento')
        policial = get_object_or_404(Policial, id=policial_id)
        armamento = get_object_or_404(Armamento, id=armamento_id)
        
        Cautela.objects.create(policial=policial, armamento=armamento)
        armamento.disponivel = False
        armamento.save()

        return redirect('cautelar_armamento')

    return render(request, 'cautela/cautelar_armamento.html', {'policiais': policiais, 'armamentos': armamentos})


@login_required
def descautelar_armamento(request):
    # Buscar todas as cautelas que ainda não foram descauteladas
    cautelas = Cautela.objects.filter(data_descautela__isnull=True)
    print(cautelas)

    if request.method == 'POST':
        cautela_id = request.POST.get('cautela_id')
        cautela = get_object_or_404(Cautela, id=cautela_id)
        
        # Marcar como descautelado
        cautela.data_descautela = timezone.now()

        # Atualizar o status do armamento, munição, viatura, bicicleta, e moto para disponível
        if cautela.arma:
            cautela.arma.cautelado = False
            cautela.arma.save()
        if cautela.municao:
            cautela.municao.cautelado = False
            cautela.municao.save()
        if cautela.vtr:
            cautela.vtr.cautelado = False
            cautela.vtr.save()
        if cautela.bicicleta:
            cautela.bicicleta.cautelado = False
            cautela.bicicleta.save()
        if cautela.moto:
            cautela.moto.cautelado = False
            cautela.moto.save()

        cautela.save()

        return redirect('descautelar_armamento')

    return render(request, 'armamento/descautela.html', {'descautela': descautelar_armamento})
