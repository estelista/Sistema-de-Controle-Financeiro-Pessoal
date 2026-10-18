from financeiro.lancamento import Lancamento


class Conciliacao:

    def __init__(self, lancamentos: list[Lancamento]) -> None:
        self._lancamentos = list(lancamentos)

    @property
    def total_debitos(self) -> float:
        return sum(l.valor for l in self._lancamentos if l.eh_debito())

    @property
    def total_creditos(self) -> float:
        return sum(l.valor for l in self._lancamentos if l.eh_credito())

    @property
    def diferenca(self) -> float:
        return round(self.total_creditos - self.total_debitos, 2)

    def esta_conciliada(self) -> bool:
        return self.diferenca == 0

    def verificar(self) -> None:
        if not self.esta_conciliada():
            raise ValueError(
                "Conciliacao nao bate: "
                f"debitos=R$ {self.total_debitos:.2f}, "
                f"creditos=R$ {self.total_creditos:.2f}, "
                f"diferenca=R$ {self.diferenca:.2f}"
            )


if __name__ == "__main__":
    from datetime import date

    from financeiro.categoria import Categoria

    cat = Categoria("Alimentacao")
    debito = Lancamento("Mercado", 150.0, date.today(), cat, "debito")
    credito = Lancamento("Estorno", 100.0, date.today(), cat, "credito")

    conciliacao = Conciliacao([debito, credito])
    print(f"Conciliada: {conciliacao.esta_conciliada()}")
    print(f"Diferenca: R$ {conciliacao.diferenca:.2f}")
