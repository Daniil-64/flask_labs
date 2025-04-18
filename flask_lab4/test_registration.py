"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""

import unittest
import json
from registration import app


class TestRegistrationForm(unittest.TestCase):
    """Тестирование формы регистрации и её валидаторов"""

    @classmethod
    def setUpClass(cls):
        """Настройка тестового клиента и отключение CSRF"""
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def test_valid_registration(self):
        """Тест успешной регистрации с валидными данными"""
        # Подготавливаем валидные данные
        valid_data = {
            "email": "test@example.com",
            "phone": 1234567890,
            "name": "John Doe",
            "address": "123 Main St",
            "index": 12345,
            "comment": "Optional comment"
        }

        # Отправляем POST-запрос
        response = self.client.post("/registration", data=valid_data)

        # Проверяем ответ
        self.assertEqual(response.status_code, 200)
        self.assertIn("Successfully registered", response.data.decode())

    def test_missing_required_fields(self):
        """Тест на отсутствие обязательных полей"""
        # Отправляем пустую форму
        response = self.client.post("/registration", data={})

        # Проверяем ответ
        self.assertEqual(response.status_code, 400)

        # Проверяем, что все обязательные поля вызвали ошибки
        response_data = response.data.decode()
        self.assertIn("email", response_data)
        self.assertIn("phone", response_data)
        self.assertIn("name", response_data)
        self.assertIn("address", response_data)
        self.assertIn("index", response_data)

    # Тесты для поля email
    def test_email_valid_format(self):
        """Тест валидации формата email"""
        # Тестируем валидный email
        valid_data = {
            "email": "test@example.com",
            "phone": 1234567890,
            "name": "John Doe",
            "address": "123 Main St",
            "index": 12345
        }
        response = self.client.post("/registration", data=valid_data)
        self.assertEqual(response.status_code, 200)

        # Тестируем невалидный email
        invalid_data = valid_data.copy()
        invalid_data["email"] = "invalid-email"
        response = self.client.post("/registration", data=invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Email", response.data.decode())

    # Тесты для поля phone
    def test_phone_length(self):
        """Тест валидации длины номера телефона"""
        valid_data = {
            "email": "test@example.com",
            "phone": 1234567890,  # 10 цифр - валидно
            "name": "John Doe",
            "address": "123 Main St",
            "index": 12345
        }
        response = self.client.post("/registration", data=valid_data)
        self.assertEqual(response.status_code, 200)

        # Слишком короткий номер
        invalid_data = valid_data.copy()
        invalid_data["phone"] = 123456789  # 9 цифр - невалидно
        response = self.client.post("/registration", data=invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("phone", response.data.decode().lower())

        # Слишком длинный номер
        invalid_data["phone"] = 12345678901  # 11 цифр - невалидно
        response = self.client.post("/registration", data=invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("phone", response.data.decode().lower())

    def test_phone_positive(self):
        """Тест на положительное значение телефона"""
        valid_data = {
            "email": "test@example.com",
            "phone": 1234567890,
            "name": "John Doe",
            "address": "123 Main St",
            "index": 12345
        }

        # Отрицательный номер телефона
        invalid_data = valid_data.copy()
        invalid_data["phone"] = -1234567890
        response = self.client.post("/registration", data=invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("phone", response.data.decode().lower())

    # Тесты для поля name
    def test_name_required(self):
        """Тест на обязательность поля name"""
        valid_data = {
            "email": "test@example.com",
            "phone": 1234567890,
            "name": "John Doe",
            "address": "123 Main St",
            "index": 12345
        }

        # Пустое имя
        invalid_data = valid_data.copy()
        invalid_data["name"] = ""
        response = self.client.post("/registration", data=invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.data.decode().lower())

    # Тесты для поля address
    def test_address_required(self):
        """Тест на обязательность поля address"""
        valid_data = {
            "email": "test@example.com",
            "phone": 1234567890,
            "name": "John Doe",
            "address": "123 Main St",
            "index": 12345
        }

        # Пустой адрес
        invalid_data = valid_data.copy()
        invalid_data["address"] = ""
        response = self.client.post("/registration", data=invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("address", response.data.decode().lower())

    # Тесты для поля index
    def test_index_number(self):
        """Тест на числовой тип индекса"""
        valid_data = {
            "email": "test@example.com",
            "phone": 1234567890,
            "name": "John Doe",
            "address": "123 Main St",
            "index": 12345
        }

        # Нечисловой индекс
        invalid_data = valid_data.copy()
        invalid_data["index"] = "abc123"
        response = self.client.post("/registration", data=invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("index", response.data.decode().lower())

    # Тесты для поля comment
    def test_comment_optional(self):
        """Тест на опциональность поля comment"""
        # Без комментария
        valid_data = {
            "email": "test@example.com",
            "phone": 1234567890,
            "name": "John Doe",
            "address": "123 Main St",
            "index": 12345
            # комментарий отсутствует
        }
        response = self.client.post("/registration", data=valid_data)
        self.assertEqual(response.status_code, 200)

        # С комментарием
        valid_data["comment"] = "Some comment"
        response = self.client.post("/registration", data=valid_data)
        self.assertEqual(response.status_code, 200)

    def test_unexpected_data_format(self):
        """Тест на защиту от неверного формата данных"""
        # Отправляем некорректный JSON вместо form-data
        response = self.client.post(
            "/registration",
            data=json.dumps({"email": "test@example.com"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()