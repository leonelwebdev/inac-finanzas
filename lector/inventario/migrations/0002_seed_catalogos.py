# inventario/migrations/0002_seed_catalogos.py
from django.db import migrations

ESTADOS_VENC = [
    "Llegó", "No llegó", "Ver por internet", "A vencer",
    "Vencida", "Pagada", "Cobro", "No pagada",
]

CONCEPTOS = [
    "Luz iglesia", "Luz casa pastoral", "Gas iglesia",
    "Librería", "Art. Limpieza", "Otros",
]

SITUACIONES = [
    "Efectivo", "Débito", "Personal MP", "Otros", "Chequeado",
]

DESCRIPCIONES = [
    "Iglesia", "Casa pastoral", "Escuelita",
]

ESTADOS_MONEDA = [
    "Activo", "En proceso", "Terminado",
]

RETIRO_BUZON = [
    "Omar Brizuela - Pastor",
    "Javier Bravo - Tesorero",
    "Sebastián Staropolis - Diácono",
    "Eduardo Intorre - Secretario",
]

ENTREGADO_A = [
    "Javier Bravo - Tesorero",
    "Lucas Apellido - Protesorero",
]


def seed_forward(apps, schema_editor):
    EstadoVencimiento = apps.get_model("inventario", "EstadoVencimiento")
    Concepto = apps.get_model("inventario", "Concepto")
    Situacion = apps.get_model("inventario", "Situacion")
    Descripcion = apps.get_model("inventario", "Descripcion")
    EstadoMoneda = apps.get_model("inventario", "EstadoMoneda")
    RetiroBuzon = apps.get_model("inventario", "RetiroBuzon")
    EntregadoA = apps.get_model("inventario", "EntregadoA")

    for nombre in ESTADOS_VENC:
        EstadoVencimiento.objects.get_or_create(nombre=nombre)

    for nombre in CONCEPTOS:
        Concepto.objects.get_or_create(nombre=nombre)

    for nombre in SITUACIONES:
        Situacion.objects.get_or_create(nombre=nombre)

    for nombre in DESCRIPCIONES:
        Descripcion.objects.get_or_create(nombre=nombre)

    for nombre in ESTADOS_MONEDA:
        EstadoMoneda.objects.get_or_create(nombre=nombre)

    for nombre in RETIRO_BUZON:
        RetiroBuzon.objects.get_or_create(nombre=nombre)

    for nombre in ENTREGADO_A:
        EntregadoA.objects.get_or_create(nombre=nombre)


def seed_reverse(apps, schema_editor):
    EstadoVencimiento = apps.get_model("inventario", "EstadoVencimiento")
    Concepto = apps.get_model("inventario", "Concepto")
    Situacion = apps.get_model("inventario", "Situacion")
    Descripcion = apps.get_model("inventario", "Descripcion")
    EstadoMoneda = apps.get_model("inventario", "EstadoMoneda")
    RetiroBuzon = apps.get_model("inventario", "RetiroBuzon")
    EntregadoA = apps.get_model("inventario", "EntregadoA")

    EstadoVencimiento.objects.filter(nombre__in=ESTADOS_VENC).delete()
    Concepto.objects.filter(nombre__in=CONCEPTOS).delete()
    Situacion.objects.filter(nombre__in=SITUACIONES).delete()
    Descripcion.objects.filter(nombre__in=DESCRIPCIONES).delete()
    EstadoMoneda.objects.filter(nombre__in=ESTADOS_MONEDA).delete()
    RetiroBuzon.objects.filter(nombre__in=RETIRO_BUZON).delete()
    EntregadoA.objects.filter(nombre__in=ENTREGADO_A).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("inventario", "0001_initial"),  # <-- ajustá si tu última migración no es 0001
    ]

    operations = [
        migrations.RunPython(seed_forward, seed_reverse),
    ]
