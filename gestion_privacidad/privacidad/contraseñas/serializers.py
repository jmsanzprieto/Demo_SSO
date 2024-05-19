from rest_framework import serializers
from .models import Contraseñas

class ContraseñasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contraseñas
        fields = ['id', 'user', 'service', 'password']
