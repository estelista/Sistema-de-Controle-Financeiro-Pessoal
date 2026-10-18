from abc import ABC, abstractmethod


class EstrategiaCorrecaoMonetaria(ABC):

    @abstractmethod
    def calcular(self, valor: float) -> float:
        ...


class CorrecaoIPCA(EstrategiaCorrecaoMonetaria):

    def __init__(self, indice_percentual: float) -> None:
        if indice_percentual < 0:
            raise ValueError("Indice de correcao nao pode ser negativo")
        self._indice_percentual = indice_percentual

    def calcular(self, valor: float) -> float:
        return valor * (1 + self._indice_percentual / 100)


class CorrecaoSelic(EstrategiaCorrecaoMonetaria):

    def __init__(self, indice_percentual: float) -> None:
        if indice_percentual < 0:
            raise ValueError("Indice de correcao nao pode ser negativo")
        self._indice_percentual = indice_percentual

    def calcular(self, valor: float) -> float:
        return valor * (1 + self._indice_percentual / 100)


if __name__ == "__main__":
    ipca = CorrecaoIPCA(4.5)
    print(f"R$ 1000 corrigido pelo IPCA: R$ {ipca.calcular(1000.0):.2f}")
