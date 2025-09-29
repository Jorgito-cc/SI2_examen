from django.db import models
from django.conf import settings

class Bitacora(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="bitacoras",
    )
    accion = models.CharField(max_length=255)
    detalle = models.TextField(blank=True, default="")
    ip = models.GenericIPAddressField(null=True, blank=True)
    path = models.CharField(max_length=255, blank=True, default="")
    user_agent = models.CharField(max_length=255, blank=True, default="")

    creado_en = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-creado_en"]
        indexes = [
            models.Index(fields=["creado_en"]),
            models.Index(fields=["usuario"]),
            models.Index(fields=["path"]),
        ]
        verbose_name = "bitácora"
        verbose_name_plural = "bitácoras"

    def __str__(self):
        u = self.usuario if self.usuario else "system"
        return f"[{self.creado_en:%Y-%m-%d %H:%M:%S}] {u} — {self.accion}"

    @property
    def fecha(self):
        return self.creado_en.date()

    @property
    def hora(self):
        return self.creado_en.time().replace(microsecond=0)
