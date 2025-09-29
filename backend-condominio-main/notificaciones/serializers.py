from rest_framework import serializers
from .models import Notificacion
from authx.serializers import UsuarioReadSerializer  # si ya lo tienes

class NotificacionSerializer(serializers.ModelSerializer):
    # lectura bonita del usuario
    usuario = UsuarioReadSerializer(read_only=True)
    # permitir setear por id (solo admins)
    usuario_id = serializers.PrimaryKeyRelatedField(
        source='usuario',
        queryset=UsuarioReadSerializer.Meta.model.objects.all(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Notificacion
        fields = [
            'id',
            'usuario', 'usuario_id',
            'titulo', 'poligono', 'descripcion',
            'leido', 'creado_en'
        ]
        read_only_fields = ['id', 'creado_en']
