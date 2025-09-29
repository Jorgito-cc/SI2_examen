from django.db import models
from django.utils import timezone
from django.conf import settings

from django.db.models import Q, F, Func
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields.ranges import RangeOperators
# OJO: ya no uses GistIndex; la ExclusionConstraint crea su índice GiST
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import transaction



#------------------------------------------------------------------------------------------------
#---------------------CUOTA-------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
def periodo_actual_str():
    # Ejemplo '2025-09'
    return timezone.now().strftime('%Y-%m')

class Cuota(models.Model):
    TIPO_CUOTA = [
        ('CUOTA', 'Cuota'),
        ('MULTA', 'Multa'),
    ]
    ESTADOS = [
        ('EMITIDA', 'Emitida'),
        ('VENCIDA', 'Vencida'),
        ('PAGADA', 'Pagada'),
        ('PARCIAL', 'Parcial'),
        ('ANULADA', 'Anulada'),
    ]

    # Relación con UnidadHabitacional
    unidad = models.ForeignKey(
        'unidades.UnidadHabitacional',
        on_delete=models.PROTECT,   # similar a RESTRICT
        related_name='cuotas'
    )

    cantidad_pago = models.DecimalField(max_digits=12, decimal_places=2)
    tipo_cuota = models.CharField(max_length=10, choices=TIPO_CUOTA)
    fecha_a_pagar = models.DateField()

    periodo = models.CharField(max_length=7, default=periodo_actual_str)  # 'YYYY-MM'
    fecha_vencimiento = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='EMITIDA')
    descripcion = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cuota'
        verbose_name = 'Cuota/Multa'
        verbose_name_plural = 'Cuotas/Multas'
        indexes = [
            models.Index(fields=['unidad', 'periodo']),
            models.Index(fields=['estado']),
            models.Index(fields=['tipo_cuota']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(cantidad_pago__gte=0),
                name='chk_cuota_cantidad_pos'
            )
        ]

    def __str__(self):
        return f"{self.tipo_cuota} {self.periodo} - Unidad {self.unidad_id} - {self.cantidad_pago}"
    

#--------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
#----------------------------RESERVA--------------------------------------------------------------------------------
class Reserva(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE   = "PENDIENTE", "Pendiente"
        APROBADA    = "APROBADA", "Aprobada"
        RECHAZADA   = "RECHAZADA", "Rechazada"
        CANCELADA   = "CANCELADA", "Cancelada"
        FINALIZADA  = "FINALIZADA", "Finalizada"

    nombre        = models.CharField(max_length=150)
    fecha_inicio  = models.DateTimeField()
    fecha_fin     = models.DateTimeField()
    horario       = models.CharField(max_length=50, blank=True, null=True)

    areacomun = models.ForeignKey(
        "amenities.AreaComun",
        db_column="areacomun_id",
        on_delete=models.SET_NULL,
        null=True,
        related_name="reservas",
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_column="usuario_id",
        on_delete=models.SET_NULL,
        null=True,
        related_name="reservas",
    )

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )

    costo_total     = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    aprobado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_column="aprobado_por",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reservas_aprobadas",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)







    class Meta:
        db_table = "reserva"
        ordering = ["-fecha_inicio", "-id"]
        indexes = [
            models.Index(fields=["areacomun"], name="ix_reserva_area"),
            models.Index(fields=["usuario"],   name="ix_reserva_usuario"),
        ]
        constraints = [
            models.CheckConstraint(
                name="chk_reserva_rango",
                check=Q(fecha_fin__gt=F("fecha_inicio")),
            ),
            ExclusionConstraint(
                name="excl_reserva_solape_por_area",
                expressions=[
                    # Igualdad por área común: usa "="
                    (F("areacomun"), "="),
                    # Solape de rango de fechas: usa OVERLAPS o "&&"
                    (Func(F("fecha_inicio"), F("fecha_fin"), function="tstzrange"), RangeOperators.OVERLAPS),
                    # (Func(F("fecha_inicio"), F("fecha_fin"), function="tstzrange"), "&&"),  # alternativa equivalente
                ],
                condition=Q(estado__in=["PENDIENTE", "APROBADA"]),
            ),
        ]


    def __str__(self):
        return f"Reserva #{self.pk} - {self.nombre}"
    
    
    
    #-----------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------
# apps/facturacion/models.py

# Ajusta estos imports según tus apps
# from reservas.models import Reserva
# from finanzas.models import Cuota
# from users.models import Usuario
# from unidades.models import UnidadHabitacional

class Factura(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", _("Pendiente")
        PAGADA    = "PAGADA", _("Pagada")
        ANULADA   = "ANULADA", _("Anulada")

    class TipoPago(models.TextChoices):
        TRANSFER = "TRANSFERENCIA", _("Transferencia")
        QR       = "QR", _("Pago QR")
        BANCO    = "BANCO", _("Depósito/Banking")
        TARJETA  = "TARJETA", _("Tarjeta")

    # ——— Identificación / Control ———
    numero        = models.CharField(max_length=30, blank=True, null=True)
    serie         = models.CharField(max_length=10, blank=True, null=True)

    # ——— Datos de cliente/facturación ———
    nit           = models.CharField(max_length=30)                 # requerido
    razon_social  = models.CharField(max_length=150, blank=True, null=True)
    moneda        = models.CharField(max_length=3, default="BOB")

    # ——— Importe y estado ———
    total         = models.DecimalField(max_digits=12, decimal_places=2)
    fecha         = models.DateField()
    estado        = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    tipo_pago     = models.CharField(max_length=30, choices=TipoPago.choices)

    # ——— Trazabilidad del usuario y unidad (opcionales pero útiles) ———
    usuario       = models.ForeignKey("authx.Usuario", on_delete=models.SET_NULL, null=True, blank=True)
    unidad        = models.ForeignKey("unidades.UnidadHabitacional", on_delete=models.SET_NULL, null=True, blank=True)

    # ——— Vínculos 1–1 al “concepto” ———
    # EXACTAMENTE UNO debe estar set: o reserva o cuota
    reserva       = models.OneToOneField("finanzas.Reserva", on_delete=models.PROTECT, null=True, blank=True, related_name="factura")
    cuota         = models.OneToOneField("finanzas.Cuota",   on_delete=models.PROTECT, null=True, blank=True, related_name="factura")

    # ——— Extras ———
    observaciones = models.TextField(blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    # ——— Validaciones a nivel de modelo ———
    def clean(self):
        super().clean()

        # Regla: total no negativo
        if self.total is not None and self.total < 0:
            raise ValidationError({"total": _("El total no puede ser negativo.")})

        # Regla XOR: exactamente uno de (reserva, cuota)
        has_reserva = self.reserva_id is not None
        has_cuota   = self.cuota_id   is not None
        if has_reserva == has_cuota:  # True==True o False==False
            raise ValidationError(_("Debes asociar la factura a una Reserva O a una Cuota (exactamente una)."))

        # (Opcional) Coherencia de unidad si la conoces desde el concepto
        # if has_reserva and self.unidad_id and self.reserva.unidad_id and self.unidad_id != self.reserva.unidad_id:
        #     raise ValidationError(_("La unidad de la factura no coincide con la unidad de la reserva."))
        # if has_cuota and self.unidad_id and self.cuota.unidad_id and self.unidad_id != self.cuota.unidad_id:
        #     raise ValidationError(_("La unidad de la factura no coincide con la unidad de la cuota."))

    def save(self, *args, **kwargs):
        # Asegura que corra clean() también en save()
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "factura"
        verbose_name = _("Factura")
        verbose_name_plural = _("Facturas")
        # Refuerza reglas en DB:
        constraints = [
            # total >= 0
            models.CheckConstraint(check=models.Q(total__gte=0), name="chk_factura_total_no_negativo"),
            # XOR: (reserva IS NULL) != (cuota IS NULL)
            models.CheckConstraint(
                check=(
                    (models.Q(reserva__isnull=True) & models.Q(cuota__isnull=False)) |
                    (models.Q(reserva__isnull=False) & models.Q(cuota__isnull=True))
                ),
                name="chk_factura_xor_reserva_o_cuota",
            ),
        ]
        indexes = [
            models.Index(fields=["estado"]),
            models.Index(fields=["fecha"]),
            models.Index(fields=["numero", "serie"]),
        ]

    def __str__(self):
        concepto = "RESERVA" if self.reserva_id else "CUOTA"
        ref_id = self.reserva_id or self.cuota_id
        return f"Factura #{self.pk or '—'} [{concepto}:{ref_id}] {self.total} {self.moneda} ({self.estado})"

    # Helpers
    @property
    def tipo_concepto(self) -> str:
        """Devuelve 'RESERVA' o 'CUOTA' según el vínculo activo."""
        return "RESERVA" if self.reserva_id else "CUOTA"

    @property
    def referencia_id(self):
        """ID del concepto ligado (reserva_id o cuota_id)."""
        return self.reserva_id or self.cuota_id




#------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
# apps/facturacion/models.py (mismo archivo donde está Factura)
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Asegúrate de que esta importación resuelva a tu Factura
# Si estás en el mismo archivo, no necesitas importar.
# from .models import Factura

class Pago(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE   = "pendiente", _("Pendiente")
        CONFIRMADO  = "confirmado", _("Confirmado")
        ANULADO     = "anulado",   _("Anulado")

    # Puedes reutilizar las choices de Factura para mantener consistencia
    class TipoPago(models.TextChoices):
        TRANSFER = "TRANSFERENCIA", _("Transferencia")
        QR       = "QR", _("Pago QR")
        BANCO    = "BANCO", _("Depósito/Banking")
        TARJETA  = "TARJETA", _("Tarjeta")

    # ——— Relación 1:1 con Factura ———
    factura = models.OneToOneField(
        "finanzas.Factura",
        on_delete=models.CASCADE,  # borra el pago si se borra la factura
        related_name="pago",
    )

    # ——— Datos del pago ———
    tipo_pago        = models.CharField(max_length=30, choices=TipoPago.choices)
    monto            = models.DecimalField(max_digits=12, decimal_places=2)
    moneda           = models.CharField(max_length=3, default="BOB")
    fecha_pago       = models.DateTimeField(default=timezone.now)
    estado           = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)

    # ——— Trazabilidad / adicionales ———
    referencia       = models.CharField(max_length=100, blank=True, null=True)  # ID transacción banco/QR
    comprobante_url  = models.TextField(blank=True, null=True)                  # URL imagen/PDF
    usuario_registro = models.ForeignKey(
        "authx.Usuario", on_delete=models.SET_NULL, null=True, blank=True
    )
    fecha_confirmacion = models.DateTimeField(blank=True, null=True)


    class Meta:
        db_table = "pago"
        verbose_name = _("Pago")
        verbose_name_plural = _("Pagos")
        constraints = [
            models.CheckConstraint(check=Q(monto__gte=0), name="chk_pago_monto_no_negativo"),
        ]
        indexes = [
            models.Index(fields=["estado"]),
            models.Index(fields=["fecha_pago"]),
            models.Index(fields=["factura"]),
        ]

    def __str__(self):
        return f"Pago #{self.pk or '—'} de Factura #{self.factura_id} - {self.monto} {self.moneda} ({self.estado})"

    # ——— Validaciones de negocio ———
    def clean(self):
        super().clean()

        if self.monto is not None and self.monto < 0:
            raise ValidationError({"monto": _("El monto no puede ser negativo.")})

        if not self.factura_id:
            raise ValidationError(_("Debe asociar el pago a una factura."))

        # No permitir pagar facturas anuladas
        if self.factura and self.factura.estado == self.factura.Estado.ANULADA:
            raise ValidationError(_("No se puede registrar pagos para una factura ANULADA."))

        # (Regla común) El pago debe coincidir con el total de la factura
        if self.factura and self.monto is not None:
            if self.monto != self.factura.total:
                raise ValidationError({"monto": _("El monto del pago debe ser igual al total de la factura.")})

        # Moneda del pago debe ser igual a la de la factura
        if self.factura and self.moneda and self.factura.moneda and self.moneda != self.factura.moneda:
            raise ValidationError({"moneda": _("La moneda del pago debe coincidir con la moneda de la factura.")})

        # Si ya existe pago (OneToOne lo garantiza), adicionalmente evita confirmar 2 veces
        if self.pk and self.estado == self.Estado.CONFIRMADO and self.fecha_confirmacion is None:
            # Si el estado es confirmado, exige fecha_confirmacion (se setea en confirmar())
            raise ValidationError(_("Falta la fecha de confirmación para un pago confirmado."))

    def save(self, *args, **kwargs):
        # Ejecuta validaciones
        self.full_clean()
        return super().save(*args, **kwargs)




    # ——— Helpers de transición ———
    @transaction.atomic
    def confirmar(self, when: timezone.datetime | None = None):
        if self.estado == self.Estado.ANULADO:
            raise ValidationError(_("No se puede confirmar un pago ANULADO."))

        # Bloquea la fila del pago y accede a la factura
        if self.pk:
            self_refrescado = (
                self.__class__.objects.select_for_update()
                .select_related("factura")
                .get(pk=self.pk)
            )
            factura = self_refrescado.factura
        else:
            factura = self.factura

        # Validaciones de coherencia
        if factura.estado == factura.Estado.ANULADA:
            raise ValidationError(_("La factura está ANULADA; no puede ser pagada."))

        if self.monto != factura.total:
            raise ValidationError(_("El monto del pago debe ser igual al total de la factura."))

        if self.moneda != factura.moneda:
            raise ValidationError(_("La moneda del pago y de la factura deben coincidir."))

        # 1) Confirmar pago
        self.estado = self.Estado.CONFIRMADO
        self.fecha_confirmacion = when or timezone.now()
        self.save(update_fields=["estado", "fecha_confirmacion", "updated_at"])

        # 2) Marcar FACTURA como PAGADA
        if factura.estado != factura.Estado.PAGADA:
            factura.estado = factura.Estado.PAGADA
            factura.updated_at = timezone.now()
            factura.save(update_fields=["estado", "updated_at"])

        # 3) Marcar CONCEPTO como PAGADA
        #    - Reserva: requiere que hayas agregado Estado.PAGADA en Reserva
        #    - Cuota: ya tienes 'PAGADA' en choices
        if factura.reserva_id:
            reserva = factura.reserva  # related_name="factura" en Factura.reserva
            if hasattr(reserva, "estado"):
                if reserva.estado != "APROBADA":
                    reserva.estado = "APROBADA"
                    # Si quieres, también puedes setear aprobado_por si aplica
                    reserva.updated_at = timezone.now()
                    reserva.save(update_fields=["estado", "updated_at"])

        elif factura.cuota_id:
            cuota = factura.cuota
            if hasattr(cuota, "estado"):
                if cuota.estado != "PAGADA":
                    cuota.estado = "PAGADA"
                    cuota.updated_at = timezone.now()
                    # Si manejas montos acumulados (pagado/saldo) en el modelo Cuota:
                    # if hasattr(cuota, "pagado"):
                    #     cuota.pagado = cuota.pagado + self.monto
                    # if hasattr(cuota, "saldo"):
                    #     cuota.saldo = max(cuota.cantidad_pago - cuota.pagado, 0)
                    cuota.save(update_fields=["estado", "updated_at"])



    @transaction.atomic
    def anular(self, motivo: str | None = None):
        """
        Anula el pago y revierte la factura a PENDIENTE (si estaba PAGADA por este pago).
        """
        if self.estado == self.Estado.ANULADO:
            return  # idempotente

        factura = (
            self.__class__.objects.select_for_update()
            .select_related("factura")
            .get(pk=self.pk)
            .factura
        )

        self.estado = self.Estado.ANULADO
        self.save(update_fields=["estado", "updated_at"])

        # Si la factura estaba PAGADA (por este único pago), vuelve a PENDIENTE
        if factura.estado == factura.Estado.PAGADA:
            factura.estado = factura.Estado.PENDIENTE
            factura.updated_at = timezone.now()
            factura.save(update_fields=["estado", "updated_at"])
