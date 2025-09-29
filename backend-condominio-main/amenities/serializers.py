# serializers.py
from rest_framework import serializers
from .models import AreaComun

class AreaComunSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaComun
        fields = ['id', 'nombre', 'estado', 'capacidad', 'ubicacion', 'descripcion', 'precio_base']
