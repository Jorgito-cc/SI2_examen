# vision/serializers.py
from rest_framework import serializers
from .models import Zona, Camara, DeteccionIA

# =======================
# ZONA
# =======================
class ZonaSerializer(serializers.ModelSerializer):
    estado_label = serializers.CharField(source='get_estado_display', read_only=True)

    class Meta:
        model = Zona
        fields = [
            'id',
            'nombre',
            'ubicacion',
            'estado',        # almacenado (choice)
            'estado_label',  # legible
        ]
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def validate_nombre(self, v):
        v = v.strip()
        if not v:
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return v

    def validate(self, attrs):
        # opcional: evita nombres duplicados por ubicación
        # if Zona.objects.filter(nombre__iexact=attrs.get('nombre'),
        #                        ubicacion__iexact=attrs.get('ubicacion')).exists():
        #     raise serializers.ValidationError("Ya existe una zona con ese nombre y ubicación.")
        return attrs


# =======================
# CÁMARA
# =======================
class CamaraReadSerializer(serializers.ModelSerializer):
    # Ids crudos
    zona_id = serializers.PrimaryKeyRelatedField(source='zona', read_only=True)
    areacomun_id = serializers.PrimaryKeyRelatedField(source='areacomun', read_only=True)

    # Labels legibles
    zona = serializers.StringRelatedField(read_only=True)
    areacomun = serializers.StringRelatedField(read_only=True)
    estado_label = serializers.CharField(source='get_estado_display', read_only=True)

    class Meta:
        model = Camara
        fields = [
            'id',
            'estado', 'estado_label',
            'zona_id', 'zona',
            'areacomun_id', 'areacomun',
        ]
        extra_kwargs = {'id': {'read_only': True}}


class CamaraWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camara
        fields = [
            'id',
            'estado',
            'zona',
            'areacomun',
        ]
        read_only_fields = ['id']

    def validate(self, attrs):
        # ejemplo: puedes impedir que una cámara en mantenimiento se cree con zona/area nulas (si lo permitieras)
        # aquí solo mostramos la estructura por si quieres reglas de negocio
        return attrs


# =======================
# DETECCIÓN IA
# =======================
class DeteccionIAReadSerializer(serializers.ModelSerializer):
    # Id crudo + label de cámara
    camara_id = serializers.PrimaryKeyRelatedField(source='camara', read_only=True)
    camara = serializers.StringRelatedField(read_only=True)

    # Datos derivados / legibles
    evidencia_label = serializers.CharField(source='get_evidencia_display', read_only=True)
    nivel_riesgo_label = serializers.CharField(source='get_nivel_riesgo_display', read_only=True)
    incidencia_label = serializers.CharField(source='get_incidencia_display', read_only=True)

    # Contexto útil: zona y área de la cámara (para no hacer otra petición)
    zona = serializers.CharField(source='camara.zona.nombre', read_only=True)
    areacomun = serializers.CharField(source='camara.areacomun.nombre', read_only=True)

    class Meta:
        model = DeteccionIA
        fields = [
            'id',
            'camara_id', 'camara',
            'confianza',
            'fechaHora',               # auto_now_add
            'evidencia', 'evidencia_label',
            'nivel_riesgo', 'nivel_riesgo_label',
            'incidencia', 'incidencia_label',
            'zona', 'areacomun',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'fechaHora': {'read_only': True},
        }


class DeteccionIAWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeteccionIA
        fields = [
            'id',
            'camara',
            'confianza',
            'evidencia',
            'nivel_riesgo',
            'incidencia',
        ]
        read_only_fields = ['id']

    # Validaciones de negocio
    def validate_confianza(self, v):
        # Esperado en 0..1 (0.92 = 92%)
        if not (0 <= v <= 1):
            raise serializers.ValidationError("confianza debe estar entre 0 y 1 (ej. 0.92).")
        return v

    def validate(self, attrs):
        # ejemplo extra: si la incidencia es 'incendio' exigir evidencia 'video' o 'imagen'
        # if attrs.get('incidencia') == 'incendio' and attrs.get('evidencia') not in ('video', 'imagen'):
        #     raise serializers.ValidationError("Para 'incendio' la evidencia debe ser video o imagen.")
        return attrs




#----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------

class FaceEnrollSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
    imagenes = serializers.ListField(
        child=serializers.CharField(), allow_empty=False
    )
    label = serializers.CharField(required=False, default="principal")

class FaceRecognizeSerializer(serializers.Serializer):
    imagen = serializers.CharField()
    umbral = serializers.FloatField(required=False)
