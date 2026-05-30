from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from catalog.models import Exercise
from catalog.serializers.exercise import (
    ExerciseSerializer, ExercisePublicSerializer
)
from catalog.permissions import IsAdminOrReadOnly
from catalog.filters import ExerciseFilter


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.select_related('lesson__level__language').all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ExerciseFilter
    search_fields = ['pregunta']
    ordering_fields = ['id', 'orden', 'puntos']

    def get_serializer_class(self):
        # Admin ve la respuesta correcta, usuarios normales no
        if self.request.user.is_staff:
            return ExerciseSerializer
        return ExercisePublicSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]  # Solo usuarios logueados
        return super().get_permissions()
