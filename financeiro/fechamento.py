from financeiro.lancamento import Lancamento


class Fechamento:

    def __init__(self, periodo: str, lancamentos: list[Lancamento]) -> None:
        self._periodo = periodo
        self._lancamentos = list(lancamentos)

    @property
    def periodo(self) -> str:
        return self._periodo

    @property
    def lancamentos(self) -> list[Lancamento]:
        return list(self._lancamentos)

    def quantidade_lancamentos(self) -> int:
        return len(self._lancamentos)

    def total_debitos(self) -> float:
        return sum(l.valor for l in self._lancamentos if l.eh_debito())

    def total_creditos(self) -> float:
        return sum(l.valor for l in self._lancamentos if l.eh_credito())

    def saldo(self) -> float:
        return self.total_creditos() - self.total_debitos()


if __name__ == "__main__":
    from datetime import date

    from financeiro.categoria import Categoria

    cat = Categoria("Alimentacao")
    debito = Lancamento("Mercado", 150.0, date.today(), cat, "debito")
    credito = Lancamento("Salario", 3000.0, date.today(), cat, "credito")

    fechamento = Fechamento("2026-08", [debito, credito])
    print(f"Lancamentos: {fechamento.quantidade_lancamentos()}")
    print(f"Saldo: R$ {fechamento.saldo():.2f}")
