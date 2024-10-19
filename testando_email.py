import os
import django
from django.core.mail import send_mail

# Defina o módulo de configurações do Django (substitua 'base.settings' pelo caminho correto para seu settings.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

# Inicialize o Django
django.setup()

# Agora você pode usar o Django, incluindo a função send_mail
send_mail(
    'Teste de email',
    'Este é um email de teste.',
    'mendesjunior2007@gmail.com',
    ['mendesjunior2007@hotmail.com'],
    fail_silently=False,
    
)
