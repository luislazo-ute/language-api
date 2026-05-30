from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from catalog.models import Enrollment
from catalog.serializers.enrollment import EnrollmentSerializer
from catalog.permissions import IsOwnerOrAdmin
from catalog.filters import EnrollmentFilter


class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = EnrollmentFilter
    ordering_fields = ['inscrito_en']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Enrollment.objects.select_related(
                'user', 'level__language'
            ).all()
        return Enrollment.objects.select_related(
            'user', 'level__language'
        ).filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
