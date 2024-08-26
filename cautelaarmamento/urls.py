from django.urls import path
from .views import registro_view, inventario_equipamentos, cautela_de_armamento, formulario_sucesso, descautelar_armamento

urlpatterns = [
    path('registro/', registro_view, name='registro'),
    path('inventario/', inventario_equipamentos, name='inventario_equipamentos'),
    path('cautela/', cautela_de_armamento, name='cautela_de_armamento'), 
    path('sucesso/', formulario_sucesso, name='formulario_sucesso'),# Nov
    path('descautelar/', descautelar_armamento, name='descautelar_armamento'),
]
