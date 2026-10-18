# Sistema de Controle Financeiro Pessoal - Parte 1

Primeira etapa do projeto financeiro de POO II, desenvolvido em Python. Aqui
ficam as entidades básicas do domínio e o fluxo de fechamento, conciliação e
extrato.

## O que tem nesta parte

- `Categoria`: só o nome, usada para classificar os lançamentos.
- `Conta`: nome e saldo, com `creditar()` e `debitar()` (os dois recusam valor
  menor ou igual a zero).
- `Lancamento`: descrição, valor, data, categoria e tipo (`"debito"` ou
  `"credito"`). É imutável: só tem leitura, não existe nenhum jeito de alterar
  depois de criado.
- `Fechamento`: reúne os lançamentos de um período e calcula quantidade, total
  de débitos, total de créditos e saldo.
- `Conciliacao`: confere se o total de débitos bate com o de créditos.
- `Extrato`: junta vários fechamentos e gera o resumo do período.

## Perguntas de projeto

### 1. No `Fechamento`, os lançamentos originais foram copiados ou referenciados?

Os objetos `Lancamento` são **referenciados**, mas a lista que os guarda é uma
**cópia** (`list(lancamentos)`).

Como `Lancamento` é imutável, não existe risco em compartilhar a referência:
o valor, a data e o tipo nunca mudam depois de criados, então copiar cada
lançamento só duplicaria informação sem nenhum ganho. Já a lista precisa ser
copiada para que o `Fechamento` não fique ligado à lista original: se alguém
adicionar ou remover itens dela depois, o fechamento já criado não é afetado.
Isso está coberto no teste `test_lista_interna_e_copia`.

### 2. A `Conciliacao` virou uma classe própria ou um método do `Fechamento`?

Virou uma **classe própria**.

O `Fechamento` tem a responsabilidade de consolidar (contar e somar). A
`Conciliacao` tem outra: verificar uma regra de negócio, a de que débitos e
créditos precisam bater. Misturar as duas deixaria a classe com dois motivos
para mudar, e é a mesma separação que existe entre `Pedido` e `Pagamento` no
exemplo do e-commerce. Como consequência, uma `Conciliacao` pode ser feita
sobre qualquer lista de lançamentos, inclusive de fechamentos diferentes, sem
depender de um `Fechamento` pronto.

### 3. O que acontece quando não há lançamentos no período, ou quando a conciliação não bate?

- **Período sem lançamentos:** `Fechamento` e `Extrato` aceitam lista vazia e
  retornam tudo zerado, sem erro. Um mês sem nenhuma movimentação é uma
  situação normal no domínio financeiro, diferente de finalizar um carrinho
  vazio, que não faria sentido.
- **Conciliação que não bate:** existem dois métodos. `esta_conciliada()`
  devolve `True` ou `False` sem interromper nada (a diferença é arredondada
  para duas casas antes de comparar com zero, para não falhar por imprecisão
  de ponto flutuante). `verificar()` lança `ValueError` com uma mensagem que
  já traz o total de débitos, o total de créditos e a diferença. O `Extrato`
  usa a primeira forma em `possui_conciliacao_pendente()`.

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
tests/
    __init__.py
    test_categoria.py
    test_conta.py
    test_lancamento.py
    test_fechamento.py
    test_conciliacao.py
    test_extrato.py
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

Resultado esperado: `26 passed`.

### Exemplos

Cada arquivo tem um pequeno exemplo no final. Eles devem ser executados como
módulo, a partir da pasta raiz (no Linux, usar `python3` no lugar de `python`):

```
python -m financeiro.conta
python -m financeiro.lancamento
python -m financeiro.fechamento
python -m financeiro.conciliacao
python -m financeiro.extrato
```
