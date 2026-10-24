import unittest

from ghost_wires.cifras import cesar, deslocar_letra, forca_bruta_cesar, vigenere


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


if __name__ == "__main__":
    unittest.main()
