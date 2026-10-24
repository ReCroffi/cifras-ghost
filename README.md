# Decifrador

Enquanto eu lia `Ghost in the Wires`, de Kevin Mitchnik, vi que o começo de cada capítulo possuia um texto cifrado.

Esse projeto nasce da curiosidade de saber o que está escrito no início de cada capítulo.

## Instalação e uso

Instale o projeto com [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

O comando aceita o texto como argumento ou lê da entrada padrão:

```bash
uv run ghost-wires cesar -n 3 "bom dia"
echo "bom dia" | uv run ghost-wires cesar -n 3
uv run ghost-wires forca-bruta "texto cifrado"
uv run ghost-wires vigenere --chave lemon "attack at dawn"
uv run ghost-wires texto-para-numeros --base 16 "Olá"
uv run ghost-wires numeros-para-texto --base 16 "4f 6c 61"
uv run ghost-wires inteiro-para-base36 12345
uv run ghost-wires base36-para-inteiro 9ix
uv run ghost-wires texto-para-base64 "Olá"
uv run ghost-wires base64-para-texto "T2zDoQ=="
uv run ghost-wires texto-para-morse "SOS 2026!"
uv run ghost-wires morse-para-texto "... --- ... / ..--- ----- ..--- -...."
```

Use `uv run ghost-wires --help` para listar todos os subcomandos.
