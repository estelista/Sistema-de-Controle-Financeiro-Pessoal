from abc import ABC, abstractmethod
from datetime import date
from enum import Enum

from financeiro.categoria import Categoria
from financeiro.lancamento import Lancamento


class Importador(ABC):

    @abstractmethod
    def importar(self, linhas: list[str]) -> list[Lancamento]:
        ...


class ImportadorBancoAlfa(Importador):

    def importar(self, linhas: list[str]) -> list[Lancamento]:
        lancamentos = []
        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue
            data_str, descricao, valor_str = linha.split(";")
            valor = float(valor_str)
            tipo = "credito" if valor >= 0 else "debito"
            lancamentos.append(
                Lancamento(
                    descricao=descricao,
                    valor=abs(valor),
                    data=date.fromisoformat(data_str),
                    categoria=Categoria("Importado"),
                    tipo=tipo,
                )
            )
        return lancamentos


class ImportadorBancoBeta(Importador):

    def importar(self, linhas: list[str]) -> list[Lancamento]:
        lancamentos = []
        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue
            descricao, data_str, tipo_letra, valor_str = linha.split(",")
            tipo = "debito" if tipo_letra.upper() == "D" else "credito"
            lancamentos.append(
                Lancamento(
                    descricao=descricao,
                    valor=float(valor_str),
                    data=date.fromisoformat(data_str),
                    categoria=Categoria("Importado"),
                    tipo=tipo,
                )
            )
        return lancamentos


class BancoOrigem(Enum):
    ALFA = "alfa"
    BETA = "beta"


class CriadorImportador:

    def criar(self, banco: BancoOrigem) -> Importador:
        if banco == BancoOrigem.ALFA:
            return ImportadorBancoAlfa()
        if banco == BancoOrigem.BETA:
            return ImportadorBancoBeta()
        raise ValueError(f"Banco de origem desconhecido: {banco}")


if __name__ == "__main__":
    linhas_alfa = ["2026-08-01;Mercado;-150.0", "2026-08-05;Salario;3000.0"]
    importador = CriadorImportador().criar(BancoOrigem.ALFA)
    for lancamento in importador.importar(linhas_alfa):
        print(f"{lancamento.descricao}: R$ {lancamento.valor:.2f} ({lancamento.tipo})")
