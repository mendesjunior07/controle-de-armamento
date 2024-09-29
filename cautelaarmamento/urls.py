from django.urls import path
from .views import (
    index,
    cautela_de_armamento_view, 
    cadastrar_pessoa,
    get_subcategorias_armamento,
    get_subcategorias_municao,
    obter_quantidade_total, 
    sucesso_view,
    listar_registros_cautela,  # Esta é a função correta
    descautelar_sa,
    descautelar_ca,
    # atualizar_quantidade_municao,
    # descautelar_municao_ca,
    # atualizar_quantidade_municao
)

urlpatterns = [
    path('', index, name='index'),
    path('sucesso/', sucesso_view, name='sucesso'),
    path('cautela/', cautela_de_armamento_view, name='cautelar_de_armamento'), 
    path('subcategorias_armamento/<int:categoria_id>/', get_subcategorias_armamento, name='get_subcategorias_armamento'),
    path('subcategorias_municao/<int:categoria_id>/', get_subcategorias_municao, name='get_subcategorias_municao'),
    path('cadastrar-pessoa/', cadastrar_pessoa, name='cadastrar_pessoa'),
    path('obter_quantidade_total/<int:subcategoria_id>/', obter_quantidade_total, name='obter_quantidade_total'),
    path('listar_cautelas/', listar_registros_cautela, name='listar_cautelas'),  # Use o nome correto da função
    path('descautelar_sa/', descautelar_sa, name='descautelar_sa'),
    # path('descautelar-ca/', descautelar_ca, name='descautelar_ca'),
    path('descautelar_ca/', descautelar_ca, name='descautelar_ca'),
    # path('atualizar-quantidade-municao/', atualizar_quantidade_municao, name='atualizar_quantidade_municao'),
    # path('sua-url-para-atualizar-quantidade/', atualizar_quantidade_municao, name='atualizar_quantidade_municao'),
    # path('descautelar_municao/', descautelar_municao_ca, name='descautelar_municao_ca'),
]
