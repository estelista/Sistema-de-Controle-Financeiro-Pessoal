import tempfile

import pytest

from financeiro.leitor import CriadorLeitor, FormatoLeitor, LeitorCSV, LeitorOFX


def _arquivo_temporario(conteudo: str, sufixo: str) -> str:
    with tempfile.NamedTemporaryFile(mode="w", suffix=sufixo, delete=False, encoding="utf-8") as tmp:
        tmp.write(conteudo)
        return tmp.name


class TestLeitorCSV:

    def test_le_lancamentos_de_um_csv(self) -> None:
        caminho = _arquivo_temporario(
            "descricao,valor,data,categoria,tipo\nMercado,150.0,2026-08-01,Alimentacao,debito\n",
            ".csv",
        )
        lancamentos = LeitorCSV().ler(caminho)
        assert len(lancamentos) == 1
        assert lancamentos[0].descricao == "Mercado"
        assert lancamentos[0].valor == 150.0
        assert lancamentos[0].eh_debito()

    def test_pula_linhas_em_branco_e_cabecalho(self) -> None:
        caminho = _arquivo_temporario(
            "descricao,valor,data,categoria,tipo\n\nSalario,3000.0,2026-08-05,Renda,credito\n",
            ".csv",
        )
        lancamentos = LeitorCSV().ler(caminho)
        assert len(lancamentos) == 1


class TestLeitorOFX:

    def test_le_lancamentos_de_um_ofx(self) -> None:
        caminho = _arquivo_temporario("Salario;3000.0;2026-08-05;Renda;credito\n", ".ofx")
        lancamentos = LeitorOFX().ler(caminho)
        assert len(lancamentos) == 1
        assert lancamentos[0].eh_credito()


class TestCriadorLeitor:

    def test_cria_leitor_csv(self) -> None:
        leitor = CriadorLeitor().criar(FormatoLeitor.CSV)
        assert isinstance(leitor, LeitorCSV)

    def test_cria_leitor_ofx(self) -> None:
        leitor = CriadorLeitor().criar(FormatoLeitor.OFX)
        assert isinstance(leitor, LeitorOFX)

    def test_formato_desconhecido_lanca_erro(self) -> None:
        with pytest.raises(ValueError):
            CriadorLeitor().criar("csv")
