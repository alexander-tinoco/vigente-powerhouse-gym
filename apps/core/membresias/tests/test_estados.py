"""
Pruebas de la máquina de estados.

Lo importante aquí no son las transiciones válidas sino las inválidas: el
problema del gimnasio es justamente que hoy nada impide que alguien vencido
siga entrando.
"""

import pytest

from apps.core.membresias.estados import (
    ESTADOS_CON_ACCESO,
    TRANSICIONES,
    Estado,
    TransicionInvalida,
    evaluar_acceso,
    puede_transitar,
    transitar,
)


class TestTransicionesValidas:
    def test_pendiente_pasa_a_activa_con_el_pago(self):
        assert transitar(Estado.PENDIENTE, Estado.ACTIVA) is Estado.ACTIVA

    def test_activa_avisa_antes_de_vencer(self):
        assert transitar(Estado.ACTIVA, Estado.POR_VENCER) is Estado.POR_VENCER

    def test_por_vencer_entra_en_gracia_al_llegar_la_fecha(self):
        assert transitar(Estado.POR_VENCER, Estado.GRACIA) is Estado.GRACIA

    def test_gracia_se_agota_y_vence(self):
        assert transitar(Estado.GRACIA, Estado.VENCIDA) is Estado.VENCIDA

    def test_renovar_reactiva_desde_vencida(self):
        assert transitar(Estado.VENCIDA, Estado.ACTIVA) is Estado.ACTIVA

    def test_congelar_y_reactivar(self):
        congelada = transitar(Estado.ACTIVA, Estado.CONGELADA)
        assert transitar(congelada, Estado.ACTIVA) is Estado.ACTIVA


class TestTransicionesInvalidas:
    def test_cancelada_es_terminal(self):
        for destino in Estado:
            if destino is Estado.CANCELADA:
                continue
            with pytest.raises(TransicionInvalida):
                transitar(Estado.CANCELADA, destino)

    def test_no_se_salta_de_activa_a_vencida_sin_pasar_por_gracia(self):
        with pytest.raises(TransicionInvalida):
            transitar(Estado.ACTIVA, Estado.VENCIDA)

    def test_no_se_congela_una_membresia_vencida(self):
        with pytest.raises(TransicionInvalida):
            transitar(Estado.VENCIDA, Estado.CONGELADA)

    def test_no_se_entra_en_gracia_desde_congelada(self):
        with pytest.raises(TransicionInvalida):
            transitar(Estado.CONGELADA, Estado.GRACIA)

    def test_el_error_dice_cuales_si_eran_validas(self):
        with pytest.raises(TransicionInvalida) as exc:
            transitar(Estado.ACTIVA, Estado.VENCIDA)
        assert "por_vencer" in str(exc.value)


class TestAcceso:
    def test_vencida_no_abre_el_torniquete(self):
        resultado = evaluar_acceso(Estado.VENCIDA, dias_restantes=-5)
        assert resultado.permitido is False
        assert "recepción" in resultado.motivo

    def test_cancelada_no_abre_el_torniquete(self):
        assert evaluar_acceso(Estado.CANCELADA, -30).permitido is False

    def test_congelada_no_abre_el_torniquete(self):
        assert evaluar_acceso(Estado.CONGELADA, 10).permitido is False

    def test_gracia_abre_pero_avisa(self):
        resultado = evaluar_acceso(Estado.GRACIA, dias_restantes=-2)
        assert resultado.permitido is True
        assert resultado.advertencia == "Tu membresía venció hace 2 día(s)"

    def test_por_vencer_abre_y_avisa_cuantos_faltan(self):
        resultado = evaluar_acceso(Estado.POR_VENCER, dias_restantes=3)
        assert resultado.permitido is True
        assert "3 día(s)" in resultado.advertencia

    def test_activa_abre_sin_advertencia(self):
        resultado = evaluar_acceso(Estado.ACTIVA, dias_restantes=20)
        assert resultado.permitido is True
        assert resultado.advertencia is None


class TestIntegridadDelModelo:
    def test_todos_los_estados_estan_declarados(self):
        assert set(TRANSICIONES.keys()) == set(Estado)

    def test_ningun_estado_transita_a_uno_inexistente(self):
        for destinos in TRANSICIONES.values():
            assert destinos <= set(Estado)

    def test_los_estados_con_acceso_son_los_esperados(self):
        assert ESTADOS_CON_ACCESO == {
            Estado.ACTIVA,
            Estado.POR_VENCER,
            Estado.GRACIA,
        }

    def test_puede_transitar_coincide_con_transitar(self):
        for origen in Estado:
            for destino in Estado:
                if puede_transitar(origen, destino):
                    assert transitar(origen, destino) is destino
                else:
                    with pytest.raises(TransicionInvalida):
                        transitar(origen, destino)
