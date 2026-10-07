"""
Pruebas del motor de vencimientos.

Las fronteras de fecha son lo que más se rompe en este tipo de lógica, así que
están cubiertas una por una.
"""

from datetime import date

import pytest

from apps.core.membresias.estados import Estado
from apps.core.membresias.tareas import estado_que_corresponde

HOY = date(2026, 10, 7)


def corresponde(estado, fecha_fin, dias_gracia=3):
    return estado_que_corresponde(estado, fecha_fin, dias_gracia, HOY)


class TestAvisoPrevencimiento:
    def test_falta_mucho_y_no_pasa_nada(self):
        assert corresponde(Estado.ACTIVA, date(2026, 11, 20)) is None

    def test_a_ocho_dias_todavia_no_avisa(self):
        assert corresponde(Estado.ACTIVA, date(2026, 10, 15)) is None

    def test_a_siete_dias_entra_en_por_vencer(self):
        assert corresponde(Estado.ACTIVA, date(2026, 10, 14)) is Estado.POR_VENCER

    def test_no_reavisa_si_ya_estaba_por_vencer(self):
        assert corresponde(Estado.POR_VENCER, date(2026, 10, 10)) is None


class TestGracia:
    def test_el_dia_del_vencimiento_todavia_no_entra_en_gracia(self):
        assert corresponde(Estado.POR_VENCER, HOY) is None

    def test_al_dia_siguiente_entra_en_gracia(self):
        assert corresponde(Estado.POR_VENCER, date(2026, 10, 6)) is Estado.GRACIA

    def test_el_ultimo_dia_de_gracia_sigue_en_gracia(self):
        assert corresponde(Estado.POR_VENCER, date(2026, 10, 4)) is Estado.GRACIA

    def test_agotada_la_gracia_vence(self):
        assert corresponde(Estado.GRACIA, date(2026, 10, 3)) is Estado.VENCIDA

    def test_los_dias_de_gracia_son_configurables_por_plan(self):
        # Con 10 días de gracia, la misma fecha sigue en gracia.
        assert estado_que_corresponde(Estado.GRACIA, date(2026, 10, 3), 10, HOY) is None


class TestEstadosQueNoSeTocan:
    @pytest.mark.parametrize(
        "estado", [Estado.CANCELADA, Estado.CONGELADA, Estado.PENDIENTE]
    )
    def test_el_motor_no_toca_estos_estados(self, estado):
        assert corresponde(estado, date(2020, 1, 1)) is None

    def test_una_membresia_congelada_no_vence_aunque_pase_la_fecha(self):
        assert corresponde(Estado.CONGELADA, date(2025, 1, 1)) is None
