from django.urls import path
from .views import registro_view, inventario_equipamentos, cautela_de_armamento

urlpatterns = [
    path('registro/', registro_view, name='registro'),
    path('inventario/', inventario_equipamentos, name='inventario_equipamentos'),
    path('cautela/', cautela_de_armamento, name='cautela_de_armamento'),  # Nova URL adicionada
]
