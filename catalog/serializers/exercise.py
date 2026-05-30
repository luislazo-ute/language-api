from rest_framework import serializers
from catalog.models import Exercise


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
