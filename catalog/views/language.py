from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from catalog.models import Language
from catalog.serializers.language import LanguageSerializer
from catalog.permissions import IsAdminOrReadOnly
from catalog.filters import LanguageFilter


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all().order_by('nombre')
    serializer_class = LanguageSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = LanguageFilter
    search_fields = ['nombre', 'codigo']
    ordering_fields = ['id', 'nombre', 'codigo']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return super().get_permissions()
