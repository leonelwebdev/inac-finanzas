from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

MONEY_VALIDATORS = [MinValueValidator(Decimal("0"))]


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


# ====== Lookups / Catálogos ======
class EstadoVencimiento(models.Model):
    nombre = models.CharField("Estado", max_length=50, unique=True)

    class Meta:
        verbose_name = "Estado de Vencimiento"
        verbose_name_plural = "Estados de Vencimiento"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Concepto(models.Model):
    nombre = models.CharField("Concepto", max_length=100, unique=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Situacion(models.Model):
    nombre = models.CharField("Situación", max_length=50, unique=True)

    class Meta:
        verbose_name = "Situación"
        verbose_name_plural = "Situaciones"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Descripcion(models.Model):
    nombre = models.CharField("Descripción", max_length=100, unique=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class EstadoMoneda(models.Model):
    nombre = models.CharField("Estado", max_length=50, unique=True)

    class Meta:
        verbose_name = "Estado de Moneda"
        verbose_name_plural = "Estados de Moneda"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class RetiroBuzon(models.Model):
    nombre = models.CharField("Retiro buzón", max_length=100, unique=True)

    class Meta:
        verbose_name = "Retiro Buzón"
        verbose_name_plural = "Retiros Buzón"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class EntregadoA(models.Model):
    nombre = models.CharField("Entregado a", max_length=100, unique=True)

    class Meta:
        verbose_name = "Entregado A"
        verbose_name_plural = "Entregados A"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


# ====== Core ======
class Caja(TimeStampedModel):
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255, blank=True)
    ingreso = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"), validators=MONEY_VALIDATORS)
    egreso = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"), validators=MONEY_VALIDATORS)
    saldo = models.DecimalField(
        max_digits=14, decimal_places=2, help_text="Saldo luego del movimiento", validators=[MinValueValidator(Decimal("-9999999999.99"))]
    )

    class Meta:
        ordering = ["-fecha", "-id"]
        indexes = [
            models.Index(fields=["fecha"]),
        ]

    def __str__(self):
        return f"{self.fecha} - +{self.ingreso} / -{self.egreso} → {self.saldo}"


class MP(TimeStampedModel):
    fecha = models.DateField()
    ingreso = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"), validators=MONEY_VALIDATORS)
    egreso = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"), validators=MONEY_VALIDATORS)
    ganancia = models.DecimalField("Interés", max_digits=12, decimal_places=2, default=Decimal("0.00"), validators=MONEY_VALIDATORS)
    saldo = models.DecimalField(
        max_digits=14, decimal_places=2, help_text="Saldo (incluye intereses por mes/meses)"
    )

    class Meta:
        verbose_name = "Movimiento MP"
        verbose_name_plural = "Movimientos MP"
        ordering = ["-fecha", "-id"]
        indexes = [models.Index(fields=["fecha"])]

    def __str__(self):
        return f"{self.fecha} → {self.saldo}"


class Vencimiento(TimeStampedModel):
    fecha = models.DateField(help_text="Fecha de registro o recepción")
    concepto = models.ForeignKey(Concepto, on_delete=models.PROTECT, related_name="vencimientos")
    descripcion = models.ForeignKey(Descripcion, on_delete=models.PROTECT, related_name="vencimientos")
    fecha_vencimiento = models.DateField()
    importe = models.DecimalField(max_digits=12, decimal_places=2, validators=MONEY_VALIDATORS)
    nota = models.TextField(blank=True)
    estado = models.ForeignKey(EstadoVencimiento, on_delete=models.PROTECT, related_name="vencimientos")
    situacion = models.ForeignKey(Situacion, on_delete=models.PROTECT, related_name="vencimientos")

    class Meta:
        ordering = ["-fecha_vencimiento", "concepto__nombre"]
        indexes = [
            models.Index(fields=["fecha_vencimiento"]),
            models.Index(fields=["concepto"]),
            models.Index(fields=["estado"]),
        ]

    def __str__(self):
        return f"{self.concepto} - vence {self.fecha_vencimiento} - {self.importe}"


UPPER_3 = RegexValidator(regex=r"^[A-Z]{3}$", message=_("Usar código ISO 4217 en mayúsculas (p.ej., USD)."))


class MonedaExtranjera(TimeStampedModel):
    codigo = models.CharField(max_length=3, validators=[UPPER_3], help_text="Código ISO (USD, EUR, etc.)")
    fecha = models.DateField()
    ingreso = models.DecimalField("Ingreso (USD)", max_digits=14, decimal_places=6, default=Decimal("0"), validators=MONEY_VALIDATORS)
    compra_usd = models.DecimalField("Compra (USD)", max_digits=14, decimal_places=6, default=Decimal("0"), validators=MONEY_VALIDATORS)
    compra_ars = models.DecimalField("Compra (ARS)", max_digits=14, decimal_places=2, default=Decimal("0"), validators=MONEY_VALIDATORS)
    egreso_usd = models.DecimalField("Egreso (USD)", max_digits=14, decimal_places=6, default=Decimal("0"), validators=MONEY_VALIDATORS)
    usd_hoy = models.DecimalField("Cotización USD hoy", max_digits=14, decimal_places=4, default=Decimal("0"), validators=MONEY_VALIDATORS)
    venta_ars = models.DecimalField("Venta (ARS)", max_digits=14, decimal_places=2, default=Decimal("0"), validators=MONEY_VALIDATORS)
    saldo_ars = models.DecimalField("Saldo (ARS)", max_digits=16, decimal_places=2)

    estado = models.ForeignKey(EstadoMoneda, on_delete=models.PROTECT, related_name="movimientos_moneda")

    class Meta:
        verbose_name = "Moneda extranjera"
        verbose_name_plural = "Moneda extranjera"
        ordering = ["-fecha", "-id"]
        indexes = [models.Index(fields=["fecha"]), models.Index(fields=["codigo"])]

    def __str__(self):
        return f"{self.codigo} {self.fecha} → {self.saldo_ars} ARS"


class AsignacionSobres(TimeStampedModel):
    sobre_n = models.PositiveSmallIntegerField(
        "Número de sobre", validators=[MinValueValidator(1), MaxValueValidator(50)], unique=True
    )
    hermano = models.CharField(max_length=120)

    class Meta:
        verbose_name = "Asignación de sobres"
        verbose_name_plural = "Asignaciones de sobres"
        ordering = ["sobre_n"]

    def __str__(self):
        return f"Sobre {self.sobre_n} — {self.hermano}"


class Compromiso(TimeStampedModel):
    fecha = models.DateField()
    asignacion = models.ForeignKey(
        AsignacionSobres, on_delete=models.PROTECT, related_name="compromisos", verbose_name="Asignación (Sobre/Hermano)"
    )
    importe = models.DecimalField(max_digits=12, decimal_places=2, validators=MONEY_VALIDATORS)
    saldo = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name_plural = "Compromisos"
        ordering = ["-fecha", "-id"]
        indexes = [models.Index(fields=["fecha"]), models.Index(fields=["asignacion"])]

    def __str__(self):
        return f"{self.fecha} — {self.asignacion} — {self.importe}"

    # Conveniencia para mostrar en admin (sin duplicar columnas)
    @property
    def n_sobre(self):
        return self.asignacion.sobre_n

    @property
    def nombre_hermano(self):
        return self.asignacion.hermano


class OfrendaDonacion(TimeStampedModel):
    fecha = models.DateField()
    retiro_buzon = models.ForeignKey(RetiroBuzon, on_delete=models.PROTECT, related_name="ofrendas")
    entregado_a = models.ForeignKey(EntregadoA, on_delete=models.PROTECT, related_name="ofrendas")
    importe = models.DecimalField(max_digits=12, decimal_places=2, validators=MONEY_VALIDATORS)
    saldo = models.DecimalField(max_digits=12, decimal_places=2)
    concepto = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Ofrenda / Donación"
        verbose_name_plural = "Ofrendas y Donaciones"
        ordering = ["-fecha", "-id"]
        indexes = [models.Index(fields=["fecha"])]

    def __str__(self):
        return f"{self.fecha} — {self.importe} — {self.entregado_a}"


class CuotaInac(TimeStampedModel):
    class Mes(models.IntegerChoices):
        ENE = 1, _("Enero")
        FEB = 2, _("Febrero")
        MAR = 3, _("Marzo")
        ABR = 4, _("Abril")
        MAY = 5, _("Mayo")
        JUN = 6, _("Junio")
        JUL = 7, _("Julio")
        AGO = 8, _("Agosto")
        SEP = 9, _("Septiembre")
        OCT = 10, _("Octubre")
        NOV = 11, _("Noviembre")
        DIC = 12, _("Diciembre")

    hermano = models.CharField(max_length=120)
    mes = models.PositiveSmallIntegerField(choices=Mes.choices)
    anio = models.PositiveSmallIntegerField("Año", validators=[MinValueValidator(1900), MaxValueValidator(3000)])

    class Meta:
        verbose_name = "Cuota INAC"
        verbose_name_plural = "Cuotas INAC"
        ordering = ["-anio", "-mes", "hermano"]
        constraints = [
            models.UniqueConstraint(fields=["hermano", "mes", "anio"], name="unique_cuota_por_mes_anio_hermano")
        ]
        indexes = [models.Index(fields=["anio", "mes"])]

    def __str__(self):
        return f"{self.hermano} — {self.mes}/{self.anio}"
