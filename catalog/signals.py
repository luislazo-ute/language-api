from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from catalog.models import UserProfile

User = get_user_model()


@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    """Crea automáticamente un UserProfile cuando se registra un User."""
    if created:
        UserProfile.objects.get_or_create(user=instance)
