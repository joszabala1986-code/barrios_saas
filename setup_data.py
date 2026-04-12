import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import Barrio # Asegurate de que este sea el nombre de tu modelo

User = get_user_model()

# 1. Crear Superusuario si no existe
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'tu_contraseña_segura')
    print("Superusuario creado.")

# 2. Crear Barrio inicial si usas BarrioMiddleware
# Aquí poné los campos que pida tu modelo de Barrio
if hasattr(User, 'barrio'): 
    # Ajustá esto según cómo sea tu modelo de Barrio
    # Ej: b, created = Barrio.objects.get_or_create(nombre="Prueba", dominio="barrios.plantadigital.com.ar")
    print("Asegurate de tener un barrio creado en el panel de Supabase")