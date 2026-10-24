import string


def _eh_letra_ascii(c: str) -> bool:
    return len(c) == 1 and c in string.ascii_letters


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
    if not _eh_letra_ascii(c):
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
            palavra.strip(string.punctuation).lower() for palavra in tentativa.split()
        )
        nota = sum(palavra in PALAVRAS_COMUNS_INGLES for palavra in palavras)
        tentativas.append((nota, n, tentativa))

    return sorted(tentativas, key=lambda tentativa: tentativa[0], reverse=True)


def vigenere(texto: str, chave: str, decifrar: bool = False) -> str:
    """
    Aplica a cifra de Vigenère a um texto, usando uma chave fornecida.
    Para decifrar o texto, defina decifrar=True.

    Parâmetros:
    texto (str): O texto a ser cifrado ou decifrado.
    chave (str): A chave usada para o deslocamento das letras.
    decifrar (bool): Se True, decifra o texto; caso contrário, cifra.

    Retorna:
    str: O texto cifrado ou decifrado.

    Levanta:
    ValueError: Se a chave for vazia ou contiver caracteres que não sejam
        letras ASCII.
    """
    if not chave:
        raise ValueError("A chave não pode ser vazia.")
    if not all(_eh_letra_ascii(c) for c in chave):
        raise ValueError("A chave deve conter apenas letras ASCII.")

    resultado = []
    chave = chave.lower()
    indice_chave = 0
    tamanho_chave = len(chave)

    for c in texto:
        if _eh_letra_ascii(c):
            deslocamento = ord(chave[indice_chave % tamanho_chave]) - ord("a")
            if decifrar:
                deslocamento = -deslocamento
            resultado.append(deslocar_letra(c, deslocamento))
            indice_chave += 1
        else:
            resultado.append(c)

    return "".join(resultado)
