import tempfile
from datetime import date

from financeiro.categoria import Categoria
from financeiro.exportador_relatorio import ExportadorCSV, ExportadorHTML, ExportadorPDF
from financeiro.extrato import Extrato
from financeiro.fechamento import Fechamento
from financeiro.lancamento import Lancamento


class TestExportadorRelatorio:

    def setup_method(self) -> None:
        cat = Categoria("Alimentacao")
        debito = Lancamento("Mercado", 150.0, date(2026, 8, 1), cat, "debito")
        credito = Lancamento("Salario", 3000.0, date(2026, 8, 5), cat, "credito")
        self.extrato = Extrato("2026-08", [Fechamento("2026-08", [debito, credito])])

    def _caminho_temporario(self) -> str:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            return tmp.name

    def test_exportador_csv_gera_linhas_separadas_por_virgula(self) -> None:
        caminho = self._caminho_temporario()
        ExportadorCSV().exportar(self.extrato, caminho)
        with open(caminho, encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
        assert "Lancamentos,2" in conteudo
        assert "2026-08" in conteudo

    def test_exportador_html_gera_tabela(self) -> None:
        caminho = self._caminho_temporario()
        ExportadorHTML().exportar(self.extrato, caminho)
        with open(caminho, encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
        assert "<table>" in conteudo
        assert "<html>" in conteudo

    def test_exportador_pdf_gera_texto_formatado(self) -> None:
        caminho = self._caminho_temporario()
        ExportadorPDF().exportar(self.extrato, caminho)
        with open(caminho, encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
        assert "Gerado automaticamente" in conteudo

    def test_exportar_devolve_o_caminho_do_arquivo(self) -> None:
        caminho = self._caminho_temporario()
        resultado = ExportadorCSV().exportar(self.extrato, caminho)
        assert resultado == caminho
