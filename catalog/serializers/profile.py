from rest_framework import serializers
from catalog.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    is_staff = serializers.BooleanField(source='user.is_staff', read_only=True)
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
                  'racha_dias', 'xp_total', 'fecha_inicio',
                  'is_staff']
        read_only_fields = ['user', 'racha_dias', 'xp_total', 'fecha_inicio']
