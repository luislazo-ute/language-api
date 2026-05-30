from django.db import models
from .language import Language


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
