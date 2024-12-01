from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import datetime
from django.core.validators import MinValueValidator
from decimal import Decimal


class CustomUser(AbstractUser):
    ROLES = (
        ('SUPER_ADMIN', 'Super Administrador'),
        ('ADMIN', 'Administrador'),
        ('COACH', 'Entrenador'),
        ('PLAYER', 'Jugador'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='PLAYER')

    is_active = models.BooleanField(default=True)
    nombre  = models.CharField(max_length=120, verbose_name="Nombre", blank=True)
    apellido = models.CharField(max_length=120, verbose_name="Apellidos", blank=True)
    fecha_nacimiento = models.DateField(default=datetime.now())
    peso = models.FloatField(help_text="Peso en Kilogramos", null=True)
    estatura = models.FloatField(help_text="Estatura en Centimetros", null=True)
    nombre_disciplina = models.ForeignKey("Discipline",on_delete=models.CASCADE, related_name='customuser', default=1, blank=True)
        
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
    


class PerformanceMetric(models.Model):
    # Definición de las posibles posiciones en un equipo deportivo
    POSITION_CHOICES = [
        ('FORWARD', 'Delantero'),     # Jugadores de ataque
        ('MIDFIELDER', 'Mediocampista'),  # Jugadores de medio campo
        ('DEFENDER', 'Defensa'),      # Jugadores defensivos
        ('GOALKEEPER', 'Portero')     # Portero/Guardameta
    ]
    
    # Relación con el modelo de usuario personalizado
    # CASCADE: Si se elimina el usuario, se eliminan todas sus métricas
    athlete = models.ForeignKey(
        CustomUser,  # Reemplazar con el modelo de usuario real
        on_delete=models.CASCADE, 
        related_name='performance_metrics'  # Nombre para acceder a las métricas desde el usuario
    )
    
    # Relación con el modelo de disciplina/deporte
    sport = models.ForeignKey(
        Discipline,  # Reemplazar con el modelo de deporte real
        on_delete=models.CASCADE, 
        related_name='performance_metrics'
    )
    
    # Metros recorridos durante el encuentro
    # DecimalField para precisión decimal
    meters_covered = models.DecimalField(
        max_digits=8,           # Número máximo de dígitos
        decimal_places=2,       # Número de decimales
        validators=[MinValueValidator(0)],  # No se permiten valores negativos
        help_text="Metros recorridos durante el encuentro"
    )
    
    # Número de goles anotados
    goals_scored = models.IntegerField(
        default=0,               # Valor por defecto
        validators=[MinValueValidator(0)],  # Solo valores positivos
        help_text="Número de goles anotados"
    )
    
    # Número de pases interceptados
    intercepted_passes = models.IntegerField(
        default=0, 
        validators=[MinValueValidator(0)],
        help_text="Número de pases interceptados"
    )
    
    # Número de pases exitosos
    successful_passes = models.IntegerField(
        default=0, 
        validators=[MinValueValidator(0)],
        help_text="Número de pases dados exitosamente"
    )
    
    # Fecha y hora del encuentro
    match_date = models.DateTimeField(
        help_text="Fecha y hora del encuentro"
    )
    
    # Posición sugerida basada en el análisis de rendimiento
    suggested_position = models.CharField(
        max_length=20,           # Longitud máxima del texto
        choices=POSITION_CHOICES,  # Usar las opciones predefinidas
        null=True,               # Permite valores nulos en la base de datos
        blank=True,              # Permite dejar el campo vacío en formularios
        help_text="Posición sugerida basada en el análisis de rendimiento"
    )
    
    # Puntuación general de rendimiento
    performance_score = models.DecimalField(
        max_digits=5,            # Número máximo de dígitos
        decimal_places=2,        # Número de decimales
        null=True,               # Permite valores nulos
        blank=True,              # Permite dejar el campo vacío
        help_text="Puntuación general de rendimiento"
    )
    
    # Marcas de tiempo para seguimiento
    created_at = models.DateTimeField(auto_now_add=True)  # Se establece al crear el registro
    updated_at = models.DateTimeField(auto_now=True)      # Se actualiza en cada guardado
    
    def calculate_performance_score(self):
        """
        Calcula la puntuación de rendimiento basada en diferentes métricas.
        
        Fórmula de puntuación:
        - 10 puntos por kilómetro recorrido
        - 20 puntos por gol
        - 5 puntos por pase interceptado
        - 3 puntos por cada 10 pases exitosos
        """
        # Cálculo de la puntuación
        score = (
            (self.meters_covered / Decimal('1000')) * Decimal('10') +  # Kilómetros recorridos
            self.goals_scored * Decimal('20') +  # Goles
            self.intercepted_passes * Decimal('5') +  # Pases interceptados
            (self.successful_passes / Decimal('10')) * Decimal('3')  # Pases exitosos
        )
        
        # Redondear y guardar la puntuación
        self.performance_score = round(score, 2)
        self.save()
        return self.performance_score
    
    def determine_optimal_position(self):
        """
        Determina la posición óptima basada en estadísticas de rendimiento.
        
        Criterios:
        - Más de 5 goles → Delantero
        - Más de 10 pases interceptados → Mediocampista
        - Más de 20 pases exitosos → Defensa
        """
        # Calcular puntuación si no existe
        if not self.performance_score:
            self.calculate_performance_score()
        
        # Lógica de sugerencia de posición
        if self.goals_scored > 5:
            self.suggested_position = 'FORWARD'
        elif self.intercepted_passes > 10:
            self.suggested_position = 'MIDFIELDER'
        elif self.successful_passes > 20:
            self.suggested_position = 'DEFENDER'
        
        # Guardar cambios
        self.save()
        return self.suggested_position
    
    def __str__(self):
        """
        Representación en cadena del objeto.
        Muestra el nombre de usuario y el deporte.
        """
        return f"{self.athlete.username} - {self.sport.name} Performance"
    
    class Meta:
        """
        Metadatos del modelo para configuraciones adicionales.
        """
        verbose_name = "Métrica de Rendimiento"
        verbose_name_plural = "Métricas de Rendimiento"
        ordering = ['-match_date']  # Ordenar por fecha de encuentro descendente