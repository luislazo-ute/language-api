from django.db import models


class Language(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)  # 'en', 'fr', 'de'
    bandera_emoji = models.CharField(max_length=10, blank=True, default='')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.bandera_emoji} {self.nombre} ({self.codigo})'

    class Meta:
        ordering = ['nombre']
