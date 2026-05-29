from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
 
from .models import (
    Language, Level, Lesson, Exercise,
    UserProfile, Enrollment, UserProgress
)
from .serializers import (
    LanguageSerializer, LevelSerializer, LessonSerializer,
    ExerciseSerializer, ExercisePublicSerializer,
    UserProfileSerializer, EnrollmentSerializer, UserProgressSerializer,
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all().order_by('nombre')
    serializer_class = LanguageSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['activo']
    search_fields = ['nombre', 'codigo']
    ordering_fields = ['id', 'nombre', 'codigo']
 
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return super().get_permissions()


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.select_related('language').all()
    serializer_class = LevelSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['language', 'codigo_cefr']
    search_fields = ['nombre', 'codigo_cefr']
    ordering_fields = ['id', 'orden', 'nombre']
 
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return super().get_permissions()
 
 
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.select_related('level__language').all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['level']
    search_fields = ['titulo', 'descripcion']
    ordering_fields = ['id', 'orden', 'titulo']
 
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return super().get_permissions()


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.select_related('lesson__level__language').all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['lesson', 'tipo']
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

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['language', 'level']
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

class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['level', 'completado']
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

class UserProgressViewSet(viewsets.ModelViewSet):
    serializer_class = UserProgressSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['exercise', 'correcto']
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
