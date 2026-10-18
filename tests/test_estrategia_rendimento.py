import pytest

from financeiro.estrategia_rendimento import JurosCompostos, JurosSimples


class TestJurosSimples:

    def test_calcula_rendimento_apos_alguns_meses(self) -> None:
        estrategia = JurosSimples(0.01)
        assert estrategia.calcular(1000.0, 10) == 1100.0

    def test_zero_meses_devolve_o_capital(self) -> None:
        estrategia = JurosSimples(0.01)
        assert estrategia.calcular(1000.0, 0) == 1000.0

    def test_taxa_negativa_lanca_erro(self) -> None:
        with pytest.raises(ValueError):
            JurosSimples(-0.01)

    def test_meses_negativo_lanca_erro(self) -> None:
        estrategia = JurosSimples(0.01)
        with pytest.raises(ValueError):
            estrategia.calcular(1000.0, -1)


class TestJurosCompostos:

    def test_calcula_rendimento_apos_alguns_meses(self) -> None:
        estrategia = JurosCompostos(0.10)
        assert round(estrategia.calcular(1000.0, 2), 2) == 1210.0

    def test_zero_meses_devolve_o_capital(self) -> None:
        estrategia = JurosCompostos(0.01)
        assert estrategia.calcular(1000.0, 0) == 1000.0

    def test_taxa_negativa_lanca_erro(self) -> None:
        with pytest.raises(ValueError):
            JurosCompostos(-0.01)

    def test_meses_negativo_lanca_erro(self) -> None:
        estrategia = JurosCompostos(0.01)
        with pytest.raises(ValueError):
            estrategia.calcular(1000.0, -1)

    def test_composto_rende_mais_que_simples_com_mesma_taxa(self) -> None:
        simples = JurosSimples(0.02)
        composto = JurosCompostos(0.02)
        assert composto.calcular(1000.0, 12) > simples.calcular(1000.0, 12)
