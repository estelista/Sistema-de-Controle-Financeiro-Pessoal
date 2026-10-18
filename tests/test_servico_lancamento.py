from datetime import date

from financeiro.categoria import Categoria
from financeiro.conta import Conta
from financeiro.servico_lancamento import ServicoLancamento


class TestServicoLancamento:

    def setup_method(self) -> None:
        self.conta = Conta("Carteira", 1000.0)
        self.categoria = Categoria("Alimentacao")
        self.servico = ServicoLancamento()

    def test_debito_diminui_o_saldo_da_conta(self) -> None:
        self.servico.registrar(self.conta, "Mercado", 150.0, date.today(), self.categoria, "debito")
        assert self.conta.saldo == 850.0

    def test_credito_aumenta_o_saldo_da_conta(self) -> None:
        self.servico.registrar(self.conta, "Salario", 3000.0, date.today(), self.categoria, "credito")
        assert self.conta.saldo == 4000.0

    def test_devolve_o_lancamento_criado(self) -> None:
        lancamento = self.servico.registrar(
            self.conta, "Mercado", 150.0, date.today(), self.categoria, "debito"
        )
        assert lancamento.descricao == "Mercado"
        assert lancamento.valor == 150.0

    def test_lancamento_nao_conhece_a_conta(self) -> None:
        lancamento = self.servico.registrar(
            self.conta, "Mercado", 150.0, date.today(), self.categoria, "debito"
        )
        assert not hasattr(lancamento, "conta")
