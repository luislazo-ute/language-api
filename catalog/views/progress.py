from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from catalog.models import UserProgress, UserProfile
from catalog.serializers.progress import UserProgressSerializer
from catalog.permissions import IsOwnerOrAdmin
from catalog.filters import UserProgressFilter


class UserProgressViewSet(viewsets.ModelViewSet):
    serializer_class = UserProgressSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = UserProgressFilter
    ordering_fields = ['completado_en', 'puntos_obtenidos']
    http_method_names = ['get', 'post', 'head', 'options']  # Sin PUT/PATCH/DELETE

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return UserProgress.objects.select_related(
                'user', 'exercise'
            ).all()
        return UserProgress.objects.select_related(
            'user', 'exercise'
        ).filter(user=user)

    def perform_create(self, serializer):
        progress = serializer.save(user=self.request.user)
        # Si fue correcto, sumar XP al perfil
        if progress.correcto:
            try:
                profile = self.request.user.profile
                profile.xp_total += progress.puntos_obtenidos
                profile.save(update_fields=['xp_total'])
            except UserProfile.DoesNotExist:
                pass
