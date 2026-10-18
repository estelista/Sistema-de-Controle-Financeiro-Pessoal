from datetime import date

from financeiro.categoria import Categoria


class Lancamento:

    TIPOS_VALIDOS = ("debito", "credito")

    def __init__(
        self,
        descricao: str,
        valor: float,
        data: date,
        categoria: Categoria,
        tipo: str,
    ) -> None:
        if valor <= 0:
            raise ValueError("Valor do lancamento deve ser positivo")
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo deve ser um de {self.TIPOS_VALIDOS}")
        self._descricao = descricao
        self._valor = valor
        self._data = data
        self._categoria = categoria
        self._tipo = tipo

    @property
    def descricao(self) -> str:
        return self._descricao

    @property
    def valor(self) -> float:
        return self._valor

    @property
    def data(self) -> date:
        return self._data

    @property
    def categoria(self) -> Categoria:
        return self._categoria

    @property
    def tipo(self) -> str:
        return self._tipo

    def eh_debito(self) -> bool:
        return self._tipo == "debito"

    def eh_credito(self) -> bool:
        return self._tipo == "credito"


if __name__ == "__main__":
    cat = Categoria("Alimentacao")
    l = Lancamento("Mercado", 150.0, date.today(), cat, "debito")
    print(f"{l.descricao}: R$ {l.valor:.2f} ({l.tipo})")
