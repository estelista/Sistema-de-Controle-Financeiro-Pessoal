from datetime import date

from financeiro.estrategia_rendimento import EstrategiaRendimento


class Aplicacao:

    def __init__(
        self,
        descricao: str,
        valor_aplicado: float,
        data_aplicacao: date,
        estrategia_rendimento: EstrategiaRendimento,
    ) -> None:
        if valor_aplicado <= 0:
            raise ValueError("Valor aplicado deve ser positivo")
        self._descricao = descricao
        self._valor_aplicado = valor_aplicado
        self._data_aplicacao = data_aplicacao
        self._estrategia_rendimento = estrategia_rendimento

    @property
    def descricao(self) -> str:
        return self._descricao

    @property
    def valor_aplicado(self) -> float:
        return self._valor_aplicado

    @property
    def data_aplicacao(self) -> date:
        return self._data_aplicacao

    def calcular_valor_atual(self, meses: int) -> float:
        return self._estrategia_rendimento.calcular(self._valor_aplicado, meses)

    def calcular_rendimento(self, meses: int) -> float:
        return self.calcular_valor_atual(meses) - self._valor_aplicado


if __name__ == "__main__":
    from financeiro.estrategia_rendimento import JurosCompostos

    aplicacao = Aplicacao("CDB Banco X", 1000.0, date.today(), JurosCompostos(0.01))
    print(f"Valor em 12 meses: R$ {aplicacao.calcular_valor_atual(12):.2f}")
    print(f"Rendimento em 12 meses: R$ {aplicacao.calcular_rendimento(12):.2f}")
