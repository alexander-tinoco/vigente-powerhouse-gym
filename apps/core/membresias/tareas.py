"""
Motor de vencimientos.

Este es el componente que el gimnasio hoy no tiene. Corre cada hora, revisa
los contratos y cambia los estados sin que nadie tenga que acordarse de
revisar la libreta.
"""

from __future__ import annotations

import logging
from datetime import date, timedelta

from celery import shared_task

from .estados import Estado, transitar

log = logging.getLogger(__name__)

DIAS_AVISO_PREVENCIMIENTO = 7
DIAS_PARA_CANCELACION_AUTOMATICA = 60


def _dias_restantes(fecha_fin: date, hoy: date) -> int:
    return (fecha_fin - hoy).days


def estado_que_corresponde(
    estado_actual: Estado,
    fecha_fin: date,
    dias_gracia: int,
    hoy: date,
) -> Estado | None:
    """
    Dado el estado actual y las fechas, devuelve el estado al que debería
    moverse, o None si no hay nada que hacer.

    Se mantiene como función pura para poder probarla sin base de datos.
    """
    if estado_actual in (Estado.CANCELADA, Estado.CONGELADA, Estado.PENDIENTE):
        return None

    restantes = _dias_restantes(fecha_fin, hoy)

    if restantes < -dias_gracia:
        return Estado.VENCIDA if estado_actual is not Estado.VENCIDA else None

    if restantes < 0:
        return Estado.GRACIA if estado_actual is not Estado.GRACIA else None

    if restantes <= DIAS_AVISO_PREVENCIMIENTO:
        return Estado.POR_VENCER if estado_actual is Estado.ACTIVA else None

    return None


@shared_task(name="membresias.revisar_vencimientos")
def revisar_vencimientos() -> dict[str, int]:
    """
    Tarea programada en Celery Beat. Configurada para correr cada hora en
    config/celery.py.
    """
    from .models import Membresia  # import tardío para no romper el autoload

    hoy = date.today()
    contadores = {"revisadas": 0, "cambiadas": 0, "errores": 0}

    pendientes = Membresia.objects.exclude(
        estado__in=[Estado.CANCELADA, Estado.CONGELADA]
    ).select_related("socio", "plan")

    for membresia in pendientes:
        contadores["revisadas"] += 1
        destino = estado_que_corresponde(
            Estado(membresia.estado),
            membresia.fecha_fin,
            membresia.plan.dias_gracia,
            hoy,
        )
        if destino is None:
            continue

        try:
            membresia.estado = transitar(Estado(membresia.estado), destino)
            membresia.save(update_fields=["estado", "actualizada_en"])
            contadores["cambiadas"] += 1
            log.info(
                "Membresía %s de %s pasó a %s",
                membresia.pk,
                membresia.socio,
                destino.value,
            )
        except Exception:
            contadores["errores"] += 1
            log.exception("Falló la transición de la membresía %s", membresia.pk)

    return contadores


@shared_task(name="membresias.cancelar_abandonadas")
def cancelar_abandonadas() -> int:
    """Cancela las membresías vencidas hace más de 60 días."""
    from .models import Membresia

    corte = date.today() - timedelta(days=DIAS_PARA_CANCELACION_AUTOMATICA)
    candidatas = Membresia.objects.filter(estado=Estado.VENCIDA, fecha_fin__lt=corte)

    canceladas = 0
    for membresia in candidatas:
        membresia.estado = transitar(Estado.VENCIDA, Estado.CANCELADA)
        membresia.save(update_fields=["estado", "actualizada_en"])
        canceladas += 1

    return canceladas
