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

from django.contrib import admin
from .models import PolicialMilitar

@admin.register(PolicialMilitar)
class PolicialMilitarAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'numero_identificacao', 'cpf', 'patente', 'unidade', 'status', 'data_ingresso')  # Campos exibidos na lista
    search_fields = ('nome_completo', 'numero_identificacao', 'cpf', 'patente', 'unidade')  # Campos para busca
    list_filter = ('patente', 'unidade', 'status')  # Filtros laterais
    ordering = ['nome_completo']  # Ordenação padrão
    fieldsets = (
        ('Dados Pessoais', {
            'fields': ('nome_completo', 'numero_identificacao', 'cpf', 'data_nascimento')
        }),
        ('Informações de Contato', {
            'fields': ('telefone', 'email', 'endereco')
        }),
        ('Dados de Serviço', {
            'fields': ('patente', 'unidade', 'data_ingresso', 'lotacao_atual')
        }),
        ('Situação na Corporação', {
            'fields': ('status',)
        }),
        ('Outros Dados', {
            'fields': ('observacoes',)
        }),
    )

