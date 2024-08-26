from django.contrib import admin
from .models import Armas, Municoes, Cautela, PolicialMilitar, Vtr, Bicicleta, Moto

@admin.register(Armas)
class ArmasAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'marca', 'modelo', 'calibre', 'numero_arma', 'localizacao', 'cautelado']
    search_fields = ['tipo', 'marca', 'modelo', 'numero_arma']
    list_filter = ['marca', 'calibre', 'cautelado']
    ordering = ['tipo', 'marca', 'modelo']

@admin.register(Municoes)
class MunicoesAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'calibre', 'data_recebimento', 'saldo', 'cautelado']
    search_fields = ['tipo', 'calibre', 'referencia']
    list_filter = ['calibre', 'data_recebimento', 'cautelado']
    ordering = ['tipo', 'calibre', 'data_recebimento']

@admin.register(Cautela)
class CautelaAdmin(admin.ModelAdmin):
    list_display = ['policial_militar', 'arma', 'municao', 'vtr', 'bicicleta', 'moto', 'data_cautela', 'cautelado']
    search_fields = ['policial_militar__nome_completo', 'arma__modelo', 'vtr__modelo', 'bicicleta__tipo', 'moto__modelo']
    list_filter = ['data_cautela', 'cautelado']
    ordering = ['data_cautela']

@admin.register(PolicialMilitar)
class PolicialMilitarAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'numero_identificacao', 'patente', 'unidade', 'status']
    search_fields = ['nome_completo', 'numero_identificacao', 'cpf']
    list_filter = ['patente', 'unidade', 'status']
    ordering = ['nome_completo']

@admin.register(Vtr)
class VtrAdmin(admin.ModelAdmin):
    list_display = ['marca', 'modelo', 'placa', 'ano', 'situacao', 'cautelado']
    search_fields = ['marca', 'modelo', 'placa']
    list_filter = ['marca', 'situacao', 'cautelado']
    ordering = ['marca', 'modelo', 'ano']

@admin.register(Bicicleta)
class BicicletaAdmin(admin.ModelAdmin):
    list_display = ['marca', 'tipo', 'ano', 'cor', 'tombo', 'situacao', 'cautelado']
    search_fields = ['marca', 'tipo', 'tombo']
    list_filter = ['marca', 'tipo', 'situacao', 'cautelado']
    ordering = ['marca', 'tipo', 'ano']

@admin.register(Moto)
class MotoAdmin(admin.ModelAdmin):
    list_display = ['marca', 'modelo', 'placa', 'ano', 'situacao', 'cautelado']
    search_fields = ['marca', 'modelo', 'placa']
    list_filter = ['marca', 'situacao', 'cautelado']
    ordering = ['marca', 'modelo', 'ano']
