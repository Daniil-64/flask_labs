import unittest
from unittest import TestCase
from freezegun import freeze_time
import datetime

from person import Person  # Измените путь импорта в соответствии с вашим проектом


class TestPerson(TestCase):
    """Тесты для класса Person"""

    def setUp(self):
        """Создание тестовых объектов Person перед каждым тестом"""
        self.test_name = "John Doe"
        self.test_yob = 1990
        self.test_address = "123 Main St"
        self.person = Person(self.test_name, self.test_yob, self.test_address)
        self.homeless_person = Person("Jane Doe", 1995)

    def test_init(self):
        """Тест инициализации атрибутов"""
        self.assertEqual(self.person.name, self.test_name)
        self.assertEqual(self.person.yob, self.test_yob)
        self.assertEqual(self.person.address, self.test_address)

        # Тест пустого адреса по умолчанию
        self.assertEqual(self.homeless_person.address, "")

    @freeze_time("2023-01-01")
    def test_get_age(self):
        """Тест расчета возраста"""
        # В 2023 году человек, родившийся в 1990, должен иметь возраст 33 года
        expected_age = 2023 - self.test_yob
        self.assertEqual(self.person.get_age(), expected_age)

        # Тест с другим годом рождения
        person2 = Person("Test", 2000)
        self.assertEqual(person2.get_age(), 23)

    def test_get_name(self):
        """Тест получения имени человека"""
        self.assertEqual(self.person.get_name(), self.test_name)

    def test_set_name(self):
        """Тест установки имени человека"""
        new_name = "Jane Smith"
        self.person.set_name(new_name)
        self.assertEqual(self.person.name, new_name)
        self.assertEqual(self.person.get_name(), new_name)

    def test_get_address(self):
        """Тест получения адреса человека"""
        self.assertEqual(self.person.get_address(), self.test_address)
        self.assertEqual(self.homeless_person.get_address(), "")

    def test_set_address(self):
        """Тест установки адреса человека"""
        new_address = "456 Oak Ave"
        self.person.set_address(new_address)
        self.assertEqual(self.person.address, new_address)
        self.assertEqual(self.person.get_address(), new_address)

        # Тест установки адреса для бездомного человека
        self.homeless_person.set_address(new_address)
        self.assertEqual(self.homeless_person.address, new_address)
        self.assertEqual(self.homeless_person.get_address(), new_address)

    def test_is_homeless(self):
        """Тест проверки, является ли человек бездомным"""
        # Человек с адресом не должен быть бездомным
        self.assertFalse(self.person.is_homeless())

        # Человек с пустым адресом должен быть бездомным
        self.assertTrue(self.homeless_person.is_homeless())

        # После установки адреса, он больше не должен быть бездомным
        self.homeless_person.set_address("789 Pine St")
        self.assertFalse(self.homeless_person.is_homeless())

        # Установка пустого адреса должна снова сделать его бездомным
        self.homeless_person.set_address("")
        self.assertTrue(self.homeless_person.is_homeless())

        # Установка адреса None также должна сделать человека бездомным
        self.person.set_address(None)
        self.assertTrue(self.person.is_homeless())


if __name__ == '__main__':
    unittest.main()