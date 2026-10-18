from datetime import date

import pytest

from financeiro.aplicacao import Aplicacao
from financeiro.estrategia_rendimento import JurosCompostos, JurosSimples


class TestAplicacao:

    def test_cria_aplicacao_com_dados_basicos(self) -> None:
        aplicacao = Aplicacao("Poupanca", 1000.0, date(2026, 1, 1), JurosSimples(0.005))
        assert aplicacao.descricao == "Poupanca"
        assert aplicacao.valor_aplicado == 1000.0

    def test_valor_invalido_lanca_erro(self) -> None:
        with pytest.raises(ValueError):
            Aplicacao("Poupanca", 0, date(2026, 1, 1), JurosSimples(0.005))

    def test_calcular_valor_atual_delega_para_a_estrategia(self) -> None:
        aplicacao = Aplicacao("CDB", 1000.0, date(2026, 1, 1), JurosCompostos(0.10))
        assert round(aplicacao.calcular_valor_atual(2), 2) == 1210.0

    def test_calcular_rendimento_e_so_o_ganho(self) -> None:
        aplicacao = Aplicacao("CDB", 1000.0, date(2026, 1, 1), JurosCompostos(0.10))
        assert round(aplicacao.calcular_rendimento(2), 2) == 210.0

    def test_troca_de_estrategia_muda_o_resultado(self) -> None:
        poupanca = Aplicacao("Poupanca", 1000.0, date(2026, 1, 1), JurosSimples(0.02))
        cdb = Aplicacao("CDB", 1000.0, date(2026, 1, 1), JurosCompostos(0.02))
        assert cdb.calcular_valor_atual(12) > poupanca.calcular_valor_atual(12)
