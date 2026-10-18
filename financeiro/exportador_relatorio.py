from abc import ABC, abstractmethod

from financeiro.extrato import Extrato


class ExportadorRelatorio(ABC):

    def exportar(self, extrato: Extrato, caminho_saida: str) -> str:
        cabecalho = self._montar_cabecalho(extrato)
        corpo = self._montar_corpo(extrato)
        rodape = self._montar_rodape()
        documento = self.criar_documento(cabecalho, corpo, rodape)
        self._salvar(documento, caminho_saida)
        return caminho_saida

    def _montar_cabecalho(self, extrato: Extrato) -> str:
        return f"Extrato - {extrato.periodo}"

    def _montar_corpo(self, extrato: Extrato) -> list[tuple[str, str]]:
        return [
            ("Lancamentos", str(extrato.total_lancamentos())),
            ("Debitos", f"R$ {extrato.total_debitos():.2f}"),
            ("Creditos", f"R$ {extrato.total_creditos():.2f}"),
            ("Saldo final", f"R$ {extrato.saldo_final():.2f}"),
        ]

    def _montar_rodape(self) -> str:
        return "Gerado automaticamente"

    @abstractmethod
    def criar_documento(self, cabecalho: str, corpo: list[tuple[str, str]], rodape: str) -> str:
        ...

    def _salvar(self, documento: str, caminho_saida: str) -> None:
        with open(caminho_saida, "w", encoding="utf-8") as arquivo:
            arquivo.write(documento)


class ExportadorCSV(ExportadorRelatorio):

    def criar_documento(self, cabecalho: str, corpo: list[tuple[str, str]], rodape: str) -> str:
        linhas = [cabecalho] + [f"{label},{valor}" for label, valor in corpo] + [rodape]
        return "\n".join(linhas)


class ExportadorHTML(ExportadorRelatorio):

    def criar_documento(self, cabecalho: str, corpo: list[tuple[str, str]], rodape: str) -> str:
        linhas_tabela = "".join(f"<tr><td>{label}</td><td>{valor}</td></tr>" for label, valor in corpo)
        return f"<html><body><h1>{cabecalho}</h1><table>{linhas_tabela}</table><p>{rodape}</p></body></html>"


class ExportadorPDF(ExportadorRelatorio):

    def criar_documento(self, cabecalho: str, corpo: list[tuple[str, str]], rodape: str) -> str:
        linhas = [cabecalho, "=" * len(cabecalho)]
        linhas += [f"{label}: {valor}" for label, valor in corpo]
        linhas.append("-" * 20)
        linhas.append(rodape)
        return "\n".join(linhas)


if __name__ == "__main__":
    import tempfile
    from datetime import date

    from financeiro.categoria import Categoria
    from financeiro.fechamento import Fechamento
    from financeiro.lancamento import Lancamento

    cat = Categoria("Alimentacao")
    debito = Lancamento("Mercado", 150.0, date.today(), cat, "debito")
    credito = Lancamento("Salario", 3000.0, date.today(), cat, "credito")
    extrato = Extrato("2026-08", [Fechamento("2026-08", [debito, credito])])

    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        caminho = tmp.name

    ExportadorPDF().exportar(extrato, caminho)
    with open(caminho, encoding="utf-8") as arquivo:
        print(arquivo.read())
