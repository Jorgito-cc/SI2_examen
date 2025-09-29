from django.db import models


# ---------- TABLA UNIDAD_HABITACIONAL ----------
class UnidadHabitacional(models.Model):
    numero = models.CharField(max_length=30)
    bloque = models.CharField(max_length=30)
    estado = models.CharField(max_length=20, default="ACTIVA")
    superficie = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["bloque", "numero"], name="uniq_unidad_bloque_numero"),
        ]
        indexes = [
            models.Index(fields=["bloque", "numero"]),
        ]
        ordering = ["bloque", "numero"]

    def __str__(self):
        return f"B{self.bloque}-{self.numero}"


# ---------- TABLA RESIDENTE_UNIDAD ----------
class ResidenteUnidad(models.Model):
    residente = models.ForeignKey("authx.Residente", on_delete=models.CASCADE, related_name="vinculos")
    # OJO: si tu app se llama 'unidad', el label correcto es "unidad.UnidadHabitacional"
    unidad = models.ForeignKey("unidades.UnidadHabitacional", on_delete=models.CASCADE, related_name="vinculos")
    es_propietario = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["residente", "unidad"], name="uniq_residente_unidad"),
        ]
        indexes = [
            models.Index(fields=["unidad"]),
        ]

    def __str__(self):
        rol = "Prop." if self.es_propietario else "Inq."
        return f"{self.residente} -> {self.unidad} ({rol})"
    
    
    
    
class Mascota(models.Model):
    unidad = models.ForeignKey(
        'unidades.UnidadHabitacional',   # <--- referencia al modelo de otra app
        on_delete=models.CASCADE,
        related_name="mascotas"
    )
    nombre = models.CharField(max_length=200)
    especie = models.CharField(max_length=100)
    raza = models.CharField(max_length=200)


def __str__(self):
    return self.nombre


    
class Integrante(models.Model):
    unidad = models.ForeignKey(
        'unidades.UnidadHabitacional',
        on_delete=models.CASCADE,
        related_name="integrantes"
    )
    
    ci = models.CharField(max_length=200)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=200)
    registro_facial = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre


class Visita(models.Model):
    unidad = models.ForeignKey(
        'unidades.UnidadHabitacional',
        on_delete=models.CASCADE,
        related_name="visitas"
    )
    nombre = models.CharField(max_length=200)
    fecha_hora_llegada = models.DateTimeField()
    fecha_hora_salida = models.DateTimeField()
    


    def __str__(self):
        return self.nombre

