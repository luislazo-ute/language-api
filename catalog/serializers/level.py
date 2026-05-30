from rest_framework import serializers
from catalog.models import Level


class LevelSerializer(serializers.ModelSerializer):
    language_nombre = serializers.CharField(
        source='language.nombre', read_only=True
    )

    class Meta:
        model = Level
        fields = ['id', 'language', 'language_nombre', 'nombre',
                  'codigo_cefr', 'orden']
