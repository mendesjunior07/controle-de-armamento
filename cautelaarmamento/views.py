from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Cautela, Armas, PolicialMilitar, Vtr
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

@login_required
def cautelar_de_armamento(request):
    policiais = PolicialMilitar.objects.all()
    print(policiais)
    armamento = Armas.objects.all()

    armamentos = Armas.objects.filter(disponivel=True)
    print(armamentos)
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
    print(cautelas)

    if request.method == 'POST':
        cautela_id = request.POST.get('cautela_id')
        cautela = get_object_or_404(Cautela, id=cautela_id)
        cautela.data_descautela = timezone.now()
        cautela.armamento.disponivel = True
        cautela.armamento.save()
        cautela.save()

        return redirect('descautelar_armamento')

    return render(request, 'armamento/descautela.html', {'cautelas': cautelas})
