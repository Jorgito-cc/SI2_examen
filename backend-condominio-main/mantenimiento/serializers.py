from rest_framework import serializers
from .models import Mantenimiento, Servicio
from authx.models import Personal
from authx.serializers import UsuarioReadSerializer  # el que sí existe


class PersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personal
        fields = '__all__'


class MantenimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mantenimiento
        fields = '__all__'
        
        
        
        
    
class ServiciosSerializer(serializers.ModelSerializer):
    # Mostrar información del usuario (solo lectura)
    usuario = UsuarioReadSerializer(read_only=True)
    
    # Permitir asignar el usuario por ID al crear o actualizar
    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=UsuarioReadSerializer.Meta.model.objects.all(),
        source='usuario',
        write_only=True
    )

    class Meta:
        model = Servicio
        fields = ['id', 'usuario', 'usuario_id', 'nombre', 'descripcion']