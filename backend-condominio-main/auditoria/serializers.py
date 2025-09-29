from rest_framework import serializers
from .models import Bitacora

class BitacoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bitacora
        fields = ["id", "usuario", "accion", "detalle", "ip", "path", "user_agent", "creado_en"]
        read_only_fields = ["id", "usuario", "ip", "path", "user_agent", "creado_en"]
