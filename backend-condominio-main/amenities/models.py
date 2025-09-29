# models.py (tu app p. ej. "condominium" o "areas")
from django.db import models

class AreaComun(models.Model):
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('ocupada', 'Ocupada'),
        ('mantenimiento', 'En Mantenimiento'),
    ]

    nombre = models.CharField(max_length=200)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible')
    capacidad = models.IntegerField()
    ubicacion = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.nombre  # <-- sin coma
