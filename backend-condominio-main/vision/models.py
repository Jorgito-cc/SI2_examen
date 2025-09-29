from django.db import models
from django.conf import settings

class Zona(models.Model):
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('ocupada', 'Ocupada'),
        ('mantenimiento', 'En Mantenimiento'),
    ]

    nombre = models.CharField(max_length=200, db_index=True)
    ubicacion = models.CharField(max_length=255)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible', db_index=True)

    def __str__(self):
        return self.nombre


class Camara(models.Model):
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('ocupada', 'Ocupada'),
        ('mantenimiento', 'En Mantenimiento'),
    ]

    zona = models.ForeignKey(
        'vision.Zona',
        on_delete=models.PROTECT,              # ← PROTECT para no perder cámaras si borran la zona
        related_name='camaras',
        db_index=True
    )
    areacomun = models.ForeignKey(
        'amenities.AreaComun',
        on_delete=models.PROTECT,              # ← PROTECT para preservar histórico
        related_name='camaras',
        db_index=True
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible', db_index=True)

    def __str__(self):
        # Muestra nombres legibles
        return f"Camara {self.id} - {self.estado} en Zona {self.zona} / Área {self.areacomun}"


class DeteccionIA(models.Model):
    NIVELES_RIESGO = [
        ('bajo', 'Bajo'),
        ('medio', 'Medio'),
        ('alto', 'Alto'),
        ('critico', 'Crítico'),
    ]
    TIPOS_EVIDENCIA = [
        ('imagen', 'Imagen'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('otro', 'Otro'),
    ]
    TIPOS_INCIDENCIA = [
        ('robo', 'Robo'),
        ('vandalismo', 'Vandalismo'),
        ('incendio', 'Incendio'),
        ('otro', 'Otro'),
    ]

    camara = models.ForeignKey(
        'vision.Camara',
        on_delete=models.PROTECT,              # ← PROTECT: no queremos perder detecciones si borran una cámara
        related_name='detecciones',
        db_index=True
    )
    confianza = models.FloatField()           # 0..1 recomendado
    # renómbralo a fecha_hora si puedes (requiere migración)
    fechaHora = models.DateTimeField(auto_now_add=True, db_index=True)
    evidencia = models.CharField(max_length=20, choices=TIPOS_EVIDENCIA, db_index=True)
    nivel_riesgo = models.CharField(max_length=20, choices=NIVELES_RIESGO, default='bajo', db_index=True)
    incidencia = models.CharField(max_length=20, choices=TIPOS_INCIDENCIA, default='otro', db_index=True)

    def __str__(self):
        return f"Detección {self.id} - {self.incidencia} ({self.nivel_riesgo}, {self.confianza*100:.1f}%)"
    
    
    
    
#----------------------------------------------------------------------------------------------------------------
#-------------------------IA-------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------

class FaceProfile(models.Model):
    """Embeddings por usuario (1..N fotos)."""
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="face_profiles")
    label = models.CharField(max_length=30, default="principal")
    embedding = models.BinaryField()           # np.ndarray.tobytes() float32
    vector_dim = models.IntegerField(default=512)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["usuario"])]

class FaceEvent(models.Model):
    """Log de intentos de reconocimiento."""
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    confianza = models.FloatField()            # similitud coseno 0..1
    foto_path = models.CharField(max_length=300)
    aceptado = models.BooleanField(default=False)
    motivo = models.CharField(max_length=120, blank=True, null=True)  # p.ej. "MATCH_OK" / "SIN_MATCH"
    fecha_hora = models.DateTimeField(auto_now_add=True)
