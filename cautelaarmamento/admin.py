from django.contrib import admin
from .models import (
    Policial,
    Categoria,
    Subcategoria,
    CategoriaMunicao,
    SubcategoriaMunicao,
    CautelaDeArmamento,
    CautelaDeMunicoes,
    RegistroCautelaCompleta,
    RegistroDescautelamento
)

# Register all models
admin.site.register(Policial)
admin.site.register(Categoria)
admin.site.register(Subcategoria)
admin.site.register(CategoriaMunicao)
admin.site.register(SubcategoriaMunicao)
admin.site.register(CautelaDeArmamento)
admin.site.register(CautelaDeMunicoes)
admin.site.register(RegistroCautelaCompleta)
admin.site.register(RegistroDescautelamento)
