from django.urls import path
from .views import registro_view, inventario_equipamentos, cautelar_de_armamento, formulario_sucesso, descautelar_armamento, listar_armamentos

urlpatterns = [
    path('registro/', registro_view, name='registro'),
    path('inventario/', inventario_equipamentos, name='inventario_equipamentos'),
    path('cautela/', cautelar_de_armamento, name='cautelar_de_armamento'), 
    path('sucesso/', formulario_sucesso, name='formulario_sucesso'),
    path('descautelar/', descautelar_armamento, name='descautelar_armamento'),
    path('armamentos/', listar_armamentos, name='listar_armamentos'),
]
