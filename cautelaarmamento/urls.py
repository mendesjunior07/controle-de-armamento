from django.urls import path
from .views import registro_view, inventario_equipamentos

urlpatterns = [
    path('registro/', registro_view, name='registro'),
    path('inventario/', inventario_equipamentos, name='inventario_equipamentos'),
]
