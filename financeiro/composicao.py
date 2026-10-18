from financeiro.importador import CriadorImportador
from financeiro.servico_importacao import ServicoImportacao
from financeiro.servico_lancamento import ServicoLancamento


def montar_aplicacao() -> ServicoImportacao:
    return ServicoImportacao(
        criador_importador=CriadorImportador(),
        servico_lancamento=ServicoLancamento(),
    )


if __name__ == "__main__":
    from financeiro.conta import Conta
    from financeiro.importador import BancoOrigem

    servico_importacao = montar_aplicacao()
    conta = Conta("Carteira", 1000.0)

    linhas = ["2026-08-01;Mercado;-150.0", "2026-08-05;Salario;3000.0"]
    lancamentos = servico_importacao.importar_e_aplicar(BancoOrigem.ALFA, linhas, conta)

    print(f"{len(lancamentos)} lancamentos importados via raiz de composicao")
    print(f"Saldo final da conta: R$ {conta.saldo:.2f}")
