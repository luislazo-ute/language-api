from rest_framework import serializers
from catalog.models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    level_nombre = serializers.CharField(
        source='level.nombre', read_only=True
    )

    class Meta:
        model = Lesson
        fields = ['id', 'level', 'level_nombre', 'titulo',
                  'descripcion', 'orden', 'icono']
