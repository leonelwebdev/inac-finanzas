from django.contrib import admin
from django.db.models import DecimalField
from django.forms import TextInput

from unfold.contrib.filters.admin import RangeDateFilter

from . import models


# ========== Utilidades ==========
class MoneyAdminMixin:
    """Hace inputs más anchos para decimales en el admin."""
    formfield_overrides = {
        DecimalField: {"widget": TextInput(attrs={"style": "width: 140px"})}
    }


# ========== Lookups / Catálogos ==========
@admin.register(models.EstadoVencimiento)
class EstadoVencimientoAdmin(admin.ModelAdmin):
    search_fields = ["nombre"]
    list_display = ["nombre"]
    ordering = ["nombre"]


@admin.register(models.Concepto)
class ConceptoAdmin(admin.ModelAdmin):
    search_fields = ["nombre"]
    list_display = ["nombre"]
    ordering = ["nombre"]


@admin.register(models.Situacion)
class SituacionAdmin(admin.ModelAdmin):
    search_fields = ["nombre"]
    list_display = ["nombre"]
    ordering = ["nombre"]


@admin.register(models.Descripcion)
class DescripcionAdmin(admin.ModelAdmin):
    search_fields = ["nombre"]
    list_display = ["nombre"]
    ordering = ["nombre"]


@admin.register(models.EstadoMoneda)
class EstadoMonedaAdmin(admin.ModelAdmin):
    search_fields = ["nombre"]
    list_display = ["nombre"]
    ordering = ["nombre"]


@admin.register(models.RetiroBuzon)
class RetiroBuzonAdmin(admin.ModelAdmin):
    search_fields = ["nombre"]
    list_display = ["nombre"]
    ordering = ["nombre"]


@admin.register(models.EntregadoA)
class EntregadoAAdmin(admin.ModelAdmin):
    search_fields = ["nombre"]
    list_display = ["nombre"]
    ordering = ["nombre"]


# ========== Core ==========
@admin.register(models.Caja)
class CajaAdmin(MoneyAdminMixin, admin.ModelAdmin):
    date_hierarchy = "fecha"
    list_display = ["fecha", "descripcion", "ingreso", "egreso", "saldo"]
    list_filter = (("fecha", RangeDateFilter),)
    search_fields = ["descripcion"]
    ordering = ["-fecha", "-id"]

    fieldsets = (
        ("Movimiento", {"classes": ("tab",), "fields": ("fecha", "descripcion")}),
        ("Valores", {"classes": ("tab",), "fields": (("ingreso", "egreso", "saldo"),)}),
        ("Metadatos", {"classes": ("tab",), "fields": (("created_at", "updated_at"),)}),
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(models.MP)
class MPAdmin(MoneyAdminMixin, admin.ModelAdmin):
    date_hierarchy = "fecha"
    list_display = ["fecha", "ingreso", "egreso", "ganancia", "saldo"]
    list_filter = (("fecha", RangeDateFilter),)
    search_fields = []
    ordering = ["-fecha", "-id"]

    fieldsets = (
        ("Movimiento", {"classes": ("tab",), "fields": ("fecha",)}),
        ("Valores", {"classes": ("tab",), "fields": (("ingreso", "egreso", "ganancia", "saldo"),)}),
        ("Metadatos", {"classes": ("tab",), "fields": (("created_at", "updated_at"),)}),
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(models.Vencimiento)
class VencimientoAdmin(MoneyAdminMixin, admin.ModelAdmin):
    date_hierarchy = "fecha_vencimiento"
    list_display = [
        "fecha_vencimiento",
        "concepto",
        "descripcion",
        "importe",
        "estado",
        "situacion",
        "fecha",
    ]
    list_filter = (
        ( "fecha_vencimiento", RangeDateFilter),
        ("fecha", RangeDateFilter),
        "concepto",
        "estado",
        "situacion",
        "descripcion",
    )
    search_fields = ["nota"]
    ordering = ["-fecha_vencimiento", "concepto__nombre"]

    autocomplete_fields = ["concepto", "descripcion", "estado", "situacion"]

    fieldsets = (
        ("Datos", {"classes": ("tab",), "fields": (("fecha", "fecha_vencimiento"), ("concepto", "descripcion"))}),
        ("Estado", {"classes": ("tab",), "fields": (("estado", "situacion"),)}),
        ("Importe y notas", {"classes": ("tab",), "fields": ("importe", "nota")}),
        ("Metadatos", {"classes": ("tab",), "fields": (("created_at", "updated_at"),)}),
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(models.MonedaExtranjera)
class MonedaExtranjeraAdmin(MoneyAdminMixin, admin.ModelAdmin):
    date_hierarchy = "fecha"
    list_display = [
        "fecha",
        "codigo",
        "ingreso",
        "compra_usd",
        "compra_ars",
        "egreso_usd",
        "usd_hoy",
        "venta_ars",
        "saldo_ars",
        "estado",
    ]
    list_filter = (("fecha", RangeDateFilter), "codigo", "estado")
    search_fields = []
    ordering = ["-fecha", "-id"]
    autocomplete_fields = ["estado"]

    fieldsets = (
        ("Datos", {"classes": ("tab",), "fields": (("fecha", "codigo"), "estado")}),
        ("Movimientos", {
            "classes": ("tab",),
            "fields": (
                ("ingreso", "egreso_usd"),
                ("compra_usd", "compra_ars"),
                ("venta_ars", "usd_hoy"),
                "saldo_ars",
            ),
        }),
        ("Metadatos", {"classes": ("tab",), "fields": (("created_at", "updated_at"),)}),
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(models.AsignacionSobres)
class AsignacionSobresAdmin(admin.ModelAdmin):
    list_display = ["sobre_n", "hermano", "created_at"]
    search_fields = ["hermano"]
    ordering = ["sobre_n"]
    list_filter = []
    readonly_fields = ("created_at", "updated_at")


@admin.register(models.Compromiso)
class CompromisoAdmin(MoneyAdminMixin, admin.ModelAdmin):
    date_hierarchy = "fecha"
    list_display = ["fecha", "n_sobre", "nombre_hermano", "importe", "saldo"]
    list_select_related = ["asignacion"]
    list_filter = (("fecha", RangeDateFilter),)
    search_fields = ["asignacion__hermano"]
    ordering = ["-fecha", "-id"]
    autocomplete_fields = ["asignacion"]

    # Solo mostramos asignación; n_sobre y nombre_hermano vienen por propiedades
    fieldsets = (
        ("Datos", {"classes": ("tab",), "fields": ("fecha", "asignacion")}),
        ("Valores", {"classes": ("tab",), "fields": (("importe", "saldo"),)}),
        ("Lectura", {"classes": ("tab",), "fields": ("n_sobre", "nombre_hermano")}),
        ("Metadatos", {"classes": ("tab",), "fields": (("created_at", "updated_at"),)}),
    )
    readonly_fields = ("n_sobre", "nombre_hermano", "created_at", "updated_at")


@admin.register(models.OfrendaDonacion)
class OfrendaDonacionAdmin(MoneyAdminMixin, admin.ModelAdmin):
    date_hierarchy = "fecha"
    list_display = ["fecha", "retiro_buzon", "entregado_a", "importe", "saldo", "concepto"]
    list_filter = (("fecha", RangeDateFilter), "retiro_buzon", "entregado_a")
    search_fields = ["concepto"]
    ordering = ["-fecha", "-id"]
    autocomplete_fields = ["retiro_buzon", "entregado_a"]

    fieldsets = (
        ("Datos", {"classes": ("tab",), "fields": (("fecha",), ("retiro_buzon", "entregado_a"))}),
        ("Valores", {"classes": ("tab",), "fields": (("importe", "saldo"), "concepto")}),
        ("Metadatos", {"classes": ("tab",), "fields": (("created_at", "updated_at"),)}),
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(models.CuotaInac)
class CuotaInacAdmin(admin.ModelAdmin):
    list_display = ["anio", "mes", "hermano", "created_at"]
    list_filter = ["anio", "mes"]
    search_fields = ["hermano"]
    ordering = ["-anio", "-mes", "hermano"]
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Cuota", {"classes": ("tab",), "fields": (("anio", "mes"), "hermano")}),
        ("Metadatos", {"classes": ("tab",), "fields": (("created_at", "updated_at"),)}),
    )
