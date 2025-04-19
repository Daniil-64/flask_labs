import unittest
from unittest import TestCase
from flask_lab2.decrypt import decrypt


class DecryptTestCase(TestCase):
    """Тесты для функции расшифровки"""

    def test_single_dot_cases(self):
        """Тесты для строк с одиночными точками (точка сохраняет предыдущий символ)"""
        test_cases = [
            ("абра-кадабра.", "абра-кадабра"),
            ("2.3", "23"),
        ]

        for encrypted, expected in test_cases:
            with self.subTest(f"Тестирование расшифровки '{encrypted}'"):
                self.assertEqual(decrypt(encrypted), expected)

    def test_double_dot_cases(self):
        """Тесты для строк с двойными точками (две точки удаляют предыдущий символ)"""
        test_cases = [
            ("абраа..-кадабра", "абра-кадабра"),
            ("1..2.3", "23"),
            ("абра--..кадабра", "абра-кадабра"),
        ]

        for encrypted, expected in test_cases:
            with self.subTest(f"Тестирование расшифровки '{encrypted}'"):
                self.assertEqual(decrypt(encrypted), expected)

    def test_mixed_dots_cases(self):
        """Тесты для строк со смешанными точками"""
        test_cases = [
            ("абраа..-.кадабра", "абра-кадабра"),
            ("абрау...-кадабра", "абра-кадабра"),
        ]

        for encrypted, expected in test_cases:
            with self.subTest(f"Тестирование расшифровки '{encrypted}'"):
                self.assertEqual(decrypt(encrypted), expected)

    def test_multiple_dots_cases(self):
        """Тесты для строк с множественными точками"""
        test_cases = [
            ("абра.........", ""),  # 10 точек, удаляют все символы
            ("абр......a.", "a"),  # 6 точек, удаляют 'абр', затем 'a.' -> 'a'
            (".", ""),  # Одна точка без предыдущего символа
            ("1.......................", ""),  # Много точек, удаляющих '1'
        ]

        for encrypted, expected in test_cases:
            with self.subTest(f"Тестирование расшифровки '{encrypted}'"):
                self.assertEqual(decrypt(encrypted), expected)

    def test_edge_cases(self):
        """Тесты для граничных случаев"""
        test_cases = [
            ("", ""),  # Пустая строка
            ("..", ""),  # Две точки без предыдущего символа
            ("...", ""),  # Три точки без предыдущего символа
            ("a", "a"),  # Вообще без точек
        ]

        for encrypted, expected in test_cases:
            with self.subTest(f"Тестирование расшифровки '{encrypted}'"):
                self.assertEqual(decrypt(encrypted), expected)


if __name__ == '__main__':
    unittest.main()