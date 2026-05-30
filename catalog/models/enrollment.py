from django.db import models
from django.contrib.auth import get_user_model
from .level import Level

User = get_user_model()


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
