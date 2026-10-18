class Conta:

    def __init__(self, nome: str, saldo: float = 0.0) -> None:
        self.nome = nome
        self._saldo = saldo

    @property
    def saldo(self) -> float:
        return self._saldo

    def creditar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("Valor de credito deve ser positivo")
        self._saldo += valor

    def debitar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("Valor de debito deve ser positivo")
        self._saldo -= valor


if __name__ == "__main__":
    c = Conta("Carteira", 100.0)
    c.creditar(50.0)
    c.debitar(30.0)
    print(f"Conta: {c.nome}, Saldo: {c.saldo}")
