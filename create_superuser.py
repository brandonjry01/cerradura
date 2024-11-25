from django.contrib.auth.models import User

# Verifica si ya existe un superusuario
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin1234'
    )
    print("Superusuario creado exitosamente.")
else:
    print("Ya existe un superusuario.")