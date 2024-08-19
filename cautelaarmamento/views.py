from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Arma, Equipamento
from .forms import RegistroForm



@login_required
def index(request):
    return render(request, 'cautelaarmamento/index.html')


@login_required
def profile(request):
    return render(request, 'cautelaarmamento/profile.html')


@login_required
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            arma = form.cleaned_data['arma']
            equipamento = form.cleaned_data['equipamento']

            # Atualiza a disponibilidade
            Arma.objects.filter(id=arma.id).update(disponivel=False)
            Equipamento.objects.filter(id=equipamento.id).update(disponivel=False)

            return redirect('registro')
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})
