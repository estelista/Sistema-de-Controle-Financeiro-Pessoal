from datetime import date

import pytest

from financeiro.categoria import Categoria
from financeiro.lancamento import Lancamento


class TestLancamento:

    def setup_method(self) -> None:
        self.cat = Categoria("Alimentacao")

    def test_cria_lancamento_debito(self) -> None:
        l = Lancamento("Mercado", 150.0, date(2026, 8, 1), self.cat, "debito")
        assert l.descricao == "Mercado"
        assert l.valor == 150.0
        assert l.categoria is self.cat
        assert l.eh_debito() is True
        assert l.eh_credito() is False

    def test_cria_lancamento_credito(self) -> None:
        l = Lancamento("Salario", 3000.0, date(2026, 8, 5), self.cat, "credito")
        assert l.eh_credito() is True
        assert l.eh_debito() is False

    def test_valor_invalido_zero(self) -> None:
        with pytest.raises(ValueError):
            Lancamento("Mercado", 0, date(2026, 8, 1), self.cat, "debito")

    def test_valor_invalido_negativo(self) -> None:
        with pytest.raises(ValueError):
            Lancamento("Mercado", -10, date(2026, 8, 1), self.cat, "debito")

    def test_tipo_invalido(self) -> None:
        with pytest.raises(ValueError):
            Lancamento("Mercado", 10, date(2026, 8, 1), self.cat, "transferencia")
