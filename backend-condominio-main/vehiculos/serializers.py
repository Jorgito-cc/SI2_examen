from rest_framework import serializers
from .models import Vehiculo, AccesoQR
from authx.models import Usuario



class VehiculoSerializer(serializers.ModelSerializer):
    usuario_info = serializers.StringRelatedField(source='usuario', read_only=True)
    usuario = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all(), required=False
    )  # Ya no es obligatorio

    class Meta:
        model = Vehiculo
        fields = ['id', 'placa', 'marca', 'modelo', 'color', 'usuario', 'usuario_info']
    
    def validate_placa(self, value):
        if not value.strip():
            raise serializers.ValidationError("La placa no puede estar vacía")
        return value.upper().strip()
    
    def create(self, validated_data):
        request = self.context.get('request')
        # Si no se especifica usuario, se asigna el usuario autenticado
        if 'usuario' not in validated_data:
            validated_data['usuario'] = request.user
        return Vehiculo.objects.create(**validated_data)
    
    
    
#---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
# accesos/serializers.py


class AccesoQRReadSerializer(serializers.ModelSerializer):
    vehiculo_id = serializers.PrimaryKeyRelatedField(source='vehiculo', read_only=True)
    vehiculo_label = serializers.SerializerMethodField()

    class Meta:
        model = AccesoQR
        fields = [
            'id', 'codigo', 'tipo', 'estado',
            'creado_en', 'actualizado_en', 'valido_hasta', 'usado_en',
            'vehiculo_id', 'vehiculo_label',
        ]

    def get_vehiculo_label(self, obj):
        # Ajusta si tu modelo Vehiculo usa otro campo (ej. 'placa')
        placa = getattr(obj.vehiculo, 'placa', None)
        return f"{placa}" if placa else str(obj.vehiculo)


class AccesoQRWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccesoQR
        fields = [
            'id', 'codigo', 'tipo', 'estado',
            'valido_hasta',
            'vehiculo',
        ]
        read_only_fields = ['id']

    def validate(self, attrs):
        # Validaciones de consistencia simples
        tipo = attrs.get('tipo', getattr(self.instance, 'tipo', None))
        estado = attrs.get('estado', getattr(self.instance, 'estado', None))
        if tipo not in dict(AccesoQR.TIPOS).keys():
            raise serializers.ValidationError({"tipo": "Tipo inválido."})
        if estado not in dict(AccesoQR.ESTADOS).keys():
            raise serializers.ValidationError({"estado": "Estado inválido."})
        return attrs






