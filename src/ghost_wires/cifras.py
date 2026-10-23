import string


def deslocar_letra(c: str, n: int) -> str:
    """
    Desloca uma letra c por n posições no alfabeto.

    Parâmetros:
    c (str): O caractere a ser deslocado. Só letras de a a z (maiúsculas ou
        minúsculas) são deslocadas; qualquer outra coisa, inclusive letra
        acentuada, volta igual.
    n (int): O número de posições para deslocar. Pode ser positivo ou negativo.

    Retorna:
    str: O caractere resultante após o deslocamento.
    """
    if len(c) != 1 or c.lower() not in "abcdefghijklmnopqrstuvwxyz":
        return c

    # Determina o ponto de referência (A ou a)
    base = ord("A") if c.isupper() else ord("a")

    # Calcula a nova posição com wrap-around usando módulo
    deslocamento = (ord(c) - base + n) % 26
    nova_letra = chr(base + deslocamento)

    return nova_letra


def cesar(texto: str, n: int) -> str:
    """
    Aplica a cifra de César a um texto, deslocando cada letra por n posições.
    Para decifrar o texto, chame esta função novamente com -n.

    Parâmetros:
    texto (str): O texto a ser cifrado.
    n (int): O número de posições para deslocar cada letra.

    Retorna:
    str: O texto cifrado.
    """
    return "".join(deslocar_letra(c, n) for c in texto)


PALAVRAS_COMUNS_INGLES = {
    "a",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "for",
    "from",
    "have",
    "he",
    "in",
    "is",
    "it",
    "of",
    "on",
    "that",
    "the",
    "this",
    "to",
    "was",
    "we",
    "you",
}


def forca_bruta_cesar(texto: str) -> list[tuple[int, int, str]]:
    """
    Tenta decifrar um texto cifrado com a cifra de César, testando todas as
    26 possibilidades de deslocamento. Cada resultado é acompanhado de uma
    nota baseada na quantidade de palavras comuns em inglês e os resultados
    são ordenados da melhor tentativa para a pior.

    Parâmetros:
    texto (str): O texto cifrado.

    Retorna:
    list[tuple[int, int, str]]: Uma lista de triplas (nota, n, tentativa),
        ordenada pela nota em ordem decrescente.
    """
    tentativas = []
    for n in range(26):
        tentativa = cesar(texto, -n)
        palavras = (
            palavra.strip(string.punctuation).lower()
            for palavra in tentativa.split()
        )
        nota = sum(palavra in PALAVRAS_COMUNS_INGLES for palavra in palavras)
        tentativas.append((nota, n, tentativa))

    return sorted(tentativas, key=lambda tentativa: tentativa[0], reverse=True)
