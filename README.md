# Sistema de Controle Financeiro Pessoal - Parte 2

Segunda etapa do projeto financeiro de POO II. Sobre as classes da parte 1,
foi aplicado o padrão **Strategy** em dois pontos: o rendimento de
investimentos e a correção monetária de valores.

## O que foi adicionado nesta parte

- `EstrategiaRendimento`: interface (classe abstrata) com o método
  `calcular(capital, meses)`.
- `JurosSimples` e `JurosCompostos`: as duas implementações do rendimento.
- `Aplicacao`: um investimento contratado. Guarda a estratégia de rendimento
  escolhida e calcula o valor atual e o rendimento.
- `EstrategiaCorrecaoMonetaria`: interface separada, com o método
  `calcular(valor)`.
- `CorrecaoIPCA` e `CorrecaoSelic`: as implementações da correção.
- `Extrato.saldo_final_corrigido(estrategia)`: aplica uma correção monetária
  opcional sobre o saldo final.

As classes da parte 1 continuam como estavam, com exceção do `Extrato`, que
ganhou o método acima.

## Perguntas de projeto

### 1. Rendimento, juros e correção monetária: interfaces separadas ou reaproveitadas?

**Rendimento e juros reaproveitam a mesma interface** (`EstrategiaRendimento`).
**A correção monetária ganhou uma interface própria**
(`EstrategiaCorrecaoMonetaria`).

Rendimento de uma aplicação e juros são a mesma operação: um capital cresce ao
longo do tempo segundo uma taxa. A poupança usa a fórmula de juros simples
(`capital * (1 + taxa * meses)`) e um CDB pré-fixado usa a de juros compostos
(`capital * (1 + taxa) ** meses`). Por isso não criei classes como
`RendimentoPoupanca` ou `RendimentoCDB`: a poupança é uma instância de
`JurosSimples` com a taxa da poupança, e o CDB é uma instância de
`JurosCompostos`.

Já a correção monetária tem a mesma forma (recebe um valor e devolve um valor
ajustado), mas é outro conceito. Rendimento remunera um capital que foi
investido; correção só atualiza um valor para acompanhar a inflação. Colocar
as duas na mesma interface só porque a conta se parece misturaria duas
perguntas de negócio diferentes. É o mesmo motivo pelo qual, no e-commerce,
`EstrategiaFrete` não reaproveita `EstrategiaDesconto`.

### 2. Onde a estratégia escolhida é guardada?

- A **`EstrategiaRendimento` é guardada como atributo** da `Aplicacao`. A taxa
  é definida uma única vez, no momento em que o dinheiro é aplicado, e precisa
  continuar valendo enquanto o investimento existir. Seria estranho ter que
  informar a taxa de novo a cada consulta ao valor atual.
- A **`EstrategiaCorrecaoMonetaria` é passada como parâmetro** em
  `Extrato.saldo_final_corrigido(estrategia_correcao)`. A correção depende de
  qual índice se quer consultar naquele momento (IPCA ou Selic, por exemplo),
  e escolher um não altera o estado do `Extrato`. É um cálculo pontual, não uma
  decisão permanente do extrato.

### 3. Que tipo de regra nova dá para adicionar sem editar nenhuma classe existente?

Qualquer novo tipo de rendimento ou de correção. Um `RendimentoVariavel`, com
uma taxa diferente a cada mês, ou uma `CorrecaoINPC`, por exemplo, são só
classes novas que implementam a interface correspondente. Nenhuma linha de
`Aplicacao`, `Extrato` ou das interfaces precisa mudar, porque quem usa a
estratégia só chama `calcular()` e não sabe qual fórmula está por trás.

## Estrutura

```
financeiro/
    __init__.py
    categoria.py
    conta.py
    lancamento.py
    fechamento.py
    conciliacao.py
    extrato.py
    estrategia_rendimento.py
    aplicacao.py
    estrategia_correcao.py
tests/
    __init__.py
    test_categoria.py
    test_conta.py
    test_lancamento.py
    test_fechamento.py
    test_conciliacao.py
    test_extrato.py
    test_estrategia_rendimento.py
    test_aplicacao.py
    test_estrategia_correcao.py
requirements.txt
```

## Como executar

Criar e ativar o ambiente virtual, depois instalar as dependências.

Windows:

```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Linux:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Testes

Na pasta raiz do projeto:

```
pytest -v
```

Resultado esperado: `47 passed`.

### Exemplos

Cada arquivo tem um pequeno exemplo no final. Eles devem ser executados como
módulo, a partir da pasta raiz (no Linux, usar `python3` no lugar de `python`):

```
python -m financeiro.conta
python -m financeiro.lancamento
python -m financeiro.fechamento
python -m financeiro.conciliacao
python -m financeiro.extrato
python -m financeiro.estrategia_rendimento
python -m financeiro.aplicacao
python -m financeiro.estrategia_correcao
```
