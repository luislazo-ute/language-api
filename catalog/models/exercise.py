from django.db import models
from .lesson import Lesson


class Exercise(models.Model):
    class Tipo(models.TextChoices):
        MULTIPLE_CHOICE = 'multiple_choice', 'Opcion multiple'
        FILL_BLANK = 'fill_blank', 'Completar espacio'
        TRANSLATE = 'translate', 'Traducir'
        LISTEN = 'listen', 'Escuchar'
        SPEAK = 'speak', 'Hablar'

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
