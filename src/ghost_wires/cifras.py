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


_FORMATOS_NUMERICOS = {
    2: "08b",
    8: "03o",
    10: "03d",
    16: "02x",
}


def _validar_base(base: int) -> str:
    try:
        return _FORMATOS_NUMERICOS[base]
    except KeyError as erro:
        bases_validas = ", ".join(str(base_valida) for base_valida in _FORMATOS_NUMERICOS)
        raise ValueError(
            f"A base deve ser uma destas opções: {bases_validas}."
        ) from erro


def texto_para_numeros(texto: str, base: int) -> str:
    """
    Converte cada caractere de um texto para seu código numérico na base especificada.

    Parâmetros:
    texto (str): O texto a ser convertido.
    base (int): A base numérica para a conversão.

    Retorna:
    str: Uma string contendo os códigos numéricos de cada caractere na base especificada, separados por espaço.

    Levanta:
    ValueError: Se a base não for suportada.
    """
    formato = _validar_base(base)
    return " ".join(format(ord(c), formato) for c in texto)


def numeros_para_texto(numeros: str, base: int) -> str:
    """
    Converte uma string de códigos numéricos na base especificada de volta para texto.

    Parâmetros:
    numeros (str): Uma string contendo os códigos numéricos separados por espaço.
    base (int): A base numérica dos códigos.

    Retorna:
    str: O texto correspondente aos códigos numéricos.

    Levanta:
    ValueError: Se a base não for suportada.
    """
    _validar_base(base)

    resultado = []
    for numero in numeros.split():
        try:
            resultado.append(chr(int(numero, base)))
        except ValueError as erro:
            raise ValueError(
                f"Número inválido {numero!r} na base {base}."
            ) from erro

    return "".join(resultado)
