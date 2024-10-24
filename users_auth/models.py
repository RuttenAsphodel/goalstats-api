from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLES = (
        ('SUPER_ADMIN', 'Super Administrador'),
        ('ADMIN', 'Administrador'),
        ('COACH', 'Entrenador'),
        ('PLAYER', 'Jugador'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='PLAYER')
    
# Hacer despliegue con las disciplinas antes del 25-10-2024    
class Discipline(models.Model):
    nombre_disciplina = models.CharField(max_length=100, verbose_name='Disciplina',default='')
    descripcion = models.TextField(blank=True, verbose_name='Descripcion')

    def __str__(self):
        return self.nombre_disciplina

# Quitar este modelo de datos
# class Athlete(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='athlete')
    # Agregar estos datos para agregarlo en el perfil de usuario con rol "Player"
    # nombre  = models.CharField(max_length=120, verbose_name="Nombre"),
    # apellido = models.CharField(max_length=120, verbose_name="Apellidos"),
    # fecha_nacimiento = models.DateField()
    # peso = models.FloatField(help_text="Peso en Kilogramos")
    # estatura = models.FloatField(help_text="Estatura en Centimetros")
    # nombre_disciplina = models.ForeignKey(Discipline,on_delete=models.CASCADE, related_name='athlete', default=1)
    
    # def __str__(self):
    #     return self.user.username
    

