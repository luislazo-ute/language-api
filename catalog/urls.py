from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from catalog.views.health import health_check
from catalog.views.auth import register_view
from catalog.views.language import LanguageViewSet
from catalog.views.level import LevelViewSet
from catalog.views.lesson import LessonViewSet
from catalog.views.exercise import ExerciseViewSet
from catalog.views.profile import UserProfileViewSet
from catalog.views.enrollment import EnrollmentViewSet
from catalog.views.progress import UserProgressViewSet

router = DefaultRouter()
router.register(r'languages',   LanguageViewSet,    basename='languages')
router.register(r'levels',      LevelViewSet,       basename='levels')
router.register(r'lessons',     LessonViewSet,      basename='lessons')
router.register(r'exercises',   ExerciseViewSet,    basename='exercises')
router.register(r'profiles',    UserProfileViewSet, basename='profiles')
router.register(r'enrollments', EnrollmentViewSet,  basename='enrollments')
router.register(r'progress',    UserProgressViewSet, basename='progress')

urlpatterns = [
    path('health/', health_check, name='health'),
    path('auth/register/', register_view, name='register'),
    path('auth/login/',    TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/',  TokenRefreshView.as_view(),    name='refresh'),
    path('', include(router.urls)),
]
