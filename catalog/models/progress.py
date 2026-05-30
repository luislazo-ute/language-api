from django.db import models
from django.contrib.auth import get_user_model
from .exercise import Exercise

User = get_user_model()


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
