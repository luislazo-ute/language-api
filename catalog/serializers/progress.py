from rest_framework import serializers
from catalog.models import UserProgress


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
