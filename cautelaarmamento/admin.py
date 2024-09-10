from django.contrib import admin
from .models import (
    Categoria,          # Corrigido para usar o nome correto
    Subcategoria,
    Policial,
    CautelaDeArmamento,
    CategoriaMunicao,
    SubcategoriaMunicao,
    MunicaoCautelada,
    ArmamentoCautelado,
    CautelaDeMunicoes
)

# Registre seus modelos no admin
admin.site.register(Categoria)
admin.site.register(Subcategoria)
admin.site.register(Policial)
admin.site.register(CautelaDeArmamento)
admin.site.register(CategoriaMunicao)
admin.site.register(SubcategoriaMunicao)
admin.site.register(MunicaoCautelada)
admin.site.register(ArmamentoCautelado)
admin.site.register(CautelaDeMunicoes)
