from django.db import models
from django.db.models import Q, UniqueConstraint

from .estados import Estado


class Plan(models.Model):
    nombre = models.CharField(max_length=80)
    precio_centavos = models.PositiveIntegerField(
        help_text="En centavos. Nunca float: el dinero no se guarda en punto flotante."
    )
    duracion_dias = models.PositiveSmallIntegerField()
    dias_gracia = models.PositiveSmallIntegerField(default=3)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "plan"

    def __str__(self) -> str:
        return self.nombre


class Socio(models.Model):
    nombre = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=120)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    meta_visitas_semanal = models.PositiveSmallIntegerField(default=3)
    alta_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "socio"
        indexes = [models.Index(fields=["apellidos", "nombre"])]

    def __str__(self) -> str:
        return f"{self.nombre} {self.apellidos}"


class Membresia(models.Model):
    socio = models.ForeignKey(
        Socio, on_delete=models.PROTECT, related_name="membresias"
    )
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    estado = models.CharField(
        max_length=20,
        choices=[(e.value, e.value) for e in Estado],
        default=Estado.PENDIENTE.value,
        db_index=True,
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(db_index=True)
    creada_en = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "membresia"
        constraints = [
            # Un socio puede tener muchas membresías en el tiempo, pero solo
            # una vigente a la vez. Se garantiza en la base de datos y no solo
            # en el código, porque el código se nos puede olvidar.
            UniqueConstraint(
                fields=["socio"],
                condition=Q(
                    estado__in=[
                        Estado.ACTIVA.value,
                        Estado.POR_VENCER.value,
                        Estado.GRACIA.value,
                    ]
                ),
                name="una_membresia_vigente_por_socio",
            )
        ]

    def __str__(self) -> str:
        return f"{self.socio} · {self.plan} · {self.estado}"


class CambioDeEstado(models.Model):
    """Bitácora para poder auditar por qué una membresía está como está."""

    membresia = models.ForeignKey(
        Membresia, on_delete=models.CASCADE, related_name="historial"
    )
    estado_anterior = models.CharField(max_length=20)
    estado_nuevo = models.CharField(max_length=20)
    motivo = models.CharField(max_length=200)
    ocurrio_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cambio_estado_membresia"
        ordering = ["-ocurrio_en"]
