import argparse
import sys

from .cifras import (
    atbash,
    base36_para_inteiro,
    base64_para_texto,
    cesar,
    forca_bruta_cesar,
    inteiro_para_base36,
    inverter,
    morse_para_texto,
    playfair,
    numeros_para_texto,
    texto_para_base64,
    texto_para_morse,
    teclado_para_texto,
    texto_para_teclado,
    texto_para_numeros,
    vigenere,
    rail_fence,
)


def _texto_do_argumento_ou_stdin(texto: str | None) -> str:
    if texto is not None:
        return texto

    entrada = sys.stdin.read()
    if entrada.endswith("\n"):
        entrada = entrada[:-1]
        if entrada.endswith("\r"):
            entrada = entrada[:-1]
    return entrada


def _criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Cifra, decifra e converte textos."
    )
    subparsers = parser.add_subparsers(dest="comando", required=True)

    cesar_parser = subparsers.add_parser("cesar", help="Aplica a cifra de César.")
    cesar_parser.add_argument("-n", type=int, required=True, help="Deslocamento.")
    cesar_parser.add_argument("texto", nargs="?")

    atbash_parser = subparsers.add_parser(
        "atbash", help="Aplica a transformação Atbash."
    )
    atbash_parser.add_argument("texto", nargs="?")

    inverter_parser = subparsers.add_parser(
        "inverter", help="Inverte caracteres ou palavras."
    )
    inverter_parser.add_argument(
        "-p",
        "--por-palavra",
        action="store_true",
        help="Inverte a ordem das palavras.",
    )
    inverter_parser.add_argument("texto", nargs="?")

    playfair_parser = subparsers.add_parser(
        "playfair", help="Aplica a cifra de Playfair."
    )
    playfair_parser.add_argument("-k", "--chave", required=True)
    playfair_parser.add_argument(
        "-d", "--decifrar", action="store_true", help="Decifra o texto."
    )
    playfair_parser.add_argument("texto", nargs="?")

    rail_parser = subparsers.add_parser(
        "rail-fence", help="Aplica a cifra Rail Fence."
    )
    rail_parser.add_argument("-t", "--trilhos", type=int, required=True)
    rail_parser.add_argument(
        "-d", "--decifrar", action="store_true", help="Decifra o texto."
    )
    rail_parser.add_argument("texto", nargs="?")

    for nome, ajuda in (
        ("texto-para-teclado", "Converte texto para toques telefônicos."),
        ("teclado-para-texto", "Converte toques telefônicos para texto."),
    ):
        teclado_parser = subparsers.add_parser(nome, help=ajuda)
        teclado_parser.add_argument("texto", nargs="?")

    forca_parser = subparsers.add_parser(
        "forca-bruta", help="Tenta decifrar uma cifra de César."
    )
    forca_parser.add_argument("texto", nargs="?")

    vigenere_parser = subparsers.add_parser(
        "vigenere", help="Aplica a cifra de Vigenère."
    )
    vigenere_parser.add_argument("-k", "--chave", required=True)
    vigenere_parser.add_argument(
        "-d", "--decifrar", action="store_true", help="Decifra o texto."
    )
    vigenere_parser.add_argument("texto", nargs="?")

    for nome, funcao, ajuda in (
        ("texto-para-numeros", texto_para_numeros, "Converte texto para uma base."),
        ("numeros-para-texto", numeros_para_texto, "Converte uma base para texto."),
    ):
        conversao_parser = subparsers.add_parser(nome, help=ajuda)
        conversao_parser.add_argument("-b", "--base", type=int, required=True)
        conversao_parser.add_argument("texto", nargs="?")

    inteiro_parser = subparsers.add_parser(
        "inteiro-para-base36", help="Converte um inteiro para base 36."
    )
    inteiro_parser.add_argument("numero", type=int)

    base36_parser = subparsers.add_parser(
        "base36-para-inteiro", help="Converte base 36 para inteiro."
    )
    base36_parser.add_argument("texto", nargs="?")

    for nome, ajuda in (
        ("texto-para-base64", "Codifica texto em Base64."),
        ("base64-para-texto", "Decodifica Base64 para texto."),
        ("texto-para-morse", "Codifica texto em Morse."),
        ("morse-para-texto", "Decodifica Morse para texto."),
    ):
        conversao_parser = subparsers.add_parser(nome, help=ajuda)
        conversao_parser.add_argument("texto", nargs="?")

    return parser


def _executar(args: argparse.Namespace) -> str:
    if args.comando == "atbash":
        return atbash(_texto_do_argumento_ou_stdin(args.texto))
    if args.comando == "inverter":
        return inverter(
            _texto_do_argumento_ou_stdin(args.texto),
            por_palavra=args.por_palavra,
        )
    if args.comando == "playfair":
        return playfair(
            _texto_do_argumento_ou_stdin(args.texto),
            args.chave,
            decifrar=args.decifrar,
        )
    if args.comando == "rail-fence":
        return rail_fence(
            _texto_do_argumento_ou_stdin(args.texto),
            args.trilhos,
            decifrar=args.decifrar,
        )
    if args.comando == "texto-para-teclado":
        return texto_para_teclado(_texto_do_argumento_ou_stdin(args.texto))
    if args.comando == "teclado-para-texto":
        return teclado_para_texto(_texto_do_argumento_ou_stdin(args.texto))
    if args.comando == "cesar":
        return cesar(_texto_do_argumento_ou_stdin(args.texto), args.n)
    if args.comando == "forca-bruta":
        tentativas = forca_bruta_cesar(_texto_do_argumento_ou_stdin(args.texto))
        return "\n".join(
            f"{nota} {deslocamento} {tentativa}"
            for nota, deslocamento, tentativa in tentativas
        )
    if args.comando == "vigenere":
        return vigenere(
            _texto_do_argumento_ou_stdin(args.texto),
            args.chave,
            decifrar=args.decifrar,
        )
    if args.comando == "texto-para-numeros":
        return texto_para_numeros(
            _texto_do_argumento_ou_stdin(args.texto), args.base
        )
    if args.comando == "numeros-para-texto":
        return numeros_para_texto(
            _texto_do_argumento_ou_stdin(args.texto), args.base
        )
    if args.comando == "inteiro-para-base36":
        return inteiro_para_base36(args.numero)
    if args.comando == "base36-para-inteiro":
        return str(base36_para_inteiro(_texto_do_argumento_ou_stdin(args.texto)))
    if args.comando == "texto-para-base64":
        return texto_para_base64(_texto_do_argumento_ou_stdin(args.texto))
    if args.comando == "base64-para-texto":
        return base64_para_texto(_texto_do_argumento_ou_stdin(args.texto))
    if args.comando == "texto-para-morse":
        return texto_para_morse(_texto_do_argumento_ou_stdin(args.texto))
    if args.comando == "morse-para-texto":
        return morse_para_texto(_texto_do_argumento_ou_stdin(args.texto))
    raise ValueError(f"Comando desconhecido: {args.comando}")


def main(argv: list[str] | None = None) -> int:
    """Executa a interface de linha de comando do projeto."""
    parser = _criar_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as erro:
        return int(erro.code)

    try:
        print(_executar(args))
    except ValueError as erro:
        print(f"erro: {erro}", file=sys.stderr)
        return 2
    return 0
