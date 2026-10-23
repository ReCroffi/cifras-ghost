import unittest

from ghost_wires.cifras import cesar, deslocar_letra


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


if __name__ == "__main__":
    unittest.main()
