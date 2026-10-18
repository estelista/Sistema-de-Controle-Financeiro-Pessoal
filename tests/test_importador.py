import pytest

from financeiro.importador import BancoOrigem, CriadorImportador, ImportadorBancoAlfa, ImportadorBancoBeta


class TestImportadorBancoAlfa:

    def test_valor_negativo_vira_debito(self) -> None:
        lancamentos = ImportadorBancoAlfa().importar(["2026-08-01;Mercado;-150.0"])
        assert len(lancamentos) == 1
        assert lancamentos[0].eh_debito()
        assert lancamentos[0].valor == 150.0

    def test_valor_positivo_vira_credito(self) -> None:
        lancamentos = ImportadorBancoAlfa().importar(["2026-08-05;Salario;3000.0"])
        assert lancamentos[0].eh_credito()

    def test_ignora_linhas_em_branco(self) -> None:
        lancamentos = ImportadorBancoAlfa().importar(["2026-08-01;Mercado;-150.0", "", "  "])
        assert len(lancamentos) == 1


class TestImportadorBancoBeta:

    def test_tipo_d_vira_debito(self) -> None:
        lancamentos = ImportadorBancoBeta().importar(["Mercado,2026-08-01,D,150.0"])
        assert lancamentos[0].eh_debito()

    def test_tipo_c_vira_credito(self) -> None:
        lancamentos = ImportadorBancoBeta().importar(["Salario,2026-08-05,C,3000.0"])
        assert lancamentos[0].eh_credito()


class TestCriadorImportador:

    def test_cria_importador_alfa(self) -> None:
        importador = CriadorImportador().criar(BancoOrigem.ALFA)
        assert isinstance(importador, ImportadorBancoAlfa)

    def test_cria_importador_beta(self) -> None:
        importador = CriadorImportador().criar(BancoOrigem.BETA)
        assert isinstance(importador, ImportadorBancoBeta)

    def test_banco_desconhecido_lanca_erro(self) -> None:
        with pytest.raises(ValueError):
            CriadorImportador().criar("alfa")
