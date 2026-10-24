import unittest
from io import StringIO
from unittest.mock import patch

from ghost_wires.cifras import (
    atbash,
    cesar,
    base64_para_texto,
    base36_para_inteiro,
    deslocar_letra,
    forca_bruta_cesar,
    morse_para_texto,
    montar_grade,
    playfair,
    preparar_digramas,
    rail_fence,
    TECLAS,
    teclado_para_texto,
    texto_para_base64,
    texto_para_morse,
    texto_para_teclado,
    MORSE,
    numeros_para_texto,
    texto_para_numeros,
    vigenere,
    inteiro_para_base36,
    inverter,
)
from ghost_wires import main


class TestDeslocarLetra(unittest.TestCase):
    def test_deslocar_e_desfazer_retorna_a_letra_original(self):
        for letra in ("A", "M", "z", "é", "Ç"):
            for n in (0, 1, -1, 26, 100):
                with self.subTest(letra=letra, n=n):
                    deslocada = deslocar_letra(letra, n)
                    self.assertEqual(deslocar_letra(deslocada, -n), letra)

    def test_deslocar_por_26_nao_muda_a_letra(self):
        for letra in ("A", "M", "Z", "a", "m", "z"):
            with self.subTest(letra=letra):
                self.assertEqual(deslocar_letra(letra, 26), letra)

    def test_caractere_que_nao_e_letra_volta_igual(self):
        for caractere in ("1", " ", "!", "?"):
            with self.subTest(caractere=caractere):
                self.assertEqual(deslocar_letra(caractere, 5), caractere)

    def test_caixa_e_preservada(self):
        self.assertEqual(deslocar_letra("A", 1), "B")
        self.assertEqual(deslocar_letra("Z", 1), "A")
        self.assertEqual(deslocar_letra("a", 1), "b")
        self.assertEqual(deslocar_letra("z", 1), "a")

    def test_letra_acentuada_volta_igual(self):
        for letra in ("é", "ç", "Ã", "ü"):
            with self.subTest(letra=letra):
                self.assertEqual(deslocar_letra(letra, 3), letra)


class TestCesar(unittest.TestCase):
    def test_deslocar_e_desfazer_retorna_o_texto_original(self):
        texto = "Hello, World! Ãç"
        for n in (0, 1, -1, 13, 26, -26, 100, -100):
            with self.subTest(n=n):
                deslocado = cesar(texto, n)
                self.assertEqual(cesar(deslocado, -n), texto)

    def test_rot13_aplicado_duas_vezes_retorna_o_original(self):
        texto = "Hello, World! Ãç"
        self.assertEqual(cesar(cesar(texto, 13), 13), texto)

    def test_desloca_todas_as_letras(self):
        texto = "Hello, World!"
        deslocado = "Khoor, Zruog!"
        self.assertEqual(cesar(texto, 3), deslocado)


class TestAtbash(unittest.TestCase):
    def test_aplicar_duas_vezes_retorna_o_texto_original(self):
        texto = "Hello, World! 123 Ãç"

        self.assertEqual(atbash(atbash(texto)), texto)

    def test_espelha_as_52_letras_sem_manter_nenhuma_igual(self):
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        espelhadas = atbash(letras)

        self.assertEqual(
            espelhadas,
            "ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba",
        )
        self.assertTrue(all(original != resultado for original, resultado in zip(letras, espelhadas)))

    def test_preserva_caixa_e_caracteres_que_nao_sao_letras_ascii(self):
        self.assertEqual(atbash("aZ b1!é"), "zA y1!é")


class TestInverter(unittest.TestCase):
    def test_aplicar_duas_vezes_retorna_o_original_nos_dois_modos(self):
        texto = "Um texto\ncom palavras"

        self.assertEqual(inverter(inverter(texto)), texto)
        self.assertEqual(
            inverter(inverter(texto, por_palavra=True), por_palavra=True),
            texto,
        )

    def test_modo_por_caractere_preserva_tamanho_e_multiconjunto(self):
        texto = "a a! 22"

        resultado = inverter(texto)
        self.assertEqual(len(resultado), len(texto))
        self.assertEqual(sorted(resultado), sorted(texto))

    def test_um_caractere_e_texto_vazio(self):
        self.assertEqual(inverter("x"), "x")
        self.assertEqual(inverter("x", por_palavra=True), "x")
        self.assertEqual(inverter(""), "")
        self.assertEqual(inverter("", por_palavra=True), "")

    def test_modo_por_palavra_preserva_separadores_repetidos_e_quebras(self):
        self.assertEqual(
            inverter("um  dois\n\ttrês", por_palavra=True),
            "três  dois\n\tum",
        )

    def test_modo_por_caractere_inverte_pontos_de_codigo_decompostos(self):
        self.assertEqual(inverter("e\u0301a"), "a\u0301e")

    def test_modo_por_palavra_trata_espaco_nao_separavel_como_separador(self):
        self.assertEqual(inverter("a\u00a0b c", por_palavra=True), "c\u00a0b a")

    def test_modo_por_palavra_preserva_espacos_nas_bordas(self):
        self.assertEqual(inverter("  um dois  ", por_palavra=True), "  dois um  ")

    def test_modo_por_palavra_preserva_texto_so_com_espacos(self):
        texto = " \t  \n"

        self.assertEqual(inverter(texto, por_palavra=True), texto)


class TestPlayfair(unittest.TestCase):
    def test_monta_grade_com_chave_sem_repeticoes_e_sem_j(self):
        grade = montar_grade("banana")
        letras = [letra for linha in grade for letra in linha]

        self.assertEqual(len(letras), 25)
        self.assertEqual(len(set(letras)), 25)
        self.assertNotIn("J", letras)
        self.assertEqual(letras[:4], ["B", "A", "N", "C"])

    def test_monta_grade_trata_j_na_chave_como_i(self):
        letras = [letra for linha in montar_grade("jazz") for letra in linha]

        self.assertEqual(letras[:3], ["I", "A", "Z"])
        self.assertNotIn("J", letras)

    def test_prepara_digramas_com_filler_e_normalizacao(self):
        self.assertEqual(preparar_digramas("BALLOON"), ["BA", "LX", "LO", "ON"])
        self.assertEqual(preparar_digramas("JAZZ"), ["IA", "ZX", "ZX"])
        self.assertEqual(preparar_digramas("XX"), ["XQ", "XQ"])

        for digrama in preparar_digramas("BALLOON"):
            self.assertEqual(len(digrama), 2)
            self.assertNotEqual(digrama[0], digrama[1])

    def test_ida_e_volta_devolve_o_texto_preparado(self):
        texto_preparado = "".join(preparar_digramas("JAZZ"))
        cifrado = playfair("JAZZ", "MONARCHY")

        self.assertEqual(playfair(cifrado, "MONARCHY", decifrar=True), texto_preparado)

    def test_vetor_conhecido_com_chave_monarchy(self):
        self.assertEqual(
            playfair("instruments", "MONARCHY"),
            "GATLMZCLRQXA",
        )

    def test_aplica_as_tres_regras_e_as_desfaz(self):
        chave = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        casos = (("AB", "BC"), ("AF", "FL"), ("AG", "BF"))

        for original, esperado in casos:
            with self.subTest(original=original):
                self.assertEqual(playfair(original, chave), esperado)
                self.assertEqual(
                    playfair(esperado, chave, decifrar=True),
                    original,
                )

    def test_regras_de_linha_e_coluna_fazem_volta_circular(self):
        chave = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

        for original, esperado in (("AE", "BA"), ("AV", "FA")):
            with self.subTest(original=original):
                self.assertEqual(playfair(original, chave), esperado)
                self.assertEqual(
                    playfair(esperado, chave, decifrar=True),
                    original,
                )

    def test_saida_cifrada_tem_tamanho_par_e_apenas_letras_da_grade(self):
        cifrado = playfair("Mensagem 123", "chave")
        letras_da_grade = set("ABCDEFGHIKLMNOPQRSTUVWXYZ")

        self.assertEqual(len(cifrado) % 2, 0)
        self.assertTrue(set(cifrado) <= letras_da_grade)

    def test_rejeita_chave_vazia_ou_sem_letras(self):
        for chave in ("", "123!"):
            with self.subTest(chave=chave), self.assertRaises(ValueError):
                montar_grade(chave)

    def test_rejeita_texto_de_decifracao_com_tamanho_impar(self):
        with self.assertRaises(ValueError):
            playfair("ABC", "chave", decifrar=True)

    def test_texto_sem_letras_e_letras_acentuadas_sao_ignorados(self):
        self.assertEqual(preparar_digramas("123 !?"), [])
        self.assertEqual(preparar_digramas("ação"), ["AO"])

    def test_decifracao_de_par_duplicado_eh_aceita(self):
        self.assertEqual(len(playfair("AA", "chave", decifrar=True)), 2)


class TestTeclado(unittest.TestCase):
    def test_ida_e_volta_devolve_texto_em_maiusculas(self):
        texto = "Hello World"

        self.assertEqual(
            teclado_para_texto(texto_para_teclado(texto)),
            texto.upper(),
        )

    def test_letras_da_mesma_tecla_continuam_distintas(self):
        codificado = texto_para_teclado("AB")

        self.assertEqual(codificado, "2 22")
        self.assertEqual(teclado_para_texto(codificado), "AB")

    def test_tabela_cobre_as_26_letras_uma_vez(self):
        letras = "".join(TECLAS.values())

        self.assertEqual(len(letras), 26)
        self.assertEqual(len(set(letras)), 26)
        self.assertEqual(set(letras), set("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))

    def test_espaco_entre_palavras_e_separador_de_letras(self):
        self.assertEqual(texto_para_teclado("A A"), "2 / 2")
        self.assertEqual(teclado_para_texto("2 / 2"), "A A")

    def test_caractere_fora_da_tabela_informa_o_caractere(self):
        with self.assertRaisesRegex(ValueError, r"teclado.*'!'"):
            texto_para_teclado("A!")

    def test_sequencia_de_toques_invalida(self):
        with self.assertRaisesRegex(ValueError, "Sequência de toques inválida"):
            teclado_para_texto("0")
        with self.assertRaisesRegex(ValueError, "Sequência de toques inválida"):
            teclado_para_texto("2222")


class TestRailFence(unittest.TestCase):
    def test_vetor_conhecido_de_tres_trilhos(self):
        texto = "WEAREDISCOVEREDFLEEATONCE"

        self.assertEqual(
            rail_fence(texto, 3),
            "WECRLTEERDSOEEFEAOCAIVDEN",
        )

    def test_cifra_e_decifra_para_varios_trilhos(self):
        for texto in ("", "x", "WE ARE DISCOVERED", "A man, a plan!"):
            for trilhos in (2, 3, 4, 7):
                with self.subTest(texto=texto, trilhos=trilhos):
                    cifrado = rail_fence(texto, trilhos)
                    self.assertEqual(
                        rail_fence(cifrado, trilhos, decifrar=True),
                        texto,
                    )

    def test_resultado_preserva_os_caracteres(self):
        texto = "A man, a plan!"

        self.assertEqual(sorted(rail_fence(texto, 3)), sorted(texto))

    def test_trilhos_maiores_ou_iguais_ao_texto_nao_alteram(self):
        texto = "abc"

        self.assertEqual(rail_fence(texto, 3), texto)
        self.assertEqual(rail_fence(texto, 10), texto)

    def test_trilhos_invalidos_geram_erro(self):
        for trilhos in (0, 1, -2):
            with self.subTest(trilhos=trilhos), self.assertRaises(ValueError):
                rail_fence("texto", trilhos)

    def test_espacos_e_pontuacao_entram_na_grade(self):
        texto = "A B!"

        self.assertNotEqual(rail_fence(texto, 2), texto)
        self.assertEqual(rail_fence(rail_fence(texto, 2), 2, decifrar=True), texto)


class TestForcaBruta(unittest.TestCase):
    def test_ordena_todas_as_tentativas_pela_nota_e_preserva_o_deslocamento(self):
        texto = "this is the"
        cifrado = cesar(texto, 3)

        tentativas = forca_bruta_cesar(cifrado)
        notas = [nota for nota, _, _ in tentativas]

        self.assertEqual(len(tentativas), 26)
        self.assertEqual(tentativas[0], (3, 3, texto))
        self.assertEqual(notas, sorted(notas, reverse=True))

    def test_texto_sem_palavras_comuns_mantem_nota_zero(self):
        texto = "quick brown fox"
        cifrado = cesar(texto, 3)

        tentativas = forca_bruta_cesar(cifrado)

        self.assertTrue(all(nota == 0 for nota, _, _ in tentativas))
        self.assertEqual(tentativas[0], (0, 0, cifrado))


class TestVigenere(unittest.TestCase):
    def test_cifra_e_decifra_retorna_o_texto_original(self):
        texto = "Ataque ao amanhecer! Ãç"
        cifrado = vigenere(texto, "Chave")

        self.assertEqual(vigenere(cifrado, "chave", decifrar=True), texto)

    def test_decifra_texto_cifrado_conhecido(self):
        self.assertEqual(
            vigenere("Lxfopv ef rnhr", "lemon", decifrar=True),
            "Attack at dawn",
        )

    def test_chave_de_uma_letra_equivale_a_cesar(self):
        texto = "Hello, World!"

        self.assertEqual(vigenere(texto, "d"), cesar(texto, 3))

    def test_chave_a_nao_altera_o_texto(self):
        texto = "Hello, World! 123"

        self.assertEqual(vigenere(texto, "a"), texto)

    def test_ignora_caracteres_que_nao_sao_letras_e_nao_avanca_a_chave(self):
        texto = "a 1!b"

        self.assertEqual(vigenere(texto, "bc"), "b 1!d")

    def test_chave_maiuscula_e_minuscula_sao_equivalentes(self):
        texto = "Attack at dawn"

        self.assertEqual(vigenere(texto, "ChAvE"), vigenere(texto, "chave"))

    def test_caracteres_fora_do_ascii_nao_avancam_a_chave(self):
        self.assertEqual(vigenere("a\u212ab", "bc"), "b\u212ad")

    def test_rejeita_chave_vazia(self):
        with self.assertRaisesRegex(ValueError, "não pode ser vazia"):
            vigenere("texto", "")

    def test_rejeita_chave_com_caractere_que_nao_e_letra(self):
        for chave in ("ab1", "ab cd"):
            with self.subTest(chave=chave), self.assertRaisesRegex(
                ValueError, "apenas letras ASCII"
            ):
                vigenere("texto", chave)


class TestConversaoNumerica(unittest.TestCase):
    def test_converte_e_desconverte_nas_quatro_bases(self):
        for base in (2, 8, 10, 16):
            with self.subTest(base=base):
                numeros = texto_para_numeros("ãΩ", base)
                self.assertEqual(numeros_para_texto(numeros, base), "ãΩ")

    def test_usa_largura_minima_uniforme_por_base(self):
        esperado = {
            2: "01000001 01111010",
            8: "101 172",
            10: "065 122",
            16: "41 7a",
        }

        for base, resultado in esperado.items():
            with self.subTest(base=base):
                self.assertEqual(texto_para_numeros("Az", base), resultado)

    def test_nao_trunca_caracteres_acima_de_255(self):
        esperado = {
            2: "11100011 1110101001",
            8: "343 1651",
            10: "227 937",
            16: "e3 3a9",
        }

        for base, resultado in esperado.items():
            with self.subTest(base=base):
                self.assertEqual(texto_para_numeros("ãΩ", base), resultado)

    def test_rejeita_base_invalida_na_ida_e_na_volta(self):
        for base in (3, 12):
            with self.subTest(base=base):
                with self.assertRaisesRegex(ValueError, "2, 8, 10, 16"):
                    texto_para_numeros("A", base)
                with self.assertRaisesRegex(ValueError, "2, 8, 10, 16"):
                    numeros_para_texto("41", base)

    def test_rejeita_numero_invalido_com_token_e_base_na_mensagem(self):
        with self.assertRaisesRegex(ValueError, r"Número inválido 'zz' na base 16"):
            numeros_para_texto("41 zz", 16)


class TestBase36(unittest.TestCase):
    def test_converte_e_desconverte_uma_faixa_de_valores(self):
        for numero in range(0, 1000):
            with self.subTest(numero=numero):
                representacao = inteiro_para_base36(numero)
                self.assertEqual(int(representacao, 36), numero)
                self.assertEqual(base36_para_inteiro(representacao), numero)

    def test_conversao_eh_compativel_com_int_na_base_36(self):
        for numero in (0, 35, 36, 12345, 2**32):
            representacao = inteiro_para_base36(numero)

            with self.subTest(numero=numero):
                self.assertEqual(int(representacao, 36), numero)
                self.assertEqual(base36_para_inteiro(representacao), int(representacao, 36))

    def test_rejeita_numero_negativo(self):
        with self.assertRaisesRegex(ValueError, "não-negativo"):
            inteiro_para_base36(-1)

    def test_aceita_letras_maiusculas_e_minusculas(self):
        self.assertEqual(base36_para_inteiro("Z1a"), base36_para_inteiro("z1A"))

    def test_rejeita_sinal_kelvin_sem_normalizar_antes(self):
        with self.assertRaisesRegex(ValueError, r"Caractere inválido"):
            base36_para_inteiro("\u212a")

    def test_rejeita_entrada_vazia_sinal_e_espaco(self):
        for entrada in ("", "-1", " "):
            with self.subTest(entrada=entrada), self.assertRaises(ValueError):
                base36_para_inteiro(entrada)

    def test_base36_e_depois_cesar(self):
        codificado = cesar(inteiro_para_base36(12345), 3)

        self.assertEqual(codificado, "9la")
        self.assertEqual(
            base36_para_inteiro(cesar(codificado, -3)),
            12345,
        )


class TestBase64(unittest.TestCase):
    def test_codifica_e_decodifica_texto(self):
        texto = "Olá, mundo! こんにちは"

        self.assertEqual(base64_para_texto(texto_para_base64(texto)), texto)

    def test_rejeita_padding_invalido(self):
        with self.assertRaises(ValueError):
            base64_para_texto("SGVsbG8")

    def test_rejeita_entrada_base64_invalida(self):
        for entrada in ("!!!!", "é", "/w==", "SGVsbG8=\n"):
            with self.subTest(entrada=entrada), self.assertRaises(ValueError):
                base64_para_texto(entrada)


class TestMorse(unittest.TestCase):
    def test_codifica_e_decodifica_texto_com_palavras(self):
        texto = "SOS 2026!"

        codificado = texto_para_morse(texto)
        self.assertEqual(morse_para_texto(codificado), texto)
        self.assertEqual(codificado, "... --- ... / ..--- ----- ..--- -.... -.-.--")

    def test_tabela_cobre_letras_digitos_e_pontuacao(self):
        self.assertEqual(set("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), set(MORSE) & set("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        self.assertTrue(set("0123456789") <= MORSE.keys())
        self.assertTrue(set(".,?!") <= MORSE.keys())

    def test_tabela_nao_tem_codigos_repetidos(self):
        self.assertEqual(len(MORSE), len(set(MORSE.values())))

    def test_decodifica_letras_minusculas_como_maiusculas(self):
        self.assertEqual(morse_para_texto(texto_para_morse("sos")), "SOS")

    def test_rejeita_caractere_fora_da_tabela(self):
        for caractere in ("\u00df", "\u017f", "\u0131", "\u00e9"):
            with self.subTest(caractere=caractere), self.assertRaisesRegex(
                ValueError, "não suportado"
            ):
                texto_para_morse(caractere)

    def test_rejeita_codigo_morse_desconhecido(self):
        with self.assertRaisesRegex(ValueError, "Código Morse inválido"):
            morse_para_texto(".... .----..")


class TestLinhaDeComando(unittest.TestCase):
    def test_help_lista_todos_os_subcomandos(self):
        saida = StringIO()
        with patch("sys.stdout", saida):
            codigo = main(["--help"])

        self.assertEqual(codigo, 0)
        for comando in (
            "cesar",
            "atbash",
            "inverter",
            "forca-bruta",
            "vigenere",
            "texto-para-numeros",
            "numeros-para-texto",
            "inteiro-para-base36",
            "base36-para-inteiro",
            "texto-para-base64",
            "base64-para-texto",
            "texto-para-morse",
            "morse-para-texto",
        ):
            self.assertIn(comando, saida.getvalue())

    def test_executa_com_texto_do_argumento(self):
        saida = StringIO()
        with patch("sys.stdout", saida):
            codigo = main(["cesar", "-n", "3", "bom dia"])

        self.assertEqual(codigo, 0)
        self.assertEqual(saida.getvalue(), "erp gld\n")

    def test_executa_com_texto_da_entrada_padrao(self):
        saida = StringIO()
        with patch("sys.stdin", StringIO("bom dia\n")), patch("sys.stdout", saida):
            codigo = main(["cesar", "-n", "3"])

        self.assertEqual(codigo, 0)
        self.assertEqual(saida.getvalue(), "erp gld\n")

    def test_flag_decifrar_do_vigenere(self):
        saida = StringIO()
        with patch("sys.stdout", saida):
            codigo = main(["vigenere", "--chave", "lemon", "--decifrar", "Lxfopv"])

        self.assertEqual(codigo, 0)
        self.assertEqual(saida.getvalue(), "Attack\n")

    def test_formato_de_saida_da_forca_bruta(self):
        saida = StringIO()
        with patch("sys.stdout", saida):
            codigo = main(["forca-bruta", "wklv"])

        linhas = saida.getvalue().splitlines()
        self.assertEqual(codigo, 0)
        self.assertEqual(len(linhas), 26)
        self.assertIn("1 3 this", linhas)
        self.assertTrue(all(len(linha.split(" ", 2)) == 3 for linha in linhas))

    def test_remove_o_terminador_de_linha_da_entrada_padrao_em_todos_os_comandos(
        self,
    ):
        casos = (
            (["cesar", "-n", "3"], "bom dia\n", "erp gld\n"),
            (["forca-bruta"], "wklv\n", None),
            (["vigenere", "--chave", "d"], "a\n", "d\n"),
            (["texto-para-numeros", "--base", "16"], "Ola\n", "4f 6c 61\n"),
            (["numeros-para-texto", "--base", "16"], "4f 6c 61\n", "Ola\n"),
            (["base36-para-inteiro"], "9ix\n", "12345\n"),
            (["texto-para-base64"], "Ola\n", "T2xh\n"),
            (["base64-para-texto"], "T2zDoQ==\n", "Olá\n"),
            (["texto-para-morse"], "SOS\n", "... --- ...\n"),
            (["morse-para-texto"], "... --- ...\n", "SOS\n"),
        )

        for argumentos, entrada, esperado in casos:
            with self.subTest(argumentos=argumentos):
                saida = StringIO()
                with patch("sys.stdin", StringIO(entrada)), patch(
                    "sys.stdout", saida
                ):
                    codigo = main(argumentos)

                self.assertEqual(codigo, 0)
                if esperado is not None:
                    self.assertEqual(saida.getvalue(), esperado)
                else:
                    self.assertEqual(len(saida.getvalue().splitlines()), 26)

    def test_erro_de_uso_vai_para_stderr_e_retorna_codigo_diferente_de_zero(self):
        erro = StringIO()
        with patch("sys.stderr", erro):
            codigo = main(["texto-para-numeros", "--base", "3", "A"])

        self.assertNotEqual(codigo, 0)
        self.assertIn("base", erro.getvalue())

        erro.seek(0)
        erro.truncate(0)
        with patch("sys.stderr", erro):
            codigo = main(["vigenere", "--chave", "", "A"])

        self.assertNotEqual(codigo, 0)
        self.assertIn("vazia", erro.getvalue())


if __name__ == "__main__":
    unittest.main()
