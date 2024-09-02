# base/app/admin.py
from django.contrib import admin
from .models import Categoria, Subcategoria, CautelaDeArmamento, Policial

admin.site.register(Categoria)
admin.site.register(Subcategoria)
admin.site.register(CautelaDeArmamento)
admin.site.register(Policial)