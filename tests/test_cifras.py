import unittest

from ghost_wires.cifras import (
    cesar,
    deslocar_letra,
    forca_bruta_cesar,
    numeros_para_texto,
    texto_para_numeros,
    vigenere,
    base36_para_inteiro,
    inteiro_para_base36,
)


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


if __name__ == "__main__":
    unittest.main()
