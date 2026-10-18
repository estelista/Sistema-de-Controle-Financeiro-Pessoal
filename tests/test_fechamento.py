from datetime import date

from financeiro.categoria import Categoria
from financeiro.fechamento import Fechamento
from financeiro.lancamento import Lancamento


class TestFechamento:

    def setup_method(self) -> None:
        self.cat = Categoria("Alimentacao")
        self.debito = Lancamento("Mercado", 150.0, date(2026, 8, 1), self.cat, "debito")
        self.credito = Lancamento("Salario", 3000.0, date(2026, 8, 5), self.cat, "credito")

    def test_fechamento_vazio(self) -> None:
        f = Fechamento("2026-08", [])
        assert f.quantidade_lancamentos() == 0
        assert f.total_debitos() == 0.0
        assert f.total_creditos() == 0.0
        assert f.saldo() == 0.0

    def test_fechamento_consolida_lancamentos(self) -> None:
        f = Fechamento("2026-08", [self.debito, self.credito])
        assert f.quantidade_lancamentos() == 2
        assert f.total_debitos() == 150.0
        assert f.total_creditos() == 3000.0
        assert f.saldo() == 2850.0

    def test_fechamento_referencia_lancamentos_originais(self) -> None:
        f = Fechamento("2026-08", [self.debito])
        assert f.lancamentos[0] is self.debito

    def test_lista_interna_e_copia(self) -> None:
        lista = [self.debito]
        f = Fechamento("2026-08", lista)
        lista.append(self.credito)
        assert f.quantidade_lancamentos() == 1
