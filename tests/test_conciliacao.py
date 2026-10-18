from datetime import date

import pytest

from financeiro.categoria import Categoria
from financeiro.conciliacao import Conciliacao
from financeiro.lancamento import Lancamento


class TestConciliacao:

    def setup_method(self) -> None:
        self.cat = Categoria("Alimentacao")

    def test_conciliacao_bate(self) -> None:
        debito = Lancamento("Mercado", 100.0, date(2026, 8, 1), self.cat, "debito")
        credito = Lancamento("Estorno", 100.0, date(2026, 8, 2), self.cat, "credito")
        c = Conciliacao([debito, credito])
        assert c.esta_conciliada() is True
        c.verificar()

    def test_conciliacao_nao_bate(self) -> None:
        debito = Lancamento("Mercado", 150.0, date(2026, 8, 1), self.cat, "debito")
        credito = Lancamento("Estorno", 100.0, date(2026, 8, 2), self.cat, "credito")
        c = Conciliacao([debito, credito])
        assert c.esta_conciliada() is False

    def test_verificar_lanca_erro_quando_nao_bate(self) -> None:
        debito = Lancamento("Mercado", 150.0, date(2026, 8, 1), self.cat, "debito")
        c = Conciliacao([debito])
        with pytest.raises(ValueError):
            c.verificar()

    def test_conciliacao_sem_lancamentos_bate(self) -> None:
        c = Conciliacao([])
        assert c.esta_conciliada() is True
