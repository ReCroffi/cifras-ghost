<div align="center">

# Decifrador do Ghost

**Cifre, decifre e converta textos pela linha de comando.**<br>
Cifras clássicas e codificações, em Python puro.

![Python 3.13+](https://img.shields.io/badge/python-3.13%2B-3776AB?logo=python&logoColor=white)
![Dependências: nenhuma](https://img.shields.io/badge/depend%C3%AAncias-nenhuma-2ea44f)
![Gerenciado com uv](https://img.shields.io/badge/gerenciado%20com-uv-DE5FE9)

</div>

## Por que este projeto existe

Em *Ghost in the Wires*, Kevin Mitnick conta a história de um dos hackers mais famosos do mundo. O livro tem uma pegadinha: cada capítulo abre com um texto cifrado, um enigma pequeno esperando na primeira página antes de a história começar.

Dava para procurar a resposta na internet. Preferi o caminho mais longo e mais divertido: escrever as ferramentas para decifrar eu mesmo. Cada capítulo pedia uma técnica diferente, e cada técnica virou uma função, com teste e subcomando. O resultado é este canivete de cifras.

O projeto não traz nenhuma resposta do livro, só as ferramentas. Se você está lendo o livro, os enigmas continuam intactos.

## O que ele faz

| Família | Subcomando | O que faz |
| --- | --- | --- |
| Substituição | `cesar` | Deslocamento fixo do alfabeto. Para decifrar, use o deslocamento negativo. |
| | `forca-bruta` | Tenta os 26 deslocamentos do César e ordena pelo mais parecido com inglês. |
| | `vigenere` | César com uma chave que muda o deslocamento a cada letra. |
| | `atbash` | Alfabeto espelhado (a vira z). Cifrar e decifrar são a mesma operação. |
| | `playfair` | Cifra por pares de letras sobre uma grade 5×5 montada com uma palavra-chave. |
| Transposição | `rail-fence` | Escreve o texto em zigue-zague sobre trilhos e lê trilho por trilho. |
| | `inverter` | Inverte o texto por caractere ou a ordem das palavras. |
| Codificação | `texto-para-numeros` / `numeros-para-texto` | Código de cada caractere em binário, octal, decimal ou hexadecimal. |
| | `inteiro-para-base36` / `base36-para-inteiro` | Converte inteiros de e para base 36. |
| | `texto-para-base64` / `base64-para-texto` | Base64 em UTF-8. |
| | `texto-para-morse` / `morse-para-texto` | Código Morse. |
| | `texto-para-teclado` / `teclado-para-texto` | Toques do teclado numérico de telefone. |

## Começando

Precisa de Python 3.13 ou mais novo e do [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/ReCroffi/cifras-ghost.git
cd cifras-ghost
uv sync
```

Todo comando roda com `uv run ghost-wires`. Para listar os subcomandos ou ver as opções de um deles:

```bash
uv run ghost-wires --help
uv run ghost-wires cesar --help
```

O texto pode vir como argumento ou pela entrada padrão. O terminador de linha do final é removido, então `echo` funciona como se esperaria:

```console
$ uv run ghost-wires cesar -n 3 "bom dia"
erp gld

$ echo "erp gld" | uv run ghost-wires cesar -n -3
bom dia
```

## Exemplos

### César e força bruta

A força bruta imprime uma linha por deslocamento, no formato `nota deslocamento tentativa`. A nota conta quantas palavras comuns do inglês aparecem na tentativa, então a melhor candidata vem primeiro. Ela serve para texto em inglês.

```console
$ uv run ghost-wires forca-bruta "Wkh txlfn eurzq ira"
1 3 The quick brown fox
0 0 Wkh txlfn eurzq ira
0 1 Vjg swkem dtqyp hqz
...
```

### Vigenère

```console
$ uv run ghost-wires vigenere --chave lemon "attack at dawn"
lxfopv ef rnhr

$ uv run ghost-wires vigenere --chave lemon --decifrar "lxfopv ef rnhr"
attack at dawn
```

### Atbash

```console
$ uv run ghost-wires atbash "Hello, World!"
Svool, Dliow!

$ uv run ghost-wires atbash "Svool, Dliow!"
Hello, World!
```

### Playfair

```console
$ uv run ghost-wires playfair --chave monarchy "instruments"
GATLMZCLRQXA

$ uv run ghost-wires playfair --chave monarchy --decifrar "GATLMZCLRQXA"
INSTRUMENTSX
```

Note o `X` no fim: a cifra trabalha com pares, e o texto de tamanho ímpar recebe uma letra de enchimento. A decifração devolve o texto preparado, com o enchimento.

### Rail fence

```console
$ uv run ghost-wires rail-fence --trilhos 3 "WE ARE DISCOVERED"
WRIVDEAEDSOEE  CR

$ uv run ghost-wires rail-fence --trilhos 3 --decifrar "WRIVDEAEDSOEE  CR"
WE ARE DISCOVERED
```

### Inverter

```console
$ uv run ghost-wires inverter "bom dia"
aid mob

$ uv run ghost-wires inverter --por-palavra "um dois três"
três dois um
```

### Bases numéricas

As bases aceitas são 2, 8, 10 e 16. Cada caractere vira um número com largura mínima (`08b`, `03o`, `03d`, `02x`), separados por espaço. Caracteres com código grande não são truncados.

```console
$ uv run ghost-wires texto-para-numeros --base 16 "Olá"
4f 6c e1

$ uv run ghost-wires numeros-para-texto --base 16 "4f 6c e1"
Olá

$ uv run ghost-wires inteiro-para-base36 12345
9ix

$ uv run ghost-wires base36-para-inteiro 9ix
12345
```

### Base64

```console
$ uv run ghost-wires texto-para-base64 "Olá, mundo"
T2zDoSwgbXVuZG8=

$ uv run ghost-wires base64-para-texto "T2zDoSwgbXVuZG8="
Olá, mundo
```

### Morse

Letras são separadas por espaço e palavras por ` / `. A decodificação sempre devolve letras maiúsculas.

```console
$ uv run ghost-wires texto-para-morse "SOS 2026!"
... --- ... / ..--- ----- ..--- -.... -.-.--

$ uv run ghost-wires morse-para-texto "... --- ..."
SOS
```

### Teclado de telefone

Cada letra vira a tecla repetida tantas vezes quanto a posição da letra na tecla. As letras são separadas por espaço, o que resolve a ambiguidade entre, por exemplo, `A B` e `B`.

```console
$ uv run ghost-wires texto-para-teclado "Hello World"
44 33 555 555 666 / 9 666 777 555 3

$ uv run ghost-wires teclado-para-texto "44 33 555 555 666 / 9 666 777 555 3"
HELLO WORLD
```

### Erros

Erros de uso e entradas inválidas vão para o `stderr` com o prefixo `erro:`, e o programa sai com código 2.

```console
$ uv run ghost-wires texto-para-numeros --base 3 "A"
erro: A base deve ser uma destas opções: 2, 8, 10, 16.
```

## Decisões de projeto

Cada cifra tem pontos em que mais de um comportamento seria razoável. Estas são as escolhas, todas cobertas por teste.

- **Só letras ASCII são cifradas.** César, Vigenère e Atbash trocam apenas `a-z` e `A-Z`, e a caixa é preservada. Todo o resto passa sem mudar, inclusive letras acentuadas.
- **A chave do Vigenère só aceita letras ASCII** e não pode ser vazia. O índice da chave só avança nas letras do texto, não em espaços ou pontuação.
- **Playfair trata J como I.** A grade tem 25 letras. O enchimento é `X`, ou `Q` quando o par repetido já é `XX`. Letras acentuadas e caracteres que não são letras são ignorados, e a decifração mantém o enchimento.
- **Rail fence usa todos os caracteres.** Espaço e pontuação entram na grade. Menos de 2 trilhos é erro, e com trilhos maior ou igual ao tamanho do texto o resultado é o próprio texto.
- **Inverter trabalha com pontos de código.** Uma letra com acento decomposto (`e` mais o acento combinante) tem as duas partes trocadas de ordem. No modo por palavra, os separadores originais são preservados, inclusive espaços repetidos e quebras de linha, e o espaço não separável conta como separador.
- **Base64 é estrito.** A entrada precisa ser Base64 válida, com padding correto e sem quebras de linha, e o resultado precisa ser UTF-8.
- **Morse e teclado ignoram a caixa na ida.** `sos` e `SOS` geram o mesmo código, e a volta devolve maiúscula. O teclado aceita só letras ASCII e espaços.
- **Caracteres parecidos não são letras.** Caracteres como `ß`, `ſ` e o sinal Kelvin viram letras ASCII quando passam por `.upper()` ou `.lower()`. O projeto valida o caractere original antes de converter, e esses casos geram erro em vez de uma cifra silenciosa e errada.

## Usando como biblioteca

As funções ficam em `ghost_wires.cifras` e podem ser importadas direto:

```python
from ghost_wires.cifras import cesar, vigenere

cesar("bom dia", 3)                  # 'erp gld'
vigenere("attack at dawn", "lemon")  # 'lxfopv ef rnhr'
```

## Testes

```bash
uv run pytest
```

Cada função tem uma classe de teste em `tests/test_cifras.py`, e a linha de comando é testada chamando `main(argv)` direto, sem subprocesso. Os testes cobrem ida e volta de cada cifra, os casos de erro e as decisões acima. Onde existe um exemplo clássico publicado, como o do Vigenère com a chave `lemon` e o do Playfair com `MONARCHY`, um teste confere a saída contra ele.

## Estrutura

```text
src/ghost_wires/
├── __init__.py   # linha de comando (argparse) e função main
└── cifras.py     # as cifras e conversões
tests/
└── test_cifras.py
```

## Sobre o projeto

Projeto de estudo de Python, feito fase por fase: primeiro o deslocamento de uma letra, depois cada cifra, a linha de comando e, por fim, as cifras extras. O código é meu, escrito com revisão ponto a ponto.
