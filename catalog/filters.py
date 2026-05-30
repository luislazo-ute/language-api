import django_filters
from catalog.models import (
    Language, Level, Lesson, Exercise,
    UserProfile, Enrollment, UserProgress,
)


class LanguageFilter(django_filters.FilterSet):
    class Meta:
        model = Language
        fields = ['activo']


class LevelFilter(django_filters.FilterSet):
    class Meta:
        model = Level
        fields = ['language', 'codigo_cefr']


class LessonFilter(django_filters.FilterSet):
    class Meta:
        model = Lesson
        fields = ['level']


class ExerciseFilter(django_filters.FilterSet):
    class Meta:
        model = Exercise
        fields = ['lesson', 'tipo']


class UserProfileFilter(django_filters.FilterSet):
    class Meta:
        model = UserProfile
        fields = ['language', 'level']


class EnrollmentFilter(django_filters.FilterSet):
    class Meta:
        model = Enrollment
        fields = ['level', 'completado']


class UserProgressFilter(django_filters.FilterSet):
    class Meta:
        model = UserProgress
        fields = ['exercise', 'correcto']
