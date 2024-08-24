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
    return render(request, 'cautelaarmamento/inventario_equipamentos.html', {'equipamentos': equipamentos})
    

@login_required
def registro_view(request):
    # Sua lógica aqui
    return render(request, 'cautelaarmamento/registro.html')

# @login_required
# def registro_view(request):
#     # Verifica se a requisição é do tipo POST, o que indica que o formulário foi enviado
#     if request.method == 'POST':
#         # Cria uma instância do formulário RegistroForm com os dados enviados pelo usuário
#         form = RegistroForm(request.POST)

#         # Verifica se os dados do formulário são válidos de acordo com as validações definidas
#         if form.is_valid():
#             # Obtém os dados limpos (validados) do campo 'arma' do formulário
#             arma = form.cleaned_data['arma']
#             # Obtém os dados limpos (validados) do campo 'equipamento' do formulário
#             equipamento = form.cleaned_data['equipamento']

#             # Atualiza o campo 'disponivel' da Arma selecionada para False, indicando que a arma não está mais disponível
#             # Arma.objects.filter(id=arma.id).update(disponivel=False)
#             # # Atualiza o campo 'disponivel' do Equipamento selecionado para False, indicando que o equipamento não está mais disponível
#             # Equipamento.objects.filter(id=equipamento.id).update(disponivel=False)

#             # Redireciona o usuário para a página 'registro' após o processamento bem-sucedido do formulário
#             return redirect('registro')
#     else:
#         # Se a requisição não for do tipo POST (provavelmente GET), cria um formulário vazio
#         form = RegistroForm()

#     # Renderiza a página 'registro.html', passando o formulário como contexto
#     return render(request, 'registro.html', {'form': form})
