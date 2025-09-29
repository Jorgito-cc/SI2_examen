from django.db import models

class Mantenimiento(models.Model):
    personal = models.ForeignKey(
        'authx.Personal',   # <--- referencia al modelo de otra app
        on_delete=models.CASCADE,
        related_name="mantenimientos"
    )
    titulo = models.CharField(max_length=200)
    tipo_mantenimiento = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    prioridad = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.titulo






class Servicio(models.Model):
    usuario = models.ForeignKey(
        'authx.Usuario',   # referencia a otro modelo
        on_delete=models.CASCADE,
        related_name="servicios"
    )
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

