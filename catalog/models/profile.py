from django.db import models
from django.contrib.auth import get_user_model
from .language import Language
from .level import Level

User = get_user_model()


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
