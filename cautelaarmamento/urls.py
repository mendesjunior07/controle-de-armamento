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
    index,
    # inventario_equipamentos, 
    cautela_de_armamento_view, 
    # descautelar_armamento, 
    # listar_armamentos, 
    cadastrar_pessoa,
    get_subcategorias_armamento,
    get_subcategorias_municao,
    obter_quantidade_total, sucesso_view,
    listar_registros_cautela
)

urlpatterns = [
    path('', index, name='index'),
    path('sucesso/', sucesso_view, name='sucesso'),
    # path('inventario/', inventario_equipamentos, name='inventario_equipamentos'),
    path('cautela/', cautela_de_armamento_view, name='cautelar_de_armamento'), 
    # path('descautelar/', descautelar_armamento, name='descautelar_armamento'),
    # path('armamentos/', listar_armamentos, name='listar_armamentos'),
    path('subcategorias_armamento/<int:categoria_id>/', get_subcategorias_armamento, name='get_subcategorias_armamento'),
    path('subcategorias_municao/<int:categoria_id>/', get_subcategorias_municao, name='get_subcategorias_municao'),
    path('cadastrar-pessoa/', cadastrar_pessoa, name='cadastrar_pessoa'),
    path('obter_quantidade_total/<int:subcategoria_id>/', obter_quantidade_total, name='obter_quantidade_total'),
    # path('create-cautela/', create_cautela, name='create_cautela'),
    path('listar-cautelas/', listar_registros_cautela, name='listar_cautelas'),
]
