from rest_framework import serializers
from .models import Cuota

from django.utils import timezone
from django.db.models import Q
from .models import Reserva

from django.core.exceptions import ValidationError
from .models import Factura



#----------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
class CuotaSerializer(serializers.ModelSerializer):
    # Labels legibles para choices (opcional, útil en list/retrieve)
    tipo_cuota_label = serializers.CharField(source='get_tipo_cuota_display', read_only=True)
    estado_label = serializers.CharField(source='get_estado_display', read_only=True)

    class Meta:
        model = Cuota
        fields = [
            'id',
            'unidad',
            'cantidad_pago',
            'tipo_cuota', 'tipo_cuota_label',
            'fecha_a_pagar',
            'periodo',
            'fecha_vencimiento',
            'estado', 'estado_label',
            'descripcion',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_cantidad_pago(self, v):
        if v < 0:
            raise serializers.ValidationError("El monto no puede ser negativo.")
        return v




#------------------------------------------------------------------------------------------------------------------
#+------------------------------------------------------------------------------------------------------------------
# reservas/serializers.py

ESTADOS_ACTIVOS = ["PENDIENTE", "APROBADA"]

class ReservaReadSerializer(serializers.ModelSerializer):
    areacomun_nombre = serializers.CharField(source="areacomun.nombre", read_only=True)
    usuario_username = serializers.CharField(source="usuario.username", read_only=True)
    aprobado_por_username = serializers.CharField(source="aprobado_por.username", read_only=True)

    class Meta:
        model = Reserva
        fields = [
            "id", "nombre", "fecha_inicio", "fecha_fin", "horario",
            "areacomun", "areacomun_nombre",
            "usuario", "usuario_username",
            "estado", "costo_total",  "fecha_solicitud",
            "aprobado_por", "aprobado_por_username",
        ]


class ReservaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = [
            "nombre", "fecha_inicio", "fecha_fin", "horario",
            "areacomun", "usuario",
            "estado", "costo_total", "aprobado_por",
        ]
        extra_kwargs = {
            "usuario": {"required": False, "allow_null": True},
            "aprobado_por": {"required": False, "allow_null": True},
            "estado": {"required": False},
            "costo_total": {"required": False},
            
        }

    def validate(self, attrs):
        fecha_inicio = attrs.get("fecha_inicio", getattr(self.instance, "fecha_inicio", None))
        fecha_fin    = attrs.get("fecha_fin",    getattr(self.instance, "fecha_fin", None))

        if fecha_inicio and fecha_fin and fecha_fin <= fecha_inicio:
            raise serializers.ValidationError({"fecha_fin": "Debe ser mayor que fecha_inicio."})

        return attrs

    def _hay_solape(self, instance, areacomun, inicio, fin, estado):
        """Chequear solape básico antes de que el constraint de DB dispare."""
        if not areacomun or not inicio or not fin:
            return False

        qs = Reserva.objects.filter(
            areacomun=areacomun,
            estado__in=ESTADOS_ACTIVOS,
            fecha_inicio__lt=fin,
            fecha_fin__gt=inicio,
        )
        if instance and instance.pk:
            qs = qs.exclude(pk=instance.pk)
        return qs.exists()

    def create(self, validated_data):
        request = self.context.get("request")
        if "usuario" not in validated_data and request and request.user.is_authenticated:
            validated_data["usuario"] = request.user

        if "estado" not in validated_data:
            validated_data["estado"] = Reserva.Estado.PENDIENTE

        if self._hay_solape(
            None,
            validated_data.get("areacomun"),
            validated_data.get("fecha_inicio"),
            validated_data.get("fecha_fin"),
            validated_data.get("estado"),
        ):
            raise serializers.ValidationError("Ya existe una reserva activa que se solapa en esa área y rango.")

        return super().create(validated_data)

    def update(self, instance, validated_data):
        areacomun = validated_data.get("areacomun", instance.areacomun)
        inicio    = validated_data.get("fecha_inicio", instance.fecha_inicio)
        fin       = validated_data.get("fecha_fin", instance.fecha_fin)
        estado    = validated_data.get("estado", instance.estado)

        if self._hay_solape(instance, areacomun, inicio, fin, estado):
            raise serializers.ValidationError("El rango propuesto se solapa con otra reserva activa del área.")

        return super().update(instance, validated_data)


#------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
# facturacion/serializers.py

class FacturaSerializer(serializers.ModelSerializer):
    # Campos calculados de solo lectura
    tipo_concepto = serializers.CharField(read_only=True)
    referencia_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Factura
        fields = [
            "id",
            # Identificación / control
            "numero", "serie",
            # Cliente
            "nit", "razon_social", "moneda",
            # Importe y estado
            "total", "fecha", "estado", "tipo_pago",
            # Trazabilidad
            "usuario", "unidad",
            # Vínculo 1–1 (exactamente uno)
            "reserva", "cuota",
            # Extras
            "observaciones",
            "created_at", "updated_at",
            # Calculados
            "tipo_concepto", "referencia_id",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, attrs):
        # Al crear, usa attrs; al actualizar, combina con instancia
        reserva = attrs.get("reserva", getattr(self.instance, "reserva", None))
        cuota   = attrs.get("cuota",   getattr(self.instance, "cuota",   None))
        total   = attrs.get("total",   getattr(self.instance, "total",   None))

        has_reserva = reserva is not None
        has_cuota   = cuota   is not None
        if has_reserva == has_cuota:  # XOR: una y solo una
            raise serializers.ValidationError(
                "Debes asociar la factura a una Reserva O a una Cuota (exactamente una)."
            )

        if total is not None and total < 0:
            raise serializers.ValidationError({"total": "El total no puede ser negativo."})

        return attrs
