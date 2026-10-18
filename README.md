# Sistema de Controle Financeiro Pessoal - Parte 3

Terceira etapa do projeto financeiro de POO II. Esta parte trata de **quem
cria os objetos** (Simple Factory e Factory Method) e de **quem entrega as
dependências** (injeção de dependências e raiz de composição). Também resolve
o ponto levantado no feedback da entrega anterior: a `Conta` estava isolada e
não era afetada pelos lançamentos.

## O que foi adicionado nesta parte

- `Leitor`, `LeitorCSV`, `LeitorOFX` e `CriadorLeitor`: leitura de arquivos de
  lançamentos por formato.
- `Importador`, `ImportadorBancoAlfa`, `ImportadorBancoBeta` e
  `CriadorImportador`: interpretação das linhas de extrato de cada banco.
- `ExportadorRelatorio`, `ExportadorCSV`, `ExportadorHTML` e `ExportadorPDF`:
  exportação do extrato em diferentes formatos.
- `ServicoLancamento`: cria um lançamento e aplica o efeito dele na conta.
- `ServicoImportacao`: importa as linhas de um banco e registra cada
  lançamento numa conta.
- `composicao.py`: a raiz de composição, com a função `montar_aplicacao()`.

As classes das partes 1 e 2 continuam como estavam.

## Perguntas de projeto

### 1. Leitor, importador e exportador: Simple Factory ou Factory Method?

- **`Leitor` (CSV e OFX): Simple Factory**, com o `CriadorLeitor`. A escolha
  depende de um dado simples, o formato do arquivo. Os leitores não têm fluxo
  próprio: cada um só interpreta linhas e devolve lançamentos. Um único
  `if/elif` centralizado resolve.
- **`Importador` (Banco Alfa e Banco Beta): também Simple Factory**, com o
  `CriadorImportador`, pelo mesmo motivo: a decisão é um dado, o banco de
  origem. A diferença para o leitor está no que varia. O leitor varia pelo
  formato do arquivo; o importador varia pelas convenções de cada banco. Dois
  bancos podem enviar CSV, mas um marca débito com valor negativo e o outro
  usa uma coluna explícita de D ou C.
- **`ExportadorRelatorio` (CSV, HTML e PDF): Factory Method.** Aqui cada
  formato monta o documento de um jeito diferente, não é só trocar uma
  extensão. O método `exportar()` é o método-molde: monta cabeçalho, corpo e
  rodapé, chama `criar_documento()` e salva. Só `criar_documento()` é
  implementado por cada subclasse. É a mesma lógica do `Expedidor` do
  e-commerce.

### 2. Nos serviços, o que é injetado e o que é criado internamente?

- O **`ServicoImportacao` recebe pelo construtor** o `CriadorImportador` e o
  `ServicoLancamento`. Ele não cria nenhum dos dois, e é por isso que o teste
  `test_colaborador_pode_ser_trocado_sem_editar_o_servico` consegue trocar o
  criador real por um `CriadorImportadorFake` sem mexer em uma linha do
  serviço.
- O **`ServicoLancamento` não recebe dependências pelo construtor.** Ele não
  guarda estado e trabalha com os objetos que chegam como parâmetro de
  `registrar()` (a conta, a categoria). Como a conta é diferente a cada
  chamada, não faria sentido injetar uma conta fixa nele.
- A `Categoria("Importado")` usada pelos importadores é **criada
  internamente**, de propósito: é um detalhe da leitura (toda linha importada
  cai numa categoria genérica) e não uma dependência que precise variar.

### 3. Onde está a raiz de composição? Que colaborador dá para trocar hoje?

A raiz de composição é a função `montar_aplicacao()`, em
`financeiro/composicao.py`. É o único lugar que sabe montar o
`ServicoImportacao` com os colaboradores reais.

Hoje dá para trocar, sem editar nenhum serviço, o `CriadorImportador` (por
exemplo, por um que aceite um banco novo) e o `ServicoLancamento` (por um que
também registre um log a cada lançamento). Basta mudar a linha correspondente
na raiz de composição. Os testes de `test_servico_importacao.py` mostram isso
na prática, substituindo o criador real por um dublê.

## Ajuste da Conta isolada

No feedback da entrega anterior foi apontado que a `Conta` ficava isolada:
criar lançamentos não alterava o saldo dela.

Não fiz o `Lancamento` receber a `Conta` e alterá-la dentro do próprio
`__init__`. Isso misturaria criar um registro com produzir um efeito em outro
objeto, e prenderia o lançamento à conta: qualquer regra nova da `Conta`
(como recusar saldo negativo) estouraria no meio da criação do lançamento.

A solução foi o `ServicoLancamento`. Ele recebe a conta e os dados do
lançamento, cria o `Lancamento` (que continua simples, imutável e sem saber
que existe uma conta) e depois chama `debitar()` ou `creditar()` na conta. O
`ServicoImportacao` usa esse mesmo serviço para aplicar cada lançamento
importado.

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
    leitor.py
    importador.py
    exportador_relatorio.py
    servico_lancamento.py
    servico_importacao.py
    composicao.py
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
    test_leitor.py
    test_importador.py
    test_exportador_relatorio.py
    test_servico_lancamento.py
    test_servico_importacao.py
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

Resultado esperado: `71 passed`.

### Exemplos

Cada arquivo tem um pequeno exemplo no final. Eles devem ser executados como
módulo, a partir da pasta raiz (no Linux, usar `python3` no lugar de `python`).
O mais completo é o da raiz de composição, que importa dois lançamentos de um
banco e mostra o saldo final da conta:

```
python -m financeiro.composicao
```

Os demais:

```
python -m financeiro.conta
python -m financeiro.lancamento
python -m financeiro.fechamento
python -m financeiro.conciliacao
python -m financeiro.extrato
python -m financeiro.estrategia_rendimento
python -m financeiro.aplicacao
python -m financeiro.estrategia_correcao
python -m financeiro.leitor
python -m financeiro.importador
python -m financeiro.exportador_relatorio
python -m financeiro.servico_lancamento
python -m financeiro.servico_importacao
```
