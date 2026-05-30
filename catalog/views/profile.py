from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from catalog.models import UserProfile
from catalog.serializers.profile import UserProfileSerializer
from catalog.permissions import IsOwnerOrAdmin
from catalog.filters import UserProfileFilter


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = UserProfileFilter
    search_fields = ['user__username']
    ordering_fields = ['xp_total', 'racha_dias', 'fecha_inicio']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return UserProfile.objects.select_related(
                'user', 'language', 'level'
            ).all()
        return UserProfile.objects.select_related(
            'user', 'language', 'level'
        ).filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        '''GET /api/profiles/me/ - perfil del usuario autenticado'''
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            return Response(
                {'detail': 'Perfil no encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
