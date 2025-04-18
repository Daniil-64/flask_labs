import unittest
from unittest import TestCase
from datetime import datetime
from freezegun import freeze_time

from flask_lab2.hello_world_with_name import app, WEEKDAYS


class TestHelloWorldWithDayApp(TestCase):
    """Тесты для приложения hello_world_with_name"""

    @classmethod
    def setUpClass(cls):
        """Настройка тестового клиента перед всеми тестами"""
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        cls.app = app.test_client()
        cls.base_url = '/hello-world/'

    def test_can_get_correct_username_with_weekdate(self):
        """Тест, что имя пользователя правильно включено в ответ"""
        username = 'username'
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertIn(username, response_text)

        # Добавляем проверку на правильность дня недели
        weekday = datetime.today().weekday()
        expected_day = WEEKDAYS[weekday]
        self.assertIn(f"Хорошего {expected_day}", response_text)

    def test_day_of_week_is_correct(self):
        """Тест, что правильный день недели возвращается в приветствии для каждого дня недели"""
        # Тестируем для каждого дня недели
        for test_weekday in range(7):
            # Понедельник - это 0, воскресенье - 6
            # Используем конкретные даты, чтобы гарантировать правильный день недели
            test_date = f"2023-05-{1 + test_weekday}"  # Начиная с понедельника, 1 мая 2023
            with freeze_time(test_date):
                username = 'test_user'
                response = self.app.get(self.base_url + username)
                response_text = response.data.decode()

                # Проверяем, что правильное приветствие для этого дня недели есть в ответе
                expected_greeting = f"Хорошего {WEEKDAYS[test_weekday]}"
                self.assertIn(expected_greeting, response_text,
                              f"Для даты {test_date} (день недели {test_weekday}) ожидалось приветствие '{expected_greeting}'")

    def test_username_with_greeting_safe(self):
        """Тест обработки имен пользователей, содержащих приветствия с днем недели"""
        malicious_username = 'Хорошей среды'

        # Замораживаем время на понедельник
        with freeze_time("2023-05-01"):  # Понедельник
            response = self.app.get(self.base_url + malicious_username)
            response_text = response.data.decode()

            # Должно показывать приветствие понедельника, а не среды
            self.assertIn('Хорошего понедельника', response_text)
            # Убеждаемся, что имя пользователя все еще правильно включено
            self.assertIn(f'Привет, {malicious_username}', response_text)


if __name__ == '__main__':
    unittest.main()