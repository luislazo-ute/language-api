from django.db import models
from .level import Level


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
