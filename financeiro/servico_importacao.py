from financeiro.conta import Conta
from financeiro.importador import BancoOrigem, CriadorImportador
from financeiro.lancamento import Lancamento
from financeiro.servico_lancamento import ServicoLancamento


class ServicoImportacao:

    def __init__(
        self,
        criador_importador: CriadorImportador,
        servico_lancamento: ServicoLancamento,
    ) -> None:
        self._criador_importador = criador_importador
        self._servico_lancamento = servico_lancamento

    def importar_e_aplicar(
        self, banco: BancoOrigem, linhas: list[str], conta: Conta
    ) -> list[Lancamento]:
        importador = self._criador_importador.criar(banco)
        lidos = importador.importar(linhas)
        return [
            self._servico_lancamento.registrar(
                conta, l.descricao, l.valor, l.data, l.categoria, l.tipo
            )
            for l in lidos
        ]


if __name__ == "__main__":
    conta = Conta("Carteira", 1000.0)
    servico = ServicoImportacao(CriadorImportador(), ServicoLancamento())

    linhas = ["2026-08-01;Mercado;-150.0", "2026-08-05;Salario;3000.0"]
    lancamentos = servico.importar_e_aplicar(BancoOrigem.ALFA, linhas, conta)

    print(f"{len(lancamentos)} lancamentos importados")
    print(f"Saldo final: R$ {conta.saldo:.2f}")
