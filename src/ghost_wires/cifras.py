import base64
import binascii
import re
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


def atbash(texto: str) -> str:
    """
    Aplica a transformação Atbash, espelhando cada letra do alfabeto.

    Parâmetros:
    texto (str): O texto a ser transformado.

    Retorna:
    str: O texto com as letras ASCII espelhadas.
    """
    resultado = []
    for caractere in texto:
        if not _eh_letra_ascii(caractere):
            resultado.append(caractere)
            continue

        base = ord("A") if caractere.isupper() else ord("a")
        resultado.append(chr(base + 25 - (ord(caractere) - base)))

    return "".join(resultado)


def inverter(texto: str, por_palavra: bool = False) -> str:
    """
    Inverte um texto por caractere ou pela ordem das palavras.

    Parâmetros:
    texto (str): O texto a ser invertido.
    por_palavra (bool): Se True, inverte as palavras e preserva os
        separadores exatamente como aparecem.

    No modo por caractere, a inversão ocorre por ponto de código Unicode;
    combinações decompostas, como ``e\\u0301``, não são tratadas como um único
    grafema visual.

    Retorna:
    str: O texto invertido.
    """
    if not por_palavra:
        return texto[::-1]

    partes = re.split(r"(\s+)", texto)
    palavras = [parte for parte in partes if parte and not parte.isspace()]
    palavras.reverse()
    indice_palavra = 0
    resultado = []
    for parte in partes:
        if not parte or parte.isspace():
            resultado.append(parte)
        else:
            resultado.append(palavras[indice_palavra])
            indice_palavra += 1
    return "".join(resultado)


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
        bases_validas = ", ".join(
            str(base_valida) for base_valida in _FORMATOS_NUMERICOS
        )
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
            raise ValueError(f"Número inválido {numero!r} na base {base}.") from erro

    return "".join(resultado)


def inteiro_para_base36(n: int) -> str:
    """
    Converte um número inteiro para uma string na base 36.

    Parâmetros:
    n (int): O número inteiro a ser convertido.

    Retorna:
    str: A representação do número na base 36.

    Levanta:
    ValueError: Se o número for negativo.
    """
    if n < 0:
        raise ValueError("O número deve ser não-negativo.")

    if n == 0:
        return "0"

    base36 = ""
    while n > 0:
        n, resto = divmod(n, 36)
        if resto < 10:
            base36 = str(resto) + base36
        else:
            base36 = chr(resto - 10 + ord("a")) + base36

    return base36


def base36_para_inteiro(s: str) -> int:
    """
    Converte uma string na base 36 de volta para um número inteiro.

    Parâmetros:
    s (str): A string na base 36 a ser convertida.

    Retorna:
    int: O número inteiro correspondente.

    Levanta:
    ValueError: Se a string for vazia ou contiver um caractere que não seja
        válido na base 36.
    """
    if not s:
        raise ValueError("A string não pode ser vazia.")

    n = 0
    for caractere in s:
        if "0" <= caractere <= "9":
            n = n * 36 + (ord(caractere) - ord("0"))
        elif _eh_letra_ascii(caractere):
            caractere = caractere.lower()
            n = n * 36 + (ord(caractere) - ord("a") + 10)
        else:
            raise ValueError(f"Caractere inválido {caractere!r} na base 36.")

    return n


def texto_para_base64(texto: str) -> str:
    """
    Codifica um texto em Base64 usando UTF-8.

    Parâmetros:
    texto (str): O texto a ser codificado.

    Retorna:
    str: O texto codificado em Base64.
    """
    return base64.b64encode(texto.encode("utf-8")).decode("ascii")


def base64_para_texto(s: str) -> str:
    """
    Decodifica uma string Base64 como texto UTF-8.

    Parâmetros:
    s (str): A string Base64 a ser decodificada.

    Retorna:
    str: O texto original.

    Levanta:
    ValueError: Se a entrada não for Base64 válida ou não representar UTF-8.
    """
    try:
        dados = base64.b64decode(s.encode("ascii"), validate=True)
        return dados.decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError, binascii.Error) as erro:
        raise ValueError("A entrada não é uma Base64 válida em UTF-8.") from erro


MORSE: dict[str, str] = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    ".": ".-.-.-",
    ",": "--..--",
    "?": "..--..",
    "!": "-.-.--",
    "'": ".----.",
    '"': ".-..-.",
    ":": "---...",
    ";": "-.-.-.",
    "(": "-.--.",
    ")": "-.--.-",
    "-": "-....-",
    "/": "-..-.",
    "@": ".--.-.",
}
_MORSE_INVERSO = {codigo: caractere for caractere, codigo in MORSE.items()}


def texto_para_morse(texto: str) -> str:
    """
    Converte texto para Morse, separando letras por espaço e palavras por
    `` / ``.

    Parâmetros:
    texto (str): O texto a ser convertido.

    Retorna:
    str: O texto convertido para Morse.

    Levanta:
    ValueError: Se o texto contiver um caractere não presente em MORSE.
    """
    palavras = []
    for palavra in texto.split(" "):
        codigos = []
        for caractere in palavra:
            if _eh_letra_ascii(caractere):
                caractere = caractere.upper()
            try:
                codigos.append(MORSE[caractere])
            except KeyError as erro:
                raise ValueError(
                    f"Caractere não suportado em Morse: {caractere!r}."
                ) from erro
        palavras.append(" ".join(codigos))
    return " / ".join(palavras)


def morse_para_texto(s: str) -> str:
    """
    Converte Morse para texto, usando `` / `` entre palavras.

    A tabela de decodificação é derivada de MORSE. Letras decodificadas são
    retornadas em maiúsculas.

    Parâmetros:
    s (str): O texto em código Morse, com espaços entre letras e `` / ``
        entre palavras.

    Retorna:
    str: O texto decodificado em letras maiúsculas.

    Levanta:
    ValueError: Se um código Morse não estiver presente em MORSE.
    """
    palavras = []
    for palavra in s.split(" / "):
        caracteres = []
        for codigo in palavra.split():
            try:
                caracteres.append(_MORSE_INVERSO[codigo])
            except KeyError as erro:
                raise ValueError(f"Código Morse inválido: {codigo!r}.") from erro
        palavras.append("".join(caracteres))
    return " ".join(palavras)


_ALFABETO_PLAYFAIR = "ABCDEFGHIKLMNOPQRSTUVWXYZ"


def _limpar_playfair(texto: str) -> str:
    return "".join(
        "I" if caractere.upper() == "J" else caractere.upper()
        for caractere in texto
        if _eh_letra_ascii(caractere)
    )


def montar_grade(chave: str) -> list[list[str]]:
    """
    Monta a grade 5x5 de Playfair a partir de uma chave.

    Parâmetros:
    chave (str): A chave usada para iniciar a grade. J é tratado como I.

    Retorna:
    list[list[str]]: A grade com 25 letras distintas.

    Levanta:
    ValueError: Se a chave for vazia ou não contiver letras ASCII.
    """
    chave_limpa = _limpar_playfair(chave)
    if not chave_limpa:
        raise ValueError("A chave deve conter pelo menos uma letra ASCII.")

    letras = []
    for caractere in chave_limpa + _ALFABETO_PLAYFAIR:
        if caractere not in letras:
            letras.append(caractere)
    return [letras[inicio : inicio + 5] for inicio in range(0, 25, 5)]


def preparar_digramas(texto: str) -> list[str]:
    """
    Limpa um texto e divide-o em pares de letras diferentes.

    Letras não ASCII e caracteres que não sejam letras são ignorados. J é
    tratado como I. O filler é X, ou Q quando o par repetido já for XX.

    Parâmetros:
    texto (str): O texto a ser preparado.

    Retorna:
    list[str]: Os digramas preparados.
    """
    texto_limpo = _limpar_playfair(texto)
    digramas = []
    indice = 0
    while indice < len(texto_limpo):
        primeira = texto_limpo[indice]
        segunda_disponivel = indice + 1 < len(texto_limpo)
        if not segunda_disponivel or primeira == texto_limpo[indice + 1]:
            filler = "Q" if primeira == "X" else "X"
            digramas.append(primeira + filler)
            indice += 1
        else:
            digramas.append(primeira + texto_limpo[indice + 1])
            indice += 2
    return digramas


def playfair(texto: str, chave: str, decifrar: bool = False) -> str:
    """
    Cifra ou decifra texto usando a cifra de Playfair.

    A decifração retorna o texto preparado e mantém os fillers. Ela aceita
    pares duplicados na entrada, embora uma cifragem válida nunca os produza.

    Parâmetros:
    texto (str): O texto a ser cifrado ou decifrado.
    chave (str): A chave da grade.
    decifrar (bool): Se True, decifra o texto.

    Retorna:
    str: O texto cifrado ou o texto preparado decifrado.

    Levanta:
    ValueError: Se a chave for inválida ou o texto decifrado tiver tamanho
        ímpar.
    """
    grade = montar_grade(chave)
    posicoes = {
        caractere: (linha, coluna)
        for linha, linha_grade in enumerate(grade)
        for coluna, caractere in enumerate(linha_grade)
    }
    if decifrar:
        texto_limpo = _limpar_playfair(texto)
        if len(texto_limpo) % 2:
            raise ValueError("O texto Playfair deve ter tamanho par.")
        digramas = [
            texto_limpo[indice : indice + 2]
            for indice in range(0, len(texto_limpo), 2)
        ]
    else:
        digramas = preparar_digramas(texto)

    resultado = []
    passo = -1 if decifrar else 1
    for primeira, segunda in digramas:
        linha_a, coluna_a = posicoes[primeira]
        linha_b, coluna_b = posicoes[segunda]
        if linha_a == linha_b:
            resultado.extend(
                (
                    grade[linha_a][(coluna_a + passo) % 5],
                    grade[linha_b][(coluna_b + passo) % 5],
                )
            )
        elif coluna_a == coluna_b:
            resultado.extend(
                (
                    grade[(linha_a + passo) % 5][coluna_a],
                    grade[(linha_b + passo) % 5][coluna_b],
                )
            )
        else:
            resultado.extend(
                (grade[linha_a][coluna_b], grade[linha_b][coluna_a])
            )
    return "".join(resultado)


TECLAS: dict[str, str] = {
    "2": "ABC",
    "3": "DEF",
    "4": "GHI",
    "5": "JKL",
    "6": "MNO",
    "7": "PQRS",
    "8": "TUV",
    "9": "WXYZ",
}
_TECLAS_POR_LETRA = {
    letra: (tecla, posicao)
    for tecla, letras in TECLAS.items()
    for posicao, letra in enumerate(letras, start=1)
}
_LETRAS_POR_TOQUES = {
    tecla * posicao: letra
    for tecla, letras in TECLAS.items()
    for posicao, letra in enumerate(letras, start=1)
}


def texto_para_teclado(texto: str) -> str:
    """
    Converte letras para os toques de um teclado telefônico.

    Letras são separadas por espaço e palavras por `` / ``. A saída usa
    letras maiúsculas; somente letras ASCII e espaços são aceitos.

    Parâmetros:
    texto (str): O texto a ser convertido.

    Retorna:
    str: Os toques correspondentes ao texto.

    Levanta:
    ValueError: Se o texto contiver um caractere que não seja letra ASCII ou
        espaço.
    """
    palavras = []
    for palavra in texto.split(" "):
        toques = []
        for caractere in palavra:
            if not _eh_letra_ascii(caractere):
                raise ValueError(
                    f"Caractere não suportado no teclado: {caractere!r}."
                )
            caractere = caractere.upper()
            tecla, quantidade = _TECLAS_POR_LETRA[caractere]
            toques.append(tecla * quantidade)
        palavras.append(" ".join(toques))
    return " / ".join(palavras)


def teclado_para_texto(s: str) -> str:
    """
    Converte toques de teclado telefônico para texto em maiúsculas.

    Parâmetros:
    s (str): Toques separados por espaço e palavras por `` / ``.

    Retorna:
    str: O texto decodificado em letras maiúsculas.

    Levanta:
    ValueError: Se um grupo de toques não existir em TECLAS.
    """
    palavras = []
    for palavra in s.split(" / "):
        caracteres = []
        for toques in palavra.split():
            try:
                caracteres.append(_LETRAS_POR_TOQUES[toques])
            except KeyError as erro:
                raise ValueError(
                    f"Sequência de toques inválida: {toques!r}."
                ) from erro
        palavras.append("".join(caracteres))
    return " ".join(palavras)


def rail_fence(texto: str, trilhos: int, decifrar: bool = False) -> str:
    """
    Cifra ou decifra texto pela transposição Rail Fence.

    Todos os caracteres, inclusive espaços e pontuação, entram na grade.
    Com menos de dois trilhos, a operação é inválida. Quando a quantidade
    de trilhos é maior ou igual ao tamanho do texto, o texto retorna igual,
    pois cada posição ocupa um trilho próprio.

    Parâmetros:
    texto (str): O texto a ser cifrado ou decifrado.
    trilhos (int): A quantidade de trilhos do zigue-zague.
    decifrar (bool): Se True, desfaz a transposição.

    Retorna:
    str: O texto transformado.

    Levanta:
    ValueError: Se trilhos for menor que 2.
    """
    if trilhos < 2:
        raise ValueError("A quantidade de trilhos deve ser pelo menos 2.")
    if trilhos >= len(texto):
        return texto

    trilho_por_posicao = []
    trilho = 0
    direcao = 1
    for _ in texto:
        trilho_por_posicao.append(trilho)
        if trilho == 0:
            direcao = 1
        elif trilho == trilhos - 1:
            direcao = -1
        trilho += direcao

    ordem_por_trilho = sorted(
        range(len(texto)), key=trilho_por_posicao.__getitem__
    )
    if not decifrar:
        return "".join(texto[posicao] for posicao in ordem_por_trilho)

    resultado = [""] * len(texto)
    for posicao_cifrada, posicao_original in enumerate(ordem_por_trilho):
        resultado[posicao_original] = texto[posicao_cifrada]
    return "".join(resultado)
