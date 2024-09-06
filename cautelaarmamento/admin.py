from django.contrib import admin
from .models import Categoria, Subcategoria, Policial, CautelaDeArmamento, CategoriaMunicao, SubcategoriaMunicao, CautelaDeMunicoes

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    ordering = ('nome',)

@admin.register(Subcategoria)
class SubcategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'situacao')
    list_filter = ('categoria', 'situacao')
    search_fields = ('nome',)
    ordering = ('categoria', 'nome',)

@admin.register(Policial)
class PolicialAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'nome_guerra', 'posto_graduacao', 'matricula', 'rgpm', 'lotacao', 'data_nascimento', 'cpf')
    search_fields = ('nome_completo', 'matricula', 'rgpm', 'cpf')
    list_filter = ('posto_graduacao', 'lotacao')
    ordering = ('nome_completo',)

@admin.register(CautelaDeArmamento)
class CautelaDeArmamentoAdmin(admin.ModelAdmin):
    list_display = ('policial', 'categoria', 'subcategoria', 'tipo_servico', 'data', 'hora')
    list_filter = ('policial', 'categoria', 'subcategoria', 'tipo_servico', 'data')
    search_fields = ('policial__nome_completo', 'categoria__nome', 'subcategoria__nome')
    ordering = ('data', 'hora',)

@admin.register(CategoriaMunicao)
class CategoriaMunicaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    ordering = ('nome',)

@admin.register(SubcategoriaMunicao)
class SubcategoriaMunicaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'total_de_municoes')
    list_filter = ('categoria',)
    search_fields = ('nome',)
    ordering = ('categoria', 'nome',)

@admin.register(CautelaDeMunicoes)
class CautelaDeMunicoesAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'subcategoria', 'quantidade')
    list_filter = ('categoria', 'subcategoria')
    search_fields = ('categoria__nome', 'subcategoria__nome')
    ordering = ('categoria', 'subcategoria',)

