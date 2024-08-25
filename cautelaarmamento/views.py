from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Vtr
from .forms import CautelamentodeViatura,CauteladeBicicleta, NomedosPms

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

@login_required
def cautela_de_armamento(request):
    if request.method == 'POST':
        form01 = NomedosPms(request.POST)
        form02 = CautelamentodeViatura(request.POST)
        form03 = CauteladeBicicleta(request.POST)
        form04 = CauteladeBicicleta(request.POST)
        
        if form01.is_valid() and form02.is_valid() and form03.is_valid() and form04.is_valid():
            form01.save()
            form02.save()
            form03.save()
            form04.save()
            return render(request, 'armamento/formulario_sucesso.html')
    else:
        form01 = NomedosPms()  # Instancia um formulário vazio
        form02 = CautelamentodeViatura()     # Instancia um formulário vazio
        form03 = CauteladeBicicleta()     # Instancia um formulário vazio
        form04 = CauteladeBicicleta()     # Instancia um formulário vazio
    return render(request, 'armamento/cautela.html', {'form01': form01, 'form02': form02, 'form03': form03 , 'form04': form04})
