from abc import ABC, abstractmethod
from datetime import date
from enum import Enum

from financeiro.categoria import Categoria
from financeiro.lancamento import Lancamento


class Leitor(ABC):

    @abstractmethod
    def ler(self, caminho_arquivo: str) -> list[Lancamento]:
        ...


class LeitorCSV(Leitor):

    def ler(self, caminho_arquivo: str) -> list[Lancamento]:
        lancamentos = []
        with open(caminho_arquivo, encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha or linha.startswith("descricao"):
                    continue
                descricao, valor, data_str, categoria_nome, tipo = linha.split(",")
                lancamentos.append(
                    Lancamento(
                        descricao=descricao,
                        valor=float(valor),
                        data=date.fromisoformat(data_str),
                        categoria=Categoria(categoria_nome),
                        tipo=tipo,
                    )
                )
        return lancamentos


class LeitorOFX(Leitor):

    def ler(self, caminho_arquivo: str) -> list[Lancamento]:
        lancamentos = []
        with open(caminho_arquivo, encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha:
                    continue
                descricao, valor, data_str, categoria_nome, tipo = linha.split(";")
                lancamentos.append(
                    Lancamento(
                        descricao=descricao,
                        valor=float(valor),
                        data=date.fromisoformat(data_str),
                        categoria=Categoria(categoria_nome),
                        tipo=tipo,
                    )
                )
        return lancamentos


class FormatoLeitor(Enum):
    CSV = "csv"
    OFX = "ofx"


class CriadorLeitor:

    def criar(self, formato: FormatoLeitor) -> Leitor:
        if formato == FormatoLeitor.CSV:
            return LeitorCSV()
        if formato == FormatoLeitor.OFX:
            return LeitorOFX()
        raise ValueError(f"Formato de leitor desconhecido: {formato}")


if __name__ == "__main__":
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
        tmp.write("descricao,valor,data,categoria,tipo\n")
        tmp.write("Mercado,150.0,2026-08-01,Alimentacao,debito\n")
        caminho = tmp.name

    leitor = CriadorLeitor().criar(FormatoLeitor.CSV)
    for lancamento in leitor.ler(caminho):
        print(f"{lancamento.descricao}: R$ {lancamento.valor:.2f} ({lancamento.tipo})")
