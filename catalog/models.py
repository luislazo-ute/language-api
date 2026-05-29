from django.db import models
from django.contrib.auth import get_user_model
 
User = get_user_model()

class Language(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)  # 'en', 'fr', 'de'
    bandera_emoji = models.CharField(max_length=10, blank=True, default='')
    activo = models.BooleanField(default=True)
 
    def __str__(self):
        return f'{self.bandera_emoji} {self.nombre} ({self.codigo})'
 
    class Meta:
        ordering = ['nombre']

class Level(models.Model):
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name='levels'
    )
    nombre = models.CharField(max_length=100)
    codigo_cefr = models.CharField(max_length=5, blank=True, default='')  # A1, B2
    orden = models.IntegerField(default=0)
 
    def __str__(self):
        return f'{self.language.nombre} - {self.nombre} ({self.codigo_cefr})'
 
    class Meta:
        ordering = ['language', 'orden']
        unique_together = ['language', 'orden']


class Lesson(models.Model):
    level = models.ForeignKey(
        Level, on_delete=models.CASCADE, related_name='lessons'
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, default='')
    orden = models.IntegerField(default=0)
    icono = models.CharField(max_length=50, blank=True, default='')
 
    def __str__(self):
        return f'{self.level} - {self.titulo}'
 
    class Meta:
        ordering = ['level', 'orden']
        unique_together = ['level', 'orden']


class Exercise(models.Model):
    class Tipo(models.TextChoices):
        MULTIPLE_CHOICE = 'multiple_choice', 'Opcion multiple'
        FILL_BLANK     = 'fill_blank',      'Completar espacio'
        TRANSLATE      = 'translate',       'Traducir'
        LISTEN         = 'listen',           'Escuchar'
        SPEAK          = 'speak',            'Hablar'
 
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='exercises'
    )
    tipo = models.CharField(
        max_length=20, choices=Tipo.choices, default=Tipo.MULTIPLE_CHOICE
    )
    pregunta = models.TextField()
    opciones = models.JSONField(default=list, blank=True)
    respuesta_correcta = models.TextField()
    puntos = models.IntegerField(default=10)
    orden = models.IntegerField(default=0)
 
    def __str__(self):
        return f'[{self.get_tipo_display()}] {self.pregunta[:60]}'
 
    class Meta:
        ordering = ['lesson', 'orden']


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    language = models.ForeignKey(
        Language, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='learners'
    )
    level = models.ForeignKey(
        Level, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='current_users'
    )
    racha_dias = models.IntegerField(default=0)
    xp_total = models.IntegerField(default=0)
    fecha_inicio = models.DateField(auto_now_add=True)
 
    def __str__(self):
        return f'Perfil de {self.user.username}'

class Enrollment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='enrollments'
    )
    level = models.ForeignKey(
        Level, on_delete=models.CASCADE, related_name='enrollments'
    )
    inscrito_en = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False)
 
    def __str__(self):
        return f'{self.user.username} -> {self.level}'
 
    class Meta:
        unique_together = ['user', 'level']  # Un usuario, una inscripcion por nivel
        ordering = ['-inscrito_en']


class UserProgress(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='progress'
    )
    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, related_name='attempts'
    )
    correcto = models.BooleanField(default=False)
    puntos_obtenidos = models.IntegerField(default=0)
    completado_en = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        estado = 'correcto' if self.correcto else 'incorrecto'
        return f'{self.user.username} - Ejercicio {self.exercise_id} - {estado}'
 
    class Meta:
        ordering = ['-completado_en']

