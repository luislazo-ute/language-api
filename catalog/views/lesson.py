from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from catalog.models import Lesson
from catalog.serializers.lesson import LessonSerializer
from catalog.permissions import IsAdminOrReadOnly
from catalog.filters import LessonFilter


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.select_related('level__language').all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = LessonFilter
    search_fields = ['titulo', 'descripcion']
    ordering_fields = ['id', 'orden', 'titulo']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return super().get_permissions()
