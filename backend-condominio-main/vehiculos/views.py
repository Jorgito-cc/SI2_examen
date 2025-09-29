# vehiculos/views.py
import uuid
from django.utils import timezone

from rest_framework import permissions, status, viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import VehiculoSerializer, AccesoQRReadSerializer, AccesoQRWriteSerializer
from .models import Vehiculo, AccesoQR


def _gen_codigo():
    # Código corto legible: 12 chars hex
    return uuid.uuid4().hex[:12].upper()


class CrearVehiculoUsuarioView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = VehiculoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VehiculoViewSet(viewsets.ModelViewSet):
    """
    CRUD básico de Vehículo (para que el import exista y puedas testear).
    """
    queryset = Vehiculo.objects.all().order_by('-id')
    serializer_class = VehiculoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['placa', 'marca', 'modelo']
    ordering_fields = ['id']


class AccesoQRViewSet(viewsets.ModelViewSet):
    queryset = AccesoQR.objects.select_related('vehiculo').all().order_by('-creado_en')
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['codigo', 'tipo', 'estado', 'vehiculo__placa']  # asegúrate de tener 'placa' en Vehiculo
    ordering_fields = ['creado_en', 'actualizado_en', 'valido_hasta']

    def get_serializer_class(self):
        # Lecturas con serializer de lectura (anidado); escrituras con write
        return AccesoQRReadSerializer if self.action in ['list', 'retrieve'] else AccesoQRWriteSerializer

    def perform_create(self, serializer):
        codigo = serializer.validated_data.get('codigo') or _gen_codigo()
        instance = serializer.save(codigo=codigo)
        # Si se crea ya como usado, marcamos timestamp
        if instance.estado == 'usado' and instance.usado_en is None:
            instance.usado_en = timezone.now()
            instance.save(update_fields=['usado_en'])

    def perform_update(self, serializer):
        prev = self.get_object()
        instance = serializer.save()
        # Si se transiciona a "usado", marcar timestamp
        if instance.estado == 'usado' and prev.estado != 'usado' and instance.usado_en is None:
            instance.usado_en = timezone.now()
            instance.save(update_fields=['usado_en'])

    # --- Acciones personalizadas ---

    @action(detail=True, methods=['post'])
    def marcar_usado(self, request, pk=None):
        """
        Marca el QR como 'usado' y setea 'usado_en' con now().
        """
        qr = self.get_object()
        if qr.estado == 'usado':
            return Response({"detail": "El QR ya está marcado como usado."}, status=status.HTTP_400_BAD_REQUEST)
        qr.estado = 'usado'
        qr.usado_en = timezone.now()
        qr.save(update_fields=['estado', 'usado_en', 'actualizado_en'])
        return Response(AccesoQRReadSerializer(qr).data)

    @action(detail=True, methods=['post'])
    def revocar(self, request, pk=None):
        """
        Revoca el QR (estado='revocado').
        """
        qr = self.get_object()
        if qr.estado == 'revocado':
            return Response({"detail": "El QR ya está revocado."}, status=status.HTTP_400_BAD_REQUEST)
        qr.estado = 'revocado'
        qr.save(update_fields=['estado', 'actualizado_en'])
        return Response(AccesoQRReadSerializer(qr).data)

    @action(detail=True, methods=['get'])
    def validar(self, request, pk=None):
        """
        Valida si el QR es utilizable:
        - estado debe ser 'activo'
        - si tiene 'valido_hasta', debe ser futuro
        """
        qr = self.get_object()
        now = timezone.now()
        valido = (qr.estado == 'activo') and (qr.valido_hasta is None or qr.valido_hasta >= now)
        return Response({
            "codigo": qr.codigo,
            "estado": qr.estado,
            "valido_hasta": qr.valido_hasta,
            "valido": valido,
        })
