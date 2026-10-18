import pytest

from financeiro.estrategia_correcao import CorrecaoIPCA, CorrecaoSelic


class TestCorrecaoIPCA:

    def test_aplica_percentual_de_correcao(self) -> None:
        estrategia = CorrecaoIPCA(10.0)
        assert estrategia.calcular(1000.0) == 1100.0

    def test_indice_zero_nao_altera_o_valor(self) -> None:
        estrategia = CorrecaoIPCA(0.0)
        assert estrategia.calcular(1000.0) == 1000.0

    def test_indice_negativo_lanca_erro(self) -> None:
        with pytest.raises(ValueError):
            CorrecaoIPCA(-1.0)


class TestCorrecaoSelic:

    def test_aplica_percentual_de_correcao(self) -> None:
        estrategia = CorrecaoSelic(5.0)
        assert estrategia.calcular(2000.0) == 2100.0

    def test_indice_negativo_lanca_erro(self) -> None:
        with pytest.raises(ValueError):
            CorrecaoSelic(-1.0)
