import pytest

from financeiro.conta import Conta


class TestConta:

    def test_cria_conta_com_nome_e_saldo_zero(self) -> None:
        c = Conta("Carteira")
        assert c.nome == "Carteira"
        assert c.saldo == 0.0

    def test_cria_conta_com_saldo_inicial(self) -> None:
        c = Conta("Carteira", 100.0)
        assert c.saldo == 100.0

    def test_creditar_aumenta_saldo(self) -> None:
        c = Conta("Carteira", 100.0)
        c.creditar(50.0)
        assert c.saldo == 150.0

    def test_debitar_diminui_saldo(self) -> None:
        c = Conta("Carteira", 100.0)
        c.debitar(30.0)
        assert c.saldo == 70.0

    def test_creditar_valor_invalido(self) -> None:
        c = Conta("Carteira")
        with pytest.raises(ValueError):
            c.creditar(0)

    def test_debitar_valor_invalido(self) -> None:
        c = Conta("Carteira")
        with pytest.raises(ValueError):
            c.debitar(-10)
