"""
Ciclo de vida de una membresía, implementado con el patrón State.

El problema que resuelve: hoy el gimnasio no tiene ningún mecanismo que haga
que el vencimiento de una membresía dispare una consecuencia. Aquí cada estado
declara explícitamente a qué otros estados puede transitar y qué permisos
otorga, en vez de dejarlo repartido en condicionales por todo el código.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Estado(str, Enum):
    PENDIENTE = "pendiente"
    ACTIVA = "activa"
    POR_VENCER = "por_vencer"
    GRACIA = "gracia"
    VENCIDA = "vencida"
    CONGELADA = "congelada"
    CANCELADA = "cancelada"


class TransicionInvalida(Exception):
    """Se intentó una transición que el estado actual no permite."""

    def __init__(self, origen: Estado, destino: Estado):
        super().__init__(
            f"No se puede pasar de {origen.value} a {destino.value}. "
            f"Transiciones válidas desde {origen.value}: "
            f"{', '.join(e.value for e in TRANSICIONES[origen])}"
        )
        self.origen = origen
        self.destino = destino


# Única fuente de verdad de las transiciones permitidas.
TRANSICIONES: dict[Estado, frozenset[Estado]] = {
    Estado.PENDIENTE: frozenset({Estado.ACTIVA, Estado.CANCELADA}),
    Estado.ACTIVA: frozenset({Estado.POR_VENCER, Estado.CONGELADA, Estado.CANCELADA}),
    Estado.POR_VENCER: frozenset({Estado.ACTIVA, Estado.GRACIA, Estado.CONGELADA}),
    Estado.GRACIA: frozenset({Estado.ACTIVA, Estado.VENCIDA}),
    Estado.VENCIDA: frozenset({Estado.ACTIVA, Estado.CANCELADA}),
    Estado.CONGELADA: frozenset({Estado.ACTIVA, Estado.CANCELADA}),
    Estado.CANCELADA: frozenset(),
}

# Estados que permiten pasar el torniquete. GRACIA entra aquí a propósito:
# el socio pasa, pero la pantalla le avisa cuántos días lleva vencido.
ESTADOS_CON_ACCESO: frozenset[Estado] = frozenset(
    {Estado.ACTIVA, Estado.POR_VENCER, Estado.GRACIA}
)


@dataclass(frozen=True)
class ResultadoAcceso:
    permitido: bool
    motivo: str
    advertencia: str | None = None


def puede_transitar(origen: Estado, destino: Estado) -> bool:
    return destino in TRANSICIONES[origen]


def transitar(origen: Estado, destino: Estado) -> Estado:
    """Devuelve el estado destino, o levanta TransicionInvalida."""
    if not puede_transitar(origen, destino):
        raise TransicionInvalida(origen, destino)
    return destino


def evaluar_acceso(estado: Estado, dias_restantes: int) -> ResultadoAcceso:
    """
    Decide si el torniquete abre.

    El caso de GRACIA es el que ataca el problema original: el socio entra,
    pero ve su situación en la pantalla cada vez que pasa. El torniquete se
    convierte en el punto de cobranza y nadie tiene que confrontarlo en
    recepción.
    """
    if estado not in ESTADOS_CON_ACCESO:
        return ResultadoAcceso(
            permitido=False,
            motivo=f"Membresía {estado.value}. Pasa a recepción.",
        )

    if estado is Estado.GRACIA:
        return ResultadoAcceso(
            permitido=True,
            motivo="Acceso permitido en periodo de gracia",
            advertencia=f"Tu membresía venció hace {abs(dias_restantes)} día(s)",
        )

    if estado is Estado.POR_VENCER:
        return ResultadoAcceso(
            permitido=True,
            motivo="Acceso permitido",
            advertencia=f"Tu membresía vence en {dias_restantes} día(s)",
        )

    return ResultadoAcceso(permitido=True, motivo="Acceso permitido")
