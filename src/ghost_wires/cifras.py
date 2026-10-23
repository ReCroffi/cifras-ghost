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
