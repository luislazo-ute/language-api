from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    LanguageViewSet, LevelViewSet, LessonViewSet,
    ExerciseViewSet, UserProfileViewSet,
    EnrollmentViewSet, UserProgressViewSet,
)
 
router = DefaultRouter()
router.register(r'languages',   LanguageViewSet,    basename='languages')
router.register(r'levels',      LevelViewSet,       basename='levels')
router.register(r'lessons',     LessonViewSet,      basename='lessons')
router.register(r'exercises',   ExerciseViewSet,    basename='exercises')
router.register(r'profiles',    UserProfileViewSet, basename='profiles')
router.register(r'enrollments', EnrollmentViewSet,  basename='enrollments')
router.register(r'progress',    UserProgressViewSet,basename='progress')
 
urlpatterns = []
urlpatterns += router.urls
