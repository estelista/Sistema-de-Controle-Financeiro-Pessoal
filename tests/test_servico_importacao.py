from datetime import date

from financeiro.categoria import Categoria
from financeiro.conta import Conta
from financeiro.importador import BancoOrigem, CriadorImportador, Importador
from financeiro.lancamento import Lancamento
from financeiro.servico_importacao import ServicoImportacao
from financeiro.servico_lancamento import ServicoLancamento


class ImportadorFake(Importador):

    def __init__(self) -> None:
        self.chamado_com: list[str] | None = None

    def importar(self, linhas: list[str]) -> list[Lancamento]:
        self.chamado_com = linhas
        categoria = Categoria("Fake")
        return [Lancamento("Lancamento fake", 100.0, date.today(), categoria, "debito")]


class CriadorImportadorFake:

    def __init__(self, importador_fake: ImportadorFake) -> None:
        self._importador_fake = importador_fake
        self.bancos_pedidos: list[BancoOrigem] = []

    def criar(self, banco: BancoOrigem) -> Importador:
        self.bancos_pedidos.append(banco)
        return self._importador_fake


class TestServicoImportacaoComColaboradoresReais:

    def test_importa_e_aplica_na_conta(self) -> None:
        conta = Conta("Carteira", 1000.0)
        servico = ServicoImportacao(CriadorImportador(), ServicoLancamento())

        linhas = ["2026-08-01;Mercado;-150.0", "2026-08-05;Salario;3000.0"]
        lancamentos = servico.importar_e_aplicar(BancoOrigem.ALFA, linhas, conta)

        assert len(lancamentos) == 2
        assert conta.saldo == 1000.0 - 150.0 + 3000.0


class TestServicoImportacaoComDubles:

    def test_colaborador_pode_ser_trocado_sem_editar_o_servico(self) -> None:
        importador_fake = ImportadorFake()
        criador_fake = CriadorImportadorFake(importador_fake)
        conta = Conta("Carteira", 1000.0)

        servico = ServicoImportacao(criador_fake, ServicoLancamento())
        lancamentos = servico.importar_e_aplicar(BancoOrigem.BETA, ["linha qualquer"], conta)

        assert criador_fake.bancos_pedidos == [BancoOrigem.BETA]
        assert importador_fake.chamado_com == ["linha qualquer"]
        assert len(lancamentos) == 1
        assert conta.saldo == 900.0
