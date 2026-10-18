from abc import ABC, abstractmethod


class EstrategiaRendimento(ABC):

    @abstractmethod
    def calcular(self, capital: float, meses: int) -> float:
        ...


class JurosSimples(EstrategiaRendimento):

    def __init__(self, taxa_mensal: float) -> None:
        if taxa_mensal < 0:
            raise ValueError("Taxa mensal nao pode ser negativa")
        self._taxa_mensal = taxa_mensal

    def calcular(self, capital: float, meses: int) -> float:
        if meses < 0:
            raise ValueError("Quantidade de meses nao pode ser negativa")
        return capital * (1 + self._taxa_mensal * meses)


class JurosCompostos(EstrategiaRendimento):

    def __init__(self, taxa_mensal: float) -> None:
        if taxa_mensal < 0:
            raise ValueError("Taxa mensal nao pode ser negativa")
        self._taxa_mensal = taxa_mensal

    def calcular(self, capital: float, meses: int) -> float:
        if meses < 0:
            raise ValueError("Quantidade de meses nao pode ser negativa")
        return capital * (1 + self._taxa_mensal) ** meses


if __name__ == "__main__":
    poupanca = JurosSimples(0.005)
    cdb = JurosCompostos(0.01)
    print(f"Poupanca 12 meses: R$ {poupanca.calcular(1000.0, 12):.2f}")
    print(f"CDB 12 meses: R$ {cdb.calcular(1000.0, 12):.2f}")
