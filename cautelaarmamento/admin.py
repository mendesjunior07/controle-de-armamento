from django.contrib import admin
from .models import Policial, Categoria, Subcategoria, CategoriaMunicao, SubcategoriaMunicao, CautelaDeArmamento, CautelaDeMunicoes

# Registrando o modelo Policial no admin
@admin.register(Policial)
class PolicialAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

# Registrando o modelo Categoria de Armamento no admin
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

# Registrando o modelo Subcategoria de Armamento no admin
@admin.register(Subcategoria)
class SubcategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'categoria', 'situacao')
    search_fields = ('nome',)
    list_filter = ('situacao', 'categoria')

# Registrando o modelo Categoria de Munição no admin
@admin.register(CategoriaMunicao)
class CategoriaMunicaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

# Registrando o modelo Subcategoria de Munição no admin
@admin.register(SubcategoriaMunicao)
class SubcategoriaMunicaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'categoria', 'total_de_municoes')
    search_fields = ('nome',)
    list_filter = ('categoria',)

# Registrando o modelo Cautela de Armamento no admin
@admin.register(CautelaDeArmamento)
class CautelaDeArmamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'policial', 'tipo_servico', 'categoria', 'subcategoria', 'armeiro', 'hora_cautela')
    search_fields = ('policial__nome', 'categoria__nome', 'subcategoria__nome', 'armeiro__username')
    list_filter = ('tipo_servico', 'categoria', 'armeiro', 'hora_cautela')

    # Sobrescrevendo o método save_model para definir o armeiro automaticamente
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Se for um objeto novo, define o armeiro
            obj.armeiro = request.user
        super().save_model(request, obj, form, change)

# Registrando o modelo Cautela de Munições no admin
@admin.register(CautelaDeMunicoes)
class CautelaDeMunicoesAdmin(admin.ModelAdmin):
    list_display = ('id', 'policial', 'categoria', 'subcategoria', 'quantidade')
    search_fields = ('policial__nome', 'categoria__nome', 'subcategoria__nome')
    list_filter = ('categoria',)
