from rest_framework import serializers
from .models import UnidadHabitacional, ResidenteUnidad,Mascota, Integrante, Visita

class UnidadHabitacionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadHabitacional
        fields = "__all__"

class ResidenteUnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidenteUnidad
        fields = "__all__"






# ----------------- SERIALIZER DE MASCOTA -----------------
class MascotaSerializer(serializers.ModelSerializer):
    # Incluir datos de la unidad si se desea
    unidad = UnidadHabitacionalSerializer(read_only=True)
    unidad_id = serializers.PrimaryKeyRelatedField(
        queryset=UnidadHabitacionalSerializer.Meta.model.objects.all(), source='unidad', write_only=True
    )

    class Meta:
        model = Mascota
        fields = ['id', 'unidad', 'unidad_id', 'nombre', 'especie', 'raza']


# ----------------- SERIALIZER DE INTEGRANTE -----------------
class IntegranteSerializer(serializers.ModelSerializer):
    # Incluir datos de la unidad si se desea
    unidad = UnidadHabitacionalSerializer(read_only=True)
    unidad_id = serializers.PrimaryKeyRelatedField(
        queryset=UnidadHabitacionalSerializer.Meta.model.objects.all(), source='unidad', write_only=True
    )

    class Meta:
        model = Integrante
        fields = ['id', 'unidad', 'unidad_id', 'ci', 'nombre', 'telefono', 'registro_facial']




class VisitaSerializer(serializers.ModelSerializer):
    # Mostrar información de la unidad (read-only)
    unidad = UnidadHabitacionalSerializer(read_only=True)
    # Permitir asignar unidad por ID al crear o actualizar
    unidad_id = serializers.PrimaryKeyRelatedField(
        queryset=UnidadHabitacionalSerializer.Meta.model.objects.all(),
        source='unidad',
        write_only=True
    )

    class Meta:
        model = Visita
        fields = ['id', 'unidad', 'unidad_id', 'nombre', 'fecha_hora_llegada', 'fecha_hora_salida']





