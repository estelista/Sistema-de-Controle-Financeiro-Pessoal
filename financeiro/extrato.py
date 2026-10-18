from financeiro.conciliacao import Conciliacao
from financeiro.fechamento import Fechamento


class Extrato:

    def __init__(self, periodo: str, fechamentos: list[Fechamento]) -> None:
        self._periodo = periodo
        self._fechamentos = list(fechamentos)

    @property
    def periodo(self) -> str:
        return self._periodo

    def total_lancamentos(self) -> int:
        return sum(f.quantidade_lancamentos() for f in self._fechamentos)

    def total_debitos(self) -> float:
        return sum(f.total_debitos() for f in self._fechamentos)

    def total_creditos(self) -> float:
        return sum(f.total_creditos() for f in self._fechamentos)

    def saldo_final(self) -> float:
        return self.total_creditos() - self.total_debitos()

    def possui_conciliacao_pendente(self, conciliacoes: list[Conciliacao]) -> bool:
        return any(not c.esta_conciliada() for c in conciliacoes)

    def gerar_resumo(self) -> str:
        return (
            f"Extrato - {self._periodo}\n"
            f"Lancamentos: {self.total_lancamentos()}\n"
            f"Debitos: R$ {self.total_debitos():.2f}\n"
            f"Creditos: R$ {self.total_creditos():.2f}\n"
            f"Saldo final: R$ {self.saldo_final():.2f}"
        )


if __name__ == "__main__":
    from datetime import date

    from financeiro.categoria import Categoria
    from financeiro.lancamento import Lancamento

    cat = Categoria("Alimentacao")
    debito = Lancamento("Mercado", 150.0, date.today(), cat, "debito")
    credito = Lancamento("Salario", 3000.0, date.today(), cat, "credito")
    fechamento = Fechamento("2026-08", [debito, credito])

    extrato = Extrato("2026-08", [fechamento])
    print(extrato.gerar_resumo())
