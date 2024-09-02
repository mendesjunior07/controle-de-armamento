from django.urls import path
from .views import registro_view, inventario_equipamentos, cautela_de_armamento_view, formulario_sucesso, descautelar_armamento, listar_armamentos,get_subcategorias

urlpatterns = [
    path('registro/', registro_view, name='registro'),
    path('inventario/', inventario_equipamentos, name='inventario_equipamentos'),
    path('cautela/', cautela_de_armamento_view, name='cautelar_de_armamento'), 
    path('sucesso/', formulario_sucesso, name='sucesso'),
    path('descautelar/', descautelar_armamento, name='descautelar_armamento'),
    path('armamentos/', listar_armamentos, name='listar_armamentos'),
    path('subcategorias/<int:categoria_id>/', get_subcategorias, name='subcategorias_por_categoria'),

]

    # path('', views.index, name='index'),
    # path('subcategorias/<int:categoria_id>/', views.subcategorias_json, name='subcategorias_json'),