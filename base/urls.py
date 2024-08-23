from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from cautelaarmamento import views as cautelaarmamento_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='cautelaarmamento/login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='cautelaarmamento/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('index/', cautelaarmamento_views.index, name='index'),
    path('', include('cautelaarmamento.urls')),  # Inclua as URLs do app 'cautelaarmamento'
]
