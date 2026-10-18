from datetime import date

from financeiro.categoria import Categoria
from financeiro.conciliacao import Conciliacao
from financeiro.extrato import Extrato
from financeiro.fechamento import Fechamento
from financeiro.lancamento import Lancamento


class TestExtrato:

    def setup_method(self) -> None:
        self.cat = Categoria("Alimentacao")
        self.debito = Lancamento("Mercado", 150.0, date(2026, 8, 1), self.cat, "debito")
        self.credito = Lancamento("Salario", 3000.0, date(2026, 8, 5), self.cat, "credito")
        self.fechamento1 = Fechamento("2026-08", [self.debito, self.credito])

    def test_extrato_consolida_um_fechamento(self) -> None:
        e = Extrato("2026-08", [self.fechamento1])
        assert e.total_lancamentos() == 2
        assert e.total_debitos() == 150.0
        assert e.total_creditos() == 3000.0
        assert e.saldo_final() == 2850.0

    def test_extrato_consolida_varios_fechamentos(self) -> None:
        debito2 = Lancamento("Aluguel", 1000.0, date(2026, 9, 1), self.cat, "debito")
        fechamento2 = Fechamento("2026-09", [debito2])
        e = Extrato("2026-08 a 2026-09", [self.fechamento1, fechamento2])
        assert e.total_lancamentos() == 3
        assert e.total_debitos() == 1150.0
        assert e.total_creditos() == 3000.0

    def test_extrato_sem_fechamentos(self) -> None:
        e = Extrato("2026-08", [])
        assert e.total_lancamentos() == 0
        assert e.saldo_final() == 0.0

    def test_detecta_conciliacao_pendente(self) -> None:
        e = Extrato("2026-08", [self.fechamento1])
        conciliacao_pendente = Conciliacao([self.debito])
        assert e.possui_conciliacao_pendente([conciliacao_pendente]) is True

    def test_sem_conciliacao_pendente(self) -> None:
        e = Extrato("2026-08", [self.fechamento1])
        credito_igual = Lancamento("Estorno", 150.0, date(2026, 8, 2), self.cat, "credito")
        conciliacao_ok = Conciliacao([self.debito, credito_igual])
        assert e.possui_conciliacao_pendente([conciliacao_ok]) is False

    def test_gerar_resumo_contem_periodo(self) -> None:
        e = Extrato("2026-08", [self.fechamento1])
        resumo = e.gerar_resumo()
        assert "2026-08" in resumo
