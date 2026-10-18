from datetime import date

from financeiro.categoria import Categoria
from financeiro.conta import Conta
from financeiro.lancamento import Lancamento


class ServicoLancamento:

    def registrar(
        self,
        conta: Conta,
        descricao: str,
        valor: float,
        data: date,
        categoria: Categoria,
        tipo: str,
    ) -> Lancamento:
        lancamento = Lancamento(descricao, valor, data, categoria, tipo)

        if lancamento.eh_debito():
            conta.debitar(lancamento.valor)
        else:
            conta.creditar(lancamento.valor)

        return lancamento


if __name__ == "__main__":
    conta = Conta("Carteira", 1000.0)
    servico = ServicoLancamento()

    servico.registrar(conta, "Mercado", 150.0, date.today(), Categoria("Alimentacao"), "debito")
    print(f"Saldo apos debito: R$ {conta.saldo:.2f}")
