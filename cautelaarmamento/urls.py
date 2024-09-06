# from django.urls import path
# from .views import (
#     registro_view, 
#     inventario_equipamentos, 
#     cautela_de_armamento_view, 
#     formulario_sucesso, 
#     descautelar_armamento, 
#     listar_armamentos, 
#     get_subcategorias,
#     cadastrar_pessoa,  
#     sucesso_view, atualizar_subcategorias,cautela_municoes,obter_subcategorias  # Renomeado para evitar conflito
# )

# urlpatterns = [
#     path('registro/', registro_view, name='registro'),
#     path('inventario/', inventario_equipamentos, name='inventario_equipamentos'),
#     path('cautela/', cautela_de_armamento_view, name='cautelar_de_armamento'), 
#     path('sucesso/', formulario_sucesso, name='sucesso'),
#     path('descautelar/', descautelar_armamento, name='descautelar_armamento'),
#     path('armamentos/', listar_armamentos, name='listar_armamentos'),
#     path('subcategorias/<int:categoria_id>/', get_subcategorias, name='subcategorias_por_categoria'),
#     path('cadastrar-pessoa/', cadastrar_pessoa, name='cadastrar_pessoa'),
#     path('sucesso-cadastro/', sucesso_view, name='sucesso_cadastro'),  # Corrigido para referenciar a função correta
#     path('atualizar_subcategorias/', atualizar_subcategorias, name='atualizar_subcategorias'),
#     path('cautela-municoes/', cautela_municoes, name='cautela_municoes'),
#     path('subcategorias1/<int:categoria_id>/', obter_subcategorias, name='obter_subcategorias'),
#     path('subcategorias/<int:categoria_id>/', get_subcategorias, name='get_subcategorias'),
#     path('atualizar-subcategorias/', atualizar_subcategorias, name='atualizar_subcategorias'),
# ]
######################################################

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
    sucesso_view, 
    atualizar_subcategorias,
    cautela_municoes,
    obter_subcategorias  
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
    path('sucesso-cadastro/', sucesso_view, name='sucesso_cadastro'),
    path('atualizar_subcategorias/', atualizar_subcategorias, name='atualizar_subcategorias'),
    path('cautela-municoes/', cautela_municoes, name='cautela_municoes'),
    path('subcategorias-municoes/<int:categoria_id>/', obter_subcategorias, name='obter_subcategorias_municoes'),
]
