from django.urls import path
from .views import (
    registro_view, 
    inventario_equipamentos, 
    cautela_de_armamento_view, 
    formulario_sucesso, 
    descautelar_armamento, 
    listar_armamentos, 
    get_subcategorias,
    cadastrar_pessoa,  
    sucesso_view, atualizar_subcategorias  # Renomeado para evitar conflito
)

urlpatterns = [
    path('registro/', registro_view, name='registro'),
    path('inventario/', inventario_equipamentos, name='inventario_equipamentos'),
    path('cautela/', cautela_de_armamento_view, name='cautelar_de_armamento'), 
    path('sucesso/', formulario_sucesso, name='sucesso'),
    path('descautelar/', descautelar_armamento, name='descautelar_armamento'),
    path('armamentos/', listar_armamentos, name='listar_armamentos'),
    path('subcategorias/<int:categoria_id>/', get_subcategorias, name='subcategorias_por_categoria'),
    path('cadastrar-pessoa/', cadastrar_pessoa, name='cadastrar_pessoa'),
    path('sucesso-cadastro/', sucesso_view, name='sucesso_cadastro'),  # Corrigido para referenciar a função correta
    path('atualizar_subcategorias/', atualizar_subcategorias, name='atualizar_subcategorias'),
]
