from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Vtr

# from .forms import RegistroForm


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
            # Redirecionar para a página inicial ou dashboard
            return redirect('home')
        else:
            # Adiciona uma mensagem de erro se a autenticação falhar
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
    print('olá mundo')
    equipamentos = Vtr.objects.all()
    print(equipamentos)
    # return render(request, 'cautelaarmamento/inventario_equipamentos.html', {'equipamentos': equipamentos})
    return render(request, 'catalogo_de_equipamento/inventario_equipamentos.html', {'equipamentos': equipamentos})

@login_required
def registro_view(request):
    # Sua lógica aqui
    return render(request, 'cautelaarmamento/registro.html')

