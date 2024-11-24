from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

# Create your models here.
class Verificacion(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=10) # por que un numero tiene solo 10 digitos
    programa_academico = models.CharField(max_length=255)
    contrasena = models.CharField(max_length=6, unique=True, validators=[MinLengthValidator(6)])
    rfid = models.CharField(max_length=50, null=True, blank=True)
    lab_vision = models.BooleanField(default=False)
    lab_robotica = models.BooleanField(default=False)
    salon_210 = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.usuario.username} \n {self.nombre_completo} \n {self.programa_academico}'
    
    
class RegistroAcceso(models.Model):
    verificacion = models.ForeignKey(Verificacion, on_delete=models.SET_NULL, null=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.verificacion.nombre_completo} ingreso a esta hora {self.fecha_hora}'