from django.db import models

class Vehiculo(models.Model):
    placa = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    
    usuario = models.ForeignKey(
        'authx.Usuario',
        on_delete=models.CASCADE,
        related_name='vehiculos'
    )
    
    class Meta:
        db_table = 'vehiculo'
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'
    
    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.placa}"
    
    
    
    
class AccesoQR(models.Model):
    TIPOS = [
        ('permanente', 'Permanente'),
        ('temporal', 'Temporal'),
        ('visita', 'Visita'),
    ]
    ESTADOS = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('revocado', 'Revocado'),
        ('usado', 'Usado'),
        ('vencido', 'Vencido'),
    ]

    codigo = models.CharField(max_length=200, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPOS, default='temporal')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')

    # timestamps útiles
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    valido_hasta = models.DateTimeField(null=True, blank=True)
    usado_en = models.DateTimeField(null=True, blank=True)

    # Relación 1 a 1 con Vehiculo (una placa ↔ un QR vigente)
    vehiculo = models.OneToOneField(
        'vehiculos.Vehiculo',
        on_delete=models.CASCADE,
        related_name='qr'
    )

    def __str__(self):
        placa = getattr(self.vehiculo, 'placa', 'sin-placa')
        return f"QR {self.codigo} ({placa}) - {self.estado}"