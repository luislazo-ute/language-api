from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from catalog.models import Level
from catalog.serializers.level import LevelSerializer
from catalog.permissions import IsAdminOrReadOnly
from catalog.filters import LevelFilter


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.select_related('language').all()
    serializer_class = LevelSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = LevelFilter
    search_fields = ['nombre', 'codigo_cefr']
    ordering_fields = ['id', 'orden', 'nombre']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return super().get_permissions()
