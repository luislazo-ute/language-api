from rest_framework import serializers
from .models import (
    Language, Level, Lesson, Exercise,
    UserProfile, Enrollment, UserProgress
)

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'nombre', 'codigo', 'bandera_emoji', 'activo']

class LevelSerializer(serializers.ModelSerializer):
    language_nombre = serializers.CharField(
        source='language.nombre', read_only=True
    )
 
    class Meta:
        model = Level
        fields = ['id', 'language', 'language_nombre', 'nombre',
                  'codigo_cefr', 'orden']

class LessonSerializer(serializers.ModelSerializer):
    level_nombre = serializers.CharField(
        source='level.nombre', read_only=True
    )
 
    class Meta:
        model = Lesson
        fields = ['id', 'level', 'level_nombre', 'titulo',
                  'descripcion', 'orden', 'icono']

class ExerciseSerializer(serializers.ModelSerializer):
    lesson_titulo = serializers.CharField(
        source='lesson.titulo', read_only=True
    )
    tipo_display = serializers.CharField(
        source='get_tipo_display', read_only=True
    )
 
    class Meta:
        model = Exercise
        fields = ['id', 'lesson', 'lesson_titulo', 'tipo', 'tipo_display',
                  'pregunta', 'opciones', 'respuesta_correcta', 'puntos', 'orden']
 
 
class ExercisePublicSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(
        source='get_tipo_display', read_only=True
    )
 
    class Meta:
        model = Exercise
        fields = ['id', 'lesson', 'tipo', 'tipo_display',
                  'pregunta', 'opciones', 'puntos', 'orden']
        # Nota: 'respuesta_correcta' NO esta en la lista

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    language_nombre = serializers.CharField(
        source='language.nombre', read_only=True
    )
    level_nombre = serializers.CharField(
        source='level.nombre', read_only=True
    )
 
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'username', 'email',
                  'language', 'language_nombre',
                  'level', 'level_nombre',
                  'racha_dias', 'xp_total', 'fecha_inicio']
        read_only_fields = ['user', 'racha_dias', 'xp_total', 'fecha_inicio']


class EnrollmentSerializer(serializers.ModelSerializer):
    level_nombre = serializers.CharField(
        source='level.nombre', read_only=True
    )
    language_nombre = serializers.CharField(
        source='level.language.nombre', read_only=True
    )
    username = serializers.CharField(source='user.username', read_only=True)
 
    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'username', 'level', 'level_nombre',
                  'language_nombre', 'inscrito_en', 'completado']
        read_only_fields = ['user', 'inscrito_en']


class UserProgressSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    exercise_pregunta = serializers.CharField(
        source='exercise.pregunta', read_only=True
    )
 
    class Meta:
        model = UserProgress
        fields = ['id', 'user', 'username', 'exercise', 'exercise_pregunta',
                  'correcto', 'puntos_obtenidos', 'completado_en']
        read_only_fields = ['user', 'puntos_obtenidos', 'completado_en']
 
    def validate(self, data):
        exercise = data.get('exercise')
        correcto = data.get('correcto', False)
        if exercise and correcto:
            data['puntos_obtenidos'] = exercise.puntos
        else:
            data['puntos_obtenidos'] = 0
        return data
