import unittest
from unittest import TestCase
from flask_lab2.accounting import app, storage, monthly_sums, yearly_sums  # Импортируем ваше приложение и переменные


class AccountingTestCase(TestCase):
    """Тесты для приложения учета финансов"""

    @classmethod
    def setUpClass(cls):
        """Настройка тестовых данных и тестового клиента перед всеми тестами"""
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        cls.app = app.test_client()

        # Очищаем хранилище и кэши
        storage.clear()
        monthly_sums.clear()
        yearly_sums.clear()

        # Начальные тестовые данные
        # Год 2023, Месяц 1 (Январь), Дни 10, 15, 20 с расходами
        # Год 2023, Месяц 2 (Февраль), Дни 5, 10 с расходами
        storage[2023] = {
            1: {
                10: 1000,
                15: 2000,
                20: 1500
            },
            2: {
                5: 3000,
                10: 2500
            }
        }

        # Заполняем кэши для соответствия данным
        monthly_sums[2023] = {
            1: 4500,  # 1000 + 2000 + 1500
            2: 5500  # 3000 + 2500
        }
        yearly_sums[2023] = 10000  # 4500 + 5500

        # Год 2022 с некоторыми расходами
        storage[2022] = {
            12: {
                25: 5000,
                31: 3000
            }
        }

        # Заполняем кэши для 2022 года
        monthly_sums[2022] = {
            12: 8000  # 5000 + 3000
        }
        yearly_sums[2022] = 8000

    def test_add_expense(self):
        """Тест добавления расхода через эндпоинт /add/"""
        # Тест добавления нового расхода
        response = self.app.get('/add/20230501/2000')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Добавлена трата', response.data.decode())

        # Проверяем, что данные действительно добавлены
        self.assertIn(2023, storage)
        self.assertIn(5, storage[2023])
        self.assertIn(1, storage[2023][5])
        self.assertEqual(storage[2023][5][1], 2000)

        # Тест добавления к существующей дате
        response = self.app.get('/add/20230501/1000')
        self.assertEqual(response.status_code, 200)
        # Проверяем, что сумма добавлена к существующему значению
        self.assertEqual(storage[2023][5][1], 3000)

        # Тест добавления в новый год
        response = self.app.get('/add/20240101/5000')
        self.assertEqual(response.status_code, 200)
        self.assertIn(2024, storage)
        self.assertIn(1, storage[2024])
        self.assertIn(1, storage[2024][1])
        self.assertEqual(storage[2024][1][1], 5000)

    def test_add_expense_invalid_format(self):
        """Тест добавления расхода с неверным форматом даты"""
        # Тест с неверным форматом даты - в вашей реализации возвращается HTTP 400
        response = self.app.get('/add/202301/1000')  # Отсутствует день
        self.assertEqual(response.status_code, 400)

        response = self.app.get('/add/01012023/1000')  # Неверный порядок
        self.assertEqual(response.status_code, 400)

        response = self.app.get('/add/abcdefgh/1000')  # Не дата
        self.assertEqual(response.status_code, 400)

        # Тест с неверной суммой
        response = self.app.get('/add/20230101/abc')
        self.assertEqual(response.status_code, 404)  # Flask будет возвращать 404, т.к. маршрут ожидает число

    def test_calculate_year(self):
        """Тест расчета годовых расходов через эндпоинт /calculate/<year>"""
        # Тест для 2023 года (должен суммировать все расходы из начальных данных)
        response = self.app.get('/calculate/2023')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode()
        self.assertIn('2023', response_text)

        # Проверяем только наличие года и суммы в ответе, без проверки точного формата сообщения
        self.assertIn('2023', response_text)
        expected_total = 13000  # 10000 (начальные) + 3000 (добавленные в test_add_expense)
        self.assertIn(str(expected_total), response_text)

        # Тест для 2022 года
        response = self.app.get('/calculate/2022')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode()
        # Проверяем только наличие года и суммы в ответе
        self.assertIn('2022', response_text)
        expected_total = 8000
        self.assertIn(str(expected_total), response_text)

        # Тест для года без данных
        response = self.app.get('/calculate/2021')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode()
        self.assertIn(f"За {2021} год не было трат", response_text)

    def test_calculate_month(self):
        """Тест расчета месячных расходов через эндпоинт /calculate/<year>/<month>"""
        # Тест для января 2023
        response = self.app.get('/calculate/2023/1')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode()
        # Проверяем только наличие месяца/года и суммы в ответе
        self.assertIn('1/2023', response_text)
        expected_total = 4500
        self.assertIn(str(expected_total), response_text)

        # Тест для февраля 2023
        response = self.app.get('/calculate/2023/2')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode()
        # Проверяем только наличие месяца/года и суммы в ответе
        self.assertIn('2/2023', response_text)
        expected_total = 5500
        self.assertIn(str(expected_total), response_text)

        # Тест для месяца без данных
        response = self.app.get('/calculate/2023/3')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode()
        self.assertIn(f"За {3}/{2023} не было трат", response_text)

    def test_empty_storage(self):
        """Тест работы эндпоинтов с пустым хранилищем"""
        # Очищаем хранилище и кэши
        storage.clear()
        monthly_sums.clear()
        yearly_sums.clear()

        # Тест расчета года с пустым хранилищем
        response = self.app.get('/calculate/2023')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode()
        self.assertIn(f"За {2023} год не было трат", response_text)

        # Тест расчета месяца с пустым хранилищем
        response = self.app.get('/calculate/2023/1')
        self.assertEqual(response.status_code, 200)
        response_text = response.data.decode()
        self.assertIn(f"За {1}/{2023} не было трат", response_text)

        # Тест добавления в пустое хранилище
        response = self.app.get('/add/20230101/1000')
        self.assertEqual(response.status_code, 200)
        # Проверяем, что данные действительно добавлены в пустое хранилище
        self.assertIn(2023, storage)
        self.assertIn(1, storage[2023])
        self.assertIn(1, storage[2023][1])
        self.assertEqual(storage[2023][1][1], 1000)

        # Проверяем, что кэши также обновлены
        self.assertIn(2023, yearly_sums)
        self.assertEqual(yearly_sums[2023], 1000)
        self.assertIn(2023, monthly_sums)
        self.assertIn(1, monthly_sums[2023])
        self.assertEqual(monthly_sums[2023][1], 1000)


if __name__ == '__main__':
    unittest.main()