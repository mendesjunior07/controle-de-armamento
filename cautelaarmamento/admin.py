from django.contrib import admin
from .models import Vtr, Bicicleta

class VtrAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'placa', 'situacao', 'localizacao')
    list_filter = ('marca', 'situacao', 'ano', 'localizacao')
    search_fields = ('marca', 'modelo', 'placa', 'chassi', 'fornecedor')
    ordering = ('marca', 'modelo', 'ano')

admin.site.register(Vtr, VtrAdmin)

# @admin.register(Bicicleta)
class BicicletaAdmin(admin.ModelAdmin):
    list_display = ('marca', 'tipo', 'ano', 'cor', 'situacao', 'tombo', 'localizacao')
    search_fields = ('marca', 'tipo', 'tombo')
    list_filter = ('marca', 'tipo', 'situacao', 'ano')
    ordering = ('marca', 'tipo', 'ano')

admin.site.register(Bicicleta, BicicletaAdmin)