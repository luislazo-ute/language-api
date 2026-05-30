from rest_framework import serializers
from catalog.models import Enrollment


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
