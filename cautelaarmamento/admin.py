from django.contrib import admin
from .models import PolicialMilitar, Categoria, Armas, Vtr, Cautela

@admin.register(PolicialMilitar)
class PolicialMilitarAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'patente')
    search_fields = ('nome', 'matricula', 'patente')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Armas)
class ArmasAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'modelo', 'numero_de_serie', 'disponivel', 'categoria')
    search_fields = ('tipo', 'modelo', 'numero_de_serie')
    list_filter = ('disponivel', 'categoria')

@admin.register(Vtr)
class VtrAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'placa', 'disponivel')
    search_fields = ('modelo', 'placa')
    list_filter = ('disponivel',)

@admin.register(Cautela)
class CautelaAdmin(admin.ModelAdmin):
    list_display = ('policial', 'armamento', 'data_cautela', 'data_descautela')
    search_fields = ('policial__nome', 'armamento__tipo')
    list_filter = ('data_cautela', 'data_descautela')

