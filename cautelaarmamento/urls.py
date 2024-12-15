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
    descautelar_municao_ca,
    itens_disponiveis,
    registrar_passagem,
    listar_inventario_equipamentos,
    listar_cautelas, 
    listar_descautela, 
    gerar_relatorio,
    materiais_alterados,
    restaurar_status,
    verificador_de_autorizacao,
    # gerar_relatorio_docx,
    # atualizar_quantidade_municao,
    # descautelar_municao_ca,
    # atualizar_quantidade_municao,
    
)

urlpatterns = [
    path('', index, name='index'),
    path('gerar_relatorio/', gerar_relatorio, name='gerar_relatorio'),
    path('sucesso/', sucesso_view, name='sucesso'),
    path('cautela/', cautela_de_armamento_view, name='cautelar_de_armamento'), 
    path('subcategorias_armamento/<int:categoria_id>/', get_subcategorias_armamento, name='get_subcategorias_armamento'),
    path('subcategorias_municao/<int:categoria_id>/', get_subcategorias_municao, name='get_subcategorias_municao'),
    path('cadastrar-pessoa/', cadastrar_pessoa, name='cadastrar_pessoa'),
    path('obter_quantidade_total/<int:subcategoria_id>/', obter_quantidade_total, name='obter_quantidade_total'),
    path('listar_cautelas/', listar_registros_cautela, name='listar_cautelas'),  # Use o nome correto da função
    path('descautelar_sa/', descautelar_sa, name='descautelar_sa'),
    # path('inventario_equipamentos/<int:categoria_id>/', listar_inventario_equipamentos, name='inventario_equipamentos'),
    path('inventario_equipamentos/', listar_inventario_equipamentos, name='inventario_equipamentos'),
    # path('descautelar-ca/', descautelar_ca, name='descautelar_ca'),
    path('descautelar_ca/', descautelar_ca, name='descautelar_ca'),
    path('descautelar-municao/', descautelar_municao_ca, name='descautelar_municao_ca'),
    # path('atualizar-quantidade-municao/', atualizar_quantidade_municao, name='atualizar_quantidade_municao'),
    # path('sua-url-para-atualizar-quantidade/', atualizar_quantidade_municao, name='atualizar_quantidade_municao'),
    # path('descautelar_municao/', descautelar_municao_ca, name='descautelar_municao_ca'),
    path('itens-disponiveis/', itens_disponiveis, name='itens_disponiveis'),
    path('registrar_passagem/', registrar_passagem, name='registrar_passagem'),
    path('listar_armas_cauteladas/', listar_cautelas, name='listar_armas_cauteladas'),
    path('listar_armas_descauteladas/', listar_descautela, name='listar_armas_descauteladas'),
    path('listar_materiais_alterados/', materiais_alterados, name='listar_materiais_alterados'),
    path('restaurar_status/<int:material_id>/', restaurar_status, name='restaurar_status'),
    path('verificar_autorizacao/', verificador_de_autorizacao, name='verificar_autorizacao'),
    # path('gerar_relatorio/', gerar_relatorio_docx, name='gerar_relatorio'),
]
